from aiot_tools import *
from umqtt.robust import MQTTClient

# 定義 AIO 的 MQTT 使用者名稱和金鑰
AIO_USER = '你的 AIO 使用者名稱'
AIO_KEY = '你的 AIO 金鑰'

# 初始化 MQTT 客戶端
client = MQTTClient(client_id='',  # 用於辨識裝置
                    server='io.adafruit.com',  # AIO 的 MQTT 伺服器位址
                    user=AIO_USER,  # AIO Username
                    password=AIO_KEY)  # AIO Key

# MQTT 主題 <username>/feeds/alarm，用於接收鬧鐘狀態
TOPIC = client.user.encode() + b'/feeds/alarm'

# 回呼函式，處理接收到的 MQTT 資料
def callback(topic, msg):
    # 若接收到的資料為 1
    if msg.decode() == '1':
        print("收到 1，響起鬧鈴")
    else:
        print("關閉鬧鈴")

# 連線 Wi-Fi
connect_wifi()

# 連線到 AIO 的 MQTT 伺服器
client.connect()
print("----MQTT 連線成功----")

# 將回呼函式綁定到 MQTT 客戶端，用於處理接收到的資料
client.set_callback(callback)
# 訂閱指定的 MQTT 主題，即 alarm
client.subscribe(TOPIC)

while True:    
    client.ping()  # 發送 ping 訊息，保持與 MQTT 伺服器的連線
    client.check_msg()  # 檢查是否有新的 MQTT 資料，並觸發回呼函式
    
    time.sleep(0.5)  # 暫停 0.5 秒，確保 MQTT 訊息正常處理