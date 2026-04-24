import re
from app.models import ParsedRequest


class RequestParser:
    REPLACEMENTS = {
        "č": "c",
        "ć": "c",
        "š": "s",
        "ž": "z",
        "đ": "dj",
    }

    def normalize(self, text: str) -> str:
        value = text.lower().strip()
        for src, dst in self.REPLACEMENTS.items():
            value = value.replace(src, dst)
        return value

    def parse(self, text: str) -> ParsedRequest:
        norm = self.normalize(text)
        parsed = ParsedRequest(original_text=text, normalized_text=norm)

        if "dht22" in norm:
            parsed.sensors.append("dht22")
        if "ds18b20" in norm:
            parsed.sensors.append("ds18b20")

        if any(token in norm for token in ["led", "blicni", "blink"]):
            parsed.features.append("led_blink")
        if "wifi" in norm:
            parsed.features.append("wifi")

        parsed.gpio_candidates = [int(x) for x in re.findall(r"gpio\s*0?(\d+)", norm)]

        second_patterns = [
            r"svake\s+(\d+)\s*sek",
            r"svakih\s+(\d+)\s*sek",
            r"(\d+)\s*sekunde",
            r"(\d+)\s*sekundi",
            r"(\d+)\s*s\b",
        ]
        for pattern in second_patterns:
            match = re.search(pattern, norm)
            if match:
                parsed.seconds = int(match.group(1))
                break

        ms_patterns = [r"(\d+)\s*ms", r"(\d+)\s*milisek"]
        for pattern in ms_patterns:
            match = re.search(pattern, norm)
            if match:
                parsed.milliseconds = int(match.group(1))
                break

        if not parsed.sensors and not parsed.features:
            parsed.notes.append("Nije prepoznat poznati senzor ili funkcija iz lokalne baze.")

        return parsed
