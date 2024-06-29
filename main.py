import discord
import openai
import os
from dotenv import load_dotenv  ## Import all librairies

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNELID'))  # Assurez-vous que CHANNEL_ID est un entier
OPEN_AI_TOKEN = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.default()
intents.messages = True  # Activer les intents pour recevoir le contenu des messages

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} s\'est connecté à Discord!\n'
        f'{client.user} est connecté au serveur suivant:\n'
        f'{guild.name} (id: {guild.id})'
        f'{client.user.id}'  ## Confirmation de connexion a discord
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user not in message.mentions:
        return
    mention_a_supprimer = f"<@{client.user.id}>"  # Enlever l'id de chatgpt dans la réponse
    message.content = message.content.replace(mention_a_supprimer, "")
    print("Message reçu:", message.content)

    response = await get_chatgpt_response(message.content)

    await message.channel.send(response)
    print("Message envoyé:", response)


async def get_chatgpt_response(prompt): ## Send a request to openai
    openai.api_key = OPEN_AI_TOKEN
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        temperature=0,  # Augmenter la température pour plus de variabilité
        top_p=0.95
    )

    response_message = response.choices[0].message.content
    return response_message


client.run(TOKEN)
