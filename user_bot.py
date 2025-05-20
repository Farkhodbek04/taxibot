# import json
# import os
# from telethon import TelegramClient, events
# from rapidfuzz import process, fuzz
# from dotenv import load_dotenv
# from datetime import datetime

# load_dotenv()
# API_ID = int(os.getenv("API_ID"))
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = os.getenv("SESSION_NAME")

# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# def read_config():
#     with open('config.json', 'r') as f:
#         return json.load(f)
    
# ad_keywords = set(read_config()['ad_keywords'])
# keywords = [key for key in read_config()['keywords']]
# config = read_config()
# source_ids = [int(id) for id in config['sources']]
# destination_ids = [int(id) for id in config['destinations']]

# async def is_client_request(message):
#     if not message:
#         return False
    
#     if len(message) > 70:
#         return False
    
#     words = message.split()
#     if not words:
#         return False
    
#     # Offload RapidFuzz matching to a thread
#     loop = asyncio.get_event_loop()
#     matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
    
#     total_words = len(words)
#     match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
#     if total_words == 1:
#         return matched_words == 1
#     if total_words <= 8:
#         return matched_words >= 2 and match_percentage >= 50
#     elif total_words > 9:
#         return match_percentage >= 60

# @client.on(events.NewMessage)
# async def handler(event):
#     # Check if event is from a source group
#     message_text = event.message.message or ''
#     if event.chat_id in source_ids and len(message_text) < 70:
#         if await is_client_request(message_text):
#             # Get sender information
#             sender = await event.get_sender()
#             username = sender.username if sender.username else f"tg://user?id={sender.id}"
#             username_display = f"@{sender.username}" if sender.username else f"UserID: {sender.id}"
#             phone = sender.phone if sender.phone else "Noma'lum"

#             # Get group information
#             chat = await event.get_chat()
#             group_name = chat.title if chat.title else "Unknown Group"
#             group_link = f"https://t.me/c/{str(chat.id).replace('-100', '')}/{event.message.id}"

#             # Get timestamp
#             message_time = event.message.date
#             formatted_time = message_time.strftime("%Y-%m-%d %H:%M:%S")

#             # Format the message
#             formatted_message = (
#                 "🚖 Yangi Taksi So'rovi\n"
#                 f"👤 Kimdan: [{username_display}]({username})\n"
#                 f"📞 Telefon: {phone}\n"
#                 f"🏢 Guruh: {group_name} ([Manba]({group_link}))\n"
#                 f"🕒 Vaqt: {formatted_time}\n"
#                 f"💬 Xabar: {message_text}"
#             )

#             # Send the formatted message to all destination groups
#             for dest_id in destination_ids:
#                 await client.send_message(dest_id, formatted_message, parse_mode='markdown', link_preview=False)

# # Running bot
# async def main():
#     await client.start()
#     print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
#     await client.run_until_disconnected()
    
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())

''' Second eddition'''

# import json
# import os
# from telethon import TelegramClient, events
# from rapidfuzz import process, fuzz
# from dotenv import load_dotenv
# from datetime import datetime
# import asyncio
# import time

# load_dotenv()
# API_ID = int(os.getenv("API_ID"))
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = "user_session"
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Global variables to store configuration
# config = None
# source_ids = []
# destination_ids = []
# ad_keywords = set()
# keywords = []

# def read_config():
#     with open('config.json', 'r') as f:
#         return json.load(f)

# # Load initial configuration
# def load_config():
#     global config, source_ids, destination_ids, ad_keywords, keywords
#     config = read_config()
#     source_ids = [int(id) for id in config['sources']]
#     destination_ids = [int(id) for id in config['destinations']]
#     ad_keywords = set(config['ad_keywords'])
#     keywords = [key for key in config['keywords']]

# # Initial load
# load_config()

# async def is_client_request(message):
#     if not message:
#         return False
    
#     if len(message) > 70:
#         return False
    
#     words = message.split()
#     if not words:
#         return False
    
#     loop = asyncio.get_event_loop()
#     matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
    
#     total_words = len(words)
#     match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
#     if total_words == 1:
#         return matched_words == 1
#     if total_words <= 8:
#         return matched_words >= 2 and match_percentage >= 50
#     elif total_words > 9:
#         return match_percentage >= 60

# @client.on(events.NewMessage)
# async def handler(event):
#     message_text = event.message.message or ''
#     if event.chat_id in source_ids and len(message_text) < 70:
#         if await is_client_request(message_text):
#             sender = await event.get_sender()
#             username = sender.username if sender.username else f"tg://user?id={sender.id}"
#             username_display = f"@{sender.username}" if sender.username else f"UserID: {sender.id}"
#             phone = sender.phone if sender.phone else "Noma'lum"

#             chat = await event.get_chat()
#             group_name = chat.title if chat.title else "Unknown Group"
#             group_link = f"https://t.me/c/{str(chat.id).replace('-100', '')}/{event.message.id}"

#             message_time = event.message.date
#             formatted_time = message_time.strftime("%Y-%m-%d %H:%M:%S")

#             formatted_message = (
#                 "🚖 Yangi Taksi So'rovi\n"
#                 f"👤 Kimdan: [{username_display}]({username})\n"
#                 f"📞 Telefon: {phone}\n"
#                 f"🏢 Guruh: {group_name} ([Manba]({group_link}))\n"
#                 f"🕒 Vaqt: {formatted_time}\n"
#                 f"💬 Xabar: {message_text}"
#             )

#             for dest_id in destination_ids:
#                 await client.send_message(dest_id, formatted_message, parse_mode='markdown', link_preview=False)

# async def config_poller():
#     last_modified = os.path.getmtime('config.json')
#     while True:
#         await asyncio.sleep(10)  # Check every 10 seconds
#         current_modified = os.path.getmtime('config.json')
#         if current_modified != last_modified:
#             load_config()
#             last_modified = current_modified

# async def user_bot_main():
#     await client.start()
#     print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
#     # Start the config poller as a background task
#     asyncio.create_task(config_poller())
#     await client.run_until_disconnected()   

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(user_bot_main())
    
''' Third eddition'''
# import json
# import os
# from telethon import TelegramClient, events
# from rapidfuzz import process, fuzz
# from dotenv import load_dotenv
# from datetime import datetime
# import asyncio
# import time

# # Load environment variables
# load_dotenv()
# API_ID = int(os.getenv("API_ID"))
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = "/user_session"
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))
# BOT_TOKEN = os.getenv("BOT_TOKEN")

# # Initialize Telethon client
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Initialize bot for sending error messages to SUPERADMIN
# bot = None
# if BOT_TOKEN and SUPERADMIN:
#     from aiogram import Bot
#     bot = Bot(token=BOT_TOKEN)

# # Global variables to store configuration
# config = None
# source_ids = []
# destination_ids = []
# ad_keywords = set()
# keywords = []
# pending_errors = []  # Store errors to send once event loop is active

# def read_config():
#     try:
#         with open('config.json', 'r') as f:
#             return json.load(f)
#     except Exception as e:
#         error_msg = f"Error reading config.json in user_bot: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         pending_errors.append(error_msg)  # Store error to send later
#         raise

# # Load initial configuration
# def load_config():
#     global config, source_ids, destination_ids, ad_keywords, keywords
#     try:
#         config = read_config()
#         source_ids = [int(id) for id in config['sources']]
#         destination_ids = [int(id) for id in config['destinations']]
#         ad_keywords = set(config.get('ad_keywords', []))
#         keywords = [key for key in config['keywords']]
#     except Exception as e:
#         error_msg = f"Error loading config in user_bot: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         pending_errors.append(error_msg)  # Store error to send later
#         raise

# # Initial load
# try:
#     load_config()
# except Exception as e:
#     print(f"Failed to load initial config: {str(e)}")
#     raise

# async def is_client_request(message):
#     if not message:
#         return False
    
#     if len(message) > 70:
#         return False
    
#     words = message.split()
#     if not words:
#         return False
    
#     try:
#         loop = asyncio.get_event_loop()
#         matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
        
#         total_words = len(words)
#         match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
#         if total_words == 1:
#             return matched_words == 1
#         if total_words <= 8:
#             return matched_words >= 2 and match_percentage >= 50
#         elif total_words > 9:
#             return match_percentage >= 60
#     except Exception as e:
#         error_msg = f"Error in is_client_request: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#         return False

# @client.on(events.NewMessage)
# async def handler(event):
#     try:
#         message_text = event.message.message or ''
#         if event.chat_id in source_ids and len(message_text) < 70:
#             if await is_client_request(message_text):
#                 sender = await event.get_sender()
#                 username = sender.username if sender.username else f"tg://user?id={sender.id}"
#                 username_display = f"@{sender.username}" if sender.username else f"UserID: {sender.id}"
#                 phone = sender.phone if sender.phone else "Noma'lum"

#                 chat = await event.get_chat()
#                 group_name = chat.title if chat.title else "Unknown Group"
#                 group_link = f"https://t.me/c/{str(chat.id).replace('-100', '')}/{event.message.id}"

#                 message_time = event.message.date
#                 formatted_time = message_time.strftime("%Y-%m-%d %H:%M:%S")

#                 formatted_message = (
#                     "🚖 Yangi Taksi So'rovi\n"
#                     f"👤 Kimdan: [{username_display}]({username})\n"
#                     f"📞 Telefon: {phone}\n"
#                     f"🏢 Guruh: {group_name} ([Manba]({group_link}))\n"
#                     f"🕒 Vaqt: {formatted_time}\n"
#                     f"💬 Xabar: {message_text}"
#                 )

#                 for dest_id in destination_ids:
#                     await client.send_message(dest_id, formatted_message, parse_mode='markdown', link_preview=False)
#     except Exception as e:
#         error_msg = f"Error in message handler: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")

# async def config_poller():
#     try:
#         last_modified = os.path.getmtime('config.json')
#         while True:
#             await asyncio.sleep(10)  # Check every 10 seconds
#             current_modified = os.path.getmtime('config.json')
#             if current_modified != last_modified:
#                 load_config()
#                 last_modified = current_modified
#     except Exception as e:
#         error_msg = f"Error in config poller: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#         raise

# async def user_bot_main():
#     try:
#         # Send any pending error messages that occurred during initial load
#         if bot and SUPERADMIN and pending_errors:
#             for error_msg in pending_errors:
#                 await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#             pending_errors.clear()  # Clear after sending

#         await client.start()
#         print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
#         # Start the config poller as a background task
#         asyncio.create_task(config_poller())
#         await client.run_until_disconnected()
#     except Exception as e:
#         error_msg = f"User bot failed: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#         raise

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(user_bot_main())


# import json
# import os
# from telethon import TelegramClient, events
# from rapidfuzz import process, fuzz
# from dotenv import load_dotenv
# from datetime import datetime
# import asyncio
# import time

# # Load environment variables
# load_dotenv()
# API_ID = int(os.getenv("API_ID"))
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = "user_session"
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))
# BOT_TOKEN = os.getenv("BOT_TOKEN")

# # Initialize Telethon client
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Initialize bot for sending error messages to SUPERADMIN
# bot = None
# if BOT_TOKEN and SUPERADMIN:
#     from aiogram import Bot
#     bot = Bot(token=BOT_TOKEN)

# # Global variables to store configuration
# config = None
# source_ids = []
# destination_ids = []
# ad_keywords = set()
# keywords = []

# def read_config():
#     try:
#         with open('config.json', 'r') as f:
#             return json.load(f)
#     except Exception as e:
#         error_msg = f"Error reading config.json in user_bot: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
#         raise

# # Load initial configuration
# def load_config():
#     global config, source_ids, destination_ids, ad_keywords, keywords
#     try:
#         config = read_config()
#         # Ensure all IDs have -100 prefix
#         source_ids = [int(f"-100{abs(id)}" if id >= 0 else str(id)) for id in config.get('sources', [])]
#         destination_ids = [int(f"-100{abs(id)}" if id >= 0 else str(id)) for id in config.get('destinations', [])]
#         ad_keywords = set(config.get('ad_keywords', []))
#         keywords = [key for key in config['keywords']]
#     except Exception as e:
#         error_msg = f"Error loading config in user_bot: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
#         raise

# # Initial load
# try:
#     load_config()
# except Exception as e:
#     print(f"Failed to load initial config: {str(e)}")
#     raise

# async def is_client_request(message):
#     if not message:
#         return False
#     if len(message) > 70:
#         return False
#     words = message.split()
#     if not words:
#         return False
#     try:
#         loop = asyncio.get_event_loop()
#         matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
#         total_words = len(words)
#         match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
#         if total_words == 1:
#             return matched_words == 1
#         if total_words <= 8:
#             return matched_words >= 2 and match_percentage >= 50
#         elif total_words > 9:
#             return match_percentage >= 60
#     except Exception as e:
#         error_msg = f"Error in is_client_request: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#         return False

# @client.on(events.NewMessage)
# async def handler(event):
#     try:
#         message_text = event.message.message or ''
#         # Ensure event.chat_id has -100 prefix for comparison
#         chat_id = int(f"-100{abs(event.chat_id)}" if event.chat_id >= 0 else str(event.chat_id))
#         if chat_id in source_ids and len(message_text) < 70:
#             if await is_client_request(message_text):
#                 sender = await event.get_sender()
#                 username = sender.username if sender.username else f"tg://user?id={sender.id}"
#                 username_display = f"@{sender.username}" if sender.username else f"UserID: {sender.id}"
#                 phone = sender.phone if sender.phone else "Noma'lum"
#                 chat = await event.get_chat()
#                 group_name = chat.title if chat.title else "Unknown Group"
#                 group_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{event.message.id}"
#                 message_time = event.message.date
#                 formatted_time = message_time.strftime("%Y-%m-%d %H:%M:%S")
#                 formatted_message = (
#                     "🚖 Yangi Taksi So'rovi\n"
#                     f"👤 Kimdan: [{username_display}]({username})\n"
#                     f"📞 Telefon: {phone}\n"
#                     f"🏢 Guruh: {group_name} ([Manba]({group_link}))\n"
#                     f"🕒 Vaqt: {formatted_time}\n"
#                     f"💬 Xabar: {message_text}"
#                 )
#                 for dest_id in destination_ids:
#                     print(f"Sending to {dest_id}")  # Debug
#                     await client.send_message(dest_id, formatted_message, parse_mode='markdown', link_preview=False)
#     except Exception as e:
#         error_msg = f"Error in message handler: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")

# async def config_poller():
#     try:
#         last_modified = os.path.getmtime('config.json')
#         while True:
#             await asyncio.sleep(10)
#             current_modified = os.path.getmtime('config.json')
#             if current_modified != last_modified:
#                 load_config()
#                 last_modified = current_modified
#     except Exception as e:
#         error_msg = f"Error in config poller: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#         raise

# async def user_bot_main():
#     try:
#         await client.start()
#         print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
#         asyncio.create_task(config_poller())
#         await client.run_until_disconnected()
#     except Exception as e:
#         error_msg = f"User bot failed: {str(e)}"
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         if bot and SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
#         raise

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(user_bot_main())


import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat, User
from telethon.errors import SessionPasswordNeededError, ApiIdInvalidError, AuthKeyUnregisteredError
from rapidfuzz import process, fuzz
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import time

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
config = None
source_ids = []
destination_ids = []
ad_keywords = set()
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
        error_msg = f"Error reading config.json in user_bot: {str(e)}"
        with open('error.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️"))
        raise
    
from telethon.tl.types import Channel, Chat

async def fetch_my_groups_with_id(client):
    my_groups = {}

    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        # Include megagroups and normal groups
        if isinstance(entity, Channel) and entity.megagroup:
            group_id = entity.id
            name = entity.title
            id_str = f"-100{group_id}"
            if entity.username:
                link = f"https://t.me/{entity.username}"
                my_groups[id_str] = f"[{name}]({link})"
            else:
                my_groups[id_str] = f"[{name}](Havola yo'q)"
        elif isinstance(entity, Chat):  # classic group
            group_id = entity.id
            name = entity.title
            id_str = str(group_id)
            my_groups[id_str] = f"[{name}](Classic group - no link)"

    return my_groups


async def get_groups_dict():
    await client.start()
    my_groups = await fetch_my_groups_with_id(client)
    return my_groups   

def get_static_groups():
    return my_groups

# Load initial configuration
def load_config():
    global config, source_ids, destination_ids, ad_keywords, keywords
    try:
        config = read_config()
        source_ids = [int(f"-100{abs(id)}" if int(id) >= 0 else str(id)) for id in config.get('sources', {}).keys()]
        destination_ids = [int(f"-100{abs(id)}" if int(id) >= 0 else str(id)) for id in config.get('destinations', {}).keys()]
        keywords = [key for key in config['keywords']]
    except Exception as e:
        error_msg = f"Error loading config in user_bot: {str(e)}"
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
    if not message:
        return False
    if len(message) > 70:
        return False
    words = message.split()
    if not words:
        return False
    try:
        loop = asyncio.get_event_loop()
        matched_words = await loop.run_in_executor(None, lambda: sum(1 for word in words if process.extractOne(word, keywords, scorer=fuzz.partial_ratio, score_cutoff=80)))
        total_words = len(words)
        match_percentage = (matched_words / total_words) * 100 if total_words > 0 else 0
        if total_words == 1:
            return matched_words == 1
        if total_words <= 8:
            return matched_words >= 2 and match_percentage >= 50
        elif total_words > 9:
            return match_percentage >= 60
    except Exception as e:
        error_msg = f"Error in is_client_request: {str(e)}"
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        return False

@client.on(events.NewMessage)
async def handler(event):
    try:
        message_text = event.message.message or ''
        chat_id = int(f"-100{abs(event.chat_id)}" if event.chat_id >= 0 else str(event.chat_id))
        if chat_id in source_ids and len(message_text) <= 70:
            if await is_client_request(message_text):
                sender = await event.get_sender()
                username = sender.username if sender.username else f"tg://user?id={sender.id}"
                username_display = f"@{sender.username}" if sender.username else f"UserID: {sender.id}"
                phone = sender.phone if sender.phone else "Noma'lum"
                chat = await event.get_chat()
                group_name = chat.title if chat.title else "Unknown Group"
                group_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{event.message.id}"
                message_time = event.message.date
                formatted_time = message_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_message = (
                    "🚖 Yangi Taksi So'rovi\n"
                    f"👤 Kimdan: [{username_display}]({username})\n"
                    f"📞 Telefon: {phone}\n"
                    f"🏢 Guruh: {group_name} ([Manba]({group_link}))\n"
                    f"🕒 Vaqt: {formatted_time}\n"
                    f"💬 Xabar: {message_text}"
                )
                print(destination_ids)
                
                for dest_id in destination_ids:
                    try:
                        # Strip -100 prefix for sending
                        send_id = int(str(dest_id).replace("-100", "-"))
                        entity = await client.get_entity(dest_id)
                        print(dest_id)
                        print(f"Sending to {dest_id}")
                        await client.send_message(entity, formatted_message, parse_mode='markdown', link_preview=False)
                    except Exception as e:
                        print(f"Eroor: {e}")
                    
    except Exception as e:
        error_msg = f"Error in message handler: {str(e)}"
        print(error_msg)
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
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
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        raise

async def user_bot_main():
    try:
        await client.start()
        print("User bot ishga tushdi va xabarlarni kuzatmoqda...")
        asyncio.create_task(config_poller())
        asyncio.create_task(fetch_my_groups_with_id(client))
        await client.run_until_disconnected()
    except Exception as e:
        error_msg = f"User bot failed: {str(e)}"
        with open('error.log', 'a') as log_file:
            log_file.write(f"{error_msg}\n")
        if bot and SUPERADMIN:
            await bot.send_message(SUPERADMIN, f"🚨 UserBot: {error_msg} ⚠️")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(user_bot_main())