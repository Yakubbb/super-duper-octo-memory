import discord
from discord.ext import commands
from gtts import gTTS
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

def getenv(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        raise EnvironmentError('{} environmvet variable is missing'.format(key))
    return value

TOKEN = getenv('DISCORD_API_KEY')
ROLE_NAME = 'GLEB'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot('^', intents=intents)

async def get_client(guild: discord.Guild) -> discord.VoiceClient:
    for client in bot.voice_clients:
        client: discord.VoiceClient = client
        if client.guild == guild:
            return client
    return None

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command()
async def join(interaction: discord.Interaction):
    vc = interaction.user.voice
    if vc is not None:
        vc = await vc.channel.connect()
        await interaction.response.send_message('🤙')
    else:
        await interaction.response.send_message('🔇')

@bot.tree.command()
async def stop(interaction: discord.Interaction):
    client = await get_client(interaction.guild)
    if client is None:
        await interaction.response.send_message('🤨')
    else:
        await client.disconnect()
        await interaction.response.send_message('😩')

@bot.event
async def on_message(message: discord.Message):
    if discord.utils.get(message.author.roles, name=ROLE_NAME) != None:
        client = await get_client(message.guild)
        if client is None:
            return
        fp = BytesIO()
        gTTS(message.content, lang='ru').write_to_fp(fp)
        fp.seek(0)
        if client.is_playing():
            client.stop()
        client.play(discord.FFmpegPCMAudio(fp, pipe=True))

bot.run(TOKEN)