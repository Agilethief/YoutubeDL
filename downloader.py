import yt_dlp


def main():
    yt_url = "https://www.youtube.com/watch?v=8OAPLk20epo"
    # yt_url = "https://www.youtube.com/watch?v=WVRbo8EeJVs"
    # yt_url = "https://www.youtube.com/playlist?list=PLFBCBEdrXs4M1JOLUEwygABKBQAsUQjL0"
    # yt_url = "https://www.youtube.com/@SMWCustomSongs/videos"
    download_audio(yt_url)


def download_audio(yt_url):
    ydl_opts = {
        # "verbose": True,
        "outtmpl": "downloads" + "/%(title)s.%(ext)s",  # Save path and file name
        "format": "bestaudio/best",  # Get the best audio or fallback to best format
        "postprocessor_args": {
            "ffmpeg": ["-y"],  # Force overwrite without locking
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Extract audio from video
                "preferredcodec": "m4a",  # Convert to m4a
                "preferredquality": "5",  # '0' means best quality 9 = worst. base is 5
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
        "merge_output_format": "m4a",  # Final output format
        "windowsfilenames": True,  # Ensure Windows-compatible filenames
        "nooverwrites": True,  # Prevent overwriting
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])


if __name__ == "__main__":
    main()
