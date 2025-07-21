from aiot_tools import rgb_led
from machine import Pin, ADC
import time

# 可見光感測模組 (類比輸入)
temt = ADC(Pin(3))
# 紅外線人體移動偵測模組 (數位輸入)
pir = Pin(17, Pin.IN)

while True:
    # 讀取可見光感測模組的類比值 (代表環境亮度)
    light_adc = temt.read()
    # 讀取 PIR 輸出的數位訊號 (代表是否有人體移動)
    is_moved = pir.value()
    print(f"亮度：{light_adc}, 是否移動：{is_moved}")
    
    # 若亮度低於 1000 且有人體移動，亮起 LED 白光
    if light_adc < 1000 and is_moved:
        rgb_led(1, 1, 1)
    # 若亮度高於 1100，熄滅 LED
    elif light_adc > 1100:
        rgb_led(0, 0, 0)
   
    time.sleep(0.5)