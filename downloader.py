import subprocess
import os

def download_spotify(query):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(
        ['spotdl', query, '--output', output_dir],
        capture_output=True, text=True
    )
    files = os.listdir(output_dir)
    files = [f for f in files if f.endswith('.mp3')]
    if files:
        return os.path.join(output_dir, files[0])
    return None

def download_youtube(query):
    import youtube_dl
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        if 'entries' in info and info['entries']:
            filename = ydl.prepare_filename(info['entries'][0]).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return filename
    return None

def download_soundcloud(query):
    # این بخش نیاز به پیاده‌سازی با API ساندکلاد دارد
    # فعلاً به صورت نمونه:
    return None 