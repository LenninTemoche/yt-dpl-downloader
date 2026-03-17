# yt-dpl Downloader V0.3

Este proyecto simplifica la descarga de contenido multimedia mediante herramientas de código abierto como `yt-dlp` y `FFmpeg`. Incluye una **interfaz gráfica moderna** construida con Streamlit, diseñada con estética futurista y preparada para escalar hacia funcionalidades de IA.

---

## Preview
### Vista Principal
![Vista principal del yt-dpl Downloader](docs/screenshots/main_view.png)

### AI Suite + Historial
![Sección AI Intelligence Suite e historial de descargas](docs/screenshots/ai_suite_history.png)

---

## Estructura del Proyecto
```
yt-dpl-downloader/
├── app/
│   ├── main.py           ← Interfaz Streamlit (UI)
│   ├── core/
│   │   └── downloader.py ← Lógica de descarga (yt-dlp)  
│   ├── data/
│   │   └── history_manager.py ← Historial (JSON)
│   ├── services/         ← (Etapa 2: IA / APIs)
│   └── utils/            ← Helpers
├── descargas/            ← Videos descargados
├── docs/screenshots/     ← Capturas
├── yt-dlp.exe
├── ffmpeg.exe, ffprobe.exe
├── Lanzar_Hub.bat        ← Doble clic
├── .gitignore
└── README.md
```

## Modo Aplicación Gráfica
1. **Doble clic** `Lanzar_Hub.bat`
2. Abre `http://localhost:8501`
3. **Pega URL** → Formato → **⬇️ Download**

### Funcionalidades V0.3 
- ✅ **Solo 1er video** playlists (no bucles)
- ✅ **Sin warnings** JavaScript
- ✅ Botón deshabilitado en descarga
- ✅ Warning playlist detectada
- Barra progreso + historial

## Terminal
```powershell
.\yt-dlp.exe -f \"bv[height<=720][ext=mp4]+ba\" --merge-output-format mp4 \"URL\"
.\yt-dlp.exe -x --audio-format mp3 \"URL\"
```

## Recomendaciones
- `.\yt-dlp.exe --update`
- `python -m streamlit run app/main.py`

## Seguridad (Verificado)
- SSL verificado (sin bypass)
- Paths seguros
- subprocess tkinter seguro  
- Local-only

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
*V0.3 (2026) - Proyecto desarrollado con fines educativos y de experimentación*
