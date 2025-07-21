from aiot_tools import *
from machine import I2C
from ssd1306 import SSD1306_I2C

from bitmap_font_tool import set_font_path, draw_text
# 設置字型檔案路徑，使用指定的點陣字型 (fusion_bdf.12)
set_font_path('./lib/fonts/fusion_bdf.12')

# 指定僅取得一則股市新聞的標題及部分內容
TOPIC = "news_detail" 
NUM = 1

# I2C 通訊，用於連接 OLED 螢幕模組
i2c = I2C(0, scl=Pin(16), sda=Pin(18))
# SSD1306 OLED 顯示器，解析度為 128x64 像素
oled = SSD1306_I2C(128, 64, i2c)

# 連線 Wi-Fi
connect_wifi()
# 取得即時股市新聞資料
news_list = get_stock_news(TOPIC, NUM)

# 依序填入定義助理角色的系統訊息，以及具體的提示詞
SYSTEM = "你是一個擅長對新聞做總結的助手。請根據我給的股市新聞原文，回傳30字以內的股市新聞總結。" \
         "回傳前必須先檢查字數是否在30字以內，除了總結以外不要加其他文字"
# 將第一則股市新聞的標題與部分內容作為 Prompt
PROMPT = news_list[0]["title"] + news_list[0]["description"]

# 將抓取到的新聞作為 Prompt，以透過 LLM 生成新聞總結
answer = call_llm(SYSTEM, PROMPT)

# 清空 OLED 顯示器 (填充黑色以清除先前內容)
oled.fill(0)
# 在 OLED 上顯示 LLM 的回應
draw_text(oled, answer, 0, 4)
# 更新 OLED 顯示器，將緩衝區內容顯示出來
oled.show()