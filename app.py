from flask import Flask, render_template, request, redirect, flash, url_for
import yt_dlp
import os
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

DOWNLOAD_FOLDER = "downloads"
STATIC_FOLDER = "static"  

for folder in [DOWNLOAD_FOLDER, STATIC_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_video(link):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',  
        'merge_output_format': 'mp4'  
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        title = info_dict.get('title', 'video') + ".mp4" 
        downloaded_file = os.path.join(DOWNLOAD_FOLDER, title)
        static_file = os.path.join(STATIC_FOLDER, title)
        shutil.move(downloaded_file, static_file)

        return title 

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        link = request.form.get("link")
        if link:
            try:
                title = download_video(link)
                flash(f"Your video has been processed and is available <a href='/static/{title}' target='_blank'>here</a>", "success")
            except Exception as e:
                flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('home'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
