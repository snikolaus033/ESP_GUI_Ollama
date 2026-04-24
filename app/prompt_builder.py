from app.database import FEATURE_DB, SENSOR_DB
from app.models import ParsedRequest


class PromptBuilder:
    def build(self, parsed: ParsedRequest) -> str:
        sensor_lines = []
        for key in parsed.sensors:
            sensor = SENSOR_DB.get(key)
            if sensor:
                sensor_lines.append(
                    f"- {sensor.name}: {sensor.pins}. Napomena: {sensor.note}. Hint: {sensor.micropython_hint}"
                )

        feature_lines = []
        for key in parsed.features:
            feature = FEATURE_DB.get(key)
            if feature:
                feature_lines.append(
                    f"- {feature.name}: {feature.description}. Hint: {feature.micropython_hint}"
                )

        context_parts = []
        if sensor_lines:
            context_parts.append("Poznati senzori iz lokalne baze:\n" + "\n".join(sensor_lines))
        if feature_lines:
            context_parts.append("Poznate funkcije iz lokalne baze:\n" + "\n".join(feature_lines))
        if parsed.gpio_candidates:
            context_parts.append("GPIO kandidati pronađeni u tekstu: " + ", ".join(map(str, parsed.gpio_candidates)))
        if parsed.seconds is not None:
            context_parts.append(f"Interval u sekundama iz teksta: {parsed.seconds}")
        if parsed.milliseconds is not None:
            context_parts.append(f"Trajanje u milisekundama iz teksta: {parsed.milliseconds}")

        context = "\n\n".join(context_parts) if context_parts else "Nema dodatnog lokalnog konteksta."

        return f"""
Ti si generator isključivo valjanog MicroPython koda za ESP32.

Pravila:
1. Vrati samo čisti kod bez objašnjenja.
2. Ne koristi markdown ograde poput ```.
3. Ne piši uvod, komentar, naslov ni opis izvan koda.
4. Kod mora biti odmah spreman za snimanje u jednu .py datoteku.
5. Koristi samo MicroPython biblioteke primjerene za ESP32.
6. Ako nešto nedostaje, odaberi razumnu zadanu vrijednost i nastavi.
7. Ako je tražen DHT22, koristi dht i machine.Pin.
8. Ako je tražen LED blink, koristi Pin.OUT i time.sleep_ms.
9. Kod mora biti sintaktički konzistentan i imati beskonačnu while True petlju ako zadatak to implicira.
10. Ne spominji da si AI.

Korisnički zahtjev na hrvatskom:
{parsed.original_text}

Dodatni lokalni kontekst:
{context}
""".strip()
