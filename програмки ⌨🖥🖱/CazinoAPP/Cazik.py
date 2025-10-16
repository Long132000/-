import os
import json
import random
import math
import pytz
from datetime import datetime, timedelta, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, JobQueue

# Пути к файлам
DATA_FILE = "user_data.json"
EXCHANGE_RATE_FILE = "exchange_rate.json"
WHEEL_HISTORY_FILE = "wheel_history.json"
CLANS_FILE = "clans.json"
QUIZ_FILE = "quiz.json"
MARKET_FILE = "market.json"
AUCTION_FILE = "auction.json"
ITEMS_FILE = "items.json"
LEADERBOARD_REWARDS_FILE = "leaderboard_rewards.json"
CORPORATIONS_FILE = "corporations.json"
REAL_ESTATE_FILE = "real_estate.json"

# Начальные значения
DAILY_BONUS = 100
MIN_EXCHANGE_RATE = 50
MAX_EXCHANGE_RATE = 150
BASE_ANNUAL_RATE = 0.25  # 25% годовых
WHEEL_PRIZES = [
    {"multiplier": 0.0, "text": "💔 Проигрыш"},
    {"multiplier": 0.5, "text": "🍀 Маленький выигрыш"},
    {"multiplier": 1.0, "text": "💰 Стандартный приз"},
    {"multiplier": 2.0, "text": "🎉 Крупный выигрыш!"},
    {"multiplier": 5.0, "text": "🔥 ДЖЕКПОТ!"}
]

# Достижения
ACHIEVEMENTS = {
    "first_win": {"name": "Первая победа", "reward": 50, "description": "Выиграйте в казино первый раз"},
    "ten_wins": {"name": "Десять побед", "reward": 500, "description": "Выиграйте в казино 10 раз"},
    "rich": {"name": "Богач", "reward": 1000, "description": "Накопите 100 000 копеек"},
    "gambler": {"name": "Азартный игрок", "reward": 2000, "description": "Сделайте ставку 'всё' и выиграйте"},
    "daily_fan": {"name": "Постоянный клиент", "reward": 3000, "description": "Получите ежедневный бонус 30 дней подряд"},
    "deposit_king": {"name": "Король депозитов", "reward": 5000, "description": "Накопите 1 000 000 на депозите"},
    "wheel_master": {"name": "Мастер колеса", "reward": 2500, "description": "Выиграйте джекпот на колесе фортуны"},
    "clan_leader": {"name": "Лидер клана", "reward": 3000, "description": "Создайте клан с 10+ участниками"},
    "quiz_master": {"name": "Знаток", "reward": 1000, "description": "Правильно ответьте на 50 вопросов викторины"},
    "market_trader": {"name": "Торговец", "reward": 1500, "description": "Продайте 10 предметов на рынке"},
    "item_collector": {"name": "Коллекционер", "reward": 2000, "description": "Соберите 10 разных предметов"},
    "clan_champion": {"name": "Чемпион клана", "reward": 2500, "description": "Внесите 50 000 в банк клана"},
    "pvp_champion": {"name": "Боец", "reward": 1500, "description": "Выиграйте 10 дуэлей"},
    "clan_warrior": {"name": "Воин клана", "reward": 2000, "description": "Участвуйте в 5 клановых войнах"},
    "real_estate_tycoon": {"name": "Магнат недвижимости", "reward": 5000, "description": "Приобретите 5 объектов недвижимости"},
    "corporation_leader": {"name": "Глава корпорации", "reward": 10000, "description": "Создайте корпорацию с 3+ кланами"}
}

# Уровни (до 30 уровня)
LEVELS = [
    {"level": 1, "exp_required": 0, "deposit_bonus": 0.00, "daily_bonus": 0},
    {"level": 2, "exp_required": 100, "deposit_bonus": 0.01, "daily_bonus": 5},
    {"level": 3, "exp_required": 300, "deposit_bonus": 0.02, "daily_bonus": 10},
    {"level": 4, "exp_required": 600, "deposit_bonus": 0.03, "daily_bonus": 15},
    {"level": 5, "exp_required": 1000, "deposit_bonus": 0.04, "daily_bonus": 20},
    {"level": 6, "exp_required": 1500, "deposit_bonus": 0.05, "daily_bonus": 25},
    {"level": 7, "exp_required": 2100, "deposit_bonus": 0.06, "daily_bonus": 30},
    {"level": 8, "exp_required": 2800, "deposit_bonus": 0.07, "daily_bonus": 35},
    {"level": 9, "exp_required": 3600, "deposit_bonus": 0.08, "daily_bonus": 40},
    {"level": 10, "exp_required": 4500, "deposit_bonus": 0.09, "daily_bonus": 50},
    {"level": 11, "exp_required": 6000, "deposit_bonus": 0.10, "daily_bonus": 60},
    {"level": 12, "exp_required": 8000, "deposit_bonus": 0.11, "daily_bonus": 70},
    {"level": 13, "exp_required": 10000, "deposit_bonus": 0.12, "daily_bonus": 80},
    {"level": 14, "exp_required": 13000, "deposit_bonus": 0.13, "daily_bonus": 90},
    {"level": 15, "exp_required": 17000, "deposit_bonus": 0.14, "daily_bonus": 100},
    {"level": 16, "exp_required": 22000, "deposit_bonus": 0.15, "daily_bonus": 120},
    {"level": 17, "exp_required": 28000, "deposit_bonus": 0.16, "daily_bonus": 140},
    {"level": 18, "exp_required": 35000, "deposit_bonus": 0.17, "daily_bonus": 160},
    {"level": 19, "exp_required": 45000, "deposit_bonus": 0.18, "daily_bonus": 180},
    {"level": 20, "exp_required": 60000, "deposit_bonus": 0.19, "daily_bonus": 200},
    {"level": 21, "exp_required": 80000, "deposit_bonus": 0.20, "daily_bonus": 250},
    {"level": 22, "exp_required": 100000, "deposit_bonus": 0.21, "daily_bonus": 300},
    {"level": 23, "exp_required": 130000, "deposit_bonus": 0.22, "daily_bonus": 350},
    {"level": 24, "exp_required": 170000, "deposit_bonus": 0.23, "daily_bonus": 400},
    {"level": 25, "exp_required": 220000, "deposit_bonus": 0.24, "daily_bonus": 500},
    {"level": 26, "exp_required": 280000, "deposit_bonus": 0.25, "daily_bonus": 600},
    {"level": 27, "exp_required": 350000, "deposit_bonus": 0.26, "daily_bonus": 700},
    {"level": 28, "exp_required": 450000, "deposit_bonus": 0.27, "daily_bonus": 800},
    {"level": 29, "exp_required": 600000, "deposit_bonus": 0.28, "daily_bonus": 900},
    {"level": 30, "exp_required": 800000, "deposit_bonus": 0.30, "daily_bonus": 1000}
]

# Уровни кланов
CLAN_LEVELS = [
    {"level": 1, "required_money": 1000, "bonus": 0.001, "name": "Новички", "max_members": 10},
    {"level": 2, "required_money": 5000, "bonus": 0.002, "name": "Ученики", "max_members": 15},
    {"level": 3, "required_money": 10000, "bonus": 0.003, "name": "Подмастерья", "max_members": 20},
    {"level": 4, "required_money": 20000, "bonus": 0.004, "name": "Мастера", "max_members": 25},
    {"level": 5, "required_money": 50000, "bonus": 0.005, "name": "Грандмастера", "max_members": 30},
    {"level": 6, "required_money": 100000, "bonus": 0.006, "name": "Легенды", "max_members": 50}
]

# Уровни корпораций
CORPORATION_LEVELS = [
    {"level": 1, "required_money": 50000, "bonus": 0.005, "name": "Стартап", "max_clans": 3},
    {"level": 2, "required_money": 200000, "bonus": 0.010, "name": "Компания", "max_clans": 5},
    {"level": 3, "required_money": 500000, "bonus": 0.015, "name": "Корпорация", "max_clans": 7},
    {"level": 4, "required_money": 1000000, "bonus": 0.020, "name": "Империя", "max_clans": 10}
]

# Объекты недвижимости
REAL_ESTATE_TYPES = [
    {"id": "small_house", "name": "🏠 Небольшой дом", "price": 50000, "income": 100, "upgrade_cost": 30000},
    {"id": "apartment", "name": "🏢 Апартаменты", "price": 150000, "income": 300, "upgrade_cost": 80000},
    {"id": "villa", "name": "🏡 Вилла", "price": 500000, "income": 1000, "upgrade_cost": 200000},
    {"id": "hotel", "name": "🏨 Отель", "price": 2000000, "income": 5000, "upgrade_cost": 1000000},
    {"id": "skyscraper", "name": "🏙️ Небоскреб", "price": 10000000, "income": 25000, "upgrade_cost": 5000000}
]

# Квесты (расширенный список)
DAILY_QUESTS = [
    {"id": "daily1", "name": "🎯 Игрок дня", "description": "Сыграйте 3 раза в казино", "goal": 3, "reward_exp": 50, "reward_kopecks": 100},
    {"id": "daily2", "name": "💸 Инвестор", "description": "Положите 500 копеек на депозит", "goal": 500, "reward_exp": 75, "reward_kopecks": 150},
    {"id": "daily3", "name": "🤝 Щедрая душа", "description": "Отправьте деньги другому игроку", "goal": 1, "reward_exp": 40, "reward_kopecks": 80},
    {"id": "daily4", "name": "🎡 Крутильщик", "description": "Покрутите колесо фортуны", "goal": 1, "reward_exp": 30, "reward_kopecks": 60},
    {"id": "daily5", "name": "💰 Богач", "description": "Заработайте 1000 копеек", "goal": 1000, "reward_exp": 100, "reward_kopecks": 200},
    {"id": "daily6", "name": "💎 Рубиновый магнат", "description": "Обменяйте 500 копеек на рубии", "goal": 500, "reward_exp": 60, "reward_kopecks": 120},
    {"id": "daily7", "name": "📈 Трейдер", "description": "Продайте рубии за копейки", "goal": 1, "reward_exp": 50, "reward_kopecks": 100},
    {"id": "daily8", "name": "🏰 Строитель", "description": "Внесите 500 в банк клана", "goal": 500, "reward_exp": 70, "reward_kopecks": 150},
    {"id": "daily9", "name": "🧠 Знаток", "description": "Пройдите викторину", "goal": 1, "reward_exp": 40, "reward_kopecks": 80},
    {"id": "daily10", "name": "🛒 Покупатель", "description": "Купите предмет на рынке", "goal": 1, "reward_exp": 60, "reward_kopecks": 120},
    {"id": "daily11", "name": "🏢 Инвестор в недвижимость", "description": "Получите доход с недвижимости", "goal": 1, "reward_exp": 80, "reward_kopecks": 200}
]

WEEKLY_QUESTS = [
    {"id": "weekly1", "name": "🏆 Мастер казино", "description": "Выиграйте 15 раз в казино", "goal": 15, "reward_exp": 500, "reward_kopecks": 1000},
    {"id": "weekly2", "name": "💰 Крупный инвестор", "description": "Положите 10000 копеек на депозит", "goal": 10000, "reward_exp": 800, "reward_kopecks": 1500},
    {"id": "weekly3", "name": "🌍 Социальный деятель", "description": "Отправьте деньги 10 раз", "goal": 10, "reward_exp": 400, "reward_kopecks": 800},
    {"id": "weekly4", "name": "🎡 Любитель колеса", "description": "Покрутите колесо фортуны 10 раз", "goal": 10, "reward_exp": 600, "reward_kopecks": 1200},
    {"id": "weekly5", "name": "💼 Бизнесмен", "description": "Заработайте 50000 копеек", "goal": 50000, "reward_exp": 1000, "reward_kopecks": 2000},
    {"id": "weekly6", "name": "🏰 Строитель клана", "description": "Внесите 5000 в банк клана", "goal": 5000, "reward_exp": 700, "reward_kopecks": 1500},
    {"id": "weekly7", "name": "⭐ Звезда колеса", "description": "Выиграйте джекпот на колесе", "goal": 1, "reward_exp": 1500, "reward_kopecks": 3000},
    {"id": "weekly8", "name": "🎲 Рискованный", "description": "Сыграйте в казино 50 раз", "goal": 50, "reward_exp": 900, "reward_kopecks": 1800},
    {"id": "weekly9", "name": "💳 Депозитный магнат", "description": "Накопите 100000 на депозите", "goal": 100000, "reward_exp": 2000, "reward_kopecks": 5000},
    {"id": "weekly10", "name": "🤝 Щедрый меценат", "description": "Отправьте 10000 копеек другим игрокам", "goal": 10000, "reward_exp": 1200, "reward_kopecks": 2500},
    {"id": "weekly11", "name": "📊 Трейдер недели", "description": "Обменяйте 10000 копеек на рубии", "goal": 10000, "reward_exp": 1100, "reward_kopecks": 2200},
    {"id": "weekly12", "name": "🏆 Чемпион", "description": "Достигните 10 побед подряд", "goal": 10, "reward_exp": 1500, "reward_kopecks": 3000},
    {"id": "weekly13", "name": "🏰 Архитектор клана", "description": "Внесите 20000 в банк клана", "goal": 20000, "reward_exp": 1500, "reward_kopecks": 3000},
    {"id": "weekly14", "name": "🛒 Коммерсант", "description": "Продайте 5 предметов на рынке", "goal": 5, "reward_exp": 1000, "reward_kopecks": 2000},
    {"id": "weekly15", "name": "🏆 Победитель аукционов", "description": "Выиграйте 3 аукциона", "goal": 3, "reward_exp": 1200, "reward_kopecks": 2500},
    {"id": "weekly16", "name": "🏢 Магнат недвижимости", "description": "Получите 10000 копеек дохода с недвижимости", "goal": 10000, "reward_exp": 2000, "reward_kopecks": 5000},
    {"id": "weekly17", "name": "🏭 Лидер корпорации", "description": "Внесите 50000 в банк корпорации", "goal": 50000, "reward_exp": 2500, "reward_kopecks": 6000}
]

# Предметы для PvP
PVP_ITEMS = [
    {"id": "shield", "name": "🛡️ Щит", "effect": "block", "price": 300},
    {"id": "sword", "name": "⚔️ Меч", "effect": "attack", "price": 500},
    {"id": "potion", "name": "🧪 Зелье", "effect": "heal", "price": 200}
]

# Мини-игры для дуэлей
MINI_GAMES = [
    {"id": "reaction", "name": "Реакция", "description": "Быстрее нажми кнопку!"},
    {"id": "math", "name": "Математика", "description": "Реши пример быстрее соперника"},
    {"id": "memory", "name": "Память", "description": "Запомни последовательность"}
]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            
            defaults = {
                "kopecks": 0,
                "rubies": 0,
                "deposit": 0,
                "deposit_interest": 0,
                "username": "",
                "last_interest": datetime.now().isoformat(),
                "last_daily": "",
                "last_sell": "",
                "last_buy": "",
                "last_send": "",
                "win_count": 0,
                "daily_streak": 0,
                "achievements": {},
                "last_reset": "",
                "level": 1,
                "exp": 0,
                "daily_quests": {},
                "weekly_quests": {},
                "last_quest_update": "",
                "clan_id": "",
                "clan_role": "",
                "quiz_correct": 0,
                "items": [],
                "effects": {},
                "market_sales": 0,
                "pvp_wins": 0,
                "pvp_losses": 0,
                "clan_wars": 0,
                "spouse": "",
                "mentor": "",
                "corporation": "",
                "real_estate": {},
                "last_real_estate_income": ""
            }
            
            for user_id, user_data in data.items():
                for key, value in defaults.items():
                    if key not in user_data:
                        user_data[key] = value
            return data
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_exchange_rate():
    if not os.path.exists(EXCHANGE_RATE_FILE):
        return {"rate": 100, "last_updated": "2000-01-01"}
    with open(EXCHANGE_RATE_FILE, "r") as f:
        return json.load(f)

def save_exchange_rate(data):
    with open(EXCHANGE_RATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_wheel_history():
    if not os.path.exists(WHEEL_HISTORY_FILE):
        return {}
    with open(WHEEL_HISTORY_FILE, "r") as f:
        return json.load(f)

def save_wheel_history(data):
    with open(WHEEL_HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_clans():
    if not os.path.exists(CLANS_FILE):
        return {}
    try:
        with open(CLANS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке кланов: {e}")
        return {}

def save_clans(clans):
    try:
        with open(CLANS_FILE, "w") as f:
            json.dump(clans, f, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении кланов: {e}")

def load_quiz():
    if not os.path.exists(QUIZ_FILE):
        # Создаем базовые вопросы викторины
        quiz_data = [
            {
                "question": "Сколько будет 2+2?",
                "options": ["3", "4", "5", "6"],
                "correct": 1
            },
            {
                "question": "Столица России?",
                "options": ["Санкт-Петербург", "Москва", "Казань", "Новосибирск"],
                "correct": 1
            }
        ]
        with open(QUIZ_FILE, "w") as f:
            json.dump(quiz_data, f)
        return quiz_data
    with open(QUIZ_FILE, "r") as f:
        return json.load(f)

def load_market():
    if not os.path.exists(MARKET_FILE):
        # Создаем стартовые товары
        market_items = [
            {"id": "deposit_boost", "name": "💎 Усилитель депозита", "description": "+0.5% к годовой ставке депозита", "price": 5000, "seller_id": "system"},
            {"id": "daily_boost", "name": "📅 Усилитель бонуса", "description": "+50 к ежедневному бонусу", "price": 3000, "seller_id": "system"},
            {"id": "pvp_ticket", "name": "🎫 Билет на дуэль", "description": "Позволяет участвовать в PvP", "price": 200, "seller_id": "system"},
            {"id": "real_estate_deed", "name": "📜 Документ на недвижимость", "description": "Требуется для покупки недвижимости", "price": 50000, "seller_id": "system"},
            {"id": "corporation_token", "name": "🏢 Токен корпорации", "description": "Требуется для создания корпорации", "price": 100000, "seller_id": "system"}
        ]
        with open(MARKET_FILE, "w") as f:
            json.dump(market_items, f)
        return market_items
    try:
        with open(MARKET_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_market(market):
    with open(MARKET_FILE, "w") as f:
        json.dump(market, f, indent=2)

def load_auction():
    if not os.path.exists(AUCTION_FILE):
        return {"active": False, "items": []}
    try:
        with open(AUCTION_FILE, "r") as f:
            return json.load(f)
    except:
        return {"active": False, "items": []}

def save_auction(auction):
    with open(AUCTION_FILE, "w") as f:
        json.dump(auction, f, indent=2)

def load_items():
    if not os.path.exists(ITEMS_FILE):
        # Создаем базовый список предметов
        items = [
            {"id": "deposit_boost", "name": "💎 Усилитель депозита", "description": "+0.5% к годовой ставке депозита (постоянно)", "price": 5000, "type": "permanent"},
            {"id": "daily_boost", "name": "📅 Усилитель бонуса", "description": "+50 к ежедневному бонусу (30 дней)", "price": 3000, "type": "temporary", "duration": 30},
            {"id": "wheel_spin", "name": "🎡 Дополнительное вращение", "description": "Дополнительный спин колеса фортуны", "price": 1000, "type": "instant"},
            {"id": "exp_boost", "name": "🌟 Ускоритель опыта", "description": "+20% к получаемому опыту (7 дней)", "price": 2000, "type": "temporary", "duration": 7},
            {"id": "pvp_ticket", "name": "🎫 Билет на дуэль", "description": "Требуется для участия в PvP", "price": 200, "type": "consumable"},
            {"id": "real_estate_deed", "name": "📜 Документ на недвижимость", "description": "Требуется для покупки недвижимости", "price": 50000, "type": "consumable"},
            {"id": "corporation_token", "name": "🏢 Токен корпорации", "description": "Требуется для создания корпорации", "price": 100000, "type": "consumable"}
        ]
        with open(ITEMS_FILE, "w") as f:
            json.dump(items, f, indent=2)
        return items
    with open(ITEMS_FILE, "r") as f:
        return json.load(f)

def load_leaderboard_rewards():
    if not os.path.exists(LEADERBOARD_REWARDS_FILE):
        return {"last_rewarded": ""}
    with open(LEADERBOARD_REWARDS_FILE, "r") as f:
        return json.load(f)

def save_leaderboard_rewards(data):
    with open(LEADERBOARD_REWARDS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_corporations():
    if not os.path.exists(CORPORATIONS_FILE):
        return {}
    try:
        with open(CORPORATIONS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке корпораций: {e}")
        return {}

def save_corporations(corporations):
    try:
        with open(CORPORATIONS_FILE, "w") as f:
            json.dump(corporations, f, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении корпораций: {e}")

def load_real_estate():
    if not os.path.exists(REAL_ESTATE_FILE):
        return REAL_ESTATE_TYPES
    try:
        with open(REAL_ESTATE_FILE, "r") as f:
            return json.load(f)
    except:
        return REAL_ESTATE_TYPES

def update_exchange_rate():
    rate_data = load_exchange_rate()
    today = datetime.now().strftime("%Y-%m-%d")
    if rate_data["last_updated"] != today:
        new_rate = random.randint(MIN_EXCHANGE_RATE, MAX_EXCHANGE_RATE)
        rate_data = {"rate": new_rate, "last_updated": today}
        save_exchange_rate(rate_data)
    return rate_data["rate"]

def get_user_balance(user_id, username=""):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
        save_data(data)
    else:
        defaults = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
        for key, value in defaults.items():
            if key not in data[user_id_str]:
                data[user_id_str][key] = value
        
        if username and data[user_id_str]["username"] != username:
            data[user_id_str]["username"] = username
        
        save_data(data)
    return data[user_id_str]

def update_user_balance(user_id, kopecks=0, rubies=0, deposit_interest=0):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        get_user_balance(user_id)
        
    data[user_id_str]["kopecks"] = max(0, data[user_id_str].get("kopecks", 0) + kopecks)
    data[user_id_str]["rubies"] = max(0, data[user_id_str].get("rubies", 0) + rubies)
    data[user_id_str]["deposit_interest"] = max(0, data[user_id_str].get("deposit_interest", 0) + deposit_interest)
    save_data(data)
    return data[user_id_str]

def calculate_interest(user_id):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        return 0
    
    user_data = data[user_id_str]
    
    if "deposit" not in user_data:
        user_data["deposit"] = 0
    if "last_interest" not in user_data:
        user_data["last_interest"] = datetime.now().isoformat()
    
    try:
        last_interest = datetime.fromisoformat(user_data["last_interest"])
    except (TypeError, ValueError):
        last_interest = datetime.now()
        user_data["last_interest"] = last_interest.isoformat()
    
    hours_passed = (datetime.now() - last_interest).total_seconds() / 3600
    
    # Базовый годовой процент
    annual_rate = BASE_ANNUAL_RATE
    
    # Бонус к процентам от уровня
    level_bonus = 0
    for level in LEVELS:
        if user_data["level"] >= level["level"]:
            level_bonus = level["deposit_bonus"]
    
    # Бонус от клана
    clan_bonus = 0
    if "clan_id" in user_data and user_data["clan_id"]:
        clans = load_clans()
        clan = clans.get(user_data["clan_id"], {})
        if clan:
            clan_bonus = clan.get("bonus", 0)
    
    # Бонус от корпорации
    corporation_bonus = 0
    if "corporation" in user_data and user_data["corporation"]:
        corporations = load_corporations()
        corporation = corporations.get(user_data["corporation"], {})
        if corporation:
            corporation_bonus = corporation.get("bonus", 0)
    
    # Бонусы от предметов
    item_bonus = 0
    if "items" in user_data:
        if "deposit_boost" in user_data["items"]:
            item_bonus += 0.005  # +0.5%
    
    total_annual_rate = annual_rate + level_bonus + clan_bonus + corporation_bonus + item_bonus
    hourly_rate = total_annual_rate / (365 * 24)
    
    interest = user_data["deposit"] * hourly_rate * hours_passed
    
    # Обновляем накопленные проценты
    user_data["deposit_interest"] = user_data.get("deposit_interest", 0) + interest
    user_data["last_interest"] = datetime.now().isoformat()
    save_data(data)
    
    return interest

def calculate_minute_income(user_id):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        return 0
    
    user_data = data[user_id_str]
    deposit = user_data.get("deposit", 0)
    
    # Базовый годовой процент
    annual_rate = BASE_ANNUAL_RATE
    
    # Бонус к процентам от уровня
    level_bonus = 0
    for level in LEVELS:
        if user_data["level"] >= level["level"]:
            level_bonus = level["deposit_bonus"]
    
    # Бонус от клана
    clan_bonus = 0
    if "clan_id" in user_data and user_data["clan_id"]:
        clans = load_clans()
        clan = clans.get(user_data["clan_id"], {})
        if clan:
            clan_bonus = clan.get("bonus", 0)
    
    # Бонус от корпорации
    corporation_bonus = 0
    if "corporation" in user_data and user_data["corporation"]:
        corporations = load_corporations()
        corporation = corporations.get(user_data["corporation"], {})
        if corporation:
            corporation_bonus = corporation.get("bonus", 0)
    
    total_annual_rate = annual_rate + level_bonus + clan_bonus + corporation_bonus
    minute_rate = total_annual_rate / (365 * 24 * 60)
    
    income_per_minute = deposit * minute_rate
    
    return income_per_minute

async def add_experience(user_id, amount, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        return
    
    user_data = data[user_id_str]
    user_data["exp"] += amount
    
    # Бонус от предмета
    exp_bonus = 1.0
    if "effects" in user_data and "exp_boost" in user_data["effects"]:
        effect_end = datetime.fromisoformat(user_data["effects"]["exp_boost"])
        if datetime.now() < effect_end:
            exp_bonus = 1.2  # +20%
    
    user_data["exp"] = int(user_data["exp"] * exp_bonus)
    
    # Проверяем повышение уровня
    current_level = user_data["level"]
    next_level = None
    
    for level in LEVELS:
        if level["level"] > current_level and user_data["exp"] >= level["exp_required"]:
            next_level = level
    
    if next_level:
        user_data["level"] = next_level["level"]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 Поздравляем! Вы достигли {next_level['level']} уровня!\n"
                 f"💎 Бонус к депозиту: +{next_level['deposit_bonus']*100:.2f}%\n"
                 f"🎁 Бонус к ежедневному бонусу: +{next_level['daily_bonus']} копеек"
        )
    
    save_data(data)

async def update_quest_progress(user_id, quest_type, amount=1):
    """Обновление прогресса квестов с улучшенной логикой"""
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        return False
    
    user_data = data[user_id_str]
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # Обновляем квесты, если они устарели
    if user_data.get("last_quest_update", "") != today:
        user_data["last_quest_update"] = today
        
        # Только для ежедневных квестов
        if "daily_quests" not in user_data:
            user_data["daily_quests"] = {}
        
        # Если нет активных ежедневных квестов - создаем новые
        if not user_data["daily_quests"]:
            daily_selected = random.sample(DAILY_QUESTS, 3)
            for quest in daily_selected:
                user_data["daily_quests"][quest["id"]] = {
                    "progress": 0,
                    "completed": False,
                    "name": quest["name"],
                    "description": quest["description"],
                    "goal": quest["goal"],
                    "reward_exp": quest["reward_exp"],
                    "reward_kopecks": quest["reward_kopecks"]
                }
        
        # Обновляем еженедельные квесты в понедельник
        if now.weekday() == 0:  # Понедельник
            if "weekly_quests" not in user_data:
                user_data["weekly_quests"] = {}
            
            # Если нет активных еженедельных квестов - создаем новые
            if not user_data["weekly_quests"]:
                weekly_selected = random.sample(WEEKLY_QUESTS, 5)
                for quest in weekly_selected:
                    user_data["weekly_quests"][quest["id"]] = {
                        "progress": 0,
                        "completed": False,
                        "name": quest["name"],
                        "description": quest["description"],
                        "goal": quest["goal"],
                        "reward_exp": quest["reward_exp"],
                        "reward_kopecks": quest["reward_kopecks"]
                    }
    
    updated = False
    quests_to_check = []

    # Определяем, какие квесты нужно проверить
    if quest_type in ["earn_kopecks", "получить доход"]:
        quests_to_check = list(user_data.get("daily_quests", {}).values()) + list(user_data.get("weekly_quests", {}).values())
    else:
        if "daily_quests" in user_data:
            quests_to_check.extend(user_data["daily_quests"].values())
        if "weekly_quests" in user_data:
            quests_to_check.extend(user_data["weekly_quests"].values())

    # Обновляем прогресс квестов
    for quest in quests_to_check:
        if quest["completed"]:
            continue
            
        # Для квестов на заработок
        if quest_type == "earn_kopecks" and "заработайте" in quest["description"].lower():
            quest["progress"] = min(quest["progress"] + amount, quest["goal"])
            if quest["progress"] >= quest["goal"]:
                quest["completed"] = True
                user_data["kopecks"] += quest["reward_kopecks"]
                user_data["exp"] += quest["reward_exp"]
                updated = True
                
        # Для квестов по типам действий
        elif quest_type.lower() in quest["description"].lower():
            quest["progress"] = min(quest["progress"] + amount, quest["goal"])
            if quest["progress"] >= quest["goal"]:
                quest["completed"] = True
                user_data["kopecks"] += quest["reward_kopecks"]
                user_data["exp"] += quest["reward_exp"]
                updated = True
    
    if updated:
        save_data(data)
    
    return updated

async def check_achievements(user_id, achievement_key, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data:
        return
    
    user_data = data[user_id_str]
    
    if "achievements" not in user_data:
        user_data["achievements"] = {}
    
    if user_data["achievements"].get(achievement_key, False):
        return
    
    achievement_granted = False
    
    if achievement_key == "first_win" and user_data["win_count"] >= 1:
        achievement_granted = True
    
    elif achievement_key == "ten_wins" and user_data["win_count"] >= 10:
        achievement_granted = True
    
    elif achievement_key == "rich" and (user_data["kopecks"] + user_data["rubies"] * 100 + user_data["deposit"]) >= 100000:
        achievement_granted = True
    
    elif achievement_key == "daily_fan" and user_data["daily_streak"] >= 30:
        achievement_granted = True
    
    elif achievement_key == "gambler" and "gambler" not in user_data["achievements"]:
        # Проверяется при выигрыше allin
        achievement_granted = True
        
    elif achievement_key == "deposit_king" and user_data["deposit"] >= 1000000:
        achievement_granted = True
        
    elif achievement_key == "wheel_master" and "wheel_master" not in user_data["achievements"]:
        # Проверяется при выигрыше джекпота
        achievement_granted = True
        
    elif achievement_key == "clan_leader":
        if user_data.get("clan_role") == "leader":
            clans = load_clans()
            clan = clans.get(user_data["clan_id"], {})
            if len(clan.get("members", {})) >= 10:
                achievement_granted = True
    
    elif achievement_key == "quiz_master" and user_data.get("quiz_correct", 0) >= 50:
        achievement_granted = True
        
    elif achievement_key == "market_trader" and user_data.get("market_sales", 0) >= 10:
        achievement_granted = True
    
    elif achievement_key == "item_collector":
        unique_items = len(set(user_data.get("items", [])))
        if unique_items >= 10:
            achievement_granted = True
            
    elif achievement_key == "clan_champion":
        clans = load_clans()
        clan_id = user_data.get("clan_id")
        if clan_id:
            clan = clans.get(clan_id, {})
            if clan.get("total_deposited", 0) >= 50000:
                achievement_granted = True
                
    elif achievement_key == "pvp_champion" and user_data.get("pvp_wins", 0) >= 10:
        achievement_granted = True
        
    elif achievement_key == "clan_warrior" and user_data.get("clan_wars", 0) >= 5:
        achievement_granted = True
    
    elif achievement_key == "real_estate_tycoon":
        if "real_estate" in user_data and len(user_data["real_estate"]) >= 5:
            achievement_granted = True
            
    elif achievement_key == "corporation_leader":
        if user_data.get("clan_role") == "leader" and user_data.get("corporation"):
            corporations = load_corporations()
            corp = corporations.get(user_data["corporation"], {})
            if corp and len(corp.get("clans", [])) >= 3:
                achievement_granted = True
    
    if achievement_granted:
        achievement = ACHIEVEMENTS[achievement_key]
        user_data["kopecks"] += achievement["reward"]
        user_data["achievements"][achievement_key] = True
        save_data(data)
        
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🏆 Получено достижение: {achievement['name']}!\n"
                 f"📝 {achievement['description']}\n"
                 f"🎁 Награда: {achievement['reward']} копеек"
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    get_user_balance(user.id, username)
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n\n"
        "Добро пожаловать в Казино Бот!\n\n"
        "Доступные команды:\n"
        "/balance - твой баланс\n"
        "/daily - ежедневный бонус\n"
        "/exchange - обмен копеек на рубии (1 раз в день)\n"
        "/sell - продать рубии обратно (1 раз в день)\n"
        "/casino [сумма] - сыграть в казино\n"
        "/send [сумма] [username] - отправить деньги\n"
        "/wheel [ставка] - колесо фортуны\n"
        "/leaderboard - топ игроков\n"
        "/deposit [сумма] - положить на депозит\n"
        "/withdraw [сумма] - снять с депозита\n"
        "/withdraw_interest - снять накопленные проценты\n"
        "/allin - поставить ВСЁ (3x при выигрыше!)\n"
        "/reset - обнулить прогресс (Получите стартовые 100 копеек!!!)\n"
        "/guess - угадай число (1-3)\n"
        "/achievements - ваши достижения\n"
        "/quests - ваши квесты\n"
        "/profile - ваш профиль\n"
        "/clan - управление кланами\n"
        "/clans - список всех кланов\n"
        "/quiz - викторина\n"
        "/market - рынок предметов\n"
        "/buy [ID] - купить предмет\n"
        "/inventory - ваш инвентарь\n"
        "/duel - PvP дуэль\n"
        "/clanwar - война кланов\n"
        "/marry - заключить брак\n"
        "/mentor - система наставничества\n"
        "/corporation - корпорации кланов\n"
        "/realestate - покупка недвижимости\n"
        "/myproperties - ваша недвижимость\n"
        "/upgrade_property - улучшить недвижимость"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    balance_data = get_user_balance(user.id, username)
    exchange_rate = update_exchange_rate()
    
    # Рассчитываем проценты
    interest = calculate_interest(user.id)
    
    # Рассчитываем доход в минуту
    income_per_minute = calculate_minute_income(user.id)
    
    response = (
        f"💰 Твой баланс:\n"
        f"Копейки: {balance_data.get('kopecks', 0):.2f}\n"
        f"Рубии: {balance_data.get('rubies', 0):.2f}\n"
        f"Депозит: {balance_data.get('deposit', 0):.2f} коп.\n"
        f"Накопленные проценты: {balance_data.get('deposit_interest', 0):.2f} коп.\n"
        f"📊 Текущий курс: 1 Рубий = {exchange_rate} копеек\n"
        f"📈 Пассивный доход: {income_per_minute:.4f} коп/мин\n"
        f"🔥 Серия побед: {balance_data.get('win_count', 0)}\n"
        f"⭐ Уровень: {balance_data.get('level', 1)}"
    )
    
    # Показываем прогресс до следующего уровня
    current_level = balance_data.get("level", 1)
    current_exp = balance_data.get("exp", 0)
    
    if current_level < len(LEVELS):
        next_level_exp = LEVELS[current_level]["exp_required"]
        response += f"\n🔋 Опыт: {current_exp}/{next_level_exp}"
    else:
        response += "\n🎖️ Вы достигли максимального уровня!"
    
    if "clan_id" in balance_data and balance_data["clan_id"]:
        clans = load_clans()
        clan_name = clans.get(balance_data["clan_id"], {}).get("name", "Неизвестно")
        response += f"\n\n🏰 Клан: {clan_name} ({balance_data.get('clan_role', 'участник')})"
    
    if "corporation" in balance_data and balance_data["corporation"]:
        corporations = load_corporations()
        corp_name = corporations.get(balance_data["corporation"], {}).get("name", "Неизвестно")
        response += f"\n🏢 Корпорация: {corp_name}"
    
    await update.message.reply_text(response)

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    data = load_data()
    user_id_str = str(user.id)
    
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    user_data = data[user_id_str]
    
    if "achievements" not in user_data:
        user_data["achievements"] = {}
    if "daily_streak" not in user_data:
        user_data["daily_streak"] = 0
        
    today = datetime.now().strftime("%Y-%m-%d")
    last_claimed = user_data.get("last_daily", "")
    
    if last_claimed == today:
        await update.message.reply_text("Ты уже получал ежедневный бонус сегодня!")
        return
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if last_claimed == yesterday:
        user_data["daily_streak"] = user_data.get("daily_streak", 0) + 1
    else:
        user_data["daily_streak"] = 1
    
    # Бонус к ежедневному бонусу от уровня
    daily_bonus = DAILY_BONUS
    for level in LEVELS:
        if user_data["level"] >= level["level"]:
            daily_bonus += level["daily_bonus"]
    
    # Бонус от предмета
    if "effects" in user_data and "daily_boost" in user_data["effects"]:
        effect_end = datetime.fromisoformat(user_data["effects"]["daily_boost"])
        if datetime.now() < effect_end:
            daily_bonus += 50
    
    user_data["kopecks"] += daily_bonus
    user_data["last_daily"] = today
    
    if username and user_data.get("username") != username:
        user_data["username"] = username
    
    # Добавляем опыт за получение бонуса
    await add_experience(user.id, 10, context)
    
    # Начисляем доход с недвижимости
    real_estate_income = 0
    if "real_estate" in user_data and user_data["real_estate"]:
        real_estate_types = load_real_estate()
        for property_id, level in user_data["real_estate"].items():
            property_info = next((p for p in real_estate_types if p["id"] == property_id), None)
            if property_info:
                real_estate_income += property_info["income"] * level
        
        if real_estate_income > 0:
            user_data["kopecks"] += real_estate_income
            user_data["last_real_estate_income"] = today
            await update_quest_progress(user.id, "инвестор в недвижимость")
            await update_quest_progress(user.id, "earn_kopecks", real_estate_income)
    
    save_data(data)
    
    # Обновляем квест "Богач"
    await update_quest_progress(user.id, "earn_kopecks", daily_bonus)
    
    await check_achievements(user.id, "daily_fan", context)
    
    response = (
        f"📅 Ты получил ежедневный бонус: {daily_bonus} копеек!\n"
        f"📈 Текущая серия: {user_data['daily_streak']} дней\n"
        f"Твой баланс: {user_data['kopecks']:.2f} копеек"
    )
    
    if real_estate_income > 0:
        response += f"\n🏢 Доход с недвижимости: {real_estate_income} копеек"
    
    # Проверка на карту сокровищ
    if "items" in user_data and "treasure_map" in user_data["items"]:
        if random.random() < 0.15:  # 15% шанс найти сокровище
            treasure = random.randint(100, 1000)
            user_data["kopecks"] += treasure
            save_data(data)
            response += f"\n\n🗺️ С картой сокровищ ты нашел {treasure} копеек!"
    
    # Проверяем квесты
    await update_quest_progress(user.id, "ежедневный бонус")
    
    await update.message.reply_text(response)

async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    data = load_data()
    user_id_str = str(user.id)
    
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    user_data = data[user_id_str]
    
    # Проверка ограничения (1 раз в день)
    today = datetime.now().strftime("%Y-%m-%d")
    if user_data.get("last_buy", "") == today:
        await update.message.reply_text("❌ Покупать рубии можно только 1 раз в день!")
        return
    
    exchange_rate = update_exchange_rate()
    
    # Бонус от предмета
    if "effects" in user_data and "ruby_boost" in user_data["effects"]:
        effect_end = datetime.fromisoformat(user_data["effects"]["ruby_boost"])
        if datetime.now() < effect_end:
            exchange_rate = int(exchange_rate * 1.1)  # +10%
    
    # Бонус от философского камня
    if "items" in user_data and "philosopher_stone" in user_data["items"]:
        exchange_rate = int(exchange_rate * 1.15)  # +15%

    if not context.args:
        await update.message.reply_text(
            f"Текущий курс: 1 Рубий = {exchange_rate} копеек\n\n"
            "Использование: /exchange [количество] - обменять копейки на рубии\n"
            f"Твой баланс: {user_data['kopecks']:.2f} копеек"
        )
        return
    
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("Пожалуйста, введи положительное число!")
            return
        
        total_cost = amount * exchange_rate
        if user_data['kopecks'] < total_cost:
            await update.message.reply_text(
                f"Недостаточно копеек! Нужно {total_cost:.2f}, у тебя {user_data['kopecks']:.2f}"
            )
            return
        
        user_data["kopecks"] -= total_cost
        user_data["rubies"] += amount
        user_data["last_buy"] = today
        
        # Обновляем квесты
        await update_quest_progress(user.id, "обменяйте")
        
        save_data(data)
        
        await update.message.reply_text(
            f"✅ Обмен успешен!\n"
            f"Ты получил {amount} рубиев за {total_cost:.2f} копеек\n\n"
            f"Твой баланс:\nКопейки: {user_data['kopecks']:.2f}\nРубии: {user_data['rubies']:.2f}"
        )
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число!")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    data = load_data()
    user_id_str = str(user.id)
    
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    user_data = data[user_id_str]
    
    # Гарантируем наличие всех полей
    if "achievements" not in user_data:
        user_data["achievements"] = {}
        
    today = datetime.now().strftime("%Y-%m-%d")
    if user_data.get("last_sell", "") == today:
        await update.message.reply_text("❌ Продавать рубии можно только 1 раз в день!")
        return

    if not context.args:
        await update.message.reply_text("Использование: /sell [количество]")
        return

    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("Количество должно быть положительным!")
            return
        if user_data["rubies"] < amount:
            await update.message.reply_text(f"Недостаточно рубиев! У вас: {user_data['rubies']:.2f}")
            return
        
        exchange_rate = update_exchange_rate()
        kopecks_received = amount * exchange_rate
        
        user_data["kopecks"] += kopecks_received
        user_data["rubies"] -= amount
        user_data["last_sell"] = today
        
        if username and user_data.get("username") != username:
            user_data["username"] = username
        
        save_data(data)
        
        # Обновляем квест "Богач"
        await update_quest_progress(user.id, "earn_kopecks", kopecks_received)
        
        # Обновляем квесты
        await update_quest_progress(user.id, "продайте")
        
        await update.message.reply_text(
            f"✅ Продано {amount} рубиев за {kopecks_received:.2f} копеек!\n"
            f"Курс: 1 рубий = {exchange_rate} копеек\n"
            f"🔒 Следующая продажа доступна завтра"
        )
    except ValueError:
        await update.message.reply_text("Некорректное количество!")

async def casino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    balance_data = get_user_balance(user.id, username)
    
    if not context.args:
        await update.message.reply_text(
            "Использование: /casino [сумма] - поставить сумму в казино\n"
            "Шанс выигрыша 50%. При победе сумма удваивается, при проигрыше теряется.\n"
            f"Твой баланс: {balance_data['kopecks']:.2f} копеек"
        )
        return
    
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("Пожалуйста, введи положительное число!")
            return
        if balance_data['kopecks'] < amount:
            await update.message.reply_text(
                f"Недостаточно копеек! У тебя {balance_data['kopecks']:.2f}"
            )
            return
        
        # Добавляем опыт за игру
        exp_bonus = 1.0
        if "effects" in balance_data and "exp_boost" in balance_data["effects"]:
            effect_end = datetime.fromisoformat(balance_data["effects"]["exp_boost"])
            if datetime.now() < effect_end:
                exp_bonus = 1.2  # +20%
                
        await add_experience(user.id, int(amount // 10 * exp_bonus), context)
        # Обновляем прогресс квестов
        await update_quest_progress(user.id, "казино")
        
        # Бонус от амулета удачи
        win_chance = 0.5
        if "effects" in balance_data and "lucky_charm" in balance_data["effects"]:
            effect_end = datetime.fromisoformat(balance_data["effects"]["lucky_charm"])
            if datetime.now() < effect_end:
                win_chance = 0.55  # +5% шанс
        
        if random.random() < win_chance:
            new_balance = update_user_balance(user.id, kopecks=amount)
            data = load_data()
            user_id_str = str(user.id)
            
            data[user_id_str]["win_count"] = data[user_id_str].get("win_count", 0) + 1
            save_data(data)
            
            # Обновляем квест "Богач"
            await update_quest_progress(user.id, "earn_kopecks", amount)
            
            await check_achievements(user.id, "first_win", context)
            await check_achievements(user.id, "ten_wins", context)
            
            await update.message.reply_text(
                f"🎉 Поздравляем! Ты выиграл {amount} копеек!\nТвой баланс: {new_balance['kopecks']:.2f} копеек"
            )
        else:
            new_balance = update_user_balance(user.id, kopecks=-amount)
            data = load_data()
            user_id_str = str(user.id)
            
            data[user_id_str]["win_count"] = 0
            save_data(data)
            
            await update.message.reply_text(
                f"😢 К сожалению, ты проиграл {amount} копеек.\nТвой баланс: {new_balance['kopecks']:.2f} копеек"
            )
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число!")

async def send_money(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    sender_username = user.username or user.first_name
    data = load_data()
    user_id_str = str(user.id)
    
    # Инициализация, если нужно
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": sender_username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    user_data = data[user_id_str]
    
    # Проверяем ограничение отправки (1 раз в день)
    today = datetime.now().strftime("%Y-%m-%d")
    if user_data.get("last_send", "") == today:
        await update.message.reply_text("❌ Отправлять деньги можно только 1 раз в день!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Использование: /send [сумма] [username] - отправить копейки другому пользователю\n"
            f"Твой баланс: {user_data['kopecks']:.2f} копеек"
        )
        return
    
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("Пожалуйста, введи положительное число!")
            return
        if user_data['kopecks'] < amount:
            await update.message.reply_text(
                f"Недостаточно копеек! У тебя {user_data['kopecks']:.2f}"
            )
            return
        
        recipient_username = context.args[1].lstrip('@')
        recipient_id = None
        
        for uid, ud in data.items():
            if "username" in ud and ud["username"].lower() == recipient_username.lower():
                recipient_id = uid
                break
        
        if not recipient_id:
            await update.message.reply_text("Пользователь с таким именем не найден!")
            return
        
        if recipient_id == user_id_str:
            await update.message.reply_text("Нельзя отправить деньги самому себе!")
            return
        
        # Обновляем балансы
        user_data["kopecks"] -= amount
        if recipient_id not in data:
            data[recipient_id] = {
                "kopecks": amount,
                "rubies": 0,
                "deposit": 0,
                "deposit_interest": 0,
                "username": recipient_username,
                "last_interest": datetime.now().isoformat(),
                "last_daily": "",
                "last_sell": "",
                "last_buy": "",
                "last_send": "",
                "win_count": 0,
                "daily_streak": 0,
                "achievements": {},
                "last_reset": "",
                "level": 1,
                "exp": 0,
                "daily_quests": {},
                "weekly_quests": {},
                "last_quest_update": "",
                "clan_id": "",
                "clan_role": "",
                "quiz_correct": 0,
                "items": [],
                "effects": {},
                "market_sales": 0,
                "pvp_wins": 0,
                "pvp_losses": 0,
                "clan_wars": 0,
                "spouse": "",
                "mentor": "",
                "corporation": "",
                "real_estate": {},
                "last_real_estate_income": ""
            }
        else:
            data[recipient_id]["kopecks"] += amount
        
        # Обновляем время последней отправки
        user_data["last_send"] = today
        
        save_data(data)
        
        # Обновляем квесты
        await update_quest_progress(user.id, "отправьте")
        
        await update.message.reply_text(
            f"✅ Ты отправил {amount} копеек пользователю @{recipient_username}\n"
            f"Твой баланс: {user_data['kopecks']:.2f} копеек"
        )
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи корректную сумму!")

async def wheel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    balance_data = get_user_balance(user.id, username)
    
    # Проверка ограничения (1 раз в 2 часа)
    wheel_history = load_wheel_history()
    user_id_str = str(user.id)
    last_spin = wheel_history.get(user_id_str, "")
    
    if last_spin:
        try:
            last_spin_time = datetime.fromisoformat(last_spin)
        except (TypeError, ValueError):
            last_spin_time = datetime.now() - timedelta(hours=3)  # Сброс, если некорректное время
        
        if datetime.now() - last_spin_time < timedelta(hours=2):
            next_spin = last_spin_time + timedelta(hours=2)
            await update.message.reply_text(
                f"❌ Колесо фортуны можно крутить только раз в 2 часа!\n"
                f"Следующая попытка: {next_spin.strftime('%H:%M:%S')}"
            )
            return
    
    if not context.args:
        await update.message.reply_text(
            "🎡 Колесо фортуны:\n"
            "Использование: /wheel [ставка]\n"
            f"Твой баланс: {balance_data['kopecks']:.2f} копеек\n"
            "Призы: 0x, 0.5x, 1x, 2x, 5x!"
        )
        return
    
    try:
        bet = int(context.args[0])
        if bet <= 0:
            await update.message.reply_text("Ставка должна быть положительной!")
            return
        if balance_data["kopecks"] < bet:
            await update.message.reply_text(f"Недостаточно копеек! Ваш баланс: {balance_data['kopecks']:.2f}")
            return
        
        # Добавляем опыт за ставку
        exp_bonus = 1.0
        if "effects" in balance_data and "exp_boost" in balance_data["effects"]:
            effect_end = datetime.fromisoformat(balance_data["effects"]["exp_boost"])
            if datetime.now() < effect_end:
                exp_bonus = 1.2  # +20%
                
        await add_experience(user.id, int(bet // 10 * exp_bonus), context)
        
        # Выбираем случайный приз
        prize = random.choice(WHEEL_PRIZES)
        win = int(bet * prize["multiplier"])
        
        new_balance = update_user_balance(user.id, kopecks=win - bet)
        
        # Обновляем историю
        wheel_history[user_id_str] = datetime.now().isoformat()
        save_wheel_history(wheel_history)
        
        # Обновляем счетчик побед при выигрыше
        if win > bet:
            data = load_data()
            user_id_str = str(user.id)
            
            data[user_id_str]["win_count"] = data[user_id_str].get("win_count", 0) + 1
            save_data(data)
            
            # Обновляем квест "Богач"
            await update_quest_progress(user.id, "earn_kopecks", win)
            
            # Проверяем достижения
            await check_achievements(user.id, "first_win", context)
            await check_achievements(user.id, "ten_wins", context)
            
            # Проверяем джекпот
            if prize["multiplier"] == 5.0:
                await check_achievements(user.id, "wheel_master", context)
        elif win < bet:
            data = load_data()
            user_id_str = str(user.id)
            
            data[user_id_str]["win_count"] = 0
            save_data(data)
        
        # Обновляем прогресс квестов
        await update_quest_progress(user.id, "колесо")
        
        await update.message.reply_text(
            f"🎡 Колесо фортуны:\n{prize['text']}\n"
            f"Выигрыш: {'-' if win == 0 else '+'}{abs(win)} коп.\n"
            f"Новый баланс: {new_balance['kopecks']:.2f} коп."
        )
    except ValueError:
        await update.message.reply_text("Некорректная ставка!")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = load_data()
    
    # Топ по копейкам
    kop_top = sorted(
        [
            (ud.get("username", "Unknown"), 
             ud.get("kopecks", 0) + 
             ud.get("deposit", 0) + 
             ud.get("deposit_interest", 0) + 
             ud.get("rubies", 0) * 100)
            for ud in data.values()
            if "username" in ud
        ],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # Топ по рубиям
    rub_top = sorted(
        [(ud.get("username", "Unknown"), ud.get("rubies", 0)) for ud in data.values()
         if "username" in ud and "rubies" in ud],
        key=lambda x: x[1],
        reverse=True
    )[:10]

    response = "🏆 ТОП ПО ОБЩЕМУ БАЛАНСУ:\n" + "\n".join(
        [f"{i+1}. @{user[0]} - {user[1]:.2f} коп." for i, user in enumerate(kop_top)]
    )
    
    response += "\n\n💎 ТОП ПО РУБИЯМ:\n" + "\n".join(
        [f"{i+1}. @{user[0]} - {user[1]:.2f} руб." for i, user in enumerate(rub_top)]
    )
    
    await update.message.reply_text(response)

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    balance_data = get_user_balance(user.id, username)
    
    if not context.args:
        await update.message.reply_text(
            "🏦 Депозит под 25% годовых\n"
            "Использование: /deposit [сумма]\n"
            f"Доступно: {balance_data['kopecks']:.2f} копеек\n"
            f"На депозите: {balance_data.get('deposit', 0):.2f} коп."
        )
        return
    
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("Сумма должна быть положительной!")
            return
        if balance_data['kopecks'] < amount:
            await update.message.reply_text(f"Недостаточно копеек! Доступно: {balance_data['kopecks']:.2f}")
            return
        
        # Рассчитываем накопленные проценты
        calculate_interest(user.id)
        
        # Обновляем баланс
        data = load_data()
        user_id_str = str(user.id)
        data[user_id_str]["kopecks"] -= amount
        data[user_id_str]["deposit"] = data[user_id_str].get("deposit", 0) + amount
        save_data(data)
        
        # Обновляем прогресс квестов
        await update_quest_progress(user.id, "положите")
        
        # Проверяем достижения
        await check_achievements(user.id, "rich", context)
        await check_achievements(user.id, "deposit_king", context)
        
        await update.message.reply_text(
            f"✅ {amount} копеек успешно переведены на депозит!\n"
            f"Общая сумма на депозите: {data[user_id_str]['deposit']:.2f} коп."
        )
    except ValueError:
        await update.message.reply_text("Некорректная сумма!")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    balance_data = get_user_balance(user.id, username)
    
    if not context.args:
        await update.message.reply_text(
            "🏦 Снятие с депозита\n"
            "Использование: /withdraw [сумма]\n"
            f"На депозите: {balance_data.get('deposit', 0):.2f} коп."
        )
        return
    
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("Сумма должна быть положительной!")
            return
        
        deposit_amount = balance_data.get("deposit", 0)
        if deposit_amount < amount:
            await update.message.reply_text(f"Недостаточно средств на депозите! Доступно: {deposit_amount:.2f}")
            return
        
        # Рассчитываем накопленные проценты
        calculate_interest(user.id)
        
        # Обновляем баланс
        data = load_data()
        user_id_str = str(user.id)
        data[user_id_str]["kopecks"] += amount
        data[user_id_str]["deposit"] = max(0, deposit_amount - amount)
        
        save_data(data)
        
        # Проверяем достижения
        await check_achievements(user.id, "rich", context)
        
        await update.message.reply_text(
            f"✅ {amount} копеек сняты с депозита!\n"
            f"💳 Новый баланс: {data[user_id_str]['kopecks']:.2f} копеек"
        )
    except ValueError:
        await update.message.reply_text("Некорректная сумма!")

async def withdraw_interest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    balance_data = get_user_balance(user.id)
    
    # Рассчитываем проценты
    calculate_interest(user.id)
    
    interest = balance_data.get("deposit_interest", 0)
    if interest <= 0:
        await update.message.reply_text("❌ У вас нет накопленных процентов для снятия!")
        return
    
    # Снимаем проценты
    new_balance = update_user_balance(user.id, kopecks=interest, deposit_interest=-interest)
    
    # Обновляем квест "Богач"
    await update_quest_progress(user.id, "earn_kopecks", interest)
    
    await update.message.reply_text(
        f"✅ Вы сняли накопленные проценты: {interest:.2f} копеек!\n"
        f"💳 Ваш баланс: {new_balance['kopecks']:.2f} копеек"
    )

async def allin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user
        data = load_data()
        clans = load_clans()
        user_id_str = str(user.id)
        
        # Инициализация, если нужно
        if user_id_str not in data:
            data[user_id_str] = {
                "kopecks": 0,
                "rubies": 0,
                "deposit": 0,
                "deposit_interest": 0,
                "username": user.username or user.first_name,
                "last_interest": datetime.now().isoformat(),
                "last_daily": "",
                "last_sell": "",
                "last_buy": "",
                "last_send": "",
                "win_count": 0,
                "daily_streak": 0,
                "achievements": {},
                "last_reset": "",
                "level": 1,
                "exp": 0,
                "daily_quests": {},
                "weekly_quests": {},
                "last_quest_update": "",
                "clan_id": "",
                "clan_role": "",
                "quiz_correct": 0,
                "items": [],
                "effects": {},
                "market_sales": 0,
                "pvp_wins": 0,
                "pvp_losses": 0,
                "clan_wars": 0,
                "spouse": "",
                "mentor": "",
                "corporation": "",
                "real_estate": {},
                "last_real_estate_income": ""
            }
        
        user_data = data[user_id_str]
        
        # Гарантируем наличие всех полей
        if "achievements" not in user_data:
            user_data["achievements"] = {}
        
        # Рассчитываем общую сумму ставки с текущим курсом
        exchange_rate = update_exchange_rate()
        rubies_value = user_data.get("rubies", 0) * exchange_rate
        deposit_value = user_data.get("deposit", 0)
        kopecks_value = user_data.get("kopecks", 0)
        total_bet = rubies_value + deposit_value + kopecks_value
        
        if total_bet <= 0:
            await update.message.reply_text("❌ У тебя нет средств для ставки!")
            return
        
        # Сохраняем использованный курс
        context.user_data['awaiting_allin_confirmation'] = {
            'user_id': user_id_str,
            'total_bet': total_bet,
            'rubies': user_data.get("rubies", 0),
            'deposit': user_data.get("deposit", 0),
            'kopecks': user_data.get("kopecks", 0),
            'exchange_rate': exchange_rate
        }

        # Подтверждение ставки
        confirm_message = (
            f"⚠️ Ты собираешься поставить ВСЕ свои средства ({total_bet:.2f} копеек):\n"
            f"- Копейки: {kopecks_value:.2f}\n"
            f"- Рубии: {user_data.get('rubies', 0)} (в копейках: {rubies_value:.2f})\n"
            f"- Депозит: {deposit_value:.2f}\n\n"
            "Шанс 50% выиграть 3x суммы!\n"
            "Подтверждаешь? (да/нет)"
        )
        
        await update.message.reply_text(confirm_message)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    data = load_data()
    user_id_str = str(user.id)
    
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 100,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": datetime.now().isoformat(),
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    else:
        # Сохраняем достижения и серию ежедневных бонусов
        achievements = data[user_id_str].get("achievements", {})
        daily_streak = data[user_id_str].get("daily_streak", 0)
        last_daily = data[user_id_str].get("last_daily", "")
        
        data[user_id_str] = {
            "kopecks": 100,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": username,
            "last_interest": datetime.now().isoformat(),
            "last_daily": last_daily,
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": daily_streak,
            "achievements": achievements,
            "last_reset": datetime.now().isoformat(),
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    save_data(data)
    
    await update.message.reply_text(
        "🔄 Твой прогресс обнулен!\n"
        f"Ты получил стартовый капитал: 100 копеек\n"
        f"Ежедневный бонус: {'уже получен' if data[user_id_str]['last_daily'] == datetime.now().strftime('%Y-%m-%d') else 'доступен'}"
    )

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or user.first_name
    balance_data = get_user_balance(user.id, username)
    
    # Режим без ставки (бесплатная игра)
    if not context.args:
        # Генерируем случайное число
        secret_number = random.randint(1, 3)
        
        # Сохраняем загаданное число и ID пользователя
        context.user_data['free_guess'] = {
            'secret_number': secret_number,
            'user_id': user.id
        }
        
        await update.message.reply_text(
            "🎲 Бесплатная игра! Угадай число от 1 до 3\n"
            "Отправь цифру:"
        )
        return
    
    # Режим со ставкой
    if len(context.args) < 2:
        await update.message.reply_text(
            "🎲 Угадай число (1-3):\n"
            "Использование: /guess [ставка] [число]\n"
            "Угадаешь - получишь 3x ставки!\n"
            f"Твой баланс: {balance_data['kopecks']:.2f} копеек\n\n"
            "Для бесплатной игры просто отправь /guess"
        )
        return
    
    # Режим со ставкой
    try:
        bet = int(context.args[0])
        number = int(context.args[1])
        
        if bet <= 0:
            await update.message.reply_text("Ставка должна быть положительной!")
            return
        if number < 1 or number > 3:
            await update.message.reply_text("Число должно быть от 1 до 3!")
            return
        if balance_data['kopecks'] < bet:
            await update.message.reply_text(f"Недостаточно копеек! У тебя {balance_data['kopecks']:.2f}")
            return
        
        # Добавляем опыт за ставку
        exp_bonus = 1.0
        if "effects" in balance_data and "exp_boost" in balance_data["effects"]:
            effect_end = datetime.fromisoformat(balance_data["effects"]["exp_boost"])
            if datetime.now() < effect_end:
                exp_bonus = 1.2  # +20%
                
        await add_experience(user.id, int(bet // 10 * exp_bonus), context)
        
        # Генерируем случайное число
        secret_number = random.randint(1, 3)
        
        if number == secret_number:
            win_amount = bet * 3
            new_balance = update_user_balance(user.id, kopecks=win_amount - bet)
            
            # Обновляем счетчик побед
            data = load_data()
            user_id_str = str(user.id)
            data[user_id_str]["win_count"] = data[user_id_str].get("win_count", 0) + 1
            save_data(data)
            
            # Обновляем квест "Богач"
            await update_quest_progress(user.id, "earn_kopecks", win_amount)
            
            # Проверяем достижения
            await check_achievements(user.id, "first_win", context)
            await check_achievements(user.id, "ten_wins", context)
            
            await update.message.reply_text(
                f"🎯 Ты угадал! Загаданное число: {secret_number}\n"
                f"🏆 Выигрыш: {win_amount} копеек\n"
                f"💰 Новый баланс: {new_balance['kopecks']:.2f} копеек"
            )
        else:
            new_balance = update_user_balance(user.id, kopecks=-bet)
            
            # Сбрасываем счетчик побед
            data = load_data()
            user_id_str = str(user.id)
            data[user_id_str]["win_count"] = 0
            save_data(data)
            
            await update.message.reply_text(
                f"❌ Ты не угадал! Загаданное число: {secret_number}\n"
                f"💸 Потеряно: {bet} копеек\n"
                f"💰 Новый баланс: {new_balance['kopecks']:.2f} копеек"
            )
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи корректные значения!")

async def achievements(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    # Гарантируем наличие поля achievements
    if "achievements" not in user_data:
        user_data["achievements"] = {}
    
    response = "🏆 Ваши достижения:\n\n"
    
    if not user_data.get("achievements"):
        response += "У вас пока нет достижений!"
    else:
        for key, achieved in user_data["achievements"].items():
            if achieved and key in ACHIEVEMENTS:
                ach = ACHIEVEMENTS[key]
                response += f"✅ {ach['name']}\n{ach['description']}\nНаграда: {ach['reward']} копеек\n\n"
    
    response += "\n\n🔒 Неполученные достижения:\n"
    for key, ach in ACHIEVEMENTS.items():
        if not user_data["achievements"].get(key, False):
            response += f"❌ {ach['name']}\n{ach['description']}\nНаграда: {ach['reward']} копеек\n\n"
    
    await update.message.reply_text(response)

async def quests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    # Обновляем квесты
    await update_quest_progress(user.id, "проверка")
    
    response = "📜 Ваши текущие квесты:\n\n"
    response += "🎯 Ежедневные квесты (обновляются каждый день):\n"
    
    daily_completed = 0
    if "daily_quests" in user_data:
        for quest_id, quest in user_data["daily_quests"].items():
            status = "✅" if quest["completed"] else "⌛"
            response += f"{status} {quest['name']}: {quest['description']}\n"
            response += f"Прогресс: {quest['progress']}/{quest['goal']}\n"
            response += f"Награда: {quest['reward_kopecks']} коп. + {quest['reward_exp']} опыта\n\n"
            if quest["completed"]:
                daily_completed += 1
    
    response += "\n📅 Еженедельные квесты (обновляются по понедельникам):\n"
    weekly_completed = 0
    if "weekly_quests" in user_data:
        for quest_id, quest in user_data["weekly_quests"].items():
            status = "✅" if quest["completed"] else "⌛"
            response += f"{status} {quest['name']}: {quest['description']}\n"
            response += f"Прогресс: {quest['progress']}/{quest['goal']}\n"
            response += f"Награда: {quest['reward_kopecks']} коп. + {quest['reward_exp']} опыта\n\n"
            if quest["completed"]:
                weekly_completed += 1
    
    if daily_completed + weekly_completed == 0:
        response += "У вас пока нет активных квестов. Зайдите завтра!"
    
    await update.message.reply_text(response)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    current_level = user_data.get("level", 1)
    current_exp = user_data.get("exp", 0)
    
    # Находим текущий уровень и следующий
    current_level_data = next((l for l in LEVELS if l["level"] == current_level), None)
    next_level_data = next((l for l in LEVELS if l["level"] == current_level + 1), None) if current_level < len(LEVELS) else None
    
    response = f"👤 Ваш профиль:\n\n"
    response += f"⭐ Уровень: {current_level}\n"
    
    if next_level_data:
        exp_needed = next_level_data["exp_required"] - current_exp
        response += f"🔋 Опыт до следующего уровня: {exp_needed}\n"
    else:
        response += "🎖️ Вы достигли максимального уровня!\n"
    
    response += f"💎 Бонус к депозиту: +{current_level_data['deposit_bonus']*100 if current_level_data else 0}%\n"
    response += f"🎁 Бонус к ежедневному бонусу: +{current_level_data['daily_bonus'] if current_level_data else 0} копеек\n\n"
    
    response += "🏆 Достижения:\n"
    achievement_count = len(user_data.get("achievements", {}))
    response += f"Получено: {achievement_count}/{len(ACHIEVEMENTS)}\n\n"
    
    response += "📊 Статистика:\n"
    response += f"🔥 Серия побед: {user_data.get('win_count', 0)}\n"
    response += f"📅 Текущая серия ежедневных бонусов: {user_data.get('daily_streak', 0)} дней\n"
    response += f"💼 Общий баланс: {user_data.get('kopecks', 0) + user_data.get('deposit', 0) + user_data.get('deposit_interest', 0) + user_data.get('rubies', 0)*100:.2f} коп."
    
    if "clan_id" in user_data and user_data["clan_id"]:
        clans = load_clans()
        clan_name = clans.get(user_data["clan_id"], {}).get("name", "Неизвестно")
        response += f"\n\n🏰 Клан: {clan_name} ({user_data.get('clan_role', 'участник')})"
    
    await update.message.reply_text(response)

async def clan_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    data = load_data()
    clans = load_clans()
    user_id_str = str(user.id)
    
    # Инициализация пользователя, если нужно
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": user.username or user.first_name,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    user_data = data[user_id_str]
    
    if not context.args:
        await update.message.reply_text(
            "🏰 Управление кланами:\n"
            "/clan create [название] - создать клан (стоимость: 1000 копеек)\n"
            "/clan join [название] - вступить в клан\n"
            "/clan leave - покинуть клан\n"
            "/clan info - информация о вашем клане\n"
            "/clan deposit [сумма] - внести вклад в банк клана\n"
            "/clan withdraw [сумма] - снять средства из банка клана (только лидер)\n"
            "/clan disband - распустить клан (только лидер)\n"
            "/clan promote [username] - назначить заместителя (только лидер)\n"
            "/clan demote [username] - снять заместителя (только лидер)"
        )
        return
    
    command = context.args[0].lower()
    
    # Создание клана
    if command == "create" and len(context.args) > 1:
        if user_data["kopecks"] < 1000:
            await update.message.reply_text("❌ Недостаточно копеек! Создание клана стоит 1000 копеек.")
            return
        
        if user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы уже состоите в клане!")
            return
        
        clan_name = " ".join(context.args[1:])
        clan_id = f"clan_{random.randint(1000, 9999)}"
        
        # Проверяем уникальность названия
        for cid, clan in clans.items():
            if clan["name"].lower() == clan_name.lower():
                await update.message.reply_text("❌ Клан с таким названием уже существует!")
                return
        
        clans[clan_id] = {
            "name": clan_name,
            "leader": user_id_str,
            "members": {user_id_str: "leader"},
            "bank": 0,
            "level": 1,
            "bonus": 0.001,
            "total_deposited": 0,
            "created_at": datetime.now().isoformat(),
            "properties": {}
        }
        
        user_data["clan_id"] = clan_id
        user_data["clan_role"] = "leader"
        user_data["kopecks"] -= 1000
        
        save_clans(clans)
        save_data(data)
        
        await update.message.reply_text(
            f"🏰 Клан '{clan_name}' успешно создан!\n"
            f"💳 С вашего счета списано 1000 копеек.\n"
            f"Теперь вы лидер клана."
        )
        return
    
    # Вступление в клан
    elif command == "join" and len(context.args) > 1:
        if user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы уже состоите в клане!")
            return
        
        clan_name = " ".join(context.args[1:])
        clan_found = None
        
        for cid, clan in clans.items():
            if clan["name"].lower() == clan_name.lower():
                clan_found = clan
                clan_id = cid
                break
        
        if not clan_found:
            await update.message.reply_text("❌ Клан с таким названием не найден!")
            return
        
        # Проверяем, не состоит ли уже пользователь в клане
        if str(user.id) in clan_found["members"]:
            await update.message.reply_text("❌ Вы уже состоите в этом клане!")
            return
        
        # Проверяем максимальное количество участников
        clan_level = clan_found.get("level", 1)
        max_members = CLAN_LEVELS[clan_level-1]["max_members"]
        if len(clan_found["members"]) >= max_members:
            await update.message.reply_text("❌ Клан достиг максимального количества участников!")
            return
        
        clan_found["members"][str(user.id)] = "member"
        user_data["clan_id"] = clan_id
        user_data["clan_role"] = "member"
        
        save_clans(clans)
        save_data(load_data())
        
        await update.message.reply_text(
            f"🏰 Вы успешно вступили в клан '{clan_found['name']}'!\n"
            f"Теперь вы участник клана."
        )
        return
    
    # Покинуть клан
    elif command == "leave":
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        clan_id = user_data["clan_id"]
        clan = clans.get(clan_id)
        
        if not clan:
            await update.message.reply_text("❌ Ваш клан не найден!")
            return
        
        if user_data.get("clan_role") == "leader":
            # Лидер не может покинуть клан, должен распустить
            await update.message.reply_text("❌ Лидер не может покинуть клан! Используйте /clan disband для роспуска клана.")
            return
        
        del clan["members"][str(user.id)]
        user_data["clan_id"] = ""
        user_data["clan_role"] = ""
        
        save_clans(clans)
        save_data(load_data())
        
        await update.message.reply_text(f"🏰 Вы покинули клан '{clan['name']}'!")
        return
    
    # Информация о клане
    elif command == "info":
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        clan_id = user_data["clan_id"]
        clan = clans.get(clan_id)
        
        if not clan:
            await update.message.reply_text("❌ Ваш клан не найден!")
            return
        
        leader_data = get_user_balance(int(clan["leader"]))
        leader_name = leader_data.get("username", "Неизвестно")
        
        # Проверяем уровень клана
        clan_level = clan.get("level", 1)
        clan_bonus = clan.get("bonus", 0)
        clan_level_data = next((l for l in CLAN_LEVELS if l["level"] == clan_level), None)
        
        response = f"🏰 Информация о клане '{clan['name']}':\n\n"
        response += f"👑 Лидер: @{leader_name}\n"
        response += f"👥 Участников: {len(clan['members'])}/{clan_level_data['max_members'] if clan_level_data else '∞'}\n"
        response += f"💰 Банк клана: {clan['bank']} копеек\n"
        response += f"📊 Уровень клана: {clan_level} ({clan_level_data['name'] if clan_level_data else 'Неизвестно'})\n"
        response += f"💎 Бонус к депозиту: +{clan_bonus*100:.2f}%\n"
        response += f"📅 Создан: {datetime.fromisoformat(clan['created_at']).strftime('%d.%m.%Y')}\n\n"
        response += "Список участников:\n"
        
        deputies = []
        members = []
        
        for member_id, role in clan["members"].items():
            member_data = get_user_balance(int(member_id))
            member_name = member_data.get("username", "Неизвестно")
            if role == "deputy":
                deputies.append(f"- @{member_name} (заместитель)")
            elif role == "leader":
                response += f"- @{member_name} (лидер)\n"
            else:
                members.append(f"- @{member_name}")
        
        if deputies:
            response += "\nЗаместители:\n" + "\n".join(deputies) + "\n"
        
        if members:
            response += "\nУчастники:\n" + "\n".join(members)
        
        await update.message.reply_text(response)
        return
    
    # Внести вклад в банк клана
    elif command == "deposit" and len(context.args) > 1:
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        try:
            amount = int(context.args[1])
            if amount <= 0:
                await update.message.reply_text("❌ Сумма должна быть положительной!")
                return
            
            if user_data["kopecks"] < amount:
                await update.message.reply_text("❌ Недостаточно копеек на вашем счету!")
                return
            
            clan_id = user_data["clan_id"]
            clan = clans.get(clan_id)
            
            if not clan:
                await update.message.reply_text("❌ Ваш клан не найден!")
                return
            
            # Бонус от предмета
            deposit_bonus = 1.0
            if "effects" in user_data and "clan_booster" in user_data["effects"]:
                effect_end = datetime.fromisoformat(user_data["effects"]["clan_booster"])
                if datetime.now() < effect_end:
                    deposit_bonus = 1.1  # +10%
            
            actual_amount = int(amount * deposit_bonus)
            clan["bank"] += actual_amount
            clan["total_deposited"] = clan.get("total_deposited", 0) + actual_amount
            user_data["kopecks"] -= amount
            
            # Проверяем повышение уровня клана
            for level in CLAN_LEVELS:
                if level["level"] > clan["level"] and clan["total_deposited"] >= level["required_money"]:
                    clan["level"] = level["level"]
                    clan["bonus"] = level["bonus"]
                    await update.message.reply_text(
                        f"🎉 Ваш клан достиг {level['level']} уровня ({level['name']})!\n"
                        f"💎 Новый бонус к депозиту: +{level['bonus']*100:.2f}%"
                    )
            
            save_clans(clans)
            save_data(data)
            
            # Обновляем прогресс квестов
            await update_quest_progress(user.id, "внесите")
            
            await update.message.reply_text(
                f"💰 Вы внесли {amount} копеек в банк клана!\n"
                f"💎 С учетом бонуса: {actual_amount} копеек\n"
                f"💳 Новый баланс клана: {clan['bank']} копеек"
            )
            return
        except ValueError:
            await update.message.reply_text("❌ Некорректная сумма!")
            return
    
    # Снять средства из банка клана
    elif command == "withdraw" and len(context.args) > 1:
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        if user_data.get("clan_role") not in ["leader", "deputy"]:
            await update.message.reply_text("❌ Только лидер или заместитель могут снимать средства!")
            return
        
        try:
            amount = int(context.args[1])
            if amount <= 0:
                await update.message.reply_text("❌ Сумма должна быть положительной!")
                return
            
            clan_id = user_data["clan_id"]
            clan = clans.get(clan_id)
            
            if not clan:
                await update.message.reply_text("❌ Ваш клан не найден!")
                return
            
            if clan["bank"] < amount:
                await update.message.reply_text(f"❌ Недостаточно средств в банке клана! Доступно: {clan['bank']} копеек")
                return
            
            clan["bank"] -= amount
            user_data["kopecks"] += amount
            
            save_clans(clans)
            save_data(data)
            
            await update.message.reply_text(
                f"💰 Вы сняли {amount} копеек из банка клана!\n"
                f"💳 Новый баланс клана: {clan['bank']} копеек"
            )
            return
        except ValueError:
            await update.message.reply_text("❌ Некорректная сумма!")
            return
    
    # Роспуск клана
    elif command == "disband":
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        if user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может распустить клан!")
            return
        
        clan_id = user_data["clan_id"]
        clan = clans.get(clan_id)
        
        if not clan:
            await update.message.reply_text("❌ Ваш клан не найден!")
            return
        
        # Возвращаем средства из банка участникам пропорционально
        total_members = len(clan["members"])
        if total_members > 0 and clan["bank"] > 0:
            share = clan["bank"] // total_members
            data = load_data()
            
            for member_id in clan["members"].keys():
                if member_id in data:
                    data[member_id]["kopecks"] += share
            
            save_data(data)
        
        # Удаляем клан
        del clans[clan_id]
        
        # Обнуляем информацию о клане у участников
        data = load_data()
        for user_id, ud in data.items():
            if ud.get("clan_id") == clan_id:
                ud["clan_id"] = ""
                ud["clan_role"] = ""
        
        save_data(data)
        save_clans(clans)
        
        await update.message.reply_text(f"🏰 Клан '{clan['name']}' распущен!")
        return
    
    # Назначить заместителя
    elif command == "promote" and len(context.args) > 1:
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        if user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может назначать заместителей!")
            return
        
        target_username = context.args[1].lstrip('@')
        clan_id = user_data["clan_id"]
        clan = clans.get(clan_id)
        
        if not clan:
            await update.message.reply_text("❌ Ваш клан не найден!")
            return
        
        # Находим пользователя
        target_id = None
        for member_id, role in clan["members"].items():
            member_data = get_user_balance(int(member_id))
            if member_data.get("username", "").lower() == target_username.lower():
                target_id = member_id
                break
        
        if not target_id:
            await update.message.reply_text("❌ Пользователь не найден в вашем клане!")
            return
        
        if clan["members"][target_id] == "deputy":
            await update.message.reply_text("❌ Этот пользователь уже является заместителем!")
            return
        
        if clan["members"][target_id] == "leader":
            await update.message.reply_text("❌ Нельзя изменить роль лидера!")
            return
        
        # Проверяем количество заместителей (максимум 3)
        deputy_count = sum(1 for role in clan["members"].values() if role == "deputy")
        if deputy_count >= 3:
            await update.message.reply_text("❌ Достигнуто максимальное количество заместителей (3)!")
            return
        
        clan["members"][target_id] = "deputy"
        save_clans(clans)
        
        # Обновляем роль в данных пользователя
        data = load_data()
        if target_id in data:
            data[target_id]["clan_role"] = "deputy"
            save_data(data)
        
        await update.message.reply_text(f"✅ Пользователь @{target_username} назначен заместителем клана!")
        return
    
    # Снять заместителя
    elif command == "demote" and len(context.args) > 1:
        if not user_data.get("clan_id"):
            await update.message.reply_text("❌ Вы не состоите в клане!")
            return
        
        if user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может снимать заместителей!")
            return
        
        target_username = context.args[1].lstrip('@')
        clan_id = user_data["clan_id"]
        clan = clans.get(clan_id)
        
        if not clan:
            await update.message.reply_text("❌ Ваш клан не найден!")
            return
        
        # Находим пользователя
        target_id = None
        for member_id, role in clan["members"].items():
            member_data = get_user_balance(int(member_id))
            if member_data.get("username", "").lower() == target_username.lower():
                target_id = member_id
                break
        
        if not target_id:
            await update.message.reply_text("❌ Пользователь не найден в вашем клане!")
            return
        
        if clan["members"][target_id] != "deputy":
            await update.message.reply_text("❌ Этот пользователь не является заместителем!")
            return
        
        clan["members"][target_id] = "member"
        save_clans(clans)
        
        # Обновляем роль в данных пользователя
        data = load_data()
        if target_id in data:
            data[target_id]["clan_role"] = "member"
            save_data(data)
        
        await update.message.reply_text(f"✅ Пользователь @{target_username} снят с должности заместителя!")
        return
    
    await update.message.reply_text("❌ Неизвестная команда для клана!")

async def clans_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Список всех кланов"""
    clans = load_clans()
    
    if not clans:
        await update.message.reply_text("🏰 На данный момент нет созданных кланов.")
        return
    
    response = "🏰 Список всех кланов:\n\n"
    for clan_id, clan in clans.items():
        leader_data = get_user_balance(int(clan["leader"]))
        leader_name = leader_data.get("username", "Неизвестно")
        clan_level = clan.get("level", 1)
        clan_level_data = next((l for l in CLAN_LEVELS if l["level"] == clan_level), None)
        
        response += (
            f"🏷️ Название: {clan['name']}\n"
            f"👑 Лидер: @{leader_name}\n"
            f"👥 Участников: {len(clan['members'])}/{clan_level_data['max_members'] if clan_level_data else '∞'}\n"
            f"💰 Банк: {clan['bank']} копеек\n"
            f"📊 Уровень: {clan_level} ({clan_level_data['name'] if clan_level_data else 'Неизвестно'})\n"
            f"💎 Бонус: +{clan.get('bonus', 0)*100:.2f}%\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
        )
    
    response += "\nДля вступления в клан используйте /clan join [название]"
    await update.message.reply_text(response)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск викторины"""
    user = update.effective_user
    data = load_data()
    user_id_str = str(user.id)
    
    if user_id_str not in data:
        get_user_balance(user.id)
    
    user_data = data[user_id_str]
    
    # Проверяем, когда последний раз играли в викторину
    last_quiz = user_data.get("last_quiz", "")
    now = datetime.now()
    
    if last_quiz:
        last_quiz_time = datetime.fromisoformat(last_quiz)
        if (now - last_quiz_time) < timedelta(hours=1):
            next_quiz = last_quiz_time + timedelta(hours=1)
            await update.message.reply_text(
                f"⏳ Следующая викторина будет доступна в {next_quiz.strftime('%H:%M:%S')}"
            )
            return
    
    # Загружаем вопросы
    quiz_data = load_quiz()
    if not quiz_data:
        await update.message.reply_text("❌ Вопросы викторины временно недоступны")
        return
    
    # Выбираем случайный вопрос
    question = random.choice(quiz_data)
    options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question['options'])])
    
    # Сохраняем состояние викторины
    context.user_data['quiz'] = {
        'question': question,
        'start_time': now.isoformat(),
        'user_id': user.id
    }
    
    await update.message.reply_text(
        f"🧠 Викторина!\n\n{question['question']}\n\n{options}\n\n"
        "Отправь номер правильного ответа (1-4):"
    )

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа на викторину"""
    user = update.effective_user
    text = update.message.text.strip()
    
    if 'quiz' not in context.user_data:
        return
    
    quiz_data = context.user_data['quiz']
    if quiz_data['user_id'] != user.id:
        return
    
    try:
        answer = int(text)
        if 1 <= answer <= 4:
            question = quiz_data['question']
            if answer - 1 == question['correct']:
                # Правильный ответ
                reward = 50
                update_user_balance(user.id, kopecks=reward)
                
                # Обновляем статистику
                data = load_data()
                user_id_str = str(user.id)
                if "quiz_correct" not in data[user_id_str]:
                    data[user_id_str]["quiz_correct"] = 0
                data[user_id_str]["quiz_correct"] += 1
                data[user_id_str]["last_quiz"] = datetime.now().isoformat()
                save_data(data)
                
                # Обновляем квест "Богач"
                await update_quest_progress(user.id, "earn_kopecks", reward)
                
                # Проверяем достижения
                await check_achievements(user.id, "quiz_master", context)
                
                await update.message.reply_text(
                    f"✅ Правильно! Ты получаешь {reward} копеек!\n"
                    f"💡 Правильный ответ: {question['options'][question['correct']]}"
                )
            else:
                # Неправильный ответ
                correct_answer = question['options'][question['correct']]
                await update.message.reply_text(
                    f"❌ Неверно! Правильный ответ: {correct_answer}\n"
                    "Попробуй еще раз через час!"
                )
        else:
            await update.message.reply_text("Пожалуйста, введи число от 1 до 4")
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число от 1 до 4")
    finally:
        # Удаляем состояние викторины
        if 'quiz' in context.user_data:
            del context.user_data['quiz']

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просмотр рынка с исправлениями"""
    market_data = load_market()
    
    if not market_data:
        await update.message.reply_text("🛒 На рынке пока нет товаров!")
        return
    
    response = "🛒 Рынок предметов:\n\n"
    for i, item in enumerate(market_data, 1):
        # Обработка системных предметов
        if item['seller_id'] == 'system':
            seller_name = "Система"
        else:
            try:
                seller_id = int(item['seller_id'])
                seller_data = get_user_balance(seller_id)
                seller_name = seller_data.get('username', 'Неизвестно')
            except (ValueError, TypeError):
                seller_name = "Неизвестно"
        
        response += (
            f"{i}. {item['name']}\n"
            f"📝 {item['description']}\n"
            f"💰 Цена: {item['price']} копеек\n"
            f"👤 Продавец: {seller_name}\n"
            f"🆔 ID: {item['id']}\n\n"
        )
    
    response += "\nДля покупки используй /buy [ID предмета]"
    await update.message.reply_text(response)

async def sell_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Продажа предмета на рынке"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    items = load_items()
    
    if not context.args:
        item_list = "\n".join([f"{item['id']}: {item['name']} ({item['price']} коп.)" for item in items])
        await update.message.reply_text(
            "📦 Продажа предмета на рынке:\n"
            "Использование: /sell_item [ID предмета] [цена]\n\n"
            "Доступные предметы:\n" + item_list
        )
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Необходимо указать ID предмета и цену!")
        return
    
    item_id = context.args[0].lower()
    try:
        price = int(context.args[1])
        if price <= 0:
            await update.message.reply_text("❌ Цена должна быть положительной!")
            return
    except ValueError:
        await update.message.reply_text("❌ Некорректная цена!")
        return
    
    # Проверяем существование предмета
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        await update.message.reply_text("❌ Такого предмета не существует!")
        return
    
    # Проверяем, есть ли предмет у пользователя
    if "items" not in user_data or item_id not in user_data["items"]:
        await update.message.reply_text("❌ У вас нет этого предмета!")
        return
    
    # Выставляем на рынок
    market_data = load_market()
    new_item = {
        "id": f"item_{random.randint(1000, 9999)}",
        "item_id": item_id,
        "name": item['name'],
        "description": item['description'],
        "price": price,
        "seller_id": str(user.id),
        "listed_at": datetime.now().isoformat()
    }
    
    market_data.append(new_item)
    save_market(market_data)
    
    # Удаляем предмет у пользователя
    data = load_data()
    user_id_str = str(user.id)
    if item_id in data[user_id_str]["items"]:
        data[user_id_str]["items"].remove(item_id)
        save_data(data)
    
    # Обновляем статистику продаж
    if "market_sales" not in data[user_id_str]:
        data[user_id_str]["market_sales"] = 0
    data[user_id_str]["market_sales"] += 1
    save_data(data)
    
    # Проверяем достижения
    await check_achievements(user.id, "market_trader", context)
    await check_achievements(user.id, "item_collector", context)
    
    await update.message.reply_text(
        f"✅ Предмет {item['name']} выставлен на рынок за {price} копеек!\n"
        "Он будет доступен другим игрокам до продажи."
    )

async def buy_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Покупка предмета с рынка"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    if not context.args:
        await update.message.reply_text("❌ Укажите ID предмета для покупки: /buy [ID]")
        return
    
    item_id = context.args[0]
    market_data = load_market()
    item = next((i for i in market_data if i['id'] == item_id), None)
    
    if not item:
        await update.message.reply_text("❌ Предмет не найден!")
        return
    
    if user_data['kopecks'] < item['price']:
        await update.message.reply_text(
            f"❌ Недостаточно средств! Нужно {item['price']} копеек, у вас {user_data['kopecks']:.2f}"
        )
        return
    
    # Покупка предмета
    # 1. Переводим деньги продавцу
    seller_id = int(item['seller_id'])
    update_user_balance(seller_id, kopecks=item['price'])
    update_user_balance(user.id, kopecks=-item['price'])
    
    # 2. Добавляем предмет покупателю
    data = load_data()
    user_id_str = str(user.id)
    if "items" not in data[user_id_str]:
        data[user_id_str]["items"] = []
    data[user_id_str]["items"].append(item['item_id'])
    save_data(data)
    
    # 3. Удаляем предмет с рынка
    market_data = [i for i in market_data if i['id'] != item_id]
    save_market(market_data)
    
    # 4. Уведомляем продавца
    try:
        await context.bot.send_message(
            chat_id=seller_id,
            text=f"🎉 Ваш предмет {item['name']} был продан за {item['price']} копеек!"
        )
    except:
        pass
    
    # Обновляем квесты
    await update_quest_progress(user.id, "купите")
    # Проверяем достижения
    await check_achievements(user.id, "item_collector", context)
    
    await update.message.reply_text(
        f"✅ Вы купили {item['name']} за {item['price']} копеек!\n"
        "Предмет добавлен в ваш инвентарь."
    )

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просмотр инвентаря"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    items = load_items()
    
    if "items" not in user_data or not user_data["items"]:
        await update.message.reply_text("🎒 Ваш инвентарь пуст!")
        return
    
    # Группируем предметы по типам
    item_counts = {}
    for item_id in user_data["items"]:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
    
    # Находим описания предметов
    response = "🎒 Ваш инвентарь:\n\n"
    for item_id, count in item_counts.items():
        item = next((i for i in items if i['id'] == item_id), None)
        if item:
            response += f"{item['name']} x{count}\n📝 {item['description']}\n\n"
    
    response += "Используйте /use [ID предмета] чтобы использовать предмет"
    await update.message.reply_text(response)

async def use_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Использование предмета"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    items = load_items()
    
    if not context.args:
        await update.message.reply_text("❌ Укажите ID предмета: /use [ID предмета]")
        return
    
    item_id = context.args[0].lower()
    
    if "items" not in user_data or item_id not in user_data["items"]:
        await update.message.reply_text("❌ У вас нет этого предмета!")
        return
    
    # Находим предмет
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        await update.message.reply_text("❌ Такого предмета не существует!")
        return
    
    # Применяем эффект предмета
    data = load_data()
    user_id_str = str(user.id)
    
    # Удаляем предмет из инвентаря
    data[user_id_str]["items"].remove(item_id)
    
    # Добавляем эффект
    now = datetime.now()
    if "effects" not in data[user_id_str]:
        data[user_id_str]["effects"] = {}
    
    if item['type'] == "permanent":
        # Постоянный эффект
        if item_id not in data[user_id_str]["items"]:
            data[user_id_str]["items"].append(item_id)
            response = f"✅ {item['name']} активирован! Эффект постоянный."
    
    elif item['type'] == "temporary":
        # Временный эффект
        duration = item.get('duration', 7)
        effect_end = now + timedelta(days=duration)
        data[user_id_str]["effects"][item_id] = effect_end.isoformat()
        response = f"✅ {item['name']} активирован! Эффект продлится {duration} дней."
    
    elif item['type'] == "instant":
        # Мгновенный эффект
        if item_id == "wheel_spin":
            wheel_history = load_wheel_history()
            wheel_history[user_id_str] = "2000-01-01"  # Сбрасываем таймер
            save_wheel_history(wheel_history)
            response = "🎡 Вы получили дополнительное вращение колеса фортуны! Используйте /wheel"
        elif item_id == "time_machine":
            # Сбрасываем все таймеры
            data[user_id_str]["last_sell"] = ""
            data[user_id_str]["last_buy"] = ""
            data[user_id_str]["last_send"] = ""
            data[user_id_str]["last_quiz"] = ""
            response = "⏱️ Все таймеры действий сброшены! Теперь вы можете выполнять действия снова."
    
    elif item['type'] == "consumable":
        # Расходуемый предмет
        if item_id == "fortune_teller":
            # В следующей викторине покажет правильный ответ
            data[user_id_str]["effects"]["fortune_teller"] = True
            response = "🔮 Следующий вопрос в викторине будет с подсказкой!"
    
    save_data(data)
    
    await update.message.reply_text(response)

async def auction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просмотр активных аукционов"""
    auction_data = load_auction()
    
    if not auction_data.get("active") or not auction_data["items"]:
        await update.message.reply_text("🏛️ На данный момент нет активных аукционов.")
        return
    
    response = "🏛️ Активные аукционы:\n\n"
    for i, item in enumerate(auction_data["items"], 1):
        time_left = datetime.fromisoformat(item["end_time"]) - datetime.now()
        hours, remainder = divmod(time_left.total_seconds(), 3600)
        minutes = remainder // 60
        
        response += (
            f"{i}. {item['name']}\n"
            f"📝 {item['description']}\n"
            f"💰 Текущая ставка: {item['current_bid']} копеек\n"
            f"👤 Текущий победитель: @{item.get('winner_name', 'никто')}\n"
            f"⏳ Осталось: {int(hours)}ч {int(minutes)}мин\n"
            f"🆔 ID: {item['id']}\n\n"
        )
    
    response += "Сделать ставку: /bid [ID аукциона] [ставка]"
    await update.message.reply_text(response)

async def start_auction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск нового аукциона (только для админа)"""
    user = update.effective_user
    # Проверка прав администратора (замените YOUR_ADMIN_USER_ID на реальный ID)
    if user.id != YOUR_ADMIN_USER_ID:
        await update.message.reply_text("❌ У вас нет прав для этой команды!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🚀 Запуск аукциона:\n"
            "Использование: /start_auction [ID предмета] [начальная ставка] [длительность в часах]"
        )
        return
    
    try:
        item_id = context.args[0]
        start_bid = int(context.args[1])
        duration = int(context.args[2])
        
        if start_bid <= 0 or duration <= 0:
            await update.message.reply_text("❌ Ставка и длительность должны быть положительными!")
            return
        
        items = load_items()
        item = next((i for i in items if i['id'] == item_id), None)
        if not item:
            await update.message.reply_text("❌ Предмет не найден!")
            return
        
        auction_data = load_auction()
        auction_id = f"auc_{random.randint(1000, 9999)}"
        
        new_auction = {
            "id": auction_id,
            "item_id": item_id,
            "name": item['name'],
            "description": item['description'],
            "start_bid": start_bid,
            "current_bid": start_bid,
            "winner_id": None,
            "winner_name": None,
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=duration)).isoformat()
        }
        
        auction_data["active"] = True
        auction_data["items"].append(new_auction)
        save_auction(auction_data)
        
        await update.message.reply_text(
            f"🏛️ Аукцион запущен!\n"
            f"Предмет: {item['name']}\n"
            f"Начальная ставка: {start_bid} копеек\n"
            f"Длительность: {duration} часов"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def bid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ставка на аукционе"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Использование: /bid [ID аукциона] [ставка]")
        return
    
    try:
        auction_id = context.args[0]
        bid_amount = int(context.args[1])
        
        if bid_amount <= 0:
            await update.message.reply_text("❌ Ставка должна быть положительной!")
            return
        
        auction_data = load_auction()
        auction_item = next((i for i in auction_data["items"] if i["id"] == auction_id), None)
        
        if not auction_item:
            await update.message.reply_text("❌ Аукцион не найден!")
            return
        
        if datetime.now() > datetime.fromisoformat(auction_item["end_time"]):
            await update.message.reply_text("❌ Аукцион уже завершен!")
            return
        
        if bid_amount <= auction_item["current_bid"]:
            await update.message.reply_text(
                f"❌ Ваша ставка должна быть выше текущей ({auction_item['current_bid']} копеек)!"
            )
            return
        
        if user_data["kopecks"] < bid_amount:
            await update.message.reply_text(
                f"❌ Недостаточно средств! У вас {user_data['kopecks']:.2f} копеек"
            )
            return
        
        # Обновляем ставку
        auction_item["current_bid"] = bid_amount
        auction_item["winner_id"] = str(user.id)
        auction_item["winner_name"] = user.username or user.first_name
        
        save_auction(auction_data)
        
        await update.message.reply_text(
            f"✅ Ваша ставка {bid_amount} копеек принята!\n"
            f"Вы теперь лидируете на аукционе '{auction_item['name']}'"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def items_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просмотр списка предметов"""
    items = load_items()
    
    response = "🛍️ Доступные предметы:\n\n"
    for item in items:
        response += (
            f"🔹 {item['name']}\n"
            f"ID: {item['id']}\n"
            f"📝 {item['description']}\n"
            f"💰 Цена в магазине: {item['price']} копеек\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
        )
    
    response += "\nВы можете приобрести эти предметы на рынке (/market) или получить в качестве награды."
    await update.message.reply_text(response)

async def duel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начать PvP дуэль"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚔️ Дуэль с другим игроком:\n"
            "Использование: /duel [ставка] [@username]\n"
            "Требуется билет на дуэль (/buy pvp_ticket)\n"
            f"Ваш баланс: {user_data['kopecks']:.2f} копеек"
        )
        return
    
    try:
        bet = int(context.args[0])
        if bet <= 0:
            await update.message.reply_text("Ставка должна быть положительной!")
            return
        
        opponent_username = context.args[1].lstrip('@')
        data = load_data()
        opponent_id = None
        
        # Поиск оппонента
        for uid, ud in data.items():
            if ud.get("username", "").lower() == opponent_username.lower():
                opponent_id = int(uid)
                break
        
        if not opponent_id:
            await update.message.reply_text("Игрок с таким именем не найден!")
            return
        
        if opponent_id == user.id:
            await update.message.reply_text("Нельзя играть против себя!")
            return
        
        # Проверка билета
        if "pvp_ticket" not in user_data.get("items", []):
            await update.message.reply_text("❌ Для дуэли требуется билет! Купите в магазине (/market)")
            return
        
        # Проверка баланса
        if user_data["kopecks"] < bet:
            await update.message.reply_text(f"Недостаточно копеек! У вас: {user_data['kopecks']:.2f}")
            return
        
        opponent_data = get_user_balance(opponent_id)
        if opponent_data["kopecks"] < bet:
            await update.message.reply_text("У оппонента недостаточно средств!")
            return
        
        # Запрос подтверждения у оппонента
        context.user_data['duel_challenge'] = {
            'challenger_id': user.id,
            'challenger_name': user_data.get("username", user.first_name),
            'opponent_id': opponent_id,
            'bet': bet
        }
        
        try:
            await context.bot.send_message(
                chat_id=opponent_id,
                text=f"⚔️ Вам вызов на дуэль от @{user_data.get('username', user.first_name)}!\n"
                     f"Ставка: {bet} копеек\n"
                     f"Принять вызов? (да/нет)"
            )
        except:
            await update.message.reply_text("❌ Не удалось отправить запрос оппоненту!")
            return
        
        await update.message.reply_text(
            f"✅ Запрос на дуэль отправлен @{opponent_username}!\n"
            f"Ожидаем подтверждения..."
        )
        
    except ValueError:
        await update.message.reply_text("Некорректная ставка!")

async def clan_war(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начать войну кланов"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚔️ Война кланов:\n"
            "Использование: /clanwar [ставка] [название клана]\n"
            "Требуется: быть лидером клана, иметь достаточно средств в банке клана"
        )
        return
    
    try:
        bet = int(context.args[0])
        if bet <= 0:
            await update.message.reply_text("Ставка должна быть положительной!")
            return
        
        clan_name = " ".join(context.args[1:])
        clans = load_clans()
        
        # Проверка прав
        if not user_data.get("clan_id") or user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может начинать войны!")
            return
        
        user_clan = clans.get(user_data["clan_id"])
        if not user_clan:
            await update.message.reply_text("❌ Ваш клан не найден!")
            return
        
        # Поиск клана противника
        enemy_clan = None
        for cid, clan in clans.items():
            if clan["name"].lower() == clan_name.lower():
                enemy_clan = clan
                enemy_clan_id = cid
                break
        
        if not enemy_clan:
            await update.message.reply_text("❌ Клан противника не найден!")
            return
        
        # Проверка средств
        if user_clan["bank"] < bet:
            await update.message.reply_text(f"❌ Недостаточно средств в банке клана! Доступно: {user_clan['bank']}")
            return
        
        if enemy_clan["bank"] < bet:
            await update.message.reply_text("❌ У клана противника недостаточно средств!")
            return
        
        # Создаем войну
        war_id = f"war_{random.randint(1000, 9999)}"
        context.user_data['clan_war'] = {
            'war_id': war_id,
            'clan1_id': user_data["clan_id"],
            'clan1_name': user_clan["name"],
            'clan2_id': enemy_clan_id,
            'clan2_name': enemy_clan["name"],
            'bet': bet,
            'initiator': user.id
        }
        
        # Уведомление лидеру вражеского клана
        enemy_leader_id = int(enemy_clan["leader"])
        try:
            await context.bot.send_message(
                chat_id=enemy_leader_id,
                text=f"⚔️ Вам вызов на войну от клана {user_clan['name']}!\n"
                     f"Ставка: {bet} копеек из банка клана\n"
                     f"Принять вызов? (да/нет)"
            )
        except:
            await update.message.reply_text("❌ Не удалось отправить вызов лидеру вражеского клана!")
            return
        
        await update.message.reply_text(
            f"✅ Вызов на войну клану {enemy_clan['name']} отправлен!\n"
            f"Ожидаем подтверждения..."
        )
        
    except ValueError:
        await update.message.reply_text("Некорректная ставка!")

async def marry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Предложение брака с исправлениями"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "💍 Предложение брака:\n"
            "Использование: /marry [@username]\n"
            "Стоимость: 5000 копеек"
        )
        return
    
    try:
        partner_username = context.args[0].lstrip('@')
        data = load_data()
        partner_id = None
        
        # Поиск партнера
        for uid, ud in data.items():
            if ud.get("username", "").lower() == partner_username.lower():
                partner_id = int(uid)
                break
        
        if not partner_id:
            await update.message.reply_text("❌ Игрок с таким именем не найден!")
            return
        
        if partner_id == user.id:
            await update.message.reply_text("❌ Нельзя заключить брак с самим собой!")
            return
        
        # Проверка средств
        if user_data["kopecks"] < 5000:
            await update.message.reply_text("❌ Недостаточно средств! Требуется 5000 копеек.")
            return
        
        # Проверка текущего брака
        if user_data.get("spouse"):
            await update.message.reply_text("❌ Вы уже состоите в браке!")
            return
        
        partner_data = get_user_balance(partner_id)
        if partner_data.get("spouse"):
            await update.message.reply_text("❌ Этот игрок уже состоит в браке!")
            return
        
        # Отправка запроса
        context.user_data['marriage_proposal'] = {
            'proposer_id': user.id,
            'proposer_name': user_data.get("username", user.first_name),
            'partner_id': partner_id,
            'partner_name': partner_username
        }
        
        try:
            await context.bot.send_message(
                chat_id=partner_id,
                text=f"💍 Вам предложение брака от @{user_data.get('username', user.first_name)}!\n"
                     f"Согласны? (да/нет)"
            )
            await update.message.reply_text(f"✅ Предложение брака отправлено @{partner_username}!")
        except:
            await update.message.reply_text("❌ Не удалось отправить запрос!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def mentor_system(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Система наставничества"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    
    if not context.args:
        await update.message.reply_text(
            "👨‍🏫 Система наставничества:\n"
            "/mentor request [@username] - запросить наставника\n"
            "/mentor accept [@username] - принять запрос на наставничество\n"
            "/mentor cancel - отменить текущий запрос\n"
            "/mentor end - завершить отношения наставничества"
        )
        return
    
    command = context.args[0].lower()
    
    if command == "request" and len(context.args) > 1:
        # Запрос наставника
        mentor_username = context.args[1].lstrip('@')
        data = load_data()
        mentor_id = None
        
        # Поиск наставника
        for uid, ud in data.items():
            if ud.get("username", "").lower() == mentor_username.lower():
                mentor_id = int(uid)
                break
        
        if not mentor_id:
            await update.message.reply_text("Игрок с таким именем не найден!")
            return
        
        if mentor_id == user.id:
            await update.message.reply_text("Нельзя быть наставником самому себе!")
            return
        
        # Проверка текущих отношений
        if user_data.get("mentor"):
            await update.message.reply_text("❌ У вас уже есть наставник!")
            return
        
        mentor_data = get_user_balance(mentor_id)
        if mentor_data.get("mentor") == str(user.id):
            await update.message.reply_text("❌ Этот игрок уже является вашим учеником!")
            return
        
        # Отправка запроса
        context.user_data['mentor_request'] = {
            'student_id': user.id,
            'student_name': user_data.get("username", user.first_name),
            'mentor_id': mentor_id,
            'mentor_name': mentor_username
        }
        
        try:
            await context.bot.send_message(
                chat_id=mentor_id,
                text=f"👨‍🎓 Вам запрос на наставничество от @{user_data.get('username', user.first_name)}!\n"
                     f"Принять? (да/нет)"
            )
        except:
            await update.message.reply_text("❌ Не удалось отправить запрос!")
            return
        
        await update.message.reply_text(
            f"✅ Запрос на наставничество отправлен @{mentor_username}!\n"
            f"Ожидаем подтверждения..."
        )
    
    elif command == "accept" and len(context.args) > 1:
        # Принятие запроса на наставничество
        student_username = context.args[1].lstrip('@')
        # Реализация аналогична запросу
        
    # Другие команды наставничества...

async def corporation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Управление корпорациями"""
    user = update.effective_user
    data = load_data()
    clans = load_clans()
    corporations = load_corporations()
    user_id_str = str(user.id)
    
    if user_id_str not in data:
        data[user_id_str] = {
            "kopecks": 0,
            "rubies": 0,
            "deposit": 0,
            "deposit_interest": 0,
            "username": user.username or user.first_name,
            "last_interest": datetime.now().isoformat(),
            "last_daily": "",
            "last_sell": "",
            "last_buy": "",
            "last_send": "",
            "win_count": 0,
            "daily_streak": 0,
            "achievements": {},
            "last_reset": "",
            "level": 1,
            "exp": 0,
            "daily_quests": {},
            "weekly_quests": {},
            "last_quest_update": "",
            "clan_id": "",
            "clan_role": "",
            "quiz_correct": 0,
            "items": [],
            "effects": {},
            "market_sales": 0,
            "pvp_wins": 0,
            "pvp_losses": 0,
            "clan_wars": 0,
            "spouse": "",
            "mentor": "",
            "corporation": "",
            "real_estate": {},
            "last_real_estate_income": ""
        }
    
    user_data = data[user_id_str]
    
    if not context.args:
        await update.message.reply_text(
            "🏢 Управление корпорациями:\n"
            "/corporation create [название] - создать корпорацию (стоимость: 100 000 копеек, требуется Токен корпорации)\n"
            "/corporation join [название] - вступить в корпорацию (только лидер клана)\n"
            "/corporation leave - покинуть корпорацию\n"
            "/corporation info - информация о вашей корпорации\n"
            "/corporation deposit [сумма] - внести вклад в банк корпорации\n"
            "/corporation members - список кланов в корпорации\n"
            "/corporation upgrade - улучшить корпорацию (только лидер)"
        )
        return
    
    command = context.args[0].lower()
    
    # Создание корпорации
    if command == "create" and len(context.args) > 1:
        if user_data["kopecks"] < 100000:
            await update.message.reply_text("❌ Недостаточно копеек! Создание корпорации стоит 100 000 копеек.")
            return
        
        if "corporation_token" not in user_data.get("items", []):
            await update.message.reply_text("❌ Требуется Токен корпорации! Купите на рынке.")
            return
        
        if user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может создать корпорацию!")
            return
        
        if user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан уже состоит в корпорации!")
            return
        
        corporation_name = " ".join(context.args[1:])
        corporation_id = f"corp_{random.randint(1000, 9999)}"
        
        # Проверяем уникальность названия
        for cid, corp in corporations.items():
            if corp["name"].lower() == corporation_name.lower():
                await update.message.reply_text("❌ Корпорация с таким названием уже существует!")
                return
        
        corporations[corporation_id] = {
            "name": corporation_name,
            "leader": user_data["clan_id"],
            "clans": [user_data["clan_id"]],
            "bank": 0,
            "level": 1,
            "bonus": CORPORATION_LEVELS[0]["bonus"],
            "total_deposited": 0,
            "created_at": datetime.now().isoformat(),
        }
        
        user_data["kopecks"] -= 100000
        # Удаляем токен
        user_data["items"].remove("corporation_token")
        user_data["corporation"] = corporation_id
        
        save_corporations(corporations)
        save_data(data)
        
        await update.message.reply_text(
            f"🏢 Корпорация '{corporation_name}' успешно создана!\n"
            f"💳 С вашего счета списано 100 000 копеек.\n"
            f"Теперь вы глава корпорации."
        )
        return
    
    # Вступление в корпорацию
    elif command == "join" and len(context.args) > 1:
        if user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может вступать в корпорации!")
            return
        
        if user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан уже состоит в корпорации!")
            return
        
        corporation_name = " ".join(context.args[1:])
        corporation_found = None
        
        for cid, corp in corporations.items():
            if corp["name"].lower() == corporation_name.lower():
                corporation_found = corp
                corp_id = cid
                break
        
        if not corporation_found:
            await update.message.reply_text("❌ Корпорация с таким названием не найдена!")
            return
        
        # Проверяем максимальное количество кланов
        corp_level_data = next((l for l in CORPORATION_LEVELS if l["level"] == corporation_found["level"]), None)
        if corp_level_data and len(corporation_found["clans"]) >= corp_level_data["max_clans"]:
            await update.message.reply_text("❌ Корпорация достигла максимального количества кланов!")
            return
        
        corporation_found["clans"].append(user_data["clan_id"])
        user_data["corporation"] = corp_id
        
        save_corporations(corporations)
        save_data(load_data())
        
        await update.message.reply_text(
            f"🏢 Вы успешно вступили в корпорацию '{corporation_found['name']}'!\n"
        )
        return
    
    # Покинуть корпорацию
    elif command == "leave":
        if not user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан не состоит в корпорации!")
            return
        
        if user_data.get("clan_role") != "leader":
            await update.message.reply_text("❌ Только лидер клана может покинуть корпорацию!")
            return
        
        corp_id = user_data["corporation"]
        corp = corporations.get(corp_id)
        
        if not corp:
            await update.message.reply_text("❌ Ваша корпорация не найдена!")
            return
        
        if corp["leader"] == user_data["clan_id"]:
            # Если лидер уходит - распускаем корпорацию
            del corporations[corp_id]
            for clan_id in corp["clans"]:
                clan_data = clans.get(clan_id)
                if clan_data:
                    clan_data["corporation"] = ""
            save_clans(clans)
        else:
            # Обычный участник
            corp["clans"].remove(user_data["clan_id"])
        
        user_data["corporation"] = ""
        
        save_corporations(corporations)
        save_data(data)
        
        await update.message.reply_text(f"🏢 Вы покинули корпорацию!")
        return
    
    # Информация о корпорации
    elif command == "info":
        if not user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан не состоит в корпорации!")
            return
        
        corp_id = user_data["corporation"]
        corp = corporations.get(corp_id)
        
        if not corp:
            await update.message.reply_text("❌ Ваша корпорация не найдена!")
            return
        
        leader_clan = clans.get(corp["leader"], {})
        leader_name = leader_clan.get("name", "Неизвестно")
        
        corp_level_data = next((l for l in CORPORATION_LEVELS if l["level"] == corp["level"]), None)
        
        response = f"🏢 Информация о корпорации '{corp['name']}':\n\n"
        response += f"👑 Глава: {leader_name}\n"
        response += f"👥 Кланов: {len(corp['clans'])}/{corp_level_data['max_clans']}\n"
        response += f"💰 Банк корпорации: {corp['bank']} копеек\n"
        response += f"📊 Уровень: {corp['level']} ({corp_level_data['name']})\n"
        response += f"💎 Бонус к депозиту: +{corp['bonus']*100:.2f}%\n"
        response += f"📅 Создана: {datetime.fromisoformat(corp['created_at']).strftime('%d.%m.%Y')}"
        
        await update.message.reply_text(response)
        return
    
    # Внести вклад в банк корпорации
    elif command == "deposit" and len(context.args) > 1:
        if not user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан не состоит в корпорации!")
            return
        
        try:
            amount = int(context.args[1])
            if amount <= 0:
                await update.message.reply_text("❌ Сумма должна быть положительной!")
                return
            
            if user_data["kopecks"] < amount:
                await update.message.reply_text("❌ Недостаточно копеек на вашем счету!")
                return
            
            corp_id = user_data["corporation"]
            corp = corporations.get(corp_id)
            
            if not corp:
                await update.message.reply_text("❌ Ваша корпорация не найдена!")
                return
            
            # Обновляем балансы
            corp["bank"] += amount
            corp["total_deposited"] += amount
            user_data["kopecks"] -= amount
            
            # Проверяем повышение уровня корпорации
            for level in CORPORATION_LEVELS:
                if level["level"] > corp["level"] and corp["total_deposited"] >= level["required_money"]:
                    corp["level"] = level["level"]
                    corp["bonus"] = level["bonus"]
                    await update.message.reply_text(
                        f"🎉 Ваша корпорация достигла {level['level']} уровня ({level['name']})!\n"
                        f"💎 Новый бонус к депозиту: +{level['bonus']*100:.2f}%"
                    )
            
            save_corporations(corporations)
            save_data(data)
            
            # Обновляем прогресс квестов
            await update_quest_progress(user.id, "внесите в банк корпорации")
            
            await update.message.reply_text(
                f"💰 Вы внесли {amount} копеек в банк корпорации!\n"
                f"💳 Новый баланс корпорации: {corp['bank']} копеек"
            )
            return
        except ValueError:
            await update.message.reply_text("❌ Некорректная сумма!")
            return
    
    # Список членов корпорации
    elif command == "members":
        if not user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан не состоит в корпорации!")
            return
        
        corp_id = user_data["corporation"]
        corp = corporations.get(corp_id)
        
        if not corp:
            await update.message.reply_text("❌ Ваша корпорация не найдена!")
            return
        
        response = f"🏢 Кланы в корпорации '{corp['name']}':\n\n"
        for clan_id in corp["clans"]:
            clan = clans.get(clan_id, {})
            response += f"- {clan.get('name', 'Неизвестно')}\n"
        
        await update.message.reply_text(response)
        return
    
    # Улучшение корпорации
    elif command == "upgrade":
        if not user_data.get("corporation"):
            await update.message.reply_text("❌ Ваш клан не состоит в корпорации!")
            return
        
        if user_data.get("clan_id") != corporations[user_data["corporation"]]["leader"]:
            await update.message.reply_text("❌ Только глава корпорации может улучшать ее!")
            return
        
        corp_id = user_data["corporation"]
        corp = corporations.get(corp_id)
        
        if not corp:
            await update.message.reply_text("❌ Ваша корпорация не найдена!")
            return
        
        next_level = next((l for l in CORPORATION_LEVELS if l["level"] == corp["level"] + 1), None)
        if not next_level:
            await update.message.reply_text("🎖️ Ваша корпорация достигла максимального уровня!")
            return
        
        if corp["bank"] < next_level["required_money"]:
            await update.message.reply_text(
                f"❌ Недостаточно средств в банке! Нужно {next_level['required_money']}, доступно {corp['bank']}"
            )
            return
        
        corp["bank"] -= next_level["required_money"]
        corp["level"] = next_level["level"]
        corp["bonus"] = next_level["bonus"]
        
        save_corporations(corporations)
        
        await update.message.reply_text(
            f"🎉 Корпорация улучшена до уровня {next_level['level']} ({next_level['name']})!\n"
            f"💎 Новый бонус к депозиту: +{next_level['bonus']*100:.2f}%"
        )
        return
    
    await update.message.reply_text("❌ Неизвестная команда для корпорации!")

async def real_estate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Покупка недвижимости с пояснениями"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    real_estate_types = load_real_estate()
    
    if not context.args:
        response = "🏢 Доступная недвижимость (используйте ID для покупки):\n\n"
        for prop in real_estate_types:
            response += (
                f"🆔 {prop['id']}\n"
                f"🏠 {prop['name']}\n"
                f"💵 Цена: {prop['price']} коп.\n"
                f"📈 Доход: {prop['income']} коп./день\n"
                f"🆙 Улучшение: {prop['upgrade_cost']} коп.\n\n"
            )
        response += "Для покупки: /realestate buy [id]\nПример: /realestate buy small_house"
        await update.message.reply_text(response)
        return
    
    if context.args[0] == "buy" and len(context.args) > 1:
        property_id = context.args[1]
        property_info = next((p for p in real_estate_types if p["id"] == property_id), None)
        
        if not property_info:
            await update.message.reply_text("❌ Объект недвижимости не найден! Доступные ID: " + 
                                           ", ".join(p['id'] for p in real_estate_types))
            return
        
        # Проверяем наличие документа на недвижимость
        if "real_estate_deed" not in user_data.get("items", []):
            await update.message.reply_text("❌ Требуется Документ на недвижимость! Купите на рынке.")
            return
        
        if user_data["kopecks"] < property_info["price"]:
            await update.message.reply_text(
                f"❌ Недостаточно средств! Нужно {property_info['price']}, у вас {user_data['kopecks']:.2f}"
            )
            return
        
        # Покупаем недвижимость
        data = load_data()
        user_id_str = str(user.id)
        if "real_estate" not in data[user_id_str]:
            data[user_id_str]["real_estate"] = {}
        
        # Если уже есть такой тип недвижимости - улучшаем
        if property_id in data[user_id_str]["real_estate"]:
            data[user_id_str]["real_estate"][property_id] += 1
        else:
            data[user_id_str]["real_estate"][property_id] = 1
        
        data[user_id_str]["kopecks"] -= property_info["price"]
        # Удаляем документ
        if "real_estate_deed" in data[user_id_str].get("items", []):
            data[user_id_str]["items"].remove("real_estate_deed")
        
        save_data(data)
        
        await check_achievements(user.id, "real_estate_tycoon", context)
        await update_quest_progress(user.id, "инвестор в недвижимость")
        
        await update.message.reply_text(
            f"🏢 Вы приобрели {property_info['name']}!\n"
            f"Теперь вы будете получать {property_info['income']} копеек ежедневно."
        )
        return
    
    await update.message.reply_text("❌ Неизвестная команда! Используйте /realestate для просмотра доступных команд")

async def my_properties(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просмотр своей недвижимости"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    real_estate_types = load_real_estate()
    
    if "real_estate" not in user_data or not user_data["real_estate"]:
        await update.message.reply_text("🏢 У вас пока нет недвижимости.")
        return
    
    response = "🏢 Ваша недвижимость:\n\n"
    total_income = 0
    
    for property_id, level in user_data["real_estate"].items():
        prop_info = next((p for p in real_estate_types if p["id"] == property_id), None)
        if prop_info:
            property_income = prop_info["income"] * level
            total_income += property_income
            response += f"{prop_info['name']} (Уровень {level})\n"
            response += f"Доход: {property_income} коп./день\n"
            response += f"Улучшение: {prop_info['upgrade_cost'] * level} коп.\n\n"
    
    response += f"💵 Общий ежедневный доход: {total_income} копеек"
    await update.message.reply_text(response)

async def upgrade_property(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Улучшение недвижимости"""
    user = update.effective_user
    user_data = get_user_balance(user.id)
    real_estate_types = load_real_estate()
    
    if not context.args:
        await update.message.reply_text("❌ Укажите ID недвижимости: /upgrade_property [id]")
        return
    
    property_id = context.args[0]
    
    if "real_estate" not in user_data or property_id not in user_data["real_estate"]:
        await update.message.reply_text("❌ У вас нет этой недвижимости!")
        return
    
    prop_info = next((p for p in real_estate_types if p["id"] == property_id), None)
    if not prop_info:
        await update.message.reply_text("❌ Объект недвижимости не найден!")
        return
    
    current_level = user_data["real_estate"][property_id]
    upgrade_cost = prop_info["upgrade_cost"] * current_level
    
    if user_data["kopecks"] < upgrade_cost:
        await update.message.reply_text(f"❌ Недостаточно средств! Нужно {upgrade_cost}, у вас {user_data['kopecks']:.2f}")
        return
    
    # Улучшаем недвижимость
    data = load_data()
    user_id_str = str(user.id)
    data[user_id_str]["real_estate"][property_id] += 1
    data[user_id_str]["kopecks"] -= upgrade_cost
    
    save_data(data)
    
    new_income = prop_info["income"] * (current_level + 1)
    await update.message.reply_text(
        f"🏢 {prop_info['name']} улучшена до уровня {current_level + 1}!\n"
        f"💵 Новый доход: {new_income} копеек/день"
    )

async def award_top_players(context: ContextTypes.DEFAULT_TYPE):
    """Награждение топ-3 игроков"""
    today = datetime.now().strftime("%Y-%m-%d")
    rewards_data = load_leaderboard_rewards()
    
    if rewards_data.get("last_rewarded") == today:
        return
    
    data = load_data()
    players = []
    for user_id, user_data in data.items():
        total = user_data["kopecks"] + user_data["deposit"] + user_data["rubies"] * 100
        players.append((user_id, total))
    
    players.sort(key=lambda x: x[1], reverse=True)
    rewards = [1000, 500, 250]  # Награды за 1,2,3 места
    
    for i in range(min(3, len(players))):
        user_id = int(players[i][0])
        update_user_balance(user_id, kopecks=rewards[i])
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🏆 Вы в топ-{i+1}! Награда: {rewards[i]} копеек"
            )
        except:
            pass
    
    # Обновляем время последнего награждения
    rewards_data["last_rewarded"] = today
    save_leaderboard_rewards(rewards_data)

async def check_auction_results(context: ContextTypes.DEFAULT_TYPE):
    """Проверка результатов аукционов (запускается по расписанию)"""
    auction_data = load_auction()
    now = datetime.now()
    
    for item in auction_data["items"][:]:
        end_time = datetime.fromisoformat(item["end_time"])
        if now > end_time:
            # Аукцион завершен
            winner_id = item.get("winner_id")
            if winner_id:
                winner_data = get_user_balance(int(winner_id))
                
                # Добавляем предмет победителю
                data = load_data()
                user_id_str = winner_id
                if "items" not in data[user_id_str]:
                    data[user_id_str]["items"] = []
                data[user_id_str]["items"].append(item["item_id"])
                save_data(data)
                
                # Уведомляем победителя
                try:
                    await context.bot.send_message(
                        chat_id=int(winner_id),
                        text=f"🏆 Поздравляем! Вы выиграли аукцион на '{item['name']}'!\n"
                             f"Предмет добавлен в ваш инвентарь."
                    )
                except:
                    pass
            
            # Удаляем завершенный аукцион
            auction_data["items"].remove(item)
    
    if not auction_data["items"]:
        auction_data["active"] = False
    
    save_auction(auction_data)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для текстовых сообщений (подтверждение allin и бесплатная игра guess)"""
    user = update.effective_user
    text = update.message.text.lower()
    
    # Обработка предложения брака
    if 'marriage_proposal' in context.user_data:
        proposal = context.user_data['marriage_proposal']
        
        # Проверяем, что ответил правильный пользователь
        if user.id != proposal['partner_id']:
            return
            
        if text == 'да':
            data = load_data()
            proposer_id_str = str(proposal['proposer_id'])
            partner_id_str = str(proposal['partner_id'])
            
            # Проверяем существование пользователей
            if proposer_id_str not in data or partner_id_str not in data:
                await update.message.reply_text("❌ Один из пользователей не найден!")
                context.user_data.pop('marriage_proposal', None)
                return
                
            proposer_data = data[proposer_id_str]
            partner_data = data[partner_id_str]
            
            # Проверяем, что оба не в браке
            if proposer_data.get("spouse") or partner_data.get("spouse"):
                await update.message.reply_text("❌ Один из вас уже состоит в браке!")
                context.user_data.pop('marriage_proposal', None)
                return
                
            # Проверяем наличие денег
            if proposer_data["kopecks"] < 5000:
                await update.message.reply_text("❌ У вас недостаточно средств для заключения брака!")
                context.user_data.pop('marriage_proposal', None)
                return
                
            # Заключаем брак
            proposer_data["spouse"] = partner_id_str
            partner_data["spouse"] = proposer_id_str
            proposer_data["kopecks"] -= 5000  # Списываем стоимость
            
            save_data(data)
            
            await update.message.reply_text(
                f"💍 Поздравляем! Вы заключили брак с @{proposer_data['username']}!"
            )
            
            # Отправляем уведомление второму участнику
            try:
                await context.bot.send_message(
                    chat_id=proposal['proposer_id'],
                    text=f"💍 @{partner_data['username']} принял(а) ваше предложение о браке!"
                )
            except:
                pass
                
        elif text == 'нет':
            await update.message.reply_text("❌ Предложение брака отклонено.")
        else:
            await update.message.reply_text("Пожалуйста, ответьте 'да' или 'нет'")
            return
            
        context.user_data.pop('marriage_proposal', None)
        return

    # Обработка подтверждения для allin
    if 'awaiting_allin_confirmation' in context.user_data:
        # Проверяем, что сообщение от того же пользователя
        if context.user_data['awaiting_allin_confirmation'].get('user_id') != str(user.id):
            return
            
        if text in ['да', 'нет']:
            if text == 'нет':
                await update.message.reply_text("Ставка отменена")
                context.user_data.pop('awaiting_allin_confirmation', None)
                return
            
            # Получаем сохраненные данные
            allin_data = context.user_data['awaiting_allin_confirmation']
            user_id_str = allin_data['user_id']
            total_bet = allin_data['total_bet']
            saved_exchange_rate = allin_data['exchange_rate']
            
            # Загружаем актуальные данные
            data = load_data()
            
            if user_id_str not in data:
                await update.message.reply_text("❌ Ошибка: данные пользователя не найдены")
                context.user_data.pop('awaiting_allin_confirmation', None)
                return
                
            user_data = data[user_id_str]
            
            # Гарантируем наличие всех полей
            if "achievements" not in user_data:
                user_data["achievements"] = {}
            
            # Пересчитываем текущий баланс с сохраненным курсом
            current_total = (
                user_data.get("rubies", 0) * saved_exchange_rate + 
                user_data.get("deposit", 0) + 
                user_data.get("kopecks", 0)
            )
            
            # Проверяем изменение баланса (допуск 1 копейка)
            if abs(current_total - total_bet) > 1:
                await update.message.reply_text("❌ Баланс изменился, ставка отменена")
                context.user_data.pop('awaiting_allin_confirmation', None)
                return
            
            # Обнуляем все балансы
            user_data["kopecks"] = 0
            user_data["rubies"] = 0
            user_data["deposit"] = 0
            
            # Добавляем опыт за ставку
            exp_gain = total_bet // 10
            await add_experience(user.id, exp_gain, context)
            
            # Играем в казино с коэффициентом 3x
            if random.random() < 0.5:
                win_amount = int(total_bet * 3)
                user_data["kopecks"] = win_amount
                save_data(data)
                
                # Обновляем счетчик побед
                user_data["win_count"] = user_data.get("win_count", 0) + 1
                save_data(data)
                
                # Обновляем квест "Богач"
                await update_quest_progress(user.id, "earn_kopecks", win_amount)
                
                # Проверяем достижения
                await check_achievements(user.id, "gambler", context)
                await check_achievements(user.id, "first_win", context)
                await check_achievements(user.id, "ten_wins", context)
                await check_achievements(user.id, "rich", context)
                
                await update.message.reply_text(
                    f"🎉 ДЖЕКПОТ! Ты выиграл {win_amount:.2f} копеек (3x ставки)!\n"
                    f"Твой новый баланс: {win_amount:.2f} копеек"
                )
            else:
                # Сбрасываем счетчик побед
                user_data["win_count"] = 0
                save_data(data)
                
                await update.message.reply_text(
                    f"😢 К сожалению, ты проиграл всю свою ставку {total_bet:.2f} копеек.\n"
                    "Попробуй еще раз, когда накопишь средства!"
                )
            context.user_data.pop('awaiting_allin_confirmation', None)
        else:
            await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'")
        return
    
    # Обработка бесплатной игры guess
    if 'free_guess' in context.user_data:
        # Проверяем, что сообщение от того же пользователя
        if context.user_data['free_guess'].get('user_id') != user.id:
            return
            
        try:
            number = int(text)
            secret_number = context.user_data['free_guess']['secret_number']
            
            if number < 1 or number > 3:
                await update.message.reply_text("Число должно быть от 1 до 3!")
                return
                
            if number == secret_number:
                # Награда за бесплатную игру
                new_balance = update_user_balance(user.id, kopecks=1)
                
                # Обновляем счетчик побед
                data = load_data()
                user_id_str = str(user.id)
                data[user_id_str]["win_count"] = data[user_id_str].get("win_count", 0) + 1
                save_data(data)
                
                await update.message.reply_text(
                    f"🎯 Ты угадал! Загаданное число: {secret_number}\n"
                    f"🏆 Выигрыш: 1 копейка (бесплатная игра)\n"
                    f"💰 Новый баланс: {new_balance['kopecks']:.2f} копеек"
                )
            else:
                await update.message.reply_text(
                    f"❌ Ты не угадал! Загаданное число: {secret_number}\n"
                    "Попробуй еще раз: /guess"
                )
        except ValueError:
            await update.message.reply_text("Пожалуйста, введи число от 1 до 3!")
        finally:
            # Очищаем состояние игры
            context.user_data.pop('free_guess', None)
        return

def main():
    application = ApplicationBuilder().token("7656753322:AAHPcd3vvh7zqWDXeJYbClDRmEYr_02bl7I").build()
    
    # Основные команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("exchange", exchange))
    application.add_handler(CommandHandler("sell", sell))
    application.add_handler(CommandHandler("casino", casino))
    application.add_handler(CommandHandler("send", send_money))
    application.add_handler(CommandHandler("wheel", wheel))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("deposit", deposit))
    application.add_handler(CommandHandler("withdraw", withdraw))
    application.add_handler(CommandHandler("withdraw_interest", withdraw_interest))
    application.add_handler(CommandHandler("allin", allin))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("guess", guess))
    application.add_handler(CommandHandler("achievements", achievements))
    application.add_handler(CommandHandler("quests", quests))
    application.add_handler(CommandHandler("profile", profile))
    
    # Новые команды
    application.add_handler(CommandHandler("clan", clan_command))
    application.add_handler(CommandHandler("clans", clans_list))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("market", market))
    application.add_handler(CommandHandler("buy", buy_item))
    application.add_handler(CommandHandler("inventory", inventory))
    application.add_handler(CommandHandler("use", use_item))
    application.add_handler(CommandHandler("auction", auction))
    application.add_handler(CommandHandler("bid", bid))
    application.add_handler(CommandHandler("items", items_list))
    application.add_handler(CommandHandler("duel", duel))
    application.add_handler(CommandHandler("clanwar", clan_war))
    application.add_handler(CommandHandler("marry", marry))
    application.add_handler(CommandHandler("mentor", mentor_system))
    application.add_handler(CommandHandler("corporation", corporation))
    application.add_handler(CommandHandler("realestate", real_estate))
    application.add_handler(CommandHandler("myproperties", my_properties))
    application.add_handler(CommandHandler("upgrade_property", upgrade_property))
    
    # Админские команды
    application.add_handler(CommandHandler("start_auction", start_auction))
    
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Планировщик для награждения топ-игроков (каждый день в 00:00)
    job_queue = application.job_queue
    if job_queue:
        job_queue.run_daily(award_top_players, time=time(hour=0, minute=0))
        job_queue.run_repeating(check_auction_results, interval=300, first=10)  # Каждые 5 минут
    
    application.run_polling()

if __name__ == '__main__':
    main()