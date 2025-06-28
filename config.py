API_TOKEN = "SIZNING_BOT_TOKENINGIZ"
ADMIN_IDS = [123456789]  # Admin telegram ID larini kiriting
MANDATORY_CHANNELS = ["@your_channel1", "@your_channel2"]  # Majburiy obuna kanallari

DB_PATH = "db.sqlite3"

FREE_LIMIT_BYTES = 2 * 1024 * 1024 * 1024  # 2GB

# Tilga oid xabarlar (uz, ru, en)
MESSAGES = {
    "uz": {
        "welcome": "Botga xush kelibsiz! Fayl yuboring.",
        "subscribe": "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
        "limit_reached": "Saqlash limiti tugadi! Premiumga o'ting.",
        "file_saved": "Fayl saqlandi: {}",
        # boshqalar...
    },
    "ru": {
        "welcome": "Добро пожаловать! Отправьте файл.",
        "subscribe": "Для использования бота подпишитесь на каналы:",
        "limit_reached": "Лимит хранения исчерпан! Перейдите на премиум.",
        "file_saved": "Файл сохранён: {}",
    },
    "en": {
        "welcome": "Welcome! Send a file.",
        "subscribe": "To use the bot, please subscribe to channels:",
        "limit_reached": "Storage limit reached! Please upgrade.",
        "file_saved": "File saved: {}",
    }
}