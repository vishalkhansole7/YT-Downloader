from flask import Flask, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>VK's YouTube Downloader</title>
            <meta name="description" content="Download YouTube videos easily!">
            <meta name="keywords" content="YouTube, downloader, video, download, vk">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                input[type="text"] { width: 300px; padding: 10px; }
                input[type="submit"] { padding: 10px 20px; }
            </style>
        </head>
        <body>
            <h1>VK's YouTube Downloader</h1>
            <form action="/download" method="post">
                <input type="text" name="url" placeholder="Enter YouTube video URL" required>
                <input type="submit" value="Download">
            </form>
        </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url'].strip()  # Trim any leading/trailing spaces
    if not url:
        return "Error: URL cannot be empty.", 400  # Return an error if the URL is empty
    try:
        print(f"Attempting to download from URL: {url}")  # Debug output
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()

        # File path of the downloaded video
        file_path = video.default_filename
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"Error occurred: {e}")  # Debug output
        return str(e), 400  # Return the error message with a 400 status code

if __name__ == '__main__':
    app.run(debug=True)
