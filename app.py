from __future__ import unicode_literals
from flask import Flask
from flask import send_from_directory
import youtube_dl

app = Flask(__name__)
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dl/<id>')
def download_yt(id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './dl/' + id + ".mp3",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + id])
        return 'https://rex-yt-dl.herokuapp.com/uploads/' + id + ".mp3"

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory("./dl/", filename, as_attachment=True)

if __name__ == '__main__':
   app.run()
