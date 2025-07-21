from aiot_tools import *
import time

# 星期名稱對應表（可選中文或英文）
WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"]
#WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 取得格式化的本地當前日期、星期、時間
def get_time():
    # 取得本地當前時間
    now = time.localtime()
    # 格式化日期成 YYYY/MM/DD
    date_str = '{:04d}/{:02d}/{:02d}'.format(now[0], now[1], now[2])
    # 格式化時間成 HH:MM:SS
    time_str = '{:02d}:{:02d}:{:02d}'.format(now[3], now[4], now[5])
    # 根據星期索引取得對應的星期名稱，now[6] 是星期值 (0~6)
    weekday_str = WEEKDAYS[now[6]]

    return date_str, weekday_str, time_str

# 連線 Wi-Fi
connect_wifi()
# 執行時間同步，將設備時間設為本地時區 (UTC+8)
set_time(timezone=8)

while True:
    # 取得本地當前時間
    date_str, weekday_str, time_str = get_time()
    print(f'{date_str} {weekday_str} {time_str}')
    
    time.sleep(1)  # 每秒更新