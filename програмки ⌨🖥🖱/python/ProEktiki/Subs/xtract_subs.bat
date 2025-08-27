@echo off
setlocal
set "VIDEO=video.mp4"
set "OUTPUT=subtitles.srt"
ffmpeg -i "%VIDEO%" -map 0:s:0 "%OUTPUT%" -y
pause
