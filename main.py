#!/usr/bin/env python3
"""YouTube TUI Downloader - punto de entrada."""

from config import today_folder

if __name__ == "__main__":
    # Verifica si la carpeta de hoy existe; si no, la crea.
    today_folder()

    from tui import YTDownloaderApp

    app = YTDownloaderApp()
    app.run()