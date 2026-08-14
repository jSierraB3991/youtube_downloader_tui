import os
from datetime import date

DOWNLOADS_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "downloads"
)
HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history.json"
)


def today_folder() -> str:
    """Verifica si la carpeta de la fecha de hoy existe; si no, la crea. Devuelve la ruta."""
    folder = os.path.join(DOWNLOADS_ROOT, date.today().isoformat())
    os.makedirs(folder, exist_ok=True)
    return folder