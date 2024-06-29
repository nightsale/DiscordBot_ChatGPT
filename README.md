# ChatGPT Discord Bot

This is a Discord bot that integrates all OpenAI's model to respond to messages in Discord channels.

## Features

- Responds to mentions in Discord channels with OpenAI's GPT-3.5-turbo model.

## Installation

### Prerequisites

- Docker (for DSM/Synology NAS or general containerized setup)
- Python 3.8+
- pip (Python package installer)
- Discord bot token
- OpenAI API key

### Environment Variables

Create a `.env` file in the root of your project and add the following variables:

```plaintext
DISCORD_TOKEN=your_discord_token
DISCORD_GUILD=your_discord_guild_name
DISCORD_CHANNELID=your_discord_channel_id
OPENAI_API_KEY=your_openai_api_key
```

## Windows Setup
### Clone the repository:
```bash
git clone https://github.com/nightsale/DiscordBot_ChatGPT.git
cd DiscordBot_ChatGPT
```
### Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```
### Install the required packages:
```bash
pip install -r requirements.txt
```
Run the bot:
```bash
python main.py
```
## Docker Setup (DSM/Synology NAS)
### Clone the repository:
```bash
git clone https://github.com/nightsale/DiscordBot_ChatGPT.git
cd DiscordBot_ChatGPT
```
### Build the Docker image:

```bash
docker build -t chatgpt-discord-bot .
```
### Run the Docker container:

```bash
docker run -d --name chatgpt-bot --env-file .env chatgpt-discord-bot
```
### Configure Restart Policy:

To ensure the bot restarts automatically on reboot or if it crashes, run:

```bash
docker update --restart always chatgpt-bot
```
# Usage
Once the bot is running, it will listen for messages in the specified Discord channel. Mention the bot in your message to trigger a response from OpenAI's GPT-3.5-turbo model.

Example:

```text
Me: @ChatGPT Hello! How are you?
ChatGPT: Hello! I'm just a computer program, so I don't have feelings, but I'm here to help you. How can I assist you today?

```
# License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.

```plaintext
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.
   ...
Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

Contact
For commercial use or any queries, please contact [nightsale] at [nightsale@proton.me].

Acknowledgements
Discord.py
OpenAI
vbnet
```

This `README.md` provides comprehensive instructions to set up and run your ChatGPT Discord bot on both Windows and DSM/Synology NAS using Docker. It also includes licensing and contact information.