from aiot_tools import *
from machine import I2C
from ssd1306 import SSD1306_I2C
import dht

from bitmap_font_tool import set_font_path, draw_text
# 設置字型檔案路徑，使用指定的點陣字型 (fusion_bdf.12)
set_font_path('./lib/fonts/fusion_bdf.12')

# I2C 通訊，用於連接 OLED 螢幕模組
i2c = I2C(0, scl=Pin(16), sda=Pin(18))
# SSD1306 OLED 顯示器，解析度為 128x64 像素
oled = SSD1306_I2C(128, 64, i2c)

# DHT11 溫濕度感測模組
dht11 = dht.DHT11(Pin(8))

# 連線 Wi-Fi
connect_wifi()
# 執行時間同步，將設備時間設為本地時區 (UTC+8)
set_time()

# 先感測一次室內溫濕度
dht11.measure()
# 取得當前時間 (單位：秒)，用於定時感測室內溫濕度
dht_start = time.time()

while True:
    # 每分鐘感測一次室內溫濕度
    if (time.time()-dht_start) >= 60:
        dht11.measure()
        dht_start = time.time()  # 更新計時器的起始時間為當前時間
    
    # 取得本地當前時間
    date_str, weekday_str, time_str = get_time()
    
    # 清空 OLED 顯示器 (填充黑色以清除先前內容)
    oled.fill(0)
    # 在 OLED 上顯示時間和星期，格式為 "YYYY/MM/DD 星期  HH:MM"
    draw_text(oled, f'{date_str} {weekday_str}  {time_str[:5]}', 0, 0)
    # 在 OLED 上顯示室內溫度和濕度
    draw_text(oled, f'溫度：{str(dht11.temperature())}℃ 濕度：{str(dht11.humidity())}%', 0, 16)
    # 更新 OLED 顯示器，將緩衝區內容顯示出來
    oled.show()

    time.sleep(0.5)  # 每 0.5 秒更新