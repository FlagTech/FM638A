from aiot_tools import *
from machine import I2C
from ssd1306 import SSD1306_I2C
import mfrc522

from bitmap_font_tool import set_font_path, draw_text
# 設置字型檔案路徑，使用指定的點陣字型 (fusion_bdf.12)
set_font_path('./lib/fonts/fusion_bdf.12')

# 卡號與家庭成員名稱的對應字典
member = {'F00B99197B':'小黑', 'D256BB2E11':'蘿蔔'}

# I2C 通訊，用於連接 OLED 螢幕模組
i2c = I2C(0, scl=Pin(16), sda=Pin(18))
# SSD1306 OLED 顯示器，解析度為 128x64 像素
oled = SSD1306_I2C(128, 64, i2c)

# 設定 SPI 介面的腳位以初始化 RFID
rfid = mfrc522.MFRC522(12, 11, 10, 9, 13)  # SCK, MOSI, MISO, RST, SDA

# 初始化 MQTT 客戶端
client = mqtt_client()
# MQTT 主題 <username>/feeds/rfid，用於發佈 RFID 卡號資料
RFID_TOPIC = client.user.encode() + b'/feeds/rfid'

# 連線 Wi-Fi
connect_wifi()
# 執行時間同步，將設備時間設為本地時區 (UTC+8)
set_time()

# 連線到 AIO 的 MQTT 伺服器
client.connect()
print("----MQTT 連線成功----")

# 取得當前時間 (單位：毫秒)，用於控制 MQTT 訊息檢查間隔
mqtt_start = time.ticks_ms()

while True:
    # 每 0.5 秒檢查一次 MQTT 連線
    if (time.ticks_ms()-mqtt_start) >= 0.5*1000:
        client.ping()  # 發送 ping 訊息，保持與 MQTT 伺服器的連線
        mqtt_start = time.ticks_ms()  # 更新計時器的起始時間為當前時間
    
    # 取得本地當前時間
    date_str, weekday_str, time_str = get_time()
    
    # 局部清空 OLED 顯示器 (填充黑色以清除先前內容)
    oled.fill_rect(0, 0, 128, 16, 0)
    # 在 OLED 上顯示時間和星期，格式為 "YYYY/MM/DD 星期  HH:MM"
    draw_text(oled, f'{date_str} {weekday_str}  {time_str[:5]}', 0, 0)
    # 更新 OLED 顯示器，將緩衝區內容顯示出來
    oled.show()
    
    # 搜尋 RFID 卡片，檢查是否有卡片進入感應範圍
    stat, tag_type = rfid.request(rfid.REQIDL)
    # 如果成功偵測到卡片
    if stat == rfid.OK:
        # 讀取卡號
        stat, raw_uid = rfid.anticoll()
        # 如果成功讀取到卡號
        if stat == rfid.OK:
            # 將原始卡號轉換為十六進位字串
            id = to_hex_string(raw_uid)
            
            # 局部清空 OLED 顯示器 (填充黑色以清除先前內容)
            oled.fill_rect(0, 16, 128, 16, 0)
            # 在 OLED 上顯示對應家庭成員名稱的歡迎訊息
            draw_text(oled, f'★煞氣ㄟ{member[id]}回家了☆', 0, 16)
            # 更新 OLED 顯示器，將緩衝區內容顯示出來
            oled.show()
            
            # 透過 MQTT 發佈對應家庭成員名稱到主題 rfid
            client.publish(RFID_TOPIC, member[id].encode())