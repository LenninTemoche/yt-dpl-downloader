import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, file_path="app/data/history.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add_entry(self, title, url, mode, quality):
        entry = {
            "title": title,
            "url": url,
            "mode": mode,
            "quality": quality,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        history = self.get_history()
        history.insert(0, entry)  # Nueva entrada al inicio
        
        # Limitar a las últimas 50 descargas
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(history[:50], f, indent=4, ensure_ascii=False)

    def get_history(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
