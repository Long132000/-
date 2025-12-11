@echo off
chcp 65001 >nul
title Установка Telegram Remote Bot

echo ===============================
echo     Проверка Python
echo ===============================
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден! Установите его с python.org и включите галочку "Add to PATH".
    pause
    exit /b
)

echo.
echo ===============================
echo     Создаю скрытую папку
echo ===============================
set DEST=%APPDATA%\RemoteBot
mkdir "%DEST%" >nul 2>&1
attrib +h "%DEST%"

echo.
echo ===============================
echo     Копирую файлы
echo ===============================
copy remote_bot.py "%DEST%\remote_bot.py" /Y >nul
copy requirements.txt "%DEST%\requirements.txt" /Y >nul

echo.
echo ===============================
echo     Устанавливаю модули
echo ===============================
pip install -r "%DEST%\requirements.txt"

echo.
echo ===============================
echo     Добавляю в автозапуск
echo ===============================
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run ^
 /v RemoteBot ^
 /t REG_SZ ^
 /d "python \"%DEST%\remote_bot.py\"" ^
 /f

echo.
echo ===============================
echo     Запускаю бота в фоне
echo ===============================
start "" pythonw "%DEST%\remote_bot.py"

echo.
echo Установка завершена!
echo Можете закрыть окно.
pause
