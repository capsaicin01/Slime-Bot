import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from MusicClasses.MusicClasses import *

class MusicCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()

    @commands.command()
    async def disconnect(self,ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        await voice.disconnect()
    
    @commands.command()
    async def play(self, ctx, url:str, *args):
        voice_channel = ctx.author.voice.channel
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel")
            return
        
        if not self.client_in_same_channel(ctx.author, ctx.guild):
            await voice_channel.connect()
        
        if not url.startswith("https://"):
            url = f"ytsearch: {url} {' '.join(args)}"

        song = Song(url, ctx.author)
        voice = get(self.client.voice_clients, guild=ctx.guild)

        voice.play(discord.FFmpegPCMAudio(song.url))
        await ctx.send(f"Now playing: ***{song.title}***")

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

    def client_in_same_channel(self, author:discord.Member, guild:discord.Guild):
        voice = get(self.client.voice_clients, guild=guild)
        user_channel = author.voice.channel

        return voice is not None and voice.is_connected() and user_channel == voice.channel



async def setup(client):
    await client.add_cog(MusicCog(client))