@echo off
REM ---------- Проверяем Tesseract ----------
where tesseract >nul 2>&1
IF ERRORLEVEL 1 (
    echo Tesseract OCR не найден в PATH.
    echo Пожалуйста, установите Tesseract или добавьте его в PATH.
    pause
    exit /b
)

REM ---------- Настройки ----------
set VIDEO_FILE=%~1
if "%VIDEO_FILE%"=="" (
    echo Укажите MP4 файл в качестве аргумента:
    echo Например: extract_subs.bat "D:\AdminWork\video.mp4"
    pause
    exit /b
)

set SCRIPT_PATH=%~dp0extract_subtitles.py

REM ---------- Запуск Python скрипта ----------
C:\Users\Administrator\pythoninst\python.exe "%SCRIPT_PATH%" "%VIDEO_FILE%"

echo.
echo Готово! Субтитры должны быть сохранены рядом с видео.
pause
