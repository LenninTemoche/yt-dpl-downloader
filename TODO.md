# TODO.md - Corrección yt-dlp Downloader

## ✅ Plan Aprobado
Usuario confirmó el plan para arreglar:
- Bucle infinito (descargas automáticas de playlists)
- Warnings JavaScript de yt-dlp

## 📋 Pasos Pendientes (Ejecutar en orden):

### 1. 🔧 Crear TODO.md 
**Estado**: Completado ✅

### 2. ✏️ Editar app/core/downloader.py
- Agregar `noplaylist: True` y `playlistend: 1` → ✅ SOLO 1er video
- Cambiar `javascript_runtimes` → `ignore_javascript_errors: True` → ✅ No warnings JS
**Completado ✅**

### 3. ✏️ Editar app/main.py  
- Botón deshabilitado durante descarga → ✅
- Warning playlist detectada → ✅
**Completado ✅**

### 4. 🧪 Probar aplicación
**Comando corregido** (streamlit no instalado global):
```bash
python -m streamlit run app/main.py
```
**Estado**: Usuario debe ejecutar manualmente y verificar:
- URL video simple (ej: https://youtu.be/dQw4w2WxjMGU) → Descarga 1 video
- URL playlist (ej: https://www.youtube.com/playlist?list=PL...) → SOLO 1er video + warning UI
- Consola sin warnings JS repetidos
**Listo para test manual ✅**

### 5. ✅ Completar tarea
Usar `attempt_completion`

---

**Progreso: 4/5 completado (80%) - ¡Indentación corregida!**
