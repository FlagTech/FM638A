from aiot_tools import *
from machine import Pin, ADC
import ESPWebServer

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
    
    # 判斷請求中是否有名為 status 的參數
    if 'status' in args:
        print(f"----{args['status']}----")  # 顯示 status 參數值 
        if args['status'] == 'on':
            rgb_led(1, 1, 1) 
        elif args['status'] == 'off':
            rgb_led(0, 0, 0)
            reset = False  # 手動關燈後不允許根據光線自動控制 LED
        ESPWebServer.ok(socket, '200', 'OK')  # 若處理完指令，回傳正確
    # 若請求中無 status 參數，回傳錯誤
    else:
        ESPWebServer.err(socket, '400', 'ERR')

# 啟用網站 (網頁伺服器)
ESPWebServer.begin(80)
# 註冊 /led 路徑，當收到請求時呼叫 handle_led 函式
ESPWebServer.onPath('/led', handle_led)

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