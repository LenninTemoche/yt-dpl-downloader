import yt_dlp
import os

# Raíz del proyecto (donde están yt-dlp.exe y ffmpeg.exe)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Downloader:
    def __init__(self, output_path="descargas"):
        # Asegurar que la ruta no sea vacía o nula
        self.output_path = output_path if (output_path and output_path.strip()) else "descargas"
        if not os.path.exists(self.output_path):
            try:
                os.makedirs(self.output_path)
            except Exception:
                pass # Evitar caída si la ruta es inválida

    def _get_ffmpeg_location(self):
        """Busca ffmpeg.exe en la raíz del proyecto."""
        ffmpeg_path = os.path.join(PROJECT_ROOT, "ffmpeg.exe")
        if os.path.exists(ffmpeg_path):
            return PROJECT_ROOT
        # Fallback: buscar en subcarpeta ffmpeg
        ffmpeg_sub = os.path.join(PROJECT_ROOT, "ffmpeg", "ffmpeg.exe")
        if os.path.exists(ffmpeg_sub):
            return os.path.join(PROJECT_ROOT, "ffmpeg")
        return None

    def get_video_info(self, url: str) -> dict:
        """Obtiene información básica del video sin descargarlo."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': False,
            'no_color': True,
            'noplaylist': True,
            'playlistend': 1,
            'skip_download': True,
            'socket_timeout': 15,
            'extract_flat': True,
            'ignore_javascript_errors': True,
        }
        ffmpeg_loc = self._get_ffmpeg_location()
        if ffmpeg_loc:
            ydl_opts['ffmpeg_location'] = ffmpeg_loc

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return {"error": "No se pudo obtener información del video"}
                
                return {
                    "title": info.get("title", "Video"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", ""),
                    "uploader": info.get("uploader", ""),
                    "is_playlist": info.get("_type", "").startswith("playlist"),
                }
        except Exception as e:
            error_msg = str(e)
            if "Unsupported URL" in error_msg:
                error_msg = "URL no soportada. Verifica el enlace."
            elif "Connection" in error_msg:
                error_msg = "Error de conexión. Reintenta."
            elif "rate-limited" in error_msg:
                error_msg = "YouTube ha bloqueado temporalmente la IP (Rate Limit). Espera unos minutos."
            return {"error": error_msg}

    def download(self, url: str, mode: str = "video", quality: str = "720",
                 output_path: str = None, progress_hook=None) -> dict:
        """
        Descarga el video o audio.
        """
        save_path = output_path or self.output_path
        if not save_path or not save_path.strip():
            save_path = "descargas"
            
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path, exist_ok=True)
            except Exception:
                pass

        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'no_color': True,
            'quiet': True,
'sleep_interval': 3,
            'max_sleep_interval': 10,
            'noplaylist': True,
            'playlistend': 1,
            'ignore_javascript_errors': True,
        }

        # Agregar ruta de ffmpeg
        ffmpeg_loc = self._get_ffmpeg_location()
        if ffmpeg_loc:
            ydl_opts['ffmpeg_location'] = ffmpeg_loc

        if mode == "audio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({
                'format': f'bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[height<={quality}][ext=mp4]',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # El bucle de reintentos es manejado internamente por yt-dlp con sleep_interval
                ydl.download([url])
                return {"success": True, "path": save_path}
            except Exception as e:
                return {"success": False, "error": str(e)}
