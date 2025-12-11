"""
remote_bot.py
Remote control Telegram bot with inline menus and submenus.

Requirements:
pip install pyTelegramBotAPI psutil pillow requests

Notes:
- This bot performs potentially dangerous actions (shutdown/reboot/etc).
  Use only on your own machines and never run provided code on machines you don't own.
- This script intentionally DOES NOT implement any autorun-from-USB or stealth installation.
- To run truly "without window" on Windows, start with pythonw.exe, e.g.:
  start "" pythonw "C:\path\to\remote_bot.py"
"""

import os
import sys
import time
import subprocess
import platform
import socket
import threading
import shutil

import telebot
from telebot import types

import psutil
from PIL import ImageGrab
import requests

# ========== CONFIG ==========
BOT_TOKEN = "8582054770:AAFiMXpRjG5LbOuUPTOeOvMbXYBfb4sJSxk"  # <-- твой токен
USER_ID = 763880230  # <-- твой Telegram user id
# ============================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# Helper: allow only owner
def allowed(chat):
    return chat.from_user and chat.from_user.id == USER_ID

# Helper: send message (owner only)
def send_restricted(chat_id, text):
    bot.send_message(chat_id, text)

# -----------------------
# Keyboard builders
# -----------------------
def main_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("📊 Статус", callback_data="menu_status"),
        types.InlineKeyboardButton("🖼 Скриншот", callback_data="menu_screenshot")
    )
    kb.row(
        types.InlineKeyboardButton("📁 Файлы", callback_data="menu_files"),
        types.InlineKeyboardButton("💻 CMD", callback_data="menu_cmd")
    )
    kb.row(
        types.InlineKeyboardButton("⚙ Управление ПК", callback_data="menu_power"),
        types.InlineKeyboardButton("🔧 Процессы", callback_data="menu_procs")
    )
    kb.row(types.InlineKeyboardButton("📤 Файлы (загрузить/скачать)", callback_data="menu_transfer"))
    return kb

# simple back button
def back_kb():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
    return kb

# files submenu
def files_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("📂 Список текущей папки", callback_data="files_list_cwd"))
    kb.row(types.InlineKeyboardButton("📂 Указать путь", callback_data="files_prompt_path"))
    kb.row(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
    return kb

# cmd submenu
def cmd_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("⌨ Ввести команду", callback_data="cmd_prompt"))
    kb.row(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
    return kb

# power submenu
def power_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("⏻ Выключить", callback_data="power_shutdown"),
        types.InlineKeyboardButton("🔁 Перезагрузить", callback_data="power_reboot")
    )
    kb.row(
        types.InlineKeyboardButton("😴 Сон", callback_data="power_sleep"),
        types.InlineKeyboardButton("🔒 Блокировка", callback_data="power_lock")
    )
    kb.row(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
    return kb

# processes submenu
def procs_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("Список процессов", callback_data="procs_list"))
    kb.row(types.InlineKeyboardButton("Убить PID", callback_data="procs_kill_prompt"))
    kb.row(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
    return kb

# transfer submenu
def transfer_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("📤 Отправить файл (PC -> Telegram)", callback_data="transfer_send_prompt"))
    kb.row(types.InlineKeyboardButton("📥 Сохранить файл (Telegram -> PC)", callback_data="transfer_recv_prompt"))
    kb.row(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
    return kb

# -----------------------
# Utilities
# -----------------------
def system_info_text():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("C:/").percent if platform.system() == "Windows" else psutil.disk_usage("/").percent
        uname = platform.system() + " " + platform.release()
        procs = len(psutil.pids())
        return (f"💻 Система: {uname}\n"
                f"⚡ CPU: {cpu}%\n"
                f"🧠 RAM: {ram}%\n"
                f"💾 Диск: {disk}%\n"
                f"📊 Процессы: {procs}")
    except Exception as e:
        return f"Ошибка при получении статуса: {e}"

def safe_run_cmd(cmd, timeout=30):
    """
    Выполняем команду и пытаемся корректно вернуть русский вывод в Windows (cp866).
    """
    try:
        # Определяем подходящую кодировку
        if platform.system() == "Windows":
            encoding = "cp866"
        else:
            encoding = "utf-8"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        out = proc.stdout or proc.stderr
        if out is None:
            return "Команда выполнена (без вывода)"
        return out
    except subprocess.TimeoutExpired:
        return "Превышено время выполнения команды."
    except Exception as e:
        return f"Ошибка выполнения команды: {e}"

def list_directory(path, max_entries=200):
    try:
        entries = os.listdir(path)
        entries.sort()
        total = len(entries)
        entries = entries[:max_entries]
        lines = []
        for name in entries:
            full = os.path.join(path, name)
            try:
                size = os.path.getsize(full)
                lines.append(f"{name} — {size} bytes")
            except:
                lines.append(f"{name}")
        if total > max_entries:
            lines.append(f"\n...и ещё {total - max_entries} элементов (не показаны)")
        return "\n".join(lines) or "<пусто>"
    except Exception as e:
        return f"Ошибка доступа к папке: {e}"

# -----------------------
# Power actions (Windows)
# -----------------------
def do_shutdown():
    try:
        if platform.system() == "Windows":
            subprocess.Popen("shutdown /s /t 0", shell=True)
            return "Инициализировано выключение."
        else:
            subprocess.Popen("shutdown -h now", shell=True)
            return "Инициализировано выключение (POSIX)."
    except Exception as e:
        return f"Ошибка: {e}"

def do_reboot():
    try:
        if platform.system() == "Windows":
            subprocess.Popen("shutdown /r /t 0", shell=True)
            return "Инициализирована перезагрузка."
        else:
            subprocess.Popen("reboot", shell=True)
            return "Инициализирована перезагрузка (POSIX)."
    except Exception as e:
        return f"Ошибка: {e}"

def do_sleep():
    try:
        if platform.system() == "Windows":
            # Try SetSuspendState (may require privileges)
            # fallback to rundll32 call
            subprocess.Popen('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True)
            return "Инициализирован перевод в спящий режим (Windows)."
        else:
            subprocess.Popen("systemctl suspend", shell=True)
            return "Инициализирован перевод в спящий режим (POSIX)."
    except Exception as e:
        return f"Ошибка: {e}"

def do_lock():
    try:
        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "ПК заблокирован."
        else:
            # Try common lock commands for Linux
            cmds = ["gnome-screensaver-command -l", "xdg-screensaver lock"]
            for c in cmds:
                res = subprocess.call(c, shell=True)
            return "Попытка блокировки экрана (POSIX)."
    except Exception as e:
        return f"Ошибка: {e}"

# -----------------------
# Telegram handlers
# -----------------------

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    if not allowed(message):
        return
    text = "🤖 Добро пожаловать! Главное меню:"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# Inline button actions
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Security: only allow owner to press buttons
    try:
        user_id = call.from_user.id
    except:
        return

    if user_id != USER_ID:
        bot.answer_callback_query(call.id, "Доступ запрещён")
        return

    data = call.data

    # Back to main
    if data == "back_main":
        bot.edit_message_text("Главное меню:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
        return

    # Main menu entries
    if data == "menu_status":
        txt = system_info_text()
        bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        return

    if data == "menu_screenshot":
        bot.answer_callback_query(call.id, "Делаю скриншот...")
        try:
            img = ImageGrab.grab()
            path = os.path.join(os.getcwd(), "shot_temp.png")
            img.save(path)
            bot.send_photo(call.message.chat.id, open(path, "rb"))
            os.remove(path)
            # keep menu message, update caption
            bot.edit_message_text("Скриншот отправлен.", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        except Exception as e:
            bot.edit_message_text(f"Ошибка скриншота: {e}", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        return

    if data == "menu_files":
        bot.edit_message_text("📁 Меню Файлы:", call.message.chat.id, call.message.message_id, reply_markup=files_menu())
        return

    if data == "menu_cmd":
        bot.edit_message_text("⌨ Меню CMD:", call.message.chat.id, call.message.message_id, reply_markup=cmd_menu())
        return

    if data == "menu_power":
        bot.edit_message_text("⚙ Управление ПК:", call.message.chat.id, call.message.message_id, reply_markup=power_menu())
        return

    if data == "menu_procs":
        bot.edit_message_text("🔧 Процессы:", call.message.chat.id, call.message.message_id, reply_markup=procs_menu())
        return

    if data == "menu_transfer":
        bot.edit_message_text("📤 Передача файлов:", call.message.chat.id, call.message.message_id, reply_markup=transfer_menu())
        return

    # Files submenu actions
    if data == "files_list_cwd":
        cwd = os.getcwd()
        txt = f"Текущая папка: {cwd}\n\n" + list_directory(cwd, max_entries=400)
        bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        return

    if data == "files_prompt_path":
        msg = bot.send_message(call.message.chat.id, "Отправь путь к папке (пример: C:\\\\Users\\\\User\\\\Downloads):")
        bot.register_next_step_handler(msg, files_show_by_path)
        return

    # CMD submenu
    if data == "cmd_prompt":
        msg = bot.send_message(call.message.chat.id, "Напиши команду для выполнения в терминале (Windows: поддержка русских в выводе).")
        bot.register_next_step_handler(msg, cmd_execute_from_msg)
        return

    # Power actions
    if data == "power_shutdown":
        bot.edit_message_text("Идёт выключение...", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        res = do_shutdown()
        # Send result as new message (may not be seen if system goes down immediately)
        bot.send_message(call.message.chat.id, res)
        return

    if data == "power_reboot":
        bot.edit_message_text("Идёт перезагрузка...", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        res = do_reboot()
        bot.send_message(call.message.chat.id, res)
        return

    if data == "power_sleep":
        bot.edit_message_text("Перевод в спящий режим...", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        res = do_sleep()
        bot.send_message(call.message.chat.id, res)
        return

    if data == "power_lock":
        bot.edit_message_text("Блокирую экран...", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        res = do_lock()
        bot.send_message(call.message.chat.id, res)
        return

    # Processes
    if data == "procs_list":
        try:
            procs = []
            for p in psutil.process_iter(['pid','name']):
                info = p.info
                procs.append(f"{info['pid']}: {info['name']}")
            text = "Процессы (первые 200):\n\n" + "\n".join(procs[:200])
        except Exception as e:
            text = f"Ошибка получения процессов: {e}"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        return

    if data == "procs_kill_prompt":
        msg = bot.send_message(call.message.chat.id, "Отправь PID процесса, который нужно завершить (число):")
        bot.register_next_step_handler(msg, procs_kill_by_msg)
        return

    # Transfer
    if data == "transfer_send_prompt":
        msg = bot.send_message(call.message.chat.id, "Укажи путь к файлу на ПК, который нужно отправить (пример: C:\\\\path\\\\file.txt):")
        bot.register_next_step_handler(msg, transfer_send_file)
        return

    if data == "transfer_recv_prompt":
        bot.edit_message_text("Отправь файл в этот чат — он будет сохранён на ПК в текущую папку.", call.message.chat.id, call.message.message_id, reply_markup=back_kb())
        return

    # unknown
    bot.answer_callback_query(call.id, "Неизвестная команда.")

# -----------------------
# Next-step handlers
# -----------------------

def files_show_by_path(message):
    if not allowed(message):
        return
    path = message.text.strip()
    txt = f"Содержимое {path}:\n\n" + list_directory(path, max_entries=400)
    bot.send_message(message.chat.id, txt, reply_markup=back_kb())

def cmd_execute_from_msg(message):
    if not allowed(message):
        return
    cmd_text = message.text.strip()
    bot.send_message(message.chat.id, "Выполняю...")
    out = safe_run_cmd(cmd_text, timeout=60)
    # Telegram message length limit handling
    for i in range(0, len(out), 4000):
        bot.send_message(message.chat.id, out[i:i+4000])
    bot.send_message(message.chat.id, "Готово.", reply_markup=back_kb())

def procs_kill_by_msg(message):
    if not allowed(message):
        return
    try:
        pid = int(message.text.strip())
        p = psutil.Process(pid)
        p.terminate()
        gone, alive = psutil.wait_procs([p], timeout=3)
        if alive:
            p.kill()
        bot.send_message(message.chat.id, f"Процесс {pid} завершён.", reply_markup=back_kb())
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось завершить процесс: {e}", reply_markup=back_kb())

def transfer_send_file(message):
    if not allowed(message):
        return
    path = message.text.strip()
    if not os.path.isfile(path):
        bot.send_message(message.chat.id, f"Файл не найден: {path}", reply_markup=back_kb())
        return
    try:
        bot.send_document(message.chat.id, open(path, "rb"))
        bot.send_message(message.chat.id, "Файл отправлен.", reply_markup=back_kb())
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка отправки файла: {e}", reply_markup=back_kb())

# Receive file from Telegram and save to current folder
@bot.message_handler(content_types=['document', 'audio', 'video', 'photo', 'sticker', 'voice'])
def handle_incoming_file(message):
    if not allowed(message):
        return
    # Only process documents and photos in practice
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded = bot.download_file(file_info.file_path)
            local_fname = os.path.join(os.getcwd(), os.path.basename(file_info.file_path))
            with open(local_fname, 'wb') as f:
                f.write(downloaded)
            bot.reply_to(message, f"Файл сохранён: {local_fname}")
        elif message.photo:
            # take highest resolution
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded = bot.download_file(file_info.file_path)
            local_fname = os.path.join(os.getcwd(), "photo_from_telegram.jpg")
            with open(local_fname, 'wb') as f:
                f.write(downloaded)
            bot.reply_to(message, f"Фото сохранено как {local_fname}")
        else:
            bot.reply_to(message, "Тип файла не поддерживается для сохранения.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка сохранения файла: {e}")

# -----------------------
# Extra admin commands (text commands)
# -----------------------
@bot.message_handler(func=lambda m: allowed(m) and m.text and m.text.startswith("/"))
def handle_text_commands(message):
    # owner-only slash commands not handled by buttons
    cmd = message.text.strip().split()[0].lower()

    if cmd == "/status":
        bot.reply_to(message, system_info_text())
        return

    if cmd == "/ip":
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "Ошибка"
        try:
            external_ip = requests.get("https://api.ipify.org").text
        except:
            external_ip = "Не удалось получить внешний IP"
        bot.reply_to(message, f"Имя ПК: {hostname}\nЛокальный IP: {local_ip}\nВнешний IP: {external_ip}")
        return

    if cmd == "/make_exe":
        # Create an EXE using pyinstaller (if available)
        bot.reply_to(message, "Запускаю сборку EXE с помощью pyinstaller (если установлен). Это может занять время.")
        threading.Thread(target=make_exe_background, args=(message.chat.id,)).start()
        return

    # exec raw cmd fallback
    if cmd == "/cmd":
        # user might send "/cmd ipconfig"
        text = message.text[len("/cmd"):].strip()
        if not text:
            bot.reply_to(message, "Напиши команду после /cmd")
            return
        out = safe_run_cmd(text, timeout=60)
        for i in range(0, len(out), 4000):
            bot.reply_to(message, out[i:i+4000])
        return

    # shutdown/reboot via text
    if cmd == "/shutdown":
        bot.reply_to(message, do_shutdown())
        return

    if cmd == "/reboot":
        bot.reply_to(message, do_reboot())
        return

    if cmd == "/sleep":
        bot.reply_to(message, do_sleep())
        return

    if cmd == "/lock":
        bot.reply_to(message, do_lock())
        return

    # unknown
    bot.reply_to(message, "Неизвестная команда. Используй меню.", reply_markup=main_menu())

# -----------------------
# EXE builder (pyinstaller)
# -----------------------
def make_exe_background(chat_id):
    """
    Попробует запустить pyinstaller --onefile для текущего скрипта.
    Пользователь сам должен иметь pyinstaller в окружении.
    """
    try:
        script = os.path.abspath(sys.argv[0])
        # Create dist folder path
        bot.send_message(chat_id, f"Собираю EXE из {script} ...")
        # Ensure pyinstaller exists
        if shutil.which("pyinstaller") is None:
            bot.send_message(chat_id, "pyinstaller не найден в PATH. Установи: pip install pyinstaller")
            return
        cmd = f'pyinstaller --onefile --noconsole "{script}"'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # stream output
        for line in proc.stdout:
            bot.send_message(chat_id, line.strip())
        proc.wait()
        if proc.returncode == 0:
            dist_name = os.path.splitext(os.path.basename(script))[0] + ".exe"
            dist_path = os.path.join(os.getcwd(), "dist", dist_name)
            if os.path.exists(dist_path):
                bot.send_document(chat_id, open(dist_path, 'rb'))
            else:
                bot.send_message(chat_id, "Сборка завершена, но не удалось найти exe в dist/.")
        else:
            bot.send_message(chat_id, f"pyinstaller вернул код {proc.returncode}")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка сборки EXE: {e}")

# -----------------------
# Keep bot alive loop with auto-restart on exception
# -----------------------
def run_bot_polling():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print("Polling error:", e)
            time.sleep(5)

if __name__ == "__main__":
    print("Remote bot started. Owner ID:", USER_ID)
    # main message
    try:
        # send a startup message to owner (if bot allowed to message)
        try:
            bot.send_message(USER_ID, "Бот запущен. Главное меню:", reply_markup=main_menu())
        except Exception:
            pass
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)

    # run polling in main thread (function contains restart logic)
    run_bot_polling()
