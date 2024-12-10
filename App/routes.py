from App import app
from flask import (
    render_template,
    flash,
    redirect,
    request,
    jsonify,
    send_file,
    send_from_directory,
)
from App.forms import DownloadVideoForm
import threading
import time
from App.service_downloader import downloader
import os, io
import zipfile


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "WOWIE HARRY POTTER"}
    form = DownloadVideoForm()
    return render_template("index.html", title="Home", form=form)


@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    print(data)

    video_url = data["video_url"]
    download_type = data["download_type"]
    quality = data["quality"]

    global progressAmount, task_complete, message
    progressAmount = 0
    task_complete = False
    message = "Starting download..."
    thread = threading.Thread(
        target=downloader.download_from_yt, args=(video_url, quality, download_type)
    )
    thread.daemon = True
    thread.start()

    return jsonify({"message": "Starting"})


# Simple route to get progress of the download
@app.route("/progress")
def progress():
    downloader_progress = downloader.get_progress()
    print("progress", downloader_progress)
    return jsonify(
        {
            "progress": downloader_progress["progress"],
            "task_complete": downloader_progress["task_complete"],
            "message": downloader_progress["message"],
            "download_url": downloader_progress["download_url"],
        }
    )

    # Old way to test with
    return jsonify(
        {
            "progress": progressAmount,
            "task_complete": task_complete,
            "message": message,
        }
    )


# Simulate a long-running task just for testing
def download_task():
    global progressAmount, task_complete, message

    # Simulate a long-running task
    for i in range(101):
        progressAmount = i
        message = downloader.test()
        time.sleep(0.1)
    task_complete = True


@app.route("/download_file/<filename>")
def download_file(filename):

    file_url = f"downloads/{filename}"
    # return send_from_directory
    return send_file(file_url, as_attachment=True)


@app.route("/delete_file/<filename>")
def delete_file(filename):

    file_url = f"App/downloads/{filename}"
    os.remove(file_url)
    return redirect("/")


@app.route("/download_all")
def download_all_files():

    zipbuffer = io.BytesIO()

    with zipfile.ZipFile(zipbuffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir("App/downloads"):
            file_path = os.path.join("App/downloads", file)  # Full path to the file
            arcname = os.path.basename(file)  # Only the file name
            zip_file.write(file_path, arcname=arcname)

    zipbuffer.seek(0)

    # return send_from_directory
    return send_file(
        zipbuffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="downloaded_youtube_files.zip",
    )


@app.route("/delete_all")
def delete_all_files():
    files = get_download_files()
    for filename in files:
        file_url = f"App/downloads/{filename}"
        os.remove(file_url)

    return redirect("/")


@app.route("/downloadedfiles")
def downloads_page():
    files = get_download_files()
    return render_template("downloadedfiles.html", files=files)


@app.route("/get_downloadedfiles")
def get_downloaded_files():
    files = get_download_files()
    print(files)
    print(jsonify(files))
    return jsonify(files)


def get_download_files():
    files = os.listdir("App/downloads")
    print(files)
    for file in files:
        print(file)
    return files
