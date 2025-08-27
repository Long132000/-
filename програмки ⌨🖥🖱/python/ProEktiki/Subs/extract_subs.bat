@echo off
setlocal enabledelayedexpansion

REM Проверка аргумента
if "%~1"=="" (
    echo Использование: %0 "путь_к_видео.mp4"
    exit /b
)

set "VIDEO=%~1"
set "BASENAME=%~n1"
set "TEMPFRAMES=%TEMP%\frames_%BASENAME%"
set "OUTPUT=%~dp1%~n1.srt"

REM Создаём папку для кадров
if exist "!TEMPFRAMES!" rmdir /s /q "!TEMPFRAMES!"
mkdir "!TEMPFRAMES!"

echo Извлечение кадров из видео...
ffmpeg -i "!VIDEO!" -vf "fps=1" "!TEMPFRAMES!\frame_%%04d.png"

echo Распознавание текста Tesseract...
set "INDEX=1"
set "SRTINDEX=1"
> "!OUTPUT!" echo.

for %%F in ("!TEMPFRAMES!\*.png") do (
    tesseract "%%F" "%%F_out" -l eng >nul 2>&1
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
    set /a INDEX+=1
)

echo Субтитры сохранены в "!OUTPUT!"
goto :eof

:TimeCode
set /a H=%1/3600
set /a M=(%1%%3600)/60
set /a S=%1%%60
set "TC=00:00:00,000"
if %H% lss 10 (set "H=0%H%")
if %M% lss 10 (set "M=0%M%")
if %S% lss 10 (set "S=0%S%")
set "%2=%H%:%M%:%S%,000"
exit /b
