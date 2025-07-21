from machine import Pin
import time

# 內建 LED 腳位 (GPIO15)
led = Pin(15, Pin.OUT)

# 無限迴圈，讓 LED 閃爍
while True:
    led.value(1)  # 點亮 LED (高電位)
    time.sleep(0.5)  # 暫停 0.5 秒
    led.value(0)  # 熄滅 LED (低電位)
    time.sleep(0.5)  # 暫停 0.5 秒