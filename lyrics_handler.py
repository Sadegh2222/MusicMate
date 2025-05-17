import lyricsgenius
from config import GENIUS_API_TOKEN

def get_lyrics(song_name):
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
    song = genius.search_song(song_name)
    return song.lyrics if song else "متن آهنگ پیدا نشد." 