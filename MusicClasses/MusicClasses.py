import discord
import youtube_dl


class Song(dict):

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
    def description(self):
        return self.get("description")

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
    def requested_by(self):
        return self.get("requested_by")