ESP32 MicroPython Generator + Ollama

Opis:
Aplikacija prima hrvatski opis zadatka, šalje ga lokalnoj Ollami uz strogi prompt da vrati samo valjan MicroPython kod za ESP32, prikaže kod u GUI-ju i spremi ga u .py datoteku.

Preduvjeti:
Pokretanje ollama LLM-a:
1. preuzmi sa https://ollama.com/download 
2. pokreni skinuti OllamaSetup.exe
3. test u cmdu: ollama --version
4. ollama pull qwen2.5-coder:7b
5. ollama run qwen2.5-coder:7b

1. Python 3.10+
2. Lokalno instalirana Ollama
3. Povučeni model, npr.:
   ollama pull qwen2.5-coder:7b
4. Pokrenuta Ollama usluga
5. Instaliran PySide6

Pokretanje:
pip install -r requirements.txt
python main.py

Primjer unosa:
Učitaj temperaturu i vlagu sa dht22 svake dve sekunde i blicni 200 ms led na esp32 GPIO02

Metrika provjere:
Instalirati IDE za MicroPython (Thonny ili sl.)
Testirati dobiveni kod na ESP32 uređaju.

Napomene:
- Zadani izlaz je generated/main.py
- Ako Ollama ne vrati odgovor, može se uključiti fallback generator.
- Lokalna baza senzora i funkcija nalazi se u app/database.py
- Strogi prompt za Ollamu nalazi se u app/prompt_builder.py
