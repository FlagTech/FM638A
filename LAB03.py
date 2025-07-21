from machine import Pin, ADC
from aiot_tools import rgb_led
import time

# 可見光感測模組 (類比輸入)
temt = ADC(Pin(3))

while True:
    # 讀取可見光感測模組的類比值 (代表環境亮度)
    light_adc = temt.read()
    print(f"亮度：{light_adc}")
    
    # 若亮度低於 1000，亮起 LED 白光
    if light_adc < 1000:
        rgb_led(1, 1, 1)
    # 若亮度高於 1100，熄滅 LED
    elif light_adc > 1100:
        rgb_led(0, 0, 0)
   
    time.sleep(0.5)