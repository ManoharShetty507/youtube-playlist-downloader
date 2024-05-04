from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube, Playlist
from pathlib import Path
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['downloadType']

    try:
        if download_type == 'single':
            filename, download_link = get_video_download_link(url)
            return render_template('index.html', filename=filename, download_link=download_link)
        elif download_type == 'playlist':
            playlist_title, playlist_download_links = get_playlist_download_links(url)
            return render_template('playlist.html', playlist_title=playlist_title, download_links=playlist_download_links)
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('index.html', error=str(e))

def get_video_download_link(video_url):
    try:
        video = YouTube(video_url)
        stream = video.streams.get_highest_resolution()
        download_link = stream.url
        filename = f'{video.title}.mp4'
        return filename, download_link
    except Exception as e:
        print(f"Error getting video download link: {e}")
        return None, None

def get_playlist_download_links(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title
        playlist_download_links = []

        for video in playlist.videos:
            filename, download_link = get_video_download_link(video.watch_url)
            playlist_download_links.append((filename, download_link))

        return playlist_title, playlist_download_links
    except Exception as e:
        print(f"Error getting playlist download links: {e}")
        return None, None

@app.route('/download_video', methods=['GET'])
def download_video():
    download_link = request.args.get('download_link')
    response = requests.get(download_link)
    if response.status_code == 200:
        return response.content, 200, {'Content-Type': 'application/octet-stream', 'Content-Disposition': 'attachment; filename=video.mp4'}
    else:
        return "Error downloading video", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
