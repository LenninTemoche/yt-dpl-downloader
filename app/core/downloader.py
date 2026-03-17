import yt_dlp
import os

# Raíz del proyecto (donde están yt-dlp.exe y ffmpeg.exe)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Downloader:
    def __init__(self, output_path="descargas"):
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

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
            'no_warnings': True,
            'no_color': True,
        }
        ffmpeg_loc = self._get_ffmpeg_location()
        if ffmpeg_loc:
            ydl_opts['ffmpeg_location'] = ffmpeg_loc

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get("title", "Video"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", ""),
                    "uploader": info.get("uploader", ""),
                }
            except Exception as e:
                return {"error": str(e)}

    def download(self, url: str, mode: str = "video", quality: str = "720",
                 output_path: str = None, progress_hook=None) -> dict:
        """
        Descarga el video o audio.
        mode: 'video' o 'audio'
        quality: '360', '720', '1080'
        output_path: ruta donde guardar (opcional, usa self.output_path por defecto)
        """
        save_path = output_path or self.output_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'no_color': True,
            'quiet': True,
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
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return {"success": True, "path": save_path}
            except Exception as e:
                return {"success": False, "error": str(e)}
