#!/usr/bin/env python3
# remote_panel.py
"""
Async Telegram "Admin Panel" remote control using aiogram 3.x.
Fast, non-blocking UI: one dashboard message with inline buttons,
background execution for heavy tasks.

Usage:
 - Fill BOT_TOKEN and OWNER_ID
 - pip install -r requirements.txt
 - python remote_panel.py
"""

import asyncio
import platform
import socket
import subprocess
import sys
import time
from pathlib import Path

import psutil
import requests
from PIL import ImageGrab

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

# ========== CONFIG ==========
BOT_TOKEN = "8582054770:AAFiMXpRjG5LbOuUPTOeOvMbXYBfb4sJSxk"
OWNER_ID = 763880230  # <-- put your telegram id (int)
DOWNLOADS = Path.cwd() / "downloads"
DOWNLOADS.mkdir(exist_ok=True)
TELEGRAM_MSG_LIMIT = 4000
# ============================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Keep track of the dashboard message id per chat (user)
dashboard_message = {}  # chat_id -> message_id

# Utils
def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

def split_long_text(text: str, limit: int = TELEGRAM_MSG_LIMIT):
    for i in range(0, len(text), limit):
        yield text[i:i + limit]

def run_cmd_sync(cmd: str, timeout: int = 60) -> tuple[str, int]:
    """
    Run shell command synchronously (for to_thread). Handles Windows cp866 encoding.
    Returns (output, returncode).
    """
    if platform.system().lower().startswith("win"):
        enc = "cp866"
    else:
        enc = "utf-8"
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=enc, errors="replace", timeout=timeout)
        out = (proc.stdout or "") + (proc.stderr or "")
        return out, proc.returncode
    except subprocess.TimeoutExpired:
        return "Команда превысила лимит времени", -1
    except Exception as e:
        return f"Ошибка выполнения: {e}", -2

def get_local_ip() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Ошибка"

def get_external_ip() -> str:
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "Не удалось получить"

async def run_cmd_async(cmd: str) -> tuple[str, int]:
    return await asyncio.to_thread(run_cmd_sync, cmd)

async def take_screenshot(save_path: Path) -> None:
    # runs in thread
    def _grab(p: Path):
        im = ImageGrab.grab()
        im.save(p)
    await asyncio.to_thread(_grab, save_path)

# ========== DASHBOARD / KEYBOARDS ==========
def build_dashboard(text: str = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # first row: status (info text updated), screenshot quick
    kb.row(
        InlineKeyboardButton(text="📊 Status", callback_data="dash_status"),
        InlineKeyboardButton(text="🖼 Screenshot", callback_data="dash_screenshot"),
    )
    # second row: Files / CMD
    kb.row(
        InlineKeyboardButton(text="📁 Files", callback_data="dash_files"),
        InlineKeyboardButton(text="💻 CMD", callback_data="dash_cmd"),
    )
    # third row: Power / Processes
    kb.row(
        InlineKeyboardButton(text="⚙ Power", callback_data="dash_power"),
        InlineKeyboardButton(text="🚨 Processes", callback_data="dash_procs"),
    )
    # fourth: utilities
    kb.row(
        InlineKeyboardButton(text="📤 Upload file", callback_data="dash_upload"),
        InlineKeyboardButton(text="📥 Download file", callback_data="dash_download"),
    )
    # last row: refresh / close
    kb.row(
        InlineKeyboardButton(text="🔁 Refresh", callback_data="dash_refresh"),
        InlineKeyboardButton(text="❌ Close", callback_data="dash_close"),
    )
    return kb.as_markup()

def build_files_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton("📂 List current dir", callback_data="files_list_cwd"))
    kb.row(InlineKeyboardButton("🔍 List specific path", callback_data="files_list_path"))
    kb.row(InlineKeyboardButton("⬅ Back", callback_data="dash_back"))
    return kb.as_markup()

def build_cmd_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton("✏️ Enter command", callback_data="cmd_enter"))
    kb.row(InlineKeyboardButton("🌐 IP info", callback_data="cmd_ip"))
    kb.row(InlineKeyboardButton("⬅ Back", callback_data="dash_back"))
    return kb.as_markup()

def build_power_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton("⏻ Shutdown", callback_data="power_shutdown"),
        InlineKeyboardButton("🔁 Reboot", callback_data="power_reboot"),
    )
    kb.row(
        InlineKeyboardButton("💤 Sleep", callback_data="power_sleep"),
        InlineKeyboardButton("🔒 Lock", callback_data="power_lock"),
    )
    kb.row(InlineKeyboardButton("⬅ Back", callback_data="dash_back"))
    return kb.as_markup()

def build_procs_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton("📋 List processes", callback_data="procs_list"))
    kb.row(InlineKeyboardButton("💀 Kill PID", callback_data="procs_kill"))
    kb.row(InlineKeyboardButton("⬅ Back", callback_data="dash_back"))
    return kb.as_markup()

def confirm_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton("✅ Confirm", callback_data="confirm_yes"),
        InlineKeyboardButton("❌ Cancel", callback_data="confirm_no"),
    )
    return kb.as_markup()

# ========== HELPERS FOR DASHBOARD CONTENT ==========
def make_status_text() -> str:
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:/").percent if platform.system().lower().startswith("win") else psutil.disk_usage("/").percent
    host = platform.system() + " " + platform.release()
    text = f"💻 Host: {socket.gethostname()} ({host})\n⚡ CPU: {cpu}%   🧠 RAM: {ram}%\n💾 Disk: {disk}%\n\nClick buttons to act."
    return text

# State for interactive single-step operations per user
# owner_id -> {"mode": str, "meta": {...}}
interactive_state: dict[int, dict] = {}

# ========== HANDLERS ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if not is_owner(message.from_user.id):
        await message.reply("Доступ запрещён.")
        return
    txt = make_status_text()
    sent = await message.answer(txt, reply_markup=build_dashboard(txt))
    dashboard_message[message.chat.id] = sent.message_id

@dp.callback_query()
async def callback_router(callback: types.CallbackQuery):
    user = callback.from_user
    if not is_owner(user.id):
        await callback.answer("Доступ запрещён", show_alert=True)
        return

    data = callback.data
    chat_id = callback.message.chat.id

    # Dash: refresh
    if data == "dash_refresh":
        try:
            await callback.message.edit_text(make_status_text(), reply_markup=build_dashboard())
        except TelegramBadRequest:
            pass
        await callback.answer()
        return

    if data == "dash_close":
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
        await callback.answer()
        return

    # Status quick
    if data == "dash_status":
        await callback.message.edit_text(make_status_text(), reply_markup=build_dashboard())
        await callback.answer()
        return

    # Screenshot: heavy -> run in background
    if data == "dash_screenshot":
        await callback.answer("Taking screenshot...", show_alert=False)
        path = DOWNLOADS / f"shot_{int(time.time())}.png"
        try:
            await take_screenshot(path)
            await bot.send_photo(chat_id, path.open("rb"))
            path.unlink(missing_ok=True)
            await callback.message.edit_text("📸 Screenshot done.", reply_markup=build_dashboard())
        except Exception as e:
            await callback.message.edit_text(f"Error taking screenshot: {e}", reply_markup=build_dashboard())
        return

    # Files submenu
    if data == "dash_files":
        await callback.message.edit_text("Files menu:", reply_markup=build_files_kb())
        await callback.answer()
        return

    if data == "files_list_cwd":
        await callback.answer()
        cwd = Path.cwd()
        try:
            items = list(cwd.iterdir())
            out = f"Directory: {cwd}\n\n"
            for p in items[:200]:
                t = "<DIR>" if p.is_dir() else f"{p.stat().st_size} bytes"
                out += f"{p.name} — {t}\n"
            # send in parts if long
            for piece in split_long_text(out):
                await bot.send_message(chat_id, piece)
        except Exception as e:
            await bot.send_message(chat_id, f"Error: {e}")
        await callback.message.edit_text("Files menu:", reply_markup=build_files_kb())
        return

    if data == "files_list_path":
        interactive_state[user.id] = {"mode": "files_list_path"}
        await callback.message.edit_text("Send the path to list (absolute or relative):", reply_markup=build_files_kb())
        await callback.answer()
        return

    if data == "dash_cmd":
        await callback.message.edit_text("CMD menu:", reply_markup=build_cmd_kb())
        await callback.answer()
        return

    if data == "cmd_enter":
        interactive_state[user.id] = {"mode": "cmd_enter"}
        await callback.message.edit_text("Send the command to execute (plain text):", reply_markup=build_cmd_kb())
        await callback.answer()
        return

    if data == "cmd_ip":
        local = get_local_ip()
        ext = get_external_ip()
        await callback.message.edit_text(f"Host: {socket.gethostname()}\nLocal IP: {local}\nExternal IP: {ext}", reply_markup=build_cmd_kb())
        await callback.answer()
        return

    # Power menu
    if data == "dash_power":
        await callback.message.edit_text("Power menu:", reply_markup=build_power_kb())
        await callback.answer()
        return

    if data in ("power_shutdown", "power_reboot", "power_sleep", "power_lock"):
        # ask confirm
        interactive_state[user.id] = {"mode": "power_confirm", "action": data}
        await callback.message.edit_text("Confirm action:", reply_markup=confirm_kb())
        await callback.answer()
        return

    if data == "confirm_no":
        interactive_state.pop(user.id, None)
        await callback.message.edit_text("Cancelled.", reply_markup=build_dashboard())
        await callback.answer()
        return

    if data == "confirm_yes":
        state = interactive_state.pop(user.id, None)
        if not state:
            await callback.answer("Nothing to confirm")
            return
        act = state.get("action")
        await callback.message.edit_text("Executing...", reply_markup=build_dashboard())
        await callback.answer()
        # perform action in thread
        asyncio.create_task(execute_power_action(chat_id, act))
        return

    # Processes
    if data == "dash_procs":
        await callback.message.edit_text("Processes menu:", reply_markup=build_procs_kb())
        await callback.answer()
        return

    if data == "procs_list":
        await callback.answer("Collecting processes...")
        # run in thread
        out = await asyncio.to_thread(list, psutil.process_iter(attrs=['pid','name','username']))
        lines = []
        for p in out[:500]:
            try:
                info = p.info
                lines.append(f"{info['pid']}\t{info['name']}\t{info.get('username','')}")
            except Exception:
                pass
        text = "PID\tNAME\tUSER\n" + "\n".join(lines)
        for piece in split_long_text(text):
            await bot.send_message(chat_id, piece)
        await callback.message.edit_text("Processes menu (partial list sent).", reply_markup=build_procs_kb())
        return

    if data == "procs_kill":
        interactive_state[user.id] = {"mode": "procs_kill"}
        await callback.message.edit_text("Send PID to kill (number):", reply_markup=build_procs_kb())
        await callback.answer()
        return

    # upload/download entries
    if data == "dash_upload":
        interactive_state[user.id] = {"mode": "upload_file"}
        await callback.message.edit_text("Send a file to upload to the PC (it will be saved to downloads/)", reply_markup=build_dashboard())
        await callback.answer()
        return

    if data == "dash_download":
        interactive_state[user.id] = {"mode": "download_file"}
        await callback.message.edit_text("Send the path to the file to download (absolute or relative):", reply_markup=build_dashboard())
        await callback.answer()
        return

    if data == "dash_back":
        await callback.message.edit_text(make_status_text(), reply_markup=build_dashboard())
        await callback.answer()
        return

    await callback.answer("Unknown action")

# Message handler for interactive states and general commands
@dp.message()
async def message_router(message: types.Message):
    user = message.from_user
    if not is_owner(user.id):
        return
    state = interactive_state.get(user.id)

    text = (message.text or "").strip()

    # If user is entering something for a mode:
    if state:
        mode = state.get("mode")
        if mode == "files_list_path":
            path = Path(text)
            if not path.is_absolute():
                path = Path.cwd() / path
            if not path.exists():
                await message.reply(f"Path not found: {path}")
            else:
                try:
                    items = list(path.iterdir())
                    out = f"Directory: {path}\n\n"
                    for p in items[:500]:
                        t = "<DIR>" if p.is_dir() else f"{p.stat().st_size} bytes"
                        out += f"{p.name} — {t}\n"
                    for piece in split_long_text(out):
                        await message.reply(piece)
                except Exception as e:
                    await message.reply(f"Error listing: {e}")
            interactive_state.pop(user.id, None)
            return

        if mode == "cmd_enter":
            await message.reply("Executing...")
            cmd_text = text
            out, code = await run_cmd_async(cmd_text)
            payload = f"Return code: {code}\n\n{out or '<no output>'}"
            # If long, send as file
            if len(payload) > TELEGRAM_MSG_LIMIT:
                p = DOWNLOADS / f"cmd_out_{int(time.time())}.txt"
                p.write_text(payload, encoding="utf-8", errors="replace")
                await bot.send_document(user.id, p.open("rb"))
                p.unlink(missing_ok=True)
            else:
                for piece in split_long_text(payload):
                    await message.reply(piece)
            interactive_state.pop(user.id, None)
            return

        if mode == "procs_kill":
            try:
                pid = int(text)
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait(timeout=5)
                await message.reply(f"Process {pid} terminated.")
            except Exception as e:
                await message.reply(f"Error killing pid: {e}")
            interactive_state.pop(user.id, None)
            return

        if mode == "upload_file":
            await message.reply("Please send a file (attach) to upload.")
            # we keep mode until file arrives
            return

        if mode == "download_file":
            path = Path(text)
            if not path.is_absolute():
                path = Path.cwd() / path
            if not path.exists() or not path.is_file():
                await message.reply(f"File not found: {path}")
            else:
                await message.reply("Sending file...")
                try:
                    await bot.send_document(user.id, path.open("rb"))
                except Exception as e:
                    await message.reply(f"Error sending file: {e}")
            interactive_state.pop(user.id, None)
            return

    # If no active state and message is a command-like
    if text.startswith("/cmd "):
        cmd_text = text.replace("/cmd ", "", 1)
        await message.reply("Running command...")
        out, code = await run_cmd_async(cmd_text)
        payload = f"Return code: {code}\n\n{out or '<no output>'}"
        if len(payload) > TELEGRAM_MSG_LIMIT:
            p = DOWNLOADS / f"cmd_out_{int(time.time())}.txt"
            p.write_text(payload, encoding="utf-8", errors="replace")
            await bot.send_document(user.id, p.open("rb"))
            p.unlink(missing_ok=True)
        else:
            for piece in split_long_text(payload):
                await message.reply(piece)
        return

    # fallback quick helpers
    if text == "/start" or text.lower() == "menu":
        await message.reply(make_status_
