from App import app
from flask import render_template, flash, redirect, request, jsonify
from App.forms import DownloadVideoForm
import threading
import time
from App.service_downloader import downloader


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
