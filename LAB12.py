from aiot_tools import *
import urequests

# 可選擇取得 "news" 股市新聞標題，或 "news_detail" 股市新聞的標題及部分內容
#TOPIC = "news"
TOPIC = "news_detail"
NUM = 3  # 指定取得的新聞數量

# 從 Google Apps Script 提供的 API 獲取股市新聞資料
def get_stock_news(topic, num):
    print("----Yahoo 股市新聞查詢中----")
    # Google Apps Script 的 API 網址，用於請求股市新聞資料
    url = (
        "https://script.google.com/macros/s/"
        "AKfycbxBGGlGz0dqV5k7BqyQxmkBKObkUMMhg_-"
        "BtxbRG8zX8nf21502qGlvpgPrnanm5zl6/exec"
    )
    # 發送 HTTP GET 請求，網址後附加查詢參數 "?topic=" 和 "&num="，分別傳入主題和新聞數量
    response = urequests.get(url + "?topic=" + topic + "&num=" + str(num))
    print(f"狀態碼：{response.status_code}")  # HTTP 回應的狀態碼 (200 表示成功)
    
    # 將回應的 JSON 文字轉換為 Python 物件
    news_list = response.json()
    # 關閉 HTTP 回應物件，釋放資源
    response.close()
    
    # 回傳抓取到的股市新聞資料
    return news_list

# 連線 Wi-Fi
connect_wifi()
# 取得即時股市新聞資料
news_list = get_stock_news(TOPIC, NUM)

# 走訪 news_list 中的每則新聞
for news in news_list:
    print('-' * 20)
    # 根據開頭 TOPIC 的選擇來顯示對應的內容
    if TOPIC == "news":
        print(news)
    elif TOPIC == "news_detail":
        print(news["title"])
        print(news["description"])