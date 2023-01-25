import json
import discord
import re
from discord.ext import commands
# from config.discord_config import DISCORD_TOKEN, DISCORD_SERVER_ID, DISCORD_CHANNEL_NAME

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
DISCORD_CONFIG = "./config/discord_config.json"

with open(DISCORD_CONFIG, 'r+') as f:
    config = json.load(f)

def extract_urls(content):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls

async def fetch_server_channel_ids(invite_link: str, bot: commands.Bot):
    invite = await bot.fetch_invite(invite_link)
    guild = bot.get_guild(invite.guild.id)
    channels = {}
    print(guild.id)
    # for channel in guild.channels:
    #     channels[channel.name] = channel.id
    # config['DISCORD_SERVER_ID'] = guild.id
    # config['DISCORD_CHANNEL_NAME'] = channels
    # with open(DISCORD_CONFIG, 'w') as f:
    #     json.dump(config, f)

async def join_server(application_id: int, invite_link: str):
    try:
        await bot.start(application_id)
        await bot.join(invite_link)
        print("Bot joined the server")
    except Exception as e:
        print(f"Error joining server: {e}")
        
async def leave_server(guild: discord.Guild):
    try:
        await guild.leave()
        print("Bot left the server")
    except Exception as e:
        print(f"Error leaving server: {e}")

# @bot.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord!')
#     server = bot.get_guild(DISCORD_SERVER_ID)
#     channel = discord.utils.get(server.channels, name=DISCORD_CHANNEL_NAME)
#     async for message in channel.history(limit=None):
#         urls = extract_urls(message.content)
#         for url in urls:
#             print(url, message.author, message.channel.name, message.created_at)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await fetch_server_channel_ids(config['DISCORD_INVITE_LINK'], bot)

bot.run(config['DISCORD_TOKEN'])