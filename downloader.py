import os
import re
from datetime import date
from typing import Literal

import yt_dlp

from config import today_folder

MediaType = Literal["video", "playlist"]


class DownloadError(Exception):
    """Error de descarga o de tipo de URL incorrecto."""


def sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()


def detect_type(url: str) -> MediaType:
    """Consulta la URL (sin descargar) para saber si es un video o una playlist."""
    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        raise DownloadError(f"No se pudo leer la URL: {e}")

    if info is None:
        raise DownloadError("No se pudo obtener información de la URL.")

    if info.get("_type") == "playlist" or "entries" in info:
        return "playlist"
    return "video"


def download_video(url: str) -> dict:
    """Descarga un solo video en la carpeta de hoy.

    Lanza DownloadError si la URL corresponde a una playlist.
    """
    if detect_type(url) == "playlist":
        raise DownloadError(
            "Esa URL es de una PLAYLIST, no de un video. Usa la tecla de playlist (p)."
        )

    folder = today_folder()
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filepath)
        mp4_path = base + ".mp4"
        if os.path.exists(mp4_path):
            filepath = mp4_path

    return {
        "title": info.get("title", "Video sin título"),
        "type": "video",
        "date": date.today().isoformat(),
        "folder": folder,
        "filepath": filepath,
        "url": url,
    }


def download_playlist(url: str) -> dict:
    """Descarga una playlist completa en una subcarpeta dentro de la carpeta de hoy.

    Lanza DownloadError si la URL corresponde a un solo video.
    """
    if detect_type(url) == "video":
        raise DownloadError(
            "Esa URL es de un VIDEO, no de una playlist. Usa la tecla de video (v)."
        )

    base_folder = today_folder()

    probe_opts = {"quiet": True, "no_warnings": True, "extract_flat": True}
    with yt_dlp.YoutubeDL(probe_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    playlist_title = sanitize(info.get("title") or "Playlist")

    playlist_folder = os.path.join(base_folder, playlist_title)
    os.makedirs(playlist_folder, exist_ok=True)

    opts = {
        "quiet": True,
        "no_warnings": True,
        "outtmpl": os.path.join(playlist_folder, "%(playlist_index)s - %(title)s.%(ext)s"),
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    return {
        "title": playlist_title,
        "type": "playlist",
        "date": date.today().isoformat(),
        "folder": playlist_folder,
        "filepath": None,
        "url": url,
    }