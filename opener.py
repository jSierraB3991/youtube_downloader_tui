import os
import platform
import subprocess
import webbrowser


def open_path(path: str) -> None:
    """Abre un archivo o carpeta con la aplicación/explorador predeterminado del sistema."""
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)  # type: ignore[attr-defined]
        elif system == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def open_in_browser(url: str) -> None:
    """Abre una URL de YouTube en el navegador predeterminado."""
    webbrowser.open(url)