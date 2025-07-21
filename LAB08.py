from aiot_tools import *
from machine import Pin, ADC
import time

# 依序填入定義助理角色的系統訊息，以及具體的提示詞
SYSTEM = "你是一個協助控制 RGB LED 的助手。請根據我給的描述，回傳對應顏色的 RGB 和 brightness 值，範圍都是 0~255，" \
         "並以這種格式回應：set_rgb_bright(red, green, blue, brightness)，不要加其他文字"
PROMPT = "我想要神秘的燈色，燈光亮度要暗一點"

# 可見光感測模組 (類比輸入)
temt = ADC(Pin(3))
# 紅外線人體移動偵測模組 (數位輸入)
pir = Pin(17, Pin.IN)

# 連線 Wi-Fi
connect_wifi()
# 發送請求到 LLM API
answer = call_llm(SYSTEM, PROMPT)

# 將回應儲存到 txt 檔案
with open('rgb_bright.txt', 'w') as f:
    f.write(answer)

# 讀取存放 LLM 回應的 txt 檔案
with open('rgb_bright.txt', 'r') as f:
    answer = f.read()

# 執行檔案內容，即呼叫 set_rgb_bright() 函式
eval(answer)
time.sleep(5)

while True:
    # 讀取可見光感測模組的類比值 (代表環境亮度)
    light_adc = temt.read()
    # 讀取 PIR 輸出的數位訊號 (代表是否有人體移動)
    is_moved = pir.value()
    
    # 若亮度低於 1000 且有人體移動，亮起 LLM 設定的燈光
    if light_adc < 1000 and is_moved:
        eval(answer)
    # 若亮度高於 1100，熄滅 LED
    elif light_adc > 1100:
        set_rgb_bright(0, 0, 0, 0)
   
    time.sleep(0.5)