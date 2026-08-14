# YouTube TUI Downloader

TUI en Python para descargar videos y playlists de YouTube, organizados por fecha.

## Cómo se ve

```
┌ YouTube TUI Downloader ────────────────────────────────── 14:32:07 ┐
│ Modo actual: VIDEO   (v = video, p = playlist, o = abrir en YouTube)│
│ ┌──────────────────────────────────────────────────────────────┐   │
│ │ Pega aquí la URL de un video de YouTube...                    │   │
│ └──────────────────────────────────────────────────────────────┘   │
│ Descargado: Nombre del video de ejemplo                             │
│ ┌────────────┬───────────────────────────┬────────────┬─────────┐ │
│ │ Tipo       │ Título                    │ Fecha      │ Carpeta │ │
│ ├────────────┼───────────────────────────┼────────────┼─────────┤ │
│ │ Video      │ Nombre del video ejemplo  │ 2026-08-14 │ .../14  │ │
│ │ Playlist   │ Mi playlist de música     │ 2026-08-14 │ .../14  │ │
│ │ Video      │ Otro video más            │ 2026-08-13 │ .../13  │ │
│ └────────────┴───────────────────────────┴────────────┴─────────┘ │
│ v Modo Video   p Modo Playlist   o Ver en YouTube   q Salir         │
└──────────────────────────────────────────────────────────────────┘
```

- La etiqueta superior indica el modo activo (video o playlist).
- El campo de texto es donde pegas la URL.
- Debajo aparece el mensaje de estado (éxito, error, "descargando...").
- La tabla inferior es el historial: cada fila muestra tipo, título, fecha y carpeta.
- La barra inferior (Footer) lista los atajos de teclado disponibles.

## Requisitos

- Python 3.9+
- ffmpeg instalado en el sistema (necesario para que yt-dlp fusione audio y video)

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

### Atajos

- **v** — Modo video (pega la URL de un video individual)
- **p** — Modo playlist (pega la URL de una playlist)
- **Enter** (en el campo de texto) — Descarga la URL pegada
- **Enter** (sobre una fila del historial) — Reproduce el video en el reproductor predeterminado, o abre la carpeta de la playlist en el explorador de archivos
- **o** — Abre la URL del elemento seleccionado en el navegador predeterminado
- **q** — Salir

### Validación de tipo

Si pegas una URL de playlist estando en modo video (o viceversa), la app muestra un error y no descarga nada.

## Estructura de descargas

```
downloads/
  2026-08-14/
    Nombre del video.mp4
    Nombre de la playlist/
      1 - Primer video.mp4
      2 - Segundo video.mp4
```

Cada día se crea automáticamente su propia carpeta con la fecha (AAAA-MM-DD).

## Historial

El historial se guarda en `history.json`, junto a `main.py`. Cada entrada registra:

- Título del video o playlist
- Tipo (video o playlist)
- Fecha de descarga
- Carpeta donde quedó guardado
- URL original

## Licencia

Este proyecto está bajo la licencia [GPL v3](./LICENSE). Ver el archivo `LICENSE` en esta misma carpeta para el texto completo.
