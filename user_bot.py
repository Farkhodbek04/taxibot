import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat, User
from telethon import TelegramClient, Button
from telethon.errors import SessionPasswordNeededError, ApiIdInvalidError, AuthKeyUnregisteredError
from rapidfuzz import process, fuzz
from dotenv import load_dotenv
from datetime import datetime
import asyncio


# Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "user_session"
SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Telethon client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Initialize bot for sending error messages to SUPERADMIN
bot = None
if BOT_TOKEN and SUPERADMIN:
    from aiogram import Bot
    bot = Bot(token=BOT_TOKEN)

# Global variables to store configuration
config = {}
source_ids = {}
destination_ids = {}
keywords = []
my_groups = {}

async def regenerate_session():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        await client.start()
        string = client.session.save()
        print(f"\n🔐 New string session:\n{string}")
        return string

def read_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        error_msg = f"{datetime.now()} Error reading config.json in user_bot: {str(e)}"
        print( error_msg)
        with open('error.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
        raise
    
from telethon.tl.types import Channel, Chat

async def fetch_my_groups_with_id(client):
    my_groups = {}
    try:
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            # Include megagroups and normal groups
            if isinstance(entity, Channel) and entity.megagroup:
                group_id = entity.id
                name = entity.title
                id_str = f"-100{str(group_id)}"
                if entity.username:
                    link = f"https://t.me/{entity.username}"
                    my_groups[id_str] = f"[{name}]({link})"
                else:
                    my_groups[id_str] = f"[{name}](Havola yo'q)"
            elif isinstance(entity, Chat):  # classic group
                group_id = entity.id
                name = entity.title
                id_str = f"-{str(group_id)}"
                my_groups[id_str] = f"[{name}](Classic guruh - havola yo'q)"
    except Exception as e:
        error_msg = f"{datetime.now()} Error with getting groups list:{str(e)}"
        print(error_msg)
        with open("error.log", "a") as f:
            f.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
        raise

    return my_groups


async def get_groups_dict():
    try:
        await client.start()
        my_groups = await fetch_my_groups_with_id(client)
        return my_groups   
    except Exception as e:
        error_msg = f"{datetime.now()} Error with getting groups list:{str(e)}"
        print(error_msg)
        with open("error.log", "a") as f:
            f.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
        raise

# Load initial configuration
def load_config():
    global config, source_ids, destination_ids, keywords
    try:
        config = read_config()
        source_ids = [int(id) for id in config.get('sources', {}).keys()]
        destination_ids = [int(id) for id in config.get('destinations', {}).keys()]
        keywords = list(config.get('keywords', []))
    except Exception as e:
        error_msg = f"Error loading config in user_bot: {str(e)}"
        print(error_msg)
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
        raise

# Initial load
try:
    load_config()
except Exception as e:
    print(f"Failed to load initial config: {str(e)}")
    raise

async def is_client_request(message):
    negatives = {'olamiz', 'olyappiz', 'yuramiz', 'yuryappiz', 'yuriladi', 'kam', 'benzin', 'propan', 'prapan', "bo'sh",
    'оламиз', 'олйаппиз', 'йурамиз', 'йурйаппиз', 'йурилади', 'кам', 'бензин', 'пропан', 'прапан', 'бош', "юрамиз", 
    "юрйаппиз", "юрилади", "оляппиз", "оляпиз", "йуряппиз", "йуряпиз", "olyapiz", "yuryapiz", "pustoy", "пустой"}
    if sum(1 if val.lower() in negatives  else 0 for val in message.split()) >= 1:
        return False
    
    words = message.split()
    
    if len(words) > 10:
        return False
    if not words:
        return False
    if not keywords:  # Check if keywords is empty
        return False
    try:
        loop = asyncio.get_event_loop()
        matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
        total_words = len(words)
        match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
        if total_words == 1:
            return matched_words == 1
        if total_words <= 8:
            return  match_percentage >= 50
        elif total_words > 9:
            return match_percentage >= 60
    except Exception as e:
        error_msg = f"Error in is_client_request: {str(e)}"
        print(error_msg)
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        return False

@client.on(events.NewMessage)
async def handler(event):
    from bot_admin import send_to_group
    try:
        message_text = event.message.message
        chat_id = event.chat_id
        sender_id = 0
        if chat_id in source_ids:
            if await is_client_request(message_text):
                print(message_text)
                sender = await event.get_sender()
                sender_id = sender.id
                formatted_message = (
                    "🚖 Yangi kilent\n\n"                    
                    f"<b>XABAR:</b> {message_text} \n"
                )
                message_id = event.message.id
                if sender.username:
                    formatted_message = formatted_message+f"\n@{sender.username}"
                
                for dest_id in destination_ids:
                    try:
                        print(f"Sending to {dest_id}")
                        await send_to_group(dest_id, sender_id, formatted_message, sender.username, chat_id, message_id)
                    except Exception as e:
                        error_msg = f"{datetime.now()} Error with sending:{str(e)}"
                        print(error_msg)
                        with open("error.log", "a") as f:
                            f.write(f"{error_msg}\n")
                        if bot and SUPERADMIN and "NoneType" not in str(e):
                            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
                        print(f"Eroor: {e}")
                        raise         
    except Exception as e:
        error_msg = f"Error in message handler: {str(e)}"
        print(error_msg)
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN and "NoneType" not in str(e):
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")

async def config_poller():
    try:
        last_modified = os.path.getmtime('config.json')
        while True:
            await asyncio.sleep(10)
            current_modified = os.path.getmtime('config.json')
            if current_modified != last_modified:
                load_config()
                last_modified = current_modified
    except Exception as e:
        error_msg = f"Error in config poller: {str(e)}"
        print(error_msg)
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        raise
    
async def user_bot_main():
    try:
        await client.start()
        asyncio.create_task(config_poller())
        print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
        await client.run_until_disconnected()
    except Exception as e:
        error_msg = f"User bot failed: {str(e)}"
        print(error_msg)
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN and "NoneType" not in str(e):
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(user_bot_main())