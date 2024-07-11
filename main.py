import discord
import openai
import os
import google.generativeai as google
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNELID'))  # Ensure CHANNEL_ID is an integer
OPEN_AI_TOKEN = os.getenv('OPENAI_API_KEY')
GEMINI_AI_TOKEN = os.getenv('GEMINI_API_KEY')
image_word = "/image"  # add /image in a variable to search after in a discord message
gemini_word = "/gemini"
intents = discord.Intents.default()
intents.messages = True  # Enable intents to receive message content

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    global guild
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the following server:\n'
        f'{guild.name} (id: {guild.id})\n'
        f'{client.user.id}'  # Confirmation of connection to Discord
    )


@client.event
async def on_message(message):
    if message.author == client.user:  #Try to not reply at this answer himself
        return
    if client.user not in message.mentions: #Answer only if chatGPT has been mentioned
        print(client.user)
        return

    mention_to_remove = f"<@{client.user.id}>"  # Remove the ChatGPT ID from the response
    message_content = message.content.replace(mention_to_remove, "").strip()
    print("Message received:", message_content)

    if image_word in message_content:  # Verify if /image in message
        prompt = message_content[len(image_word):].strip()  # Remove /image to the prompt
        if prompt:
            print("Generating image for prompt:", prompt)
            image_url = await generate_image(prompt)
            response = image_url if image_url else "Failed to generate image."  # Error message if problem with OpenAI
        else:
            response = "Please provide a prompt after /image."  # Error if no prompt
    elif gemini_word in message_content:
        prompt = message_content[len(gemini_word):].strip() # Remove /gemini to the prompt
        if prompt:
            print("Generating with Gemini :",prompt)
            response = await get_gemini_response(prompt)
    else:
        response = await get_chatgpt_response(message_content)  # If no /image answer with OpenAI chat

    await message.channel.send(response)
    print("Message sent:", response)


async def get_chatgpt_response(prompt):  # Send a request to OpenAI for text generation
    openai.api_key = OPEN_AI_TOKEN
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        temperature=0,  # Increase temperature for more variability
        top_p=0.95
    )

    response_message = response.choices[0].message.content
    return response_message


async def generate_image(prompt):  # Generate an image from a prompt with openAI
    openai.api_key = OPEN_AI_TOKEN
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",  # Adjust the size as needed
            quality="standard"
        )
        image_url = response.data[0].url
        print("Image URL generated:", image_url)
        return image_url
    except Exception as e:
        print("Error generating image:", e)
        return None

async  def get_gemini_response(prompt):
    google.configure(api_key=GEMINI_AI_TOKEN)
    model = google.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    response_message = response.text
    return response_message



client.run(TOKEN)
