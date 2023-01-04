import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import youtube_dl
from MusicClasses.MusicClasses import *

class MusicCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.music_queues = {}

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

        if not ctx.guild.id in self.music_queues:
            self.music_queues.update({ctx.guild.id: Queue()})
            print(self.music_queues)

        voice = get(self.client.voice_clients, guild=ctx.guild)
        queue = self.music_queues[ctx.guild.id]

        voice_channel = ctx.author.voice.channel
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel")
            return
        
        if not url.startswith("https://"):
            url = f"ytsearch: {url} {' '.join(args)}"

        song = Song(url, ctx.author)
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queue.append(song)
        await ctx.send(f"***{song.title}*** has been added to the queue.")
        
        if not self.is_in_same_channel(ctx.author, ctx.guild):
            await voice_channel.connect()
        
        await self.play_queue(ctx.guild)
        await self.inactivity_disconnect(ctx.guild)

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
    
    @commands.command()
    async def songinfo(self, ctx, song_idx = None):
        queue = self.music_queues[ctx.guild.id]
        embed = queue.get_embed()
        await ctx.send(embed=embed)

    async def play_song(self, guild:discord.Guild, song:Song):
        voice = get(self.client.voice_clients, guild=guild)
        voice.play(discord.FFmpegPCMAudio(song.url))

    async def wait_for_end_of_song(self, guild:discord.Guild):
        voice = get(self.client.voice_clients, guild=guild)
        while voice.is_playing():
            await asyncio.sleep(3)

    async def play_queue(self, guild:discord.Guild):

        queue = self.music_queues[guild.id]

        while True:
            try:
                await self.wait_for_end_of_song(guild)
                song = queue.next_song()
                await self.play_song(guild, song)
            except:
                break

    async def inactivity_disconnect(self, guild:discord.Guild):
        client_channel = guild.voice_client.channel

        while True:
            if len(client_channel.members) == 1:
                await self.leave_voice(guild)
            await asyncio.sleep(60)
            

    async def leave_voice(self, guild:discord.Guild):
        voice = get(self.client.voice_clients, guild=guild)
        await voice.disconnect()
        self.music_queues[guild.id].clear()


    def is_in_same_channel(self, author:discord.Member, guild:discord.Guild):
        voice = get(self.client.voice_clients, guild=guild)
        user_channel = author.voice.channel

        return voice is not None and voice.is_connected() and user_channel == voice.channel



async def setup(client):
    await client.add_cog(MusicCog(client))