from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import re

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_DIR = "downloads"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="VK's YouTube Downloader - Download your favorite YouTube videos effortlessly.">
    <meta name="keywords" content="YouTube, Video Downloader, VK's YT Downloader, Flask App">
    <title>VK's YT Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        input[type="submit"] {
            background: #28a745;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        input[type="submit"]:hover {
            background: #218838;
        }
        .error {
            color: red;
            text-align: center;
        }
    </style>
    <script>
        function validateURL() {
            const urlInput = document.getElementById("url");
            const url = urlInput.value;
            const regex = /^(https?:\\/\\/)?(www\\.)?(youtube\\.com|youtu\\.be)\\/[^\\s]+$/;
            if (!regex.test(url)) {
                alert("Please enter a valid YouTube URL.");
                urlInput.focus();
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
<script type="text/javascript">
	atOptions = {
		'key' : '32c894c8b7c3109ac13f4527145b12e6',
		'format' : 'iframe',
		'height' : 90,
		'width' : 728,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//humiliatesmug.com/32c894c8b7c3109ac13f4527145b12e6/invoke.js"></script>

<script type="text/javascript">
	atOptions = {
		'key' : '32c894c8b7c3109ac13f4527145b12e6',
		'format' : 'iframe',
		'height' : 90,
		'width' : 728,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//humiliatesmug.com/32c894c8b7c3109ac13f4527145b12e6/invoke.js"></script>

<script async="async" data-cfasync="false" src="//humiliatesmug.com/36469c754dfca52f78bbad579a80bb97/invoke.js"></script>
<div id="container-36469c754dfca52f78bbad579a80bb97"></div>
<script type="text/javascript">
	atOptions = {
		'key' : '32c894c8b7c3109ac13f4527145b12e6',
		'format' : 'iframe',
		'height' : 90,
		'width' : 728,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//humiliatesmug.com/32c894c8b7c3109ac13f4527145b12e6/invoke.js"></script>


<script type="text/javascript">
	atOptions = {
		'key' : '32c894c8b7c3109ac13f4527145b12e6',
		'format' : 'iframe',
		'height' : 90,
		'width' : 728,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//humiliatesmug.com/32c894c8b7c3109ac13f4527145b12e6/invoke.js"></script>


    <h1>VK's YT Downloader</h1>
    <form action="/" method="POST" onsubmit="return validateURL();">
        <input type="text" name="url" id="url" placeholder="Enter YouTube video URL" required>
        <input type="submit" value="Download">
    </form>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    <p>
    <script type="text/javascript">
	atOptions = {
		'key' : '32c894c8b7c3109ac13f4527145b12e6',
		'format' : 'iframe',
		'height' : 90,
		'width' : 728,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//humiliatesmug.com/32c894c8b7c3109ac13f4527145b12e6/invoke.js"></script>
<script type="text/javascript">
	atOptions = {
		'key' : '32c894c8b7c3109ac13f4527145b12e6',
		'format' : 'iframe',
		'height' : 90,
		'width' : 728,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//humiliatesmug.com/32c894c8b7c3109ac13f4527145b12e6/invoke.js"></script>

   <script async="async" data-cfasync="false" src="//humiliatesmug.com/36469c754dfca52f78bbad579a80bb97/invoke.js"></script>
<div id="container-36469c754dfca52f78bbad579a80bb97"></div>
    </p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not is_valid_youtube_url(url):
            return render_template_string(HTML_TEMPLATE, error="Invalid YouTube URL. Please enter a valid URL.")
        
        try:
            video_path = download_video(url)
            return send_file(video_path, as_attachment=True)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
    return render_template_string(HTML_TEMPLATE)

def download_video(url):
    ydl_opts = {
        'format': 'best',  # No need for format conversion
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = os.path.join(DOWNLOAD_DIR, f"{info_dict['title']}.{info_dict['ext']}")
        if not os.path.exists(file_path):
            raise Exception("Download failed.")
        return file_path

def is_valid_youtube_url(url):
    regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    return re.match(regex, url) is not None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
