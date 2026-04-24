import network
import socket
import time

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESPAP', password='password')

while not ap.isconnected():
    pass

ip = ap.ifconfig()[0]
print(ip)

led = machine.Pin(2, machine.Pin.OUT)

def web_page():
    html = """<!DOCTYPE html>
<html>
<head><title>Pozdrav Lipik</title></head>
<body><h1>Pozdrav Lipik</h1></body>
</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    client, addr = s.accept()
    request = client.recv(1024)
    response = web_page()
    client.send('HTTP/1.1 200 OK\n')
    client.send('Content-Type: text/html\n')
    client.send('Connection: close\n\n')
    client.sendall(response)
    client.close()

    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
