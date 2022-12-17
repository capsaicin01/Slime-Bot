import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import os
import time
import platform
from keep_alive import keep_alive



client = commands.Bot(
    command_prefix = "s.",
    case_insensitive = True,
    intents = discord.Intents.all()
)


@client.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC ", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + "Logged in as " + Fore.YELLOW + client.user.name + "#" + client.user.discriminator)
    print(prfx + "Bot ID " + Fore.YELLOW + str(client.user.id))
    print(prfx + "Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + "Python Version " + Fore.YELLOW + str(platform.python_version()))


@client.command(aliases=["userinfo", "uinfo"])
async def user_info(ctx, member: discord.Member=None):
    
    if not member:
        member = ctx.message.author
    
    roles = [role for role in member.roles]
    
    embed = discord.Embed()
    embed.color = discord.Color.green()
    embed.title = "User Info"
    embed.description = f'Here is the user info on the user "{member.name}"'
    embed.timestamp = ctx.message.created_at

    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="ID", value = member.id)
    embed.add_field(name="Name", value = f"{member.name}#{member.discriminator}")
    embed.add_field(name="Nickname", value = member.display_name)
    embed.add_field(name="Status", value = member.status)
    embed.add_field(name="Created At", value = member.created_at.strftime("%d %B %Y, UTC %I:%M %p"))
    embed.add_field(name="Joined At", value = member.joined_at.strftime("%d %B %Y, UTC %I:%M %p"))
    embed.add_field(name=f"Roles({len(roles)})", value = " ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role", value = member.top_role.mention)
    embed.add_field(name="Is Bot?", value = member.bot)

    await ctx.send(embed = embed)


@client.command(aliases=["sinfo", "server"])
async def serverinfo(ctx):

    embed = discord.Embed()
    embed.color = discord.Color.green()
    embed.title = "Server Info"
    embed.description = f'Here is the server info on the server "{ctx.guild.name}"'
    embed.timestamp = ctx.message.created_at

    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name="Members", value = ctx.guild.member_count)
    embed.add_field(name="Channels", value = f"{len(ctx.guild.text_channels)} text | {len(ctx.guild.voice_channels)} voice")
    embed.add_field(name="Owner", value = ctx.guild.owner.mention)
    embed.add_field(name="Description", value = ctx.guild.description)
    embed.add_field(name="Created at", value = ctx.guild.created_at.strftime("%d %B %Y, UTC %I:%M %p"))

    await ctx.send(embed = embed)


token = os.environ.get("bot_token") # I stored my bot token as environment variable so you can just paste your own like: token = "your_token"
#keep_alive()  #if you want to host the bot on replit you must delete the hash in the start of this line
client.run(token)