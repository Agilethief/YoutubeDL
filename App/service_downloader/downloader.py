import yt_dlp
import os

global download_progress, download_status, download_path, download_format
download_progress = 0
download_status = "starting"
download_path = "No path yet"
download_format = ""


def test():
    print("Hello from downloader.py")
    return "Hello from downloader.py"


def main():
    yt_url = "https://www.youtube.com/watch?v=8OAPLk20epo"
    # yt_url = "https://www.youtube.com/watch?v=WVRbo8EeJVs"
    # yt_url = "https://www.youtube.com/playlist?list=PLFBCBEdrXs4M1JOLUEwygABKBQAsUQjL0"
    # yt_url = "https://www.youtube.com/@SMWCustomSongs/videos"
    download_from_yt(yt_url, "high", "m4a")


def download_from_yt(yt_url, quality="high", download_type="m4a"):
    ydl_opts = {}
    global download_progress, download_status, download_path, download_format
    download_progress = 0
    download_status = "starting"
    download_path = "No path yet"
    download_format = download_type

    # Set quality value
    if quality == "high":
        q_value = 0
    elif quality == "med":
        q_value = 5
    else:
        q_value = 9

    # Set download type
    if download_type == "m4a":
        ydl_opts = get_audio_options(q_value, download_type)
    elif download_type == "mp3":
        ydl_opts = get_audio_options(q_value, download_type)
    else:
        ydl_opts = get_video_options()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])


def get_video_options():
    ydl_opts = {
        # "verbose": True,
        "outtmpl": "App/downloads" + "/%(title)s.%(ext)s",  # Save path and file name
        "format": "bestvideo+bestaudio/best",  # Get the best video and audio, fallback to best format
        "merge_output_format": "mp4",  # Ensure the final output is in MP4 format
        "windowsfilenames": True,  # Ensure Windows-compatible filenames
        "nooverwrites": True,  # Prevent overwriting
        "progress_hooks": [progress_hook],
    }

    return ydl_opts


def get_audio_options(quality, download_type):
    ydl_opts = {
        # "verbose": True,
        "outtmpl": "App/downloads" + "/%(title)s.%(ext)s",  # Save path and file name
        "format": "bestaudio/best",  # Get the best audio or fallback to best format
        "postprocessor_args": {
            "ffmpeg": ["-y"],  # Force overwrite without locking
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Extract audio from video
                "preferredcodec": f"{download_type}",  # Convert to m4a
                "preferredquality": f"{quality}",  # '0' means best quality 9 = worst. base is 5
            },
            {
                "key": "FFmpegMetadata",  # Embed metadata (e.g., title, artist)
            },
            {
                "key": "EmbedThumbnail",  # Embed thumbnail into the audio file
                "already_have_thumbnail": False,  # Download thumbnail if not already available
            },
        ],
        "writethumbnail": True,  # Ensure thumbnail is downloaded
        "addmetadata": True,  # Ensure metadata is added
        "merge_output_format": f"{download_type}",  # Final output format
        "windowsfilenames": True,  # Ensure Windows-compatible filenames
        "nooverwrites": True,  # Prevent overwriting
        "progress_hooks": [progress_hook],
    }

    return ydl_opts


# This function is called by the download process to update the progress
def progress_hook(d):
    global download_progress, download_status, download_path, download_format
    print(d)
    if d["status"] == "downloading":
        download_progress = d["downloaded_bytes"] / d["total_bytes"] * 100
        download_status = d["status"]
        download_path = "No path yet"
        print(
            f"Downloading: {d['_percent_str']} of {d['_total_bytes_str'] or 'Unknown size'} at {d['_speed_str']} | ETA: {d['_eta_str']}"
        )

    # Post-processing progress
    elif d["status"] == "postprocessing":
        download_progress = d["downloaded_bytes"] / d["total_bytes"] * 100
        download_status = d["status"]
        download_path = "No path yet"
        print(
            f"Post-processing: {d['postprocessor']} {d.get('postprocessor_stage', '')}"
        )

    # All tasks complete
    elif d["status"] == "finished":
        download_progress = 100
        download_status = d["status"]
        download_path = d["filename"]
        print(f"Download complete: {d['filename']}")

    return


# This function is called by the web client to get the progress of the download
def get_progress():
    global download_progress, download_status, download_path, download_format

    # 0-10 getting thumbnail etc
    # 10-75 downloading
    # 75-90 post-processing
    # 90-100 finished
    if download_progress < 10:
        return {
            "progress": 10,
            "task_complete": False,
            "message": "getting thumbnail",
            "download_url": "no path yet",
            "download_format": download_format,
        }
    elif download_progress < 75:
        return {
            "progress": download_progress,
            "task_complete": False,
            "message": download_status,
            "download_url": download_path,
            "download_format": download_format,
        }
    elif download_progress < 90:
        return {
            "progress": 90,
            "task_complete": False,
            "message": "post processing",
            "download_url": "no path yet",
            "download_format": download_format,
        }
    elif download_progress > 90:

        if download_status == "finished":
            return {
                "progress": 100,
                "task_complete": True,
                "message": download_status,
                "download_url": download_path,
                "download_format": download_format,
            }

        return {
            "progress": download_progress,
            "task_complete": False,
            "message": download_status,
            "download_url": download_path,
            "download_format": download_format,
        }


if __name__ == "__main__":
    main()
