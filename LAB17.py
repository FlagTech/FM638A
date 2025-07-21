from aiot_tools import *
from machine import I2C
from ssd1306 import SSD1306_I2C

from bitmap_font_tool import set_font_path, draw_text
# 設置字型檔案路徑，使用指定的點陣字型 (fusion_bdf.12)
set_font_path('./lib/fonts/fusion_bdf.12')

# 設定鬧鐘 (24 小時制，格式為 HH:MM)
ALARM_STR = '06:00'

# I2C 通訊，用於連接 OLED 螢幕模組
i2c = I2C(0, scl=Pin(16), sda=Pin(18))
# SSD1306 OLED 顯示器，解析度為 128x64 像素
oled = SSD1306_I2C(128, 64, i2c)

# 按鈕腳位 (數位輸入)，並啟用內建下拉電阻
button = Pin(21, Pin.IN, Pin.PULL_DOWN)

# 初始化 MQTT 客戶端
client = mqtt_client()
# MQTT 主題 <username>/feeds/alarm，用於接收鬧鐘狀態
TOPIC = client.user.encode() + b'/feeds/alarm'

# 回呼函式，處理接收到的 MQTT 資料
def callback(topic, msg):
    # 宣告使用全域變數 alarm_on，以便在函式內修改其值
    global alarm_on
    # 若接收到的訊息為 1
    if msg.decode() == '1':
        alarm_on = True
    else:
        alarm_on = False

# 連線 Wi-Fi
connect_wifi()
# 執行時間同步，將設備時間設為本地時區 (UTC+8)
set_time()

# 連線到 AIO 的 MQTT 伺服器
client.connect()
print("----MQTT 連線成功----")

# 將回呼函式綁定到 MQTT 客戶端，用於處理接收到的資料
client.set_callback(callback)
# 訂閱指定的 MQTT 主題，即 alarm
client.subscribe(TOPIC)

# 鬧鐘初始為關閉狀態
alarm_on = False
# 初始化揚聲器為 None
speaker = None
# 音符串列的索引，初始為 0
i = 0
# 取得當前時間 (單位：秒)，用於控制音符播放時間
note_start = time.time()
# 取得當前時間 (單位：毫秒)，用於控制 MQTT 訊息檢查間隔
mqtt_start = time.ticks_ms()

while True:
    # 每 0.5 秒檢查一次 MQTT 連線與新資料
    if (time.ticks_ms()-mqtt_start) >= 0.5*1000:
        client.ping()  # 發送 ping 訊息，保持與 MQTT 伺服器的連線
        client.check_msg()  # 檢查是否有新的 MQTT 資料，並觸發回呼函式
        mqtt_start = time.ticks_ms()  # 更新計時器的起始時間為當前時間
    
    # 取得本地當前時間
    date_str, weekday_str, time_str = get_time()
    
    # 清空 OLED 顯示器 (填充黑色以清除先前內容)
    oled.fill(0)
    # 在 OLED 上顯示時間和星期，格式為 "YYYY/MM/DD 星期  HH:MM"
    draw_text(oled, f'{date_str} {weekday_str}  {time_str[:5]}', 0, 0)
    # 更新 OLED 顯示器，將緩衝區內容顯示出來
    oled.show()
    
    # 檢查當前時間是否為鬧鐘設定時間 (精確到秒)
    if time_str == ALARM_STR + ':00':
        alarm_on = True
        
    # 當按鈕被按下
    if button.value() == 1:
        alarm_on = False
    
    # 當鬧鐘狀態為開啟
    if alarm_on == True:
        if speaker is None:  # 檢查 speaker 是否已初始化
            speaker = speaker_init()  # 初始化揚聲器，預設 GPIO6
        # 每 1 秒播放一個音符
        if (time.time()-note_start) >= 1:
            play_note(speaker, i)  # 播放當前索引的音符
            i += 1  # 遞增音符索引，準備播放下一個音符
            note_start = time.time()  # 更新計時器的起始時間為當前時間 
    else:
        if speaker is not None:  # 檢查 speaker 是否已初始化
            speaker = speaker_deinit(speaker)  # 靜音並釋放揚聲器
        i = 0  # 重置音符索引，準備下次播放