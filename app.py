from flask import Flask, redirect, render_template, request, send_file
from pytubefix import Search, YouTube
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search = request.form.get("search")
        titles = []
        ids = []
        try:
            search = Search(search)
            for result in search.videos:
                titles.append(result.title)
                ids.append(result.video_id)
            musics = zip(titles, ids)
        except Exception as e:
            print(f"An error occurred: {e}")
        return render_template("main.html", musics=musics)
    else:
        return render_template("main.html")

@app.route("/download", methods=["POST"])
def download():
    id = request.form.get("id")
    yt = YouTube.from_id(id).streams.get_audio_only()
    path = yt.download(filename=f"{yt.title}.mp3", output_path="static/buffer")
    response = send_file(path, as_attachment=True, download_name=f"{yt.title}.mp3")
    os.remove(path)
    return response

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
