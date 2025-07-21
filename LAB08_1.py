from aiot_tools import *
from machine import Pin, ADC
import ESPWebServer

# 依序填入定義助理角色的系統訊息，以及具體的提示詞
SYSTEM = "你是一個協助控制 RGB LED 的助手。請根據我給的描述，回傳對應顏色的 RGB 和 brightness 值，範圍都是 0~255，" \
         "並以這種格式回應：set_rgb_bright(red, green, blue, brightness)，不要加其他文字"

# 可見光感測模組 (類比輸入)
temt = ADC(Pin(3))
# 紅外線人體移動偵測模組 (數位輸入)
pir = Pin(17, Pin.IN)

# 連線 Wi-Fi
connect_wifi()

# 處理 /send 路徑請求的函式
def handle_send(socket, args):    
    # 判斷請求中是否有名為 description 的參數
    if 'description' in args:
        prompt = args['description']
        print(f"輸入的描述：{prompt}")
        
        # 發送請求到 LLM API
        answer = call_llm(SYSTEM, prompt)
        # 將回應儲存到 txt 檔案
        with open('rgb_bright.txt', 'w') as f:
            f.write(answer)
        
        ESPWebServer.ok(socket, '200', 'OK')  # 若處理完指令，回傳正確
    # 若請求中無 description 參數，回傳錯誤
    else:
        ESPWebServer.err(socket, '400', 'ERR')

# 啟用網站 (網頁伺服器)
ESPWebServer.begin(80)
# 註冊 /send 路徑，當收到請求時呼叫 handle_send 函式
ESPWebServer.onPath('/send', handle_send)

while True:
    try:
        # 讀取存放 LLM 回應的 txt 檔案
        with open('rgb_bright.txt', 'r') as f:
            answer = f.read()
    except:
        # 避免 S2 mini 上沒有此 txt 檔案而出錯 (預設白光)
        with open('rgb_bright.txt', 'w') as f:
            f.write('set_rgb_bright(255, 255, 255, 255)')
    
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
        
    # 處理客戶端請求
    ESPWebServer.handleClient()