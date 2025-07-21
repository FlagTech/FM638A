from aiot_tools import *
from machine import Pin, ADC
import ESPWebServer

# RGB LED 腳位 (數位輸出)
rled, gled, bled = rgb_led()

# 可見光感測模組 (類比輸入)
temt = ADC(Pin(3))

# 連線 Wi-Fi
connect_wifi()

# 用以控制是否允許根據光線自動控制 LED
reset = True

# 處理 /led 路徑請求的函式
def handle_led(socket, args):
    # 指定為全域變數，以供函式外的程式使用
    global reset
    
    # 判斷請求中是否有名為 color 和 status 的參數
    if 'color' in args and 'status' in args:
        print(f"----{args['color']}:{args['status']}----")  # 顯示參數值 
        status = 1 if args['status'] == 'on' else 0
        if args['color'] == 'r':
            rled.value(status)
        elif args['color'] == 'g':
            gled.value(status)
        elif args['color'] == 'b':
            bled.value(status)
        if status == 0:
            reset = False  # 手動關燈後不允許根據光線自動控制 LED
        ESPWebServer.ok(socket, '200', 'OK')  # 處理完指令，回傳正確
    # 若請求中無 color 或 status 參數，回傳錯誤
    else:
        ESPWebServer.err(socket, '400', 'ERR')

# 處理 /status 路徑請求的函式，用於回傳 LED 狀態
def handle_status(socket, args):
    # 讀取 RGB LED 的當前值
    r_value = rled.value()
    g_value = gled.value()
    b_value = bled.value()
    # 回傳 JSON 格式的 RGB 狀態
    ESPWebServer.ok(socket, '200', '{"r":' + str(r_value) + ',"g":' + str(g_value) + ',"b":' + str(b_value) + '}')

# 啟用網站 (網頁伺服器)
ESPWebServer.begin(80)
# 註冊 /led 路徑，當收到請求時呼叫 handle_led 函式
ESPWebServer.onPath('/led', handle_led)
# 註冊 /status 路徑，當收到請求時呼叫 handle_status 函式
ESPWebServer.onPath('/status', handle_status)

while True:
    # 讀取可見光感測模組的類比值 (代表環境亮度)
    light_adc = temt.read()
    
    # 若亮度低於 1000，亮起 LED 白光
    if light_adc < 1000 and reset == True:
        rgb_led(1, 1, 1)
    # 若亮度高於 1100，熄滅 LED
    elif light_adc > 1100:
        rgb_led(0, 0, 0)
        reset = True  # 恢復自動控制功能
    
    # 處理客戶端請求
    ESPWebServer.handleClient()