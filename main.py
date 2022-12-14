import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform



client = commands.Bot(
    command_prefix = "!",
    case_insensitive = True,
    intents = discord.Intents.all()
)


@client.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + "Logged in as " + Fore.YELLOW + client.user.name)
    print(prfx + "Bot ID " + Fore.YELLOW + str(client.user.id))
    print(prfx + "Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + "Python Version " + Fore.YELLOW + str(platform.python_version()))