import os
import time
from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import FSInputFile, Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import *
from keyboards import language_keyboard, main_menu_keyboard
from config import MESSAGES, FREE_LIMIT_BYTES
from utils import check_user_limit, format_size

router = Router()

FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)


@router.message(Command("start"))
async def start_command(message: Message):
    add_user_if_not_exists(message.from_user.id)
    lang = get_user_language(message.from_user.id)
    await message.answer(
        MESSAGES[lang]["welcome"],
        reply_markup=language_keyboard()
    )


@router.callback_query(Text(startswith="lang_"))
async def change_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    set_user_language(callback.from_user.id, lang)
    await callback.message.edit_text(MESSAGES[lang]["welcome"], reply_markup=main_menu_keyboard(lang))
    await callback.answer()


@router.message(F.content_type.in_({"document", "photo", "video", "audio"}))
async def handle_file(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    file_size = 0
    file_name = ""
    file_obj = None

    if message.document:
        file_size = message.document.file_size
        file_name = message.document.file_name
        file_obj = message.document
    elif message.photo:
        file_size = message.photo[-1].file_size
        file_name = f"photo_{message.message_id}.jpg"
        file_obj = message.photo[-1]
    elif message.video:
        file_size = message.video.file_size
        file_name = message.video.file_name or f"video_{message.message_id}.mp4"
        file_obj = message.video
    elif message.audio:
        file_size = message.audio.file_size
        file_name = message.audio.file_name or f"audio_{message.message_id}.mp3"
        file_obj = message.audio

    if not check_user_limit(user_id, file_size):
        await message.answer(MESSAGES[lang]["limit_reached"])
        return

    # Faylni yuklab olish
    file_info = await file_obj.get_file()
    saved_path = os.path.join(FILES_DIR, f"{user_id}_{int(time.time())}_{file_name}")
    await message.bot.download_file(file_info.file_path, destination=saved_path)

    add_file(user_id, file_name, file_size, saved_path)
    increase_user_storage(user_id, file_size)

    await message.answer(MESSAGES[lang]["file_saved"].format(file_name))


@router.callback_query(Text(text=["🗂️ Mening fayllarim", "🗂️ Мои файлы", "🗂️ My Files"]))
async def show_files(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    files = get_user_files(callback.from_user.id)
    if not files:
        no_files_text = {
            "uz": "Fayllaringiz topilmadi.",
            "ru": "Файлы не найдены.",
            "en": "No files found."
        }
        await callback.message.edit_text(no_files_text.get(lang, "No files found."))
        await callback.answer()
        return

    text = ""
    for f_id, name, size in files:
        text += f"{f_id}. {name} ({format_size(size)})\n"

    await callback.message.edit_text(text)
    await callback.answer()


@router.callback_query(Text(text=["❌ Fayl o'chirish", "❌ Удалить файл", "❌ Delete File"]))
async def delete_file_prompt(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    files = get_user_files(callback.from_user.id)
    if not files:
        no_files_text = {
            "uz": "O'chirish uchun faylingiz yo'q.",
            "ru": "Нет файлов для удаления.",
            "en": "No files to delete."
        }
        await callback.message.edit_text(no_files_text.get(lang, "No files to delete."))
        await callback.answer()
        return

    kb = InlineKeyboardMarkup(row_width=1)
    for f_id, name, size in files:
        kb.insert(InlineKeyboardButton(f"{name} ({format_size(size)})", callback_data=f"del_{f_id}"))

    prompt_text = {
        "uz": "O'chirmoqchi bo'lgan faylni tanlang:",
        "ru": "Выберите файл для удаления:",
        "en": "Select a file to delete:"
    }
    await callback.message.edit_text(prompt_text.get(lang, "Select a file to delete:"), reply_markup=kb)


@router.callback_query(Text(startswith="del_"))
async def delete_file_confirm(callback: CallbackQuery):
    file_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    file_path = get_file_path(file_id)

    if file_path:
        try:
            os.remove(file_path)
        except Exception:
            pass
        delete_file(file_id)
        deleted_text = {
            "uz": "Fayl o'chirildi.",
            "ru": "Файл удалён.",
            "en": "File deleted."
        }
        await callback.message.edit_text(deleted_text.get(lang, "File deleted."))
    else:
        not_found_text = {
            "uz": "Fayl topilmadi.",
            "ru": "Файл не найден.",
            "en": "File not found."
        }
        await callback.message.edit_text(not_found_text.get(lang, "File not found."))

    await callback.answer()