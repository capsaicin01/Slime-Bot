import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import os
import time
import platform
from keep_alive import keep_alive



client = commands.Bot(
    command_prefix = "!",
    case_insensitive = True,
    intents = discord.Intents.all()
)


@client.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC ", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + "Logged in as " + Fore.YELLOW + client.user.name)
    print(prfx + "Bot ID " + Fore.YELLOW + str(client.user.id))
    print(prfx + "Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + "Python Version " + Fore.YELLOW + str(platform.python_version()))


token = os.environ.get("bot_token")
#keep_alive()  #if you want to host the bot on replit you must delete the hash in the start of this line
client.run(token)