from aiogram import BaseMiddleware
from aiogram.types import Update
from config import MANDATORY_CHANNELS

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        user_id = None
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        if not user_id:
            return await handler(event, data)

        for channel in MANDATORY_CHANNELS:
            try:
                member = await data["bot"].get_chat_member(chat_id=channel, user_id=user_id)
                if member.status in ["left", "kicked"]:
                    if event.message:
                        await event.message.answer("Iltimos, kanalga obuna bo‘ling.")
                    elif event.callback_query:
                        await event.callback_query.message.answer("Iltimos, kanalga obuna bo‘ling.")
                    return
            except:
                pass
        return await handler(event, data)