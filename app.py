from flask import Flask, render_template, request, redirect, flash, url_for
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(link):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',  # Ensures high-quality video + audio
        'merge_output_format': 'mp4'  # Ensures mp4 output
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        link = request.form.get("link")
        if link:
            try:
                download_video(link)
                flash("Download successful!", "success")
            except Exception as e:
                flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('home'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
