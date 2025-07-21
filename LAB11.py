from aiot_tools import *
from machine import I2C
from ssd1306 import SSD1306_I2C
import dht, urequests

from bitmap_font_tool import set_font_path, draw_text
# 設置字型檔案路徑，使用指定的點陣字型 (fusion_bdf.12)
set_font_path('./lib/fonts/fusion_bdf.12')

# 指定城市名稱 (須使用繁體中文)，用於查詢天氣資料
CITY = "臺北市"

# 從 Google Apps Script 提供的 API 獲取指定城市的天氣資料
def get_weather(city=CITY):
    # Google Apps Script 的 API 網址，用於請求天氣資料
    url = (
        "https://script.google.com/macros/s/"
        "AKfycbx746K5k2ZaxOmMoJ-5Mdw9keIMsagfp"
        "12TeBIyKcVunGjZwn5bnuAB4LCePajSUhwvow/exec"
    )
    # 發送 HTTP GET 請求，網址後附加查詢參數 "?city=城市名稱"
    response = urequests.get(url + "?city=" + city)
    
    print("----中央氣象局連線成功----")
    print(f"狀態碼：{response.status_code}")  # HTTP 回應的狀態碼 (200 表示成功)
    print(f"回應內容：{response.text}")  # 伺服器回傳的完整文字內容 (JSON 格式)
    
    # 將回應的 JSON 文字轉換為 Python 物件
    weather = response.json()
    # 關閉 HTTP 回應物件，釋放資源
    response.close()
    
    # 回傳抓取到的天氣資料 (包含城市、日期、天氣狀態、降雨機率、最低溫、最高溫)
    return weather

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

# 先取一次今日天氣預報資料
weather = get_weather()
# 取得當前時間 (單位：秒)，用於定時更新天氣資料
weather_start = time.time()

# 先感測一次室內溫濕度
dht11.measure()
# 取得當前時間 (單位：秒)，用於定時感測室內溫濕度
dht_start = time.time()

while True:
    # 每六小時取一次今日天氣預報資料
    if (time.time()-weather_start) >= 6*3600:
        weather = get_weather()
        weather_start = time.time()  # 更新計時器的起始時間為當前時間
    
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
    # 在 OLED 上顯示今日氣溫和降雨機率
    draw_text(oled, f'今日氣溫：{weather["最低溫"]}℃~{weather["最高溫"]}℃', 0, 32)
    draw_text(oled, f'降雨機率：{weather["降雨機率"]}%', 0, 48)
    # 更新 OLED 顯示器，將緩衝區內容顯示出來
    oled.show()

    time.sleep(0.5)  # 每 0.5 秒更新