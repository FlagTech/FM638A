from aiot_tools import *
from machine import I2C
from ssd1306 import SSD1306_I2C

from bitmap_font_tool import set_font_path, draw_text
# 設置字型檔案路徑，使用指定的點陣字型 (fusion_bdf.12)
set_font_path('./lib/fonts/fusion_bdf.12')

# 指定取得股市新聞標題及部分內容
TOPIC = "news_detail" 
NUM = 3  # 指定取得的新聞數量

# 依序填入定義助理角色的系統訊息，以及具體的提示詞
SYSTEM = "你是一個擅長對新聞做總結的助手。請根據我給的股市新聞原文，回傳30字以內的股市新聞總結。" \
         "回傳前必須先檢查字數是否在30字以內，除了總結以外不要加其他文字"
PROMPT = ""

# I2C 通訊，用於連接 OLED 螢幕模組
i2c = I2C(0, scl=Pin(16), sda=Pin(18))
# SSD1306 OLED 顯示器，解析度為 128x64 像素
oled = SSD1306_I2C(128, 64, i2c)

# 按鈕腳位 (數位輸入)，並啟用內建下拉電阻
button = Pin(21, Pin.IN, Pin.PULL_DOWN)

# 連線 Wi-Fi
connect_wifi()
# 執行時間同步，將設備時間設為本地時區 (UTC+8)
set_time()

# 計數器，用於追蹤目前顯示的新聞索引
i = 0

while True:
    # 當按鈕未被按下且尚未開始顯示新聞
    if button.value() == 0 and i == 0:
        # 取得本地當前時間
        date_str, weekday_str, time_str = get_time()
        
        # 清空 OLED 顯示器 (填充黑色以清除先前內容)
        oled.fill(0)
        # 在 OLED 上顯示時間和星期，格式為 "YYYY/MM/DD 星期  HH:MM"
        draw_text(oled, f'{date_str} {weekday_str}  {time_str[:5]}', 0, 0)
        # 更新 OLED 顯示器，將緩衝區內容顯示出來
        oled.show()
    
    # 當按鈕被按下
    if button.value() == 1:
        # 當已顯示完所有新聞 (i 等於 NUM)
        if i == NUM:
            print(f"----股市新聞顯示完畢----")
            i = 0  # 重置計數器
        else:
            # 若為第一次按下按鈕
            if i == 0:
                # 取得即時股市新聞資料
                news_list = get_stock_news(TOPIC, NUM)
            
            # 將索引 i 的股市新聞標題與部分內容作為 Prompt
            PROMPT = news_list[i]["title"] + news_list[i]["description"]
            # 將抓取到的新聞作為 Prompt，以透過 LLM 生成新聞總結
            answer = call_llm(SYSTEM, PROMPT)
            
            # 清空 OLED 顯示器 (填充黑色以清除先前內容)
            oled.fill(0)
            # 在 OLED 上顯示 LLM 的回應
            draw_text(oled, answer, 0, 4)
            # 更新 OLED 顯示器，將緩衝區內容顯示出來
            oled.show()
            i += 1  # 遞增計數器，準備顯示下一則新聞
    
        while(button.value()==1):pass  # 避免過快的按鈕重複偵測