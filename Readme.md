# yt-dpl Downloader V0.2

Este proyecto simplifica la descarga de contenido multimedia mediante herramientas de código abierto como `yt-dlp` y `FFmpeg`. Incluye una **interfaz gráfica moderna** construida con Streamlit, diseñada con estética futurista y preparada para escalar hacia funcionalidades de IA.

---

## 📸 Preview

### Vista Principal
![Vista principal del yt-dpl Downloader](docs/screenshots/main_view.png)

### AI Suite + Historial
![Sección AI Intelligence Suite e historial de descargas](docs/screenshots/ai_suite_history.png)

---

## Estructura del Proyecto

```text
yt-dpl-downloader/
├── app/
│   ├── main.py           ← Interfaz Streamlit (UI)
│   ├── core/
│   │   └── downloader.py ← Lógica de descarga (yt-dlp)
│   ├── data/
│   │   └── history_manager.py ← Historial (JSON)
│   ├── services/         ← (Etapa 2: IA / APIs / MCP)
│   └── utils/            ← Helpers
├── descargas/            ← Videos descargados
├── docs/screenshots/     ← Capturas de pantalla
├── venv/                 ← Entorno virtual Python
├── yt-dlp.exe            ← Binario del extractor
├── ffmpeg.exe            ← Codificador audio/video
├── ffprobe.exe           ← Análisis multimedia
├── Lanzar_Hub.bat        ← Acceso directo (doble clic)
├── .env                  ← Variables de entorno (privado)
├── .gitignore            ← Archivos excluidos de Git
└── Readme.md
```

---

## Modo Aplicación Gráfica (Streamlit)

1.  Ejecuta el archivo `Lanzar_Hub.bat` (doble clic).
2.  Se abrirá automáticamente en tu navegador en `http://localhost:8501`.
3.  Pega la URL, elige formato (MP4/MP3), calidad y descarga con progreso en tiempo real.

### Funcionalidades
- **Selector de formato:** Video (MP4) o Audio (MP3)
- **Calidad:** 360p, 720p (default), 1080p
- **Barra de progreso:** Visualización en tiempo real
- **Historial:** Tabla con descargas recientes
- **Ruta de descarga:** Visible en el sidebar y en opciones

---

## Modo Terminal (Legacy)

Si prefieres la línea de comandos, abre PowerShell en la carpeta del proyecto:

### Resolución 1080p (Alta Definición)
```powershell
.\yt-dlp.exe -f "bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 "URL"
```

### Resolución 720p (Estándar)
```powershell
.\yt-dlp.exe -f "bv[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]" --merge-output-format mp4 "URL"
```

### Resolución 360p (Baja/Móvil)
```powershell
.\yt-dlp.exe -f "bv[height<=360][ext=mp4]+ba[ext=m4a]/b[height<=360][ext=mp4]" --merge-output-format mp4 "URL"
```

### Guardar en carpeta específica
```powershell
.\yt-dlp.exe -o "descargas/%(title)s.%(ext)s" "URL"
```

### Solo Audio (MP3)
```powershell
.\yt-dlp.exe -x --audio-format mp3 "URL"
```

---

## 🔧 Recomendaciones

- **Actualizar yt-dlp:** `.\yt-dlp.exe -U`
- **Entorno virtual:** Todas las dependencias están aisladas en `venv/`
- **Privacidad:** Las claves API se guardan en `.env` (excluido de Git)

---

## Roadmap: Etapa 2 (IA)

La arquitectura está preparada para escalar a:
- **Transcripción:** Conversión de audio a texto vía APIs externas
- **Resúmenes IA:** Generación automática de puntos clave
- **Chat con Video:** Consultas interactivas sobre el contenido

---

## Aviso Legal y Responsabilidad

El uso de esta herramienta está destinado exclusivamente a **fines educativos y de investigación**.

1. **Derechos de Autor:** El usuario es el único responsable de respetar los términos de servicio de las plataformas y las leyes de propiedad intelectual vigentes.
2. **Exención de Responsabilidad:** Los creadores de esta guía y herramientas no se hacen responsables del uso indebido o descargas ilegales.

---

## Créditos y Reconocimientos

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp):** Extractor de contenido multimedia open-source.
- **[FFmpeg](https://ffmpeg.org/):** Biblioteca líder para manejo de audio y video.
- **[Streamlit](https://streamlit.io/):** Framework para interfaces de datos interactivas.

---
*Proyecto para entornos de desarrollo colaborativo y educativo.*
