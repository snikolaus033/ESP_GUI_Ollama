from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.on()
    time.sleep_ms(100)
    led.off()
    time.sleep_ms(600)
