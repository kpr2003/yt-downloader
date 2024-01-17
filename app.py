from flask import Flask, render_template, request, jsonify, send_file
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('videoUrl')
    try:
        yt = YouTube(video_url)
        title = yt.title
        views = yt.views
        yd = yt.streams.get_highest_resolution()
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, f"{title}.mp4")
        yd.download(temp_dir)
        response = send_file(video_path, as_attachment=True, download_name=f"{title}.mp4")
        os.remove(video_path)
        os.rmdir(temp_dir)        
        return response
    except Exception as e:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
