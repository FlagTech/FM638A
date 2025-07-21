from sounds import *
import json

# 定義和弦與持續時間串列 (卡農和弦)
chords = ['D4 F#4 A4', 'A3 C#4 E4', 'B3 D4 F#4', 'F#3 A3 C#4', 'r', 'G3 B3 D4', 'D3 F#3 A3', 'G3 B3 D4', 'A3 C#4 E4']
durations = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

# 定義和弦與持續時間串列 (瑪利歐 1UP 音效)
#chords = ['E5', 'G5', 'E6', 'C6', 'D6', 'G6']
#durations = [0.15, 0.15, 0.15, 0.1, 0.1, 0.2]

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