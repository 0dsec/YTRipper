#!/usr/bin/env python3

import sys
import shutil
import os
import subprocess
from typing import Any
import yt_dlp

BLUE = "\033[38;5;117m"  # pastel blue
RED = "\033[38;5;203m"  # pastel red
RESET = "\033[0m"

YT = [
    "oooooo   oooo ooooooooooooo ",
    " `888.   .8'  8'   888   `8 ",
    "  `888. .8'        888      ",
    "   `888.8'         888      ",
    "    `888'          888      ",
    "     888           888      ",
    "    o888o         o888o     ",
    "                            ",
    "                            ",
]

RIPPER = [
    "ooooooooo.    o8o                                           ",
    "`888   `Y88.  `\"'                                           ",
    " 888   .d88' oooo  oo.ooooo.  oo.ooooo.   .ooooo.  oooo d8b ",
    " 888ooo88P'  `888   888' `88b  888' `88b d88' `88b `888\"\"8P ",
    " 888`88b.     888   888   888  888   888 888ooo888  888     ",
    " 888  `88b.   888   888   888  888   888 888    .o  888     ",
    "o888o  o888o o888o  888bod8P'  888bod8P' `Y8bod8P' d888b    ",
    "                    888        888                          ",
    "                   o888o      o888o                         ",
]


def clear_terminal():
    os.system("clear")


def show_banner():
    for left, right in zip(YT, RIPPER):
        print(BLUE + left + RED + right + RESET)
    print()


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed.")
        print("Install it with: sudo pacman -S ffmpeg")
        sys.exit(1)


def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\rDownloading {percent} | {speed} | ETA {eta}", end="")
    elif d["status"] == "finished":
        print("\nDownload complete. Converting to MP3...")


def download_audio(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts: dict[str, Any] = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "noplaylist": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"
        return mp3_file


def open_folder(folder):
    subprocess.Popen(["xdg-open", folder])


def main():
    clear_terminal()
    show_banner()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  ytaudio URL [output_folder]")
        sys.exit(1)

    url = sys.argv[1]

    output_folder = os.path.expanduser("~/YTRips")
    if len(sys.argv) >= 3:
        output_folder = os.path.expanduser(sys.argv[2])

    check_ffmpeg()

    saved_file = download_audio(url, output_folder)

    print("\nDone.")
    print(f"Saved to: {saved_file}")

    open_folder(output_folder)


if __name__ == "__main__":
    main()
