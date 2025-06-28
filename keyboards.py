from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    )
    return kb

def main_menu_keyboard(lang):
    texts = {
        "uz": ["🗂️ Mening fayllarim", "🔄 Konvertatsiya", "❌ Fayl o'chirish", "💎 Premium olish"],
        "ru": ["🗂️ Мои файлы", "🔄 Конвертация", "❌ Удалить файл", "💎 Купить премиум"],
        "en": ["🗂️ My Files", "🔄 Convert", "❌ Delete File", "💎 Get Premium"],
    }
    kb = InlineKeyboardMarkup(row_width=2)
    for text in texts.get(lang, texts["uz"]):
        kb.insert(InlineKeyboardButton(text, callback_data=text))
    return kb