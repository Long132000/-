@echo off
setlocal enabledelayedexpansion

REM ==== Настройка видео ====
if "%~1"=="" (
    REM Ищем mp4 в папке, если аргумент не указан
    for %%F in (*.mp4) do set "VIDEO=%%F"
) else (
    set "VIDEO=%~1"
)

if not defined VIDEO (
    echo Не найден файл видео. Положите mp4 в ту же папку или укажите путь.
    pause
    exit /b
)

set "BASENAME=%~n1"
set "TEMPFRAMES=%TEMP%\frames_%BASENAME%"
set "OUTPUT=%~dp0%~n1.srt"

REM ==== Создаём папку для кадров ====
if exist "!TEMPFRAMES!" rmdir /s /q "!TEMPFRAMES!"
mkdir "!TEMPFRAMES!"

echo.
echo Извлечение кадров из видео...
ffmpeg -i "!VIDEO!" -vf "fps=1" "!TEMPFRAMES!\frame_%%04d.png"
if errorlevel 1 (
    echo Ошибка при извлечении кадров.
    pause
    exit /b
)

echo.
echo Распознавание текста Tesseract...
set /a INDEX=1
set /a SRTINDEX=1
> "!OUTPUT!" echo.

for %%F in ("!TEMPFRAMES!\*.png") do (
    tesseract "%%F" "%%F_out" -l rus >nul 2>&1
    if exist "%%F_out.txt" (
        set /p TEXT=<"%%F_out.txt"
        if not "!TEXT!"=="" (
            REM Вычисляем примерное время кадра
            set /a START=INDEX-1
            set /a END=INDEX
            REM Форматируем таймкод hh:mm:ss,ms
            call :TimeCode !START! STARTTC
            call :TimeCode !END! ENDTOC

            echo !SRTINDEX!>>"!OUTPUT!"
            echo !STARTTC! --> !ENDTC!>>"!OUTPUT!"
            echo !TEXT!>>"!OUTPUT!"
            echo.>>"!OUTPUT!"

            set /a SRTINDEX+=1
        )
    )
    set /a INDEX+=1
)

echo.
echo Субтитры сохранены в "!OUTPUT!"
pause
exit /b

:TimeCode
set /a H=%1/3600
set /a M=(%1%%3600)/60
set /a S=%1%%60
if %H% lss 10 set "H=0%H%"
if %M% lss 10 set "M=0%M%"
if %S% lss 10 set "S=0%S%"
set "%2=%H%:%M%:%S%,000"
exit /b
