from machine import Pin
import time

# RGB LED 腳位 (數位輸出)
rled = Pin(37, Pin.OUT)
gled = Pin(35, Pin.OUT)
bled = Pin(33, Pin.OUT)

# 無限迴圈，讓 RGB LED 閃爍
while True:
    rled.value(1)
    gled.value(1)
    bled.value(1)
    time.sleep(0.5)
    
    rled.value(0)
    gled.value(0)
    bled.value(0)
    time.sleep(0.5)