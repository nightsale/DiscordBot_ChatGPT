import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNELID'))  # Ensure CHANNEL_ID is an integer
OPEN_AI_TOKEN = os.getenv('OPENAI_API_KEY')
image_word="/image"
intents = discord.Intents.default()
intents.messages = True  # Enable intents to receive message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
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
    if message.author == client.user:
        return
    if client.user not in message.mentions:
        print(client.user)
        return

    mention_to_remove = f"<@{client.user.id}>"  # Remove the ChatGPT ID from the response
    message_content = message.content.replace(mention_to_remove, "").strip()
    print("Message received:", message_content)

    if image_word in message_content:
        prompt = message_content[len("/image"):].strip()
        if prompt:
            print("Generating image for prompt:", prompt)
            image_url = await generate_image(prompt)
            response = image_url if image_url else "Failed to generate image."
        else:
            response = "Please provide a prompt after /image."
    else:
        response = await get_chatgpt_response(message_content)

    await message.channel.send(response)
    print("Message sent:", response)

async def get_chatgpt_response(prompt):  # Send a request to OpenAI
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

async def generate_image(prompt):  # Generate an image from a prompt
    openai.api_key = OPEN_AI_TOKEN
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",  # Adjust the size as needed
            quality = "standard"
        )
        image_url = response.data[0].url
        print("Image URL generated:", image_url)
        return image_url
    except Exception as e:
        print("Error generating image:", e)
        return None

client.run(TOKEN)
