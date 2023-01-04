import discord
import youtube_dl


class Song(dict):

    """
    This is a class for creating a song object from an url or a song name.

    Attributes:
        url (str): Mp3 file url of the song.
        title (str): Title of the song.
        thumbnail (str): Thumbnail url of the song.
        channel (str): Channel name of the song uploader.
        duration_raw (int): Duration of the song by seconds.
        duration_formatted (str): Duration of the song as '<minutes>m <seconds>s'.
        upload_date_raw (int): Upload date of the song as 'yyyymmdd'.
        upload_date_formatted (str): Upload date of the song as 'dd/mm/yyyy'.
        views (int): Number of views of the song.
        requested_by (discord.Member): User who requested the song.

    """



    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def __init__(self, url:str, author:discord.Member):
        super().__init__()
        self.download_info(url, author)
    
    def download_info(self, url, author:discord.Member):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:

            info = ydl.extract_info(url, download=False)
            if url.startswith("ytsearch:"):
                info = ydl.extract_info(info["entries"][0]["webpage_url"], download=False)
            info.pop("formats")
            info.pop("thumbnails")

            self.update(info)
            self["requested_by"] = author
            print(self)

    @property
    def url(self):
        return self.get("url")

    @property
    def title(self):
        return self.get("title")

    @property
    def thumbnail(self):
        return self.get("thumbnail")

    @property
    def channel(self):
        return self.get("channel")

    @property
    def duration_raw(self):
        return self.get("duration")

    @property
    def duration_formatted(self):
        minutes, seconds = self.duration_raw // 60, self.duration_raw % 60
        return f"{minutes}m {seconds}s"

    @property
    def upload_date_raw(self):
        return self.get("upload_date")

    @property
    def upload_date_formatted(self):
        date = self.upload_date_raw
        d, m, y = date[6:8], date[4:6], date[0:4]
        return f"{d}/{m}/{y}"

    @property
    def views(self):
        return self.get("view_count")

    @property
    def requested_by(self):
        return self.get("requested_by")


class Queue(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._currentSong = None

    def next_song(self):
        next_one = self.pop(0)
        self._currentSong = next_one
        return self._currentSong

    def clear(self):
        super().clear()
        self._currentSong = None
    
    def get_embed(self, song_index=0):
        
        if song_index <= 0:
            song = self._currentSong
        else:
            song = self[song_index - 1]
        
        embed = discord.Embed()
        embed.color = discord.Color.teal()
        embed.title = "Song Info"
        
        embed.set_thumbnail(url=song.thumbnail)
        embed.add_field(name="Title", value = song.title)
        embed.add_field(name="Channel", value = song.channel)
        embed.add_field(name="Duration", value = song.duration_formatted)
        embed.add_field(name="Upload Date", value = song.upload_date_formatted)
        embed.add_field(name="Views", value = song.views)
        embed.add_field(name="Requested By", value = song.requested_by.mention)

        return embed
