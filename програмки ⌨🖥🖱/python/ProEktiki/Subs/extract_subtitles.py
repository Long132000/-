import subprocess, os

video_path = r"C:\Users\Администратор\Desktop\Временный коддинг\video.mp4"
output_srt = "subtitles.srt"
ffmpeg_path = r"C:\Users\Администратор\Desktop\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"  # <-- полный путь к ffmpeg.exe

cmd = [ffmpeg_path, "-i", video_path, "-map", "0:s:0", output_srt, "-y"]
result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

if os.path.exists(output_srt):
    print(f"Субтитры сохранены как {output_srt}")
else:
    print("Субтитры не найдены или ошибка.")
