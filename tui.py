from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DataTable, Footer, Header, Input, Label

from downloader import DownloadError, download_playlist, download_video
from history import add_entry, load_history
from opener import open_in_browser, open_path


class YTDownloaderApp(App):
    CSS = """
    #mode-label {
        padding: 1;
        text-style: bold;
    }
    #status-label {
        padding: 0 1;
        color: $warning;
        height: 1;
    }
    """

    BINDINGS = [
        Binding("v", "set_mode_video", "Modo Video"),
        Binding("p", "set_mode_playlist", "Modo Playlist"),
        Binding("o", "open_browser", "Ver en YouTube"),
        Binding("q", "quit", "Salir"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.mode: str = "video"
        self.history_data: list = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label(
            "Modo actual: VIDEO   (v = video, p = playlist, o = abrir en YouTube)",
            id="mode-label",
        )
        yield Input(
            placeholder="Pega aquí la URL de un video de YouTube...", id="url-input"
        )
        yield Label("", id="status-label")
        yield DataTable(id="history-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Tipo", "Título", "Fecha", "Carpeta")
        table.cursor_type = "row"
        self.refresh_history()
        self.query_one(Input).focus()

    def refresh_history(self) -> None:
        self.history_data = load_history()
        table = self.query_one(DataTable)
        table.clear()
        for entry in self.history_data:
            tipo = "Playlist" if entry["type"] == "playlist" else "Video"
            table.add_row(tipo, entry["title"], entry["date"], entry["folder"])

    def set_status(self, message: str) -> None:
        self.query_one("#status-label", Label).update(message)

    def action_set_mode_video(self) -> None:
        self.mode = "video"
        self.query_one("#mode-label", Label).update(
            "Modo actual: VIDEO   (v = video, p = playlist, o = abrir en YouTube)"
        )
        self.query_one(Input).placeholder = "Pega aquí la URL de un video de YouTube..."
        self.set_status("")

    def action_set_mode_playlist(self) -> None:
        self.mode = "playlist"
        self.query_one("#mode-label", Label).update(
            "Modo actual: PLAYLIST   (v = video, p = playlist, o = abrir en YouTube)"
        )
        self.query_one(Input).placeholder = "Pega aquí la URL de una playlist de YouTube..."
        self.set_status("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        url = event.value.strip()
        if not url:
            return
        event.input.value = ""
        self.set_status("Descargando... esto puede tardar.")
        self.do_download(url, self.mode)

    @work(thread=True)
    def do_download(self, url: str, mode: str) -> None:
        try:
            if mode == "video":
                entry = download_video(url)
            else:
                entry = download_playlist(url)
            add_entry(entry)
            self.call_from_thread(self.on_download_success, entry)
        except DownloadError as e:
            self.call_from_thread(self.set_status, f"Error: {e}")
        except Exception as e:
            self.call_from_thread(self.set_status, f"Error inesperado: {e}")

    def on_download_success(self, entry: dict) -> None:
        self.set_status(f"Descargado: {entry['title']}")
        self.refresh_history()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        index = event.cursor_row
        if index is None or index >= len(self.history_data):
            return
        entry = self.history_data[index]
        if entry["type"] == "playlist":
            open_path(entry["folder"])
        else:
            open_path(entry["filepath"])

    def action_open_browser(self) -> None:
        table = self.query_one(DataTable)
        index = table.cursor_row
        if index is None or index >= len(self.history_data):
            self.set_status("Selecciona un elemento del historial primero.")
            return
        entry = self.history_data[index]
        open_in_browser(entry["url"])