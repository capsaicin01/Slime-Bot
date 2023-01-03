import youtube_dl
from MusicClasses.MusicClasses import *

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

song = Song("ytsearch: subaru and duck dance", "capsaicin01")
print(song.description)
print(song.duration_formatted)
print(song.upload_date_raw)
print(song.upload_date_formatted)
print(song.requested_by)