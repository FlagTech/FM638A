from machine import Pin, PWM
import time, math

# 定義音符頻率映射，基於 A4 = 440 Hz
def note_to_freq(note):
    """
    將音符轉換為頻率，基於 A4 = 440 Hz
    輸入: 音符字串 (如 'C4', 'C#5', 'Ab3')
    輸出: 頻率 (Hz)，無效輸入則回傳 None
    """
    A4_FREQ = 440.0
    pitch_map = {
        'C': -9, 'C#': -8, 'Db': -8, 'D': -7, 'D#': -6, 'Eb': -6,
        'E': -5, 'F': -4, 'F#': -3, 'Gb': -3, 'G': -2, 'G#': -1,
        'Ab': -1, 'A': 0, 'A#': 1, 'Bb': 1, 'B': 2
    }
    
    # 檢查音符格式是否有效
    if not isinstance(note, str) or len(note) < 2:
        print(f"音符格式錯誤：{note}")
        return None
    
    # 分割音符名稱和八度
    if note[-2] in '#b':
        pitch_name, octave = note[:-1], note[-1]
    else:
        pitch_name, octave = note[0], note[1:]
    
    # 檢查音符名稱是否有效
    if pitch_name not in pitch_map:
        print(f"無效音符名稱：{pitch_name}")
        return None
    
    # 檢查八度是否為有效數字
    try:
        octave = int(octave)
    except ValueError:
        print(f"無效八度：{octave}")
        return None
    
    # 計算相對於 A4 的半音數並轉換為頻率
    semitones_from_A4 = pitch_map[pitch_name] + (octave - 4) * 12
    freq = int(round(A4_FREQ * (2 ** (semitones_from_A4 / 12))))
    
    # 檢查頻率是否在可播放範圍 (通常 PWM 支援 100 Hz~20 kHz)
    if freq < 100 or freq > 20000:
        print(f"頻率 {freq} Hz 超出可播放範圍 (100~20000 Hz)")
        return None
    
    return freq

# 初始化多個揚聲器
def speakers_init(pins=[6, 7, 8]):
    """
    初始化 PWM 揚聲器，預設使用 3 個引腳
    """
    speakers = []
    for pin in pins:
        speaker = PWM(Pin(pin, Pin.OUT))
        speaker.freq(1000)  # 預設頻率
        speaker.duty(0)  # 初始靜音
        speakers.append(speaker)

    return speakers

# 釋放所有揚聲器資源
def speakers_deinit(speakers):
    """
    釋放所有 PWM 揚聲器資源
    """
    for speaker in speakers:
        speaker.deinit()

# 播放單音或和弦
def play_chord(speakers, chord, duration):
    """
    播放單音或和弦 (最多 3 音) 或休止符
    參數:
        speakers: PWM 揚聲器物件串列
        chord: 音符字串，如 'E3', 'C#5', 'Eb3 C5', 'r'
        duration: 持續時間浮點數 (秒)
    """
    if chord == 'r':  # 休止符
        for speaker in speakers:
            speaker.duty(0)  # 靜音
        time.sleep(duration)
        return
    
    notes = chord.split()  # 以空白分割，可能為單音或和弦
    num_notes = len(notes)
    if num_notes > 3 or num_notes < 1:
        print(f"無效音符數量：{chord}，僅支援 1~3 音")
        return
    
    # 計算每個音的頻率
    frequencies = []
    for note in notes:
        freq = note_to_freq(note)
        if freq:
            frequencies.append(freq)
        else:
            print(f"無效音符：{note}")
            return
    
    # 設置揚聲器頻率和音量
    for i in range(3):  # 最多3個音
        if i < num_notes:
            duty_val = 512 if num_notes == 1 else int(1023 / num_notes)  # 單音或和弦音量調整
            speakers[i].freq(frequencies[i])
            speakers[i].duty(duty_val)
        else:
            speakers[i].duty(0)  # 靜音未使用的揚聲器
    time.sleep(duration)
    
    for speaker in speakers:
        speaker.duty(0)  # 播放結束後靜音

# 播放旋律
def play_melody(speakers, chords, durations):
    """
    播放旋律，支援單音、和弦 (最多 3 音) 及休止符
    參數:
        speakers: PWM 揚聲器物件串列
        chords: 音符串列，如 ['E3', 'C#5', 'Eb3 C5', 'r']
        durations: 持續時間串列 (秒)，需與 chords 等長
    """
    if len(chords) != len(durations):
        raise ValueError("chords 和 durations 長度必須相等")
    
    for chord, duration in zip(chords, durations):
        play_chord(speakers, chord, duration)  # 逐一播放音符或和弦