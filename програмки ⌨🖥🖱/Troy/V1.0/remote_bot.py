import telebot
import subprocess
import os
import psutil
import platform
from PIL import ImageGrab
import socket
import requests

# === НАСТРОЙКИ ===
BOT_TOKEN = "8582054770:AAFiMXpRjG5LbOuUPTOeOvMbXYBfb4sJSxk"
USER_ID = 763880230
# =================

bot = telebot.TeleBot(BOT_TOKEN)

def allow(msg):
    return msg.from_user.id == USER_ID


# ===========================
#       /start
# ===========================
@bot.message_handler(commands=['start'])
def start(msg):
    if not allow(msg): 
        return
    bot.reply_to(msg,
        "🤖 Бот активен.\n"
        "Доступные команды:\n"
        "/status — состояние системы\n"
        "/screenshot — скриншот экрана\n"
        "/cmd <команда> — выполнить команду\n"
        "/ip — показать IP\n"
    )


# ===========================
#       /status
# ===========================
@bot.message_handler(commands=['status'])
def status(msg):
    if not allow(msg): 
        return

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:/").percent

    bot.reply_to(msg, 
        f"💻 Система: {platform.system()} {platform.release()}\n"
        f"⚡ CPU: {cpu}%\n"
        f"🧠 RAM: {ram}%\n"
        f"💾 Диск C: {disk}%"
    )


# ===========================
#       /screenshot
# ===========================
@bot.message_handler(commands=['screenshot'])
def screenshot(msg):
    if not allow(msg):
        return

    try:
        img = ImageGrab.grab()
        img.save("shot.png")
        with open("shot.png", "rb") as f:
            bot.send_photo(msg.chat.id, f)
        os.remove("shot.png")
    except Exception as e:
        bot.reply_to(msg, f"❌ Ошибка: {e}")


# ===========================
#       /cmd
# ===========================
@bot.message_handler(commands=['cmd'])
def cmd(msg):
    if not allow(msg):
        return

    command = msg.text.replace("/cmd ", "", 1).strip()
    if not command:
        bot.reply_to(msg, "Напиши команду после /cmd")
        return

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout or result.stderr or "Готово"

        # Отправить частями
        for i in range(0, len(output), 4000):
            bot.reply_to(msg, output[i:i+4000])

    except Exception as e:
        bot.reply_to(msg, f"Ошибка: {e}")


# ===========================
#       /ip
# ===========================
@bot.message_handler(commands=['ip'])
def get_ip(msg):
    if not allow(msg): 
        return

    hostname = socket.gethostname()

    # Локальный IP
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "Ошибка"

    # Внешний IP
    try:
        external_ip = requests.get("https://api.ipify.org").text
    except:
        external_ip = "Ошибка получения внешнего IP"

    bot.reply_to(msg,
        f"Имя ПК: {hostname}\n"
        f"Локальный IP: {local_ip}\n"
        f"Внешний IP: {external_ip}"
    )


# ===========================
#       Запуск
# ===========================
print("Бот запущен!")

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as error:
        print("Ошибка polling:", error)
        # Перезапуск через 5 сек
        import time
        time.sleep(5)
