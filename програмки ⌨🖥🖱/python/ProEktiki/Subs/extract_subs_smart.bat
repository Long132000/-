@echo off
setlocal enabledelayedexpansion

:: Файл видео
set "input_file=C:\Users\Администратор\Desktop\CodesTime\video.mp4"

:: Папка для кадров
set "frames_dir=%TEMP%\frames_video"
if not exist "%frames_dir%" mkdir "%frames_dir%"

:: Файл субтитров
set "output_srt=video_subs.srt"
if exist "%output_srt%" del "%output_srt%"

echo Извлечение кадров из видео...
ffmpeg -i "%input_file%" "%frames_dir%\frame_%%04d.png"

echo Распознавание текста Tesseract...
set /a counter=1
for /r "%frames_dir%" %%f in (*.png) do (
    set "txt_file=%%~dpnf.txt"
    tesseract "%%f" "!txt_file!" -l rus

    if exist "!txt_file!" (
        for /f "delims=" %%l in ('type "!txt_file!" ^| findstr /r /v "^$"') do (
            echo !counter!>>"%output_srt%"
            set /a start=!counter!-1
            set /a end=!counter!
            echo 00:00:!start!,000 --> 00:00:!end!,000>>"%output_srt%"
            type "!txt_file!" >>"%output_srt%"
            echo.>>"%output_srt%"
            set /a counter+=1
            goto :next_frame
        )
        :next_frame
        del "!txt_file!"
    )
)

echo Готово! Субтитры сохранены в "%output_srt%"
pause
