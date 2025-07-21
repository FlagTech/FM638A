from aiot_tools import rgb_led
import network, ESPWebServer

# 建立工作站模式的無線網路介面
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('你的 Wi-Fi 名稱', '你的 Wi-Fi 密碼')
# 等待 Wi-Fi 連線，直到連線成功
while not wlan.isconnected():
    pass
print("----Wi-Fi 連線成功----")
print(f"伺服器位址：{wlan.ifconfig()[0]}")

# 處理 /led 路徑請求的函式
def handle_led(socket, args):
    # 判斷請求中是否有名為 status 的參數
    if 'status' in args:
        print(f"----{args['status']}----")  # 顯示 status 參數值 
        if args['status'] == 'on':
            rgb_led(1, 1, 1)
        elif args['status'] == 'off':
            rgb_led(0, 0, 0)
        ESPWebServer.ok(socket, '200', 'OK')  # 若處理完指令，回傳正確
    # 若請求中無 status 參數，回傳錯誤
    else:
        ESPWebServer.err(socket, '400', 'ERR')

# 啟用網站 (網頁伺服器)
ESPWebServer.begin(80)
# 註冊 /led 路徑，當收到請求時呼叫 handle_led 函式
ESPWebServer.onPath('/led', handle_led)

# 主迴圈，持續處理客戶端請求
while True:
    ESPWebServer.handleClient()