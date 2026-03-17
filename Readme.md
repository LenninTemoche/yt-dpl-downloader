# yt-dlp Video Downloader V 0.1

Este proyecto tiene como objetivo simplificar la descarga de contenido multimedia mediante el uso de herramientas de código abierto potentes como `yt-dlp` y `FFmpeg`. Está diseñado para entornos Windows, proporcionando una interfaz de comandos optimizada para obtener videos en formato MP4 con diversas calidades.

---

## 1. Estructura del Proyecto
Para garantizar un funcionamiento óptimo, los componentes deben estar organizados en la raíz de la carpeta:

```text
yt-dlp-downloader/
├── yt-dlp.exe    <- Binario principal del extractor
├── ffmpeg.exe    <- Codificador para fusión de audio y video
├── ffprobe.exe   <- Herramienta de análisis multimedia
└── descargas/    <- Los videos se guardarán aquí (puedes cambiar el nombre)
```

---

## 2. Uso de la Terminal
No es necesario instalar programas pesados; simplemente utiliza la terminal de tu preferencia (PowerShell, CMD o la terminal de VS Code):

1. Abre la terminal en la ruta: `f:\tu-ruta\yt-dlp-downloader`.
2. Escribe el comando deseado y presiona **Enter**.

---

## 3. Comandos de Descarga (MP4)

A continuación, los comandos configurados para obtener el mejor balance entre peso y resolución:

### ✅ Resolución 1080p (Alta Definición)
```powershell
.\yt-dlp.exe -f "bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 "URL"
```

### ✅ Resolución 720p (Estándar)
```powershell
.\yt-dlp.exe -f "bv[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]" --merge-output-format mp4 "URL"
```

### ✅ Resolución 360p (Baja/Móvil)
```powershell
.\yt-dlp.exe -f "bv[height<=360][ext=mp4]+ba[ext=m4a]/b[height<=360][ext=mp4]" --merge-output-format mp4 "URL"
```

### Guardar en una carpeta específica
Si deseas que el video se guarde en una carpeta específica manualmente (por ejemplo, dentro de "descargas"), agrega `-o` seguido de la ruta:
```powershell
.\yt-dlp.exe -o "descargas/%(title)s.%(ext)s" "URL"
```
*(Nota: Si la carpeta no existe, el programa la creará automáticamente).*


---

## 4. Recomendaciones y Mantenimiento

- **Actualización:** Los canales difusores de contenido suelen actualizar sus protocolos frecuentemente. Puedes consultar el estado de los canales en la página oficial de yt-dlp o inetenta mantener tu herramienta al día usando el comando:

  ```powershell
  .\yt-dlp.exe -U
  ```

- **Solo Audio:** Si solo necesitas el audio en alta fidelidad:
  ```powershell
  .\yt-dlp.exe -x --audio-format mp3 "URL"
  ```

---

## Aviso Legal y Responsabilidad
El uso de esta herramienta está destinado exclusivamente a **fines educativos y de investigación**. 

1. **Derechos de Autor:** El usuario es el único responsable de respetar los términos de servicio de las plataformas y las leyes de propiedad intelectual vigentes. Solo descarga contenido del cual poseas derechos o permiso explícito.

2. **Exención de Responsabilidad:** Los creadores de esta guía y de las herramientas mencionadas no se hacen responsables del uso indebido, descargas ilegales o cualquier daño derivado del uso de este software.

---

## Créditos y Reconocimientos

Este proyecto es posible gracias al increíble trabajo de las comunidades de código abierto:

*   **yt-dlp:** El extractor de contenido multimedia más avanzado del mundo. [Repositorio en GitHub](https://github.com/yt-dlp/yt-dlp)

*   **FFmpeg:** La biblioteca líder para el manejo de video, audio y otros archivos multimedia. [Página Oficial](https://ffmpeg.org/)

---
*Guía generada para el entornos de desarrollo colaborativo y educativo.*
