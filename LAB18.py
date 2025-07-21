from aiot_tools import *
import mfrc522

# 設定 SPI 介面的腳位以初始化 RFID
rfid = mfrc522.MFRC522(12, 11, 10, 9, 13)  # SCK, MOSI, MISO, RST, SDA

while True:
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
            print(f"卡號：{id}")