from app.models import ParsedRequest


class FallbackGenerator:
    def generate(self, parsed: ParsedRequest) -> str:
        sensor_pin = parsed.gpio_candidates[0] if parsed.gpio_candidates else 4
        led_pin = parsed.gpio_candidates[-1] if parsed.gpio_candidates else 2
        seconds = parsed.seconds or 2
        blink_ms = parsed.milliseconds or 200

        if "dht22" in parsed.sensors:
            return f'''import time
import dht
from machine import Pin

sensor = dht.DHT22(Pin({sensor_pin}))
led = Pin({led_pin}, Pin.OUT)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temperatura:", temp, "°C")
        print("Vlaga:", hum, "%")
    except OSError as e:
        print("Greška pri očitanju senzora:", e)

    led.on()
    time.sleep_ms({blink_ms})
    led.off()
    time.sleep({seconds})
'''

        return '''from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.on()
    time.sleep_ms(200)
    led.off()
    time.sleep(1)
'''
