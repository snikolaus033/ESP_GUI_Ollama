from app.models import FeatureInfo, SensorInfo


SENSOR_DB = {
    "dht22": SensorInfo(
        key="dht22",
        name="DHT22",
        pins="VCC -> 3.3V, GND -> GND, DATA -> GPIO4",
        note="Koristi jedan digitalni pin i često treba pull-up otpornik 4.7k-10k između VCC i DATA.",
        default_gpio=4,
        micropython_hint="Koristi modul dht i klasu dht.DHT22(Pin(GPIO)).",
    ),
    "ds18b20": SensorInfo(
        key="ds18b20",
        name="DS18B20",
        pins="VCC -> 3.3V, GND -> GND, DATA -> GPIO4",
        note="Treba pull-up otpornik 4.7k između DATA i 3.3V.",
        default_gpio=4,
        micropython_hint="Koristi onewire i ds18x20 module.",
    ),
}


FEATURE_DB = {
    "led_blink": FeatureInfo(
        key="led_blink",
        name="LED blink",
        description="Pali i gasi LED na zadanom GPIO pinu.",
        micropython_hint="Koristi machine.Pin(pin, Pin.OUT), led.on(), led.off(), time.sleep_ms().",
    ),
    "wifi": FeatureInfo(
        key="wifi",
        name="WiFi",
        description="Spajanje ESP32 na WiFi mrežu.",
        micropython_hint="Koristi network.WLAN(network.STA_IF).",
    ),
}
