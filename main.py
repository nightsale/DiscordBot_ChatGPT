import discord
import openai
import os
import google.generativeai as google
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file
TOKEN, GUILD, CHANNEL_ID, OPEN_AI_TOKEN, GEMINI_AI_TOKEN = os.getenv('DISCORD_TOKEN'), os.getenv('DISCORD_GUILD'), int(os.getenv('DISCORD_CHANNELID')), os.getenv('OPENAI_API_KEY'), os.getenv('GEMINI_API_KEY')
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
    if client.user not in message.mentions:  #Answer only if chatGPT has been mentioned
        print(client.user)
        return

    mention_to_remove = f"<@{client.user.id}>"  # Remove the ChatGPT ID from the response
    message_content = message.content.replace(mention_to_remove, "").strip()
    print("Message received:", message_content)

    if "/text" in message_content:  # Verify if /text in message
        prompt = message_content[len("/text"):].strip()  # Remove /text to the prompt\
        assert prompt != 0
        if "-gemini" in prompt:
            prompt = message_content[len("-gemini"):].strip()  # Remove /gemini to the prompt
            if prompt:
                print("Generating with Gemini :", prompt)
                response = await get_gemini_text_response(prompt)
        elif "-chatgpt" in prompt:
            prompt = message_content[len("-chatgpt"):].strip()
            print("Generating with chatgpt :", prompt)
            response = await get_chatgpt_response(prompt)
        else:
            return "Enter the desired model"
    elif "/image" in message_content:
        prompt = message_content[len("/image"):].strip()
        if prompt:
            print("Generating image fo_ir prompt:", prompt)
            image_url = await openai_generate_image(prompt)
            response = image_url if image_url else "Failed to generate image."  # Error message if problem with OpenAI
    elif "/help" in message_content:
        return "For generate text use /text following with you model (-gemini or -chatgpt"
    else:
        response = "Please provide a prompt or use /help"  # Error if no prompt
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


async def openai_generate_image(prompt):  # Generate an image from a prompt with openAI
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


async def get_gemini_text_response(prompt):
    google.configure(api_key=GEMINI_AI_TOKEN)
    model = google.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    response_message = response.text
    return response_message


client.run(TOKEN)
