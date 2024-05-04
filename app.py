from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube, Playlist
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['downloadType']
    download_location = request.form['downloadLocation']  # Retrieve the download folder path from the form

    try:
        if download_type == 'single':
            download_single_video(url, download_location)  # Pass the download location to the function
        elif download_type == 'playlist':
            download_playlist_videos(url, download_location)  # Pass the download location to the function
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('index.html', error=str(e))

def download_single_video(video_url, download_location):
    try:
        video = YouTube(video_url)
        # Check if 720p stream is available, if not, try 480p
        stream_720p = video.streams.filter(res='720p', file_extension='mp4').first()
        stream_480p = video.streams.filter(res='480p', file_extension='mp4').first()

        if stream_720p:
            stream = stream_720p
            resolution = '720p'
        elif stream_480p:
            stream = stream_480p
            resolution = '480p'
        else:
            print(f"No suitable streams available for video: {video.title}")
            return

        output_file_path = Path(download_location) / f'{video.title}_{resolution}.mp4'  # Use the provided download location
        if not output_file_path.is_file():
            stream.download(download_location)
            print(f"Downloaded video ({resolution}): {video.title}")
        else:
            print(f"Video '{video.title}' ({resolution}) already exists in the download folder, skipping download.")
    except Exception as e:
        print(f"Error downloading video: {e}")

def download_playlist_videos(playlist_url, download_location):
    try:
        playlist = Playlist(playlist_url)
        for video_url in playlist.video_urls:
            download_single_video(video_url, download_location)  # Download each video in the playlist
    except Exception as e:
        print(f"Error downloading playlist videos: {e}")

if __name__ == "__main__":
    app.run(debug=True)
