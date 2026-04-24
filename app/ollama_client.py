import json
import re
from pathlib import Path
from urllib import request, error


class OllamaClient:
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "qwen2.5-coder:7b") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate_code(self, prompt: str, timeout: int = 180) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
            },
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
        except error.URLError as exc:
            raise RuntimeError(f"Ne mogu se spojiti na Ollamu: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Greška kod poziva Ollame: {exc}") from exc

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Ollama nije vratila valjan JSON odgovor.") from exc

        text = payload.get("response", "").strip()
        if not text:
            raise RuntimeError("Ollama nije vratila sadržaj.")

        return self._sanitize_code(text)

    def save_code(self, code: str, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code, encoding="utf-8")
        return output_path

    def _sanitize_code(self, text: str) -> str:
        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:python)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned.strip() + "\n"
