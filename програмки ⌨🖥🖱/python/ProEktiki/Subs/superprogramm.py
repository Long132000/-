import os
import cv2
import pytesseract
from moviepy.editor import VideoFileClip

VIDEO_FILE = "video.mp4"  # файл должен быть в той же папке, что и скрипт
OUTPUT_SRT = "subtitles.srt"
FRAME_INTERVAL = 0.5  # проверяем каждые 0.5 секунды

if not os.path.exists(VIDEO_FILE):
    print(f"Файл {VIDEO_FILE} не найден!")
    exit(1)

clip = VideoFileClip(VIDEO_FILE)
subs = []
counter = 1

for t in [i*FRAME_INTERVAL for i in range(int(clip.duration/FRAME_INTERVAL)+1)]:
    frame = clip.get_frame(t)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    text = pytesseract.image_to_string(frame_bgr, lang="rus+eng").strip()
    if text:
        start = t
        end = min(t + FRAME_INTERVAL, clip.duration)
        subs.append((counter, start, end, text))
        counter += 1

if not subs:
    print("Субтитры не найдены.")
else:
    with open(OUTPUT_SRT, "w", encoding="utf-8") as f:
        for c, start, end, text in subs:
            start_str = f"{int(start//3600):02}:{int((start%3600)//60):02}:{int(start%60):02},{int((start*1000)%1000):03}"
            end_str = f"{int(end//3600):02}:{int((end%3600)//60):02}:{int(end%60):02},{int((end*1000)%1000):03}"
            f.write(f"{c}\n{start_str} --> {end_str}\n{text}\n\n")
    print(f"Субтитры сохранены в {OUTPUT_SRT}")
