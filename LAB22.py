from aiot_tools import *
from sounds import *
import json

# 定義助理角色的系統訊息
SYSTEM = "你是一個協助生成音樂的助手。請根據我給的描述，回傳符合 ESP32-S2 mini MicroPython 音頻合成需求的 chords 和 durations 串列。" \
         "chords 包含單音音符（如 'E3', 'C#5', 'Db5'）、和弦（至多三個音符，以空格分隔，如 'C4 E4 G4'）、或休止符 'r'，" \
         "durations 包含對應的持續時間（秒，浮點數）。回傳前必須先檢查兩串列長度是否相等且小於 15，" \
         "並以 Python 的 docstring 格式回應：'''chords = [...]\ndurations = [...]\n'''，不要加其他文字"
# 預設音樂描述
PROMPT = "復古街機電玩遊戲"

# 連線 Wi-Fi
connect_wifi()

while True:
    # 發送請求到 LLM API
    answer = call_llm(SYSTEM, PROMPT, model="openai/gpt-4.1")   
    # 執行 LLM 回傳的 Python 程式碼，定義 chords 和 durations 變數
    exec(answer[3:-3])

    # 檢查 chords 和 durations 是否等長，若不等長則截斷至較短的長度
    if len(chords) != len(durations):
        length = min(len(chords), len(durations))  # 取兩者長度的最小值
        chords = chords[:length]
        durations = durations[:length]

    # 初始化揚聲器，預設 GPIO6、GPIO7、GPIO8
    speakers = speakers_init(pins=[6, 7, 8])
    # 根據 chords 與 durations 播放對應時長的和弦
    play_melody(speakers, chords, durations)
    # 釋放揚聲器
    speakers_deinit(speakers)

    # 若使用者輸入 'y' 或 'Y'，則將旋律儲存為 JSON 檔案
    if input('要存成 JSON 檔嗎 (y/n)：').lower() == 'y':
        # 建立字典來儲存和弦與持續時間
        melody = {
            "chords": chords,
            "durations": durations
        }
        # 讓使用者自行設定「英文」檔名
        MELODY_FILE = input('請輸入英文檔名 (不含副檔名)：') + '.json'
        # 將 melody 字典寫入 JSON 檔案
        with open(MELODY_FILE, 'w') as json_file:
            json.dump(melody, json_file)
        print(f"JSON 檔案已成功儲存為 {MELODY_FILE}")
    
    print('----------------')
    # 接收使用者輸入的音樂描述 (支援中文輸入)
    PROMPT = u_input('請輸入想要的音樂描述 (按 q 離開)：')
    # 若使用者輸入 'q' 或 'Q'，則跳出迴圈
    if PROMPT.lower() == 'q':
        break