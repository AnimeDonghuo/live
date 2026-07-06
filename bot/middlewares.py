from functools import wraps
from bot.config import Config

def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != Config.OWNER_ID:
            print(f"Unauthorized access attempt by {user_id}")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
