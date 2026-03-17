import subprocess
import sys
import os

def pick_folder(initial_dir: str = "") -> str:
    """
    Abre el diálogo nativo de Windows para seleccionar una carpeta.
    Ejecuta tkinter en un subproceso para evitar conflictos con Streamlit.
    Retorna la ruta seleccionada o cadena vacía si se cancela.
    """
    script = f'''
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
folder = filedialog.askdirectory(initialdir=r"{initial_dir}", title="Selecciona la carpeta de descargas")
print(folder)
root.destroy()
'''
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True, timeout=60
        )
        path = result.stdout.strip()
        if path and os.path.isdir(path):
            return path
        return ""
    except Exception:
        return ""
