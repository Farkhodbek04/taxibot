'''First eddition'''

# import json
# import os
# from aiogram import Bot, Dispatcher
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# from aiogram.filters import CommandStart
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from dotenv import load_dotenv
# from telethon import TelegramClient
# from telethon.tl.types import Channel

# # Load environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
# API_ID = os.getenv("API_ID")
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = os.getenv("SESSION_NAME")
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# # Initialize Telethon client
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Initialize bot and dispatcher with FSM storage
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

# # Telegram message character limit
# MAX_MESSAGE_LENGTH = 4096

# # Define states for handling input
# class ConfigStates(StatesGroup):
#     ADDING_SOURCE = State()
#     ADDING_DESTINATION = State()
#     ADDING_KEYWORD = State()

# # Load and save config
# def load_config():
#     with open('config.json', 'r') as file:
#         return json.load(file)

# def save_config(config):
#     with open('config.json', 'w') as file:
#         json.dump(config, file, indent=4)
#     # Create signal file to trigger reload in userbot
#     with open('reload_config.txt', 'w') as file:
#         file.write("reload")

# # Get group info (id, title, username) for a list of group IDs with monospace IDs
# async def get_group_info(group_ids):
#     group_info = []
#     async with client:
#         for group_id in group_ids:
#             try:
#                 entity = await client.get_entity(group_id)
#                 if isinstance(entity, Channel):
#                     username = f"@{entity.username}" if entity.username else ""
#                     # Format ID in monospace
#                     group_info.append(f"`{group_id}` - {entity.title} {username}".strip())
#                 else:
#                     group_info.append(f"`{group_id}` - Unknown Group")
#             except Exception:
#                 group_info.append(f"`{group_id}` - Unknown Group")
#     return group_info

# # Get all groups the user is part of, excluding those in specified IDs, with monospace IDs
# async def get_available_groups(exclude_ids):
#     groups = []
#     async with client:
#         async for dialog in client.iter_dialogs():
#             if isinstance(dialog.entity, Channel) and dialog.entity.megagroup:
#                 group_id = -dialog.entity.id  # Telegram group IDs are negative
#                 if group_id not in exclude_ids:
#                     entity = dialog.entity
#                     username = f"@{entity.username}" if entity.username else ""
#                     # Format ID in monospace
#                     groups.append(f"`{group_id}` - {entity.title} {username}".strip())
#     return groups

# # Split a long message into parts
# def split_message(text, max_length=MAX_MESSAGE_LENGTH):
#     lines = text.split('\n')
#     messages = []
#     current_message = []
#     current_length = 0

#     for line in lines:
#         if current_length + len(line) + 1 > max_length:
#             messages.append('\n'.join(current_message))
#             current_message = [line]
#             current_length = len(line) + 1
#         else:
#             current_message.append(line)
#             current_length += len(line) + 1

#     if current_message:
#         messages.append('\n'.join(current_message))

#     return messages

# # Initial config load
# config = load_config()

# # Inline keyboard markup for main menu
# main_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Ko'rish 📊", callback_data="view")],
#     [InlineKeyboardButton(text="Qo'shish ➕", callback_data="add")],
#     [InlineKeyboardButton(text="O'chirish ❌", callback_data="delete")]
# ])

# # Inline keyboard for selecting category to add
# add_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="add_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="add_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="add_keywords")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Inline keyboard for selecting category to delete
# delete_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="delete_select_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="delete_select_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="delete_select_keywords")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Handler for /start command
# @dp.message(CommandStart())
# async def send_welcome(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await message.reply("Admin botga xush kelibsiz! 😊 Quyidagi opsiyalardan birini tanlang:", reply_markup=main_menu)

# # Handler for "Ko'rish" (View)
# @dp.callback_query(lambda c: c.data == "view")
# async def process_view(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     config = load_config()
#     sources = await get_group_info(config['sources']) or ["Hech narsa yo'q"]
#     destinations = await get_group_info(config['destinations']) or ["Hech narsa yo'q"]
#     keywords = config['keywords'] or ["Hech narsa yo'q"]
#     sources_text = '\n'.join(sources)
#     destinations_text = '\n'.join(destinations)
#     keywords_text = '\n'.join(keywords)
    
#     # Combine the message with Uzbek bold titles and emojis
#     full_message = f"**Manbalar 📋**:\n{sources_text}\n\n**Manzillar 🏠**:\n{destinations_text}\n\n**Kalit so'zlar 🔍**:\n{keywords_text}"
    
#     # Split if necessary
#     messages = split_message(full_message)
    
#     await callback_query.answer()
#     for i, msg in enumerate(messages):
#         # Only the last message should have the reply markup
#         reply_markup = main_menu if i == len(messages) - 1 else None
#         await bot.send_message(
#             callback_query.from_user.id,
#             msg,
#             reply_markup=reply_markup,
#             parse_mode="Markdown"
#         )

# # Handler for "Qo'shish" (Add)
# @dp.callback_query(lambda c: c.data == "add")
# async def process_add(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Nima qo'shmoqchisiz? 😊 Kategoriyani tanlang:",
#         reply_markup=add_category_menu
#     )

# # Handler for selecting category to add
# @dp.callback_query(lambda c: c.data.startswith("add_"))
# async def process_add_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     category = callback_query.data.replace("add_", "")
#     category_map = {
#         "sources": ("manbalar", ConfigStates.ADDING_SOURCE),
#         "destinations": ("manzillar", ConfigStates.ADDING_DESTINATION),
#         "keywords": ("kalit so'zlar", ConfigStates.ADDING_KEYWORD)
#     }
#     category_key, state_name = category_map.get(category, ("", None))
#     if not state_name:
#         return
#     await callback_query.answer()
#     await state.set_state(state_name)
    
#     if category_key in ["manbalar", "manzillar"]:
#         # Get groups excluding only those in the relevant category
#         exclude_ids = set(config['sources'] if category_key == "manbalar" else config['destinations'])
#         available_groups = await get_available_groups(exclude_ids)
#         groups_text = '\n'.join(available_groups) or "Mavjud guruhlar yo'q"
#         prompt = (f"Iltimos, **{category_key.capitalize()} 📋** qo'shish uchun guruh ID sini kiriting (masalan, -1001234567890). 😊\n"
#                   f"Sizning mavjud guruhlaringiz:\n\n{groups_text}")
        
#         # Split the prompt into parts if it's too long
#         messages = split_message(prompt)
        
#         for i, msg in enumerate(messages):
#             # Only the last message should have the reply markup
#             reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]) if i == len(messages) - 1 else None
#             await bot.send_message(
#                 callback_query.from_user.id,
#                 msg,
#                 reply_markup=reply_markup,
#                 parse_mode="Markdown"
#             )
#     else:
#         prompt = f"**{category_key.capitalize()} 🔍** qo'shish uchun qiymat yuboring (masalan, 'toshkent'): 😊"
#         await bot.send_message(
#             callback_query.from_user.id,
#             prompt,
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]),
#             parse_mode="Markdown"
#         )

# # Handler for adding sources
# @dp.message(ConfigStates.ADDING_SOURCE)
# async def add_source(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     try:
#         value = int(value)
#         if value >= 0:
#             raise ValueError("Group ID must be a negative number")
#         if value not in config['sources']:
#             config['sources'].append(value)
#             save_config(config)
#             await message.reply(f"✅ **Manbalar 📋** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding destinations
# @dp.message(ConfigStates.ADDING_DESTINATION)
# async def add_destination(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     try:
#         value = int(value)
#         if value >= 0:
#             raise ValueError("Group ID must be a negative number")
#         if value not in config['destinations']:
#             config['destinations'].append(value)
#             save_config(config)
#             await message.reply(f"✅ **Manzillar 🏠** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding keywords
# @dp.message(ConfigStates.ADDING_KEYWORD)
# async def add_keyword(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     if value not in config['keywords']:
#         config['keywords'].append(value)
#         save_config(config)
#         await message.reply(f"✅ **Kalit so'zlar 🔍** ga '{value}' qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#     else:
#         await message.reply(f"⚠️ '{value}' allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "O'chirish" (Delete)
# @dp.callback_query(lambda c: c.data == "delete")
# async def process_delete(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Nimani o'chirmoqchisiz? 😊 Kategoriyani tanlang:",
#         reply_markup=delete_category_menu
#     )

# # Handler for selecting category to delete
# @dp.callback_query(lambda c: c.data.startswith("delete_select_"))
# async def process_delete_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     config = load_config()
#     category = callback_query.data.replace("delete_select_", "")
#     category_map = {
#         "sources": "manbalar",
#         "destinations": "manzillar",
#         "keywords": "kalit so'zlar"
#     }
#     category_key = category_map.get(category)
#     if not category_key:
#         return
#     await callback_query.answer()

#     items = config[category]
#     if not items:
#         await bot.send_message(
#             callback_query.from_user.id,
#             f"⚠️ **{category_key.capitalize()} 📋🏠🔍** da hech narsa yo'q!",
#             reply_markup=main_menu,
#             parse_mode="Markdown"
#         )
#         return

#     delete_menu = InlineKeyboardMarkup(inline_keyboard=[])
#     if category_key in ["manbalar", "manzillar"]:
#         item_texts = await get_group_info(items)
#         for item_text in item_texts:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=item_text, callback_data=f"delete_{category}_{item_text.split('`')[1].strip('`')}")])
#     else:
#         for item in items:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=str(item), callback_data=f"delete_{category}_{item}")])
#     delete_menu.inline_keyboard.append([InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")])
    
#     await bot.send_message(
#         callback_query.from_user.id,
#         f"**{category_key.capitalize()} 📋🏠🔍** dan o'chirish uchun tanlang: 😊",
#         reply_markup=delete_menu,
#         parse_mode="Markdown"
#     )

# # Handler for deleting items
# @dp.callback_query(lambda c: c.data.startswith("delete_"))
# async def process_delete_item(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     parts = callback_query.data.split("_")
#     if len(parts) != 3:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#         return

#     _, category, item = parts
#     try:
#         item = int(item) if category in ["sources", "destinations"] else item
#         if item in config[category]:
#             config[category].remove(item)
#             save_config(config)
#             category_map = {
#                 "sources": "Manbalar",
#                 "destinations": "Manzillar",
#                 "keywords": "Kalit so'zlar"
#             }
#             category_name = category_map.get(category, category)
#             await callback_query.answer(f"✅ {category_name} dan `{item}` o'chirildi!")
#             await bot.send_message(
#                 callback_query.from_user.id,
#                 "Muvaffaqiyatli o'chirildi! ✅",
#                 reply_markup=main_menu
#             )
#         else:
#             await callback_query.answer("Element topilmadi! ⚠️")
#             await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#     except Exception as e:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)

# # Handler for "Orqaga" (Back)
# @dp.callback_query(lambda c: c.data == "back_to_main")
# async def process_back(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await callback_query.answer()
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Asosiy menyuga qaytdingiz! 🎉",
#         reply_markup=main_menu
#     )

# # Run the bot with error logging to super admin
# async def main():
#     try:
#         # Start Telethon client
#         await client.start()
#         await dp.start_polling(bot)
#     except Exception as e:
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"Error: {str(e)}\n")
#         if SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨Botda xatolik yuz berdi: {str(e)} ⚠️")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())

'''Second eddition'''

# import json
# import os
# from aiogram import Bot, Dispatcher
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# from aiogram.filters import CommandStart, Command
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from dotenv import load_dotenv
# from telethon import TelegramClient
# from telethon.tl.types import Channel

# # Load environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
# API_ID = os.getenv("API_ID")
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = "admin_session"
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# # Initialize Telethon client
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Initialize bot and dispatcher with FSM storage
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

# # Telegram message character limit
# MAX_MESSAGE_LENGTH = 4096

# # Define states for handling input
# class ConfigStates(StatesGroup):
#     ADDING_SOURCE = State()
#     ADDING_DESTINATION = State()
#     ADDING_KEYWORD = State()
#     ADDING_ADMIN = State()

# # Load and save config
# def load_config():
#     try:
#         with open('config.json', 'r') as file:
#             config = json.load(file)
#             # Initialize admins key if not present, using ADMIN_IDS from .env as fallback
#             if "admins" not in config:
#                 config["admins"] = ADMIN_IDS
#             return config
#     except FileNotFoundError:
#         # Create default config if file doesn't exist
#         config = {
#             "sources": [],
#             "destinations": [],
#             "keywords": [],
#             "admins": ADMIN_IDS
#         }
#         save_config(config)
#         return config

# def save_config(config):
#     with open('config.json', 'w') as file:
#         json.dump(config, file, indent=4)
#     # Create signal file to trigger reload in userbot
#     with open('reload_config.txt', 'w') as file:
#         file.write("reload")

# # Get group info (id, title, username) for a list of group IDs with monospace IDs
# from telethon.tl.types import Channel, Chat

# # Get group info (id, title, username/link) for a list of group IDs with monospace IDs
# async def get_group_info(group_ids):
#     group_info = []
#     async with client:
#         for group_id in group_ids:
#             try:
#                 entity = await client.get_entity(group_id)

#                 if isinstance(entity, Channel):
#                     # Supergroup or channel
#                     if entity.username:
#                         # Public supergroup or channel
#                         link = f"@{entity.username}"
#                     else:
#                         # Private supergroup → use /c/ link format
#                         stripped_id = str(group_id).replace("-100", "")
#                         link = f"[Link](https://t.me/c/{stripped_id}/1)"  # message ID 1 assumed
#                     group_info.append(f"`{group_id}` - {entity.title} {link}".strip())

#                 elif isinstance(entity, Chat):
#                     # Basic group (no link or username)
#                     group_info.append(f"`{group_id}` - {entity.title} (Oddiy guruh — havola yo'q)")

#                 else:
#                     group_info.append(f"`{group_id}` - Noma'lum guruh turi")

#             except Exception as e:
#                 group_info.append(f"`{group_id}` - Noma'lum guruh (xato: {str(e)})")

#     return group_info


# # Get all groups the user is part of, excluding those in specified IDs, with monospace IDs
# async def get_available_groups(exclude_ids):
#     groups = []
#     async with client:
#         async for dialog in client.iter_dialogs():
#             if isinstance(dialog.entity, Channel) and dialog.entity.megagroup:
#                 group_id = -dialog.entity.id  # Telegram group IDs are negative
#                 if group_id not in exclude_ids:
#                     entity = dialog.entity
#                     username = f"@{entity.username}" if entity.username else ""
#                     # Format ID in monospace
#                     groups.append(f"`{group_id}` - {entity.title} {username}".strip())
#     return groups

# # Split a long message into parts
# def split_message(text, max_length=MAX_MESSAGE_LENGTH):
#     lines = text.split('\n')
#     messages = []
#     current_message = []
#     current_length = 0

#     for line in lines:
#         if current_length + len(line) + 1 > max_length:
#             messages.append('\n'.join(current_message))
#             current_message = [line]
#             current_length = len(line) + 1
#         else:
#             current_message.append(line)
#             current_length += len(line) + 1

#     if current_message:
#         messages.append('\n'.join(current_message))

#     return messages

# # Initial config load
# config = load_config()
# ADMIN_IDS = config.get("admins", ADMIN_IDS)  # Update ADMIN_IDS from config.json

# # Inline keyboard markup for main menu
# main_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Ko'rish 📊", callback_data="view")],
#     [InlineKeyboardButton(text="Qo'shish ➕", callback_data="add")],
#     [InlineKeyboardButton(text="O'chirish ❌", callback_data="delete")]
# ])

# # Inline keyboard for selecting category to add
# add_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="add_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="add_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="add_keywords")],
#     [InlineKeyboardButton(text="Admin qo'shish 👮", callback_data="add_admin")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Inline keyboard for selecting category to delete
# delete_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="delete_select_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="delete_select_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="delete_select_keywords")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Handler for /start command
# @dp.message(CommandStart())
# async def send_welcome(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await message.reply("Admin botga xush kelibsiz! 😊 Quyidagi opsiyalardan birini tanlang:", reply_markup=main_menu)

# # Handler for /addadmin command
# @dp.message(Command("addadmin"))
# async def process_add_admin(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id != SUPERADMIN:
#         await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.set_state(ConfigStates.ADDING_ADMIN)
#     await message.reply("Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")

# # Handler for adding admin ID
# @dp.message(ConfigStates.ADDING_ADMIN)
# async def add_admin(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id != SUPERADMIN:
#         await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#         return
#     global config, ADMIN_IDS
#     new_admin_id = message.text.strip()
#     try:
#         new_admin_id = int(new_admin_id)
#         if new_admin_id not in config["admins"]:
#             config["admins"].append(new_admin_id)
#             ADMIN_IDS = config["admins"]  # Update the global ADMIN_IDS
#             save_config(config)
#             await message.reply(f"✅ Yangi admin ID `{new_admin_id}` qo'shildi! 👮", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{new_admin_id}` allaqachon admin! 👮", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, 123456789)! 👮", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "Ko'rish" (View)
# @dp.callback_query(lambda c: c.data == "view")
# async def process_view(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     config = load_config()
#     sources = await get_group_info(config['sources']) or ["Hech narsa yo'q"]
#     destinations = await get_group_info(config['destinations']) or ["Hech narsa yo'q"]
#     keywords = config['keywords'] or ["Hech narsa yo'q"]
#     sources_text = '\n'.join(sources)
#     destinations_text = '\n'.join(destinations)
#     keywords_text = '\n'.join(keywords)
    
#     # Combine the message with Uzbek bold titles and emojis
#     full_message = f"**Manbalar 📋**:\n{sources_text}\n\n**Manzillar 🏠**:\n{destinations_text}\n\n**Kalit so'zlar 🔍**:\n{keywords_text}"
    
#     # Split if necessary
#     messages = split_message(full_message)
    
#     await callback_query.answer()
#     for i, msg in enumerate(messages):
#         # Only the last message should have the reply markup
#         reply_markup = main_menu if i == len(messages) - 1 else None
#         await bot.send_message(
#             callback_query.from_user.id,
#             msg,
#             reply_markup=reply_markup,
#             parse_mode="Markdown"
#         )

# # Handler for "Qo'shish" (Add)
# @dp.callback_query(lambda c: c.data == "add")
# async def process_add(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Nima qo'shmoqchisiz? 😊 Kategoriyani tanlang:",
#         reply_markup=add_category_menu
#     )

# # Handler for selecting category to add
# @dp.callback_query(lambda c: c.data.startswith("add_"))
# async def process_add_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     category = callback_query.data.replace("add_", "")
#     category_map = {
#         "sources": ("manbalar", ConfigStates.ADDING_SOURCE),
#         "destinations": ("manzillar", ConfigStates.ADDING_DESTINATION),
#         "keywords": ("kalit so'zlar", ConfigStates.ADDING_KEYWORD),
#         "admin": ("admin", ConfigStates.ADDING_ADMIN)
#     }
#     category_key, state_name = category_map.get(category, ("", None))
#     if not state_name:
#         return
#     await callback_query.answer()
#     await state.set_state(state_name)
    
#     if category_key in ["manbalar", "manzillar"]:
#         # Get groups excluding only those in the relevant category
#         exclude_ids = set(config['sources'] if category_key == "manbalar" else config['destinations'])
#         available_groups = await get_available_groups(exclude_ids)
#         groups_text = '\n'.join(available_groups) or "Mavjud guruhlar yo'q"
#         prompt = (f"Iltimos, **{category_key.capitalize()} 📋** qo'shish uchun guruh ID sini kiriting (masalan, -1001234567890). 😊\n"
#                   f"Sizning mavjud guruhlaringiz:\n\n{groups_text}")
        
#         # Split the prompt into parts if it's too long
#         messages = split_message(prompt)
        
#         for i, msg in enumerate(messages):
#             # Only the last message should have the reply markup
#             reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]) if i == len(messages) - 1 else None
#             await bot.send_message(
#                 callback_query.from_user.id,
#                 msg,
#                 reply_markup=reply_markup,
#                 parse_mode="Markdown"
#             )
#     else:
#         if category_key == "admin":
#             if user_id != SUPERADMIN:
#                 await bot.send_message(user_id, "Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#                 return
#             await bot.send_message(user_id, "Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")
#         else:
#             prompt = f"**{category_key.capitalize()} 🔍** qo'shish uchun qiymat yuboring (masalan, 'toshkent'): 😊"
#             await bot.send_message(
#                 callback_query.from_user.id,
#                 prompt,
#                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]),
#                 parse_mode="Markdown"
#             )

# # Handler for adding sources
# @dp.message(ConfigStates.ADDING_SOURCE)
# async def add_source(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     try:
#         value = int(value)
#         if value >= 0:
#             raise ValueError("Group ID must be a negative number")
#         if value not in config['sources']:
#             config['sources'].append(value)
#             save_config(config)
#             await message.reply(f"✅ **Manbalar 📋** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding destinations
# @dp.message(ConfigStates.ADDING_DESTINATION)
# async def add_destination(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     try:
#         value = int(value)
#         if value >= 0:
#             raise ValueError("Group ID must be a negative number")
#         if value not in config['destinations']:
#             config['destinations'].append(value)
#             save_config(config)
#             await message.reply(f"✅ **Manzillar 🏠** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding keywords
# @dp.message(ConfigStates.ADDING_KEYWORD)
# async def add_keyword(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     if value not in config['keywords']:
#         config['keywords'].append(value)
#         save_config(config)
#         await message.reply(f"✅ **Kalit so'zlar 🔍** ga '{value}' qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#     else:
#         await message.reply(f"⚠️ '{value}' allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "O'chirish" (Delete)
# @dp.callback_query(lambda c: c.data == "delete")
# async def process_delete(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Nimani o'chirmoqchisiz? 😊 Kategoriyani tanlang:",
#         reply_markup=delete_category_menu
#     )

# # Handler for selecting category to delete
# @dp.callback_query(lambda c: c.data.startswith("delete_select_"))
# async def process_delete_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     config = load_config()
#     category = callback_query.data.replace("delete_select_", "")
#     category_map = {
#         "sources": "manbalar",
#         "destinations": "manzillar",
#         "keywords": "kalit so'zlar"
#     }
#     category_key = category_map.get(category)
#     if not category_key:
#         return
#     await callback_query.answer()

#     items = config[category]
#     if not items:
#         await bot.send_message(
#             callback_query.from_user.id,
#             f"⚠️ **{category_key.capitalize()} 📋🏠🔍** da hech narsa yo'q!",
#             reply_markup=main_menu,
#             parse_mode="Markdown"
#         )
#         return

#     delete_menu = InlineKeyboardMarkup(inline_keyboard=[])
#     if category_key in ["manbalar", "manzillar"]:
#         item_texts = await get_group_info(items)
#         for item_text in item_texts:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=item_text, callback_data=f"delete_{category}_{item_text.split('`')[1].strip('`')}")])
#     else:
#         for item in items:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=str(item), callback_data=f"delete_{category}_{item}")])
#     delete_menu.inline_keyboard.append([InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")])
    
#     await bot.send_message(
#         callback_query.from_user.id,
#         f"**{category_key.capitalize()} 📋🏠🔍** dan o'chirish uchun tanlang: 😊",
#         reply_markup=delete_menu,
#         parse_mode="Markdown"
#     )

# # Handler for deleting items
# @dp.callback_query(lambda c: c.data.startswith("delete_"))
# async def process_delete_item(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     parts = callback_query.data.split("_")
#     if len(parts) != 3:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#         return

#     _, category, item = parts
#     try:
#         item = int(item) if category in ["sources", "destinations"] else item
#         if item in config[category]:
#             config[category].remove(item)
#             save_config(config)
#             category_map = {
#                 "sources": "Manbalar",
#                 "destinations": "Manzillar",
#                 "keywords": "Kalit so'zlar"
#             }
#             category_name = category_map.get(category, category)
#             await callback_query.answer(f"✅ {category_name} dan `{item}` o'chirildi!")
#             await bot.send_message(
#                 callback_query.from_user.id,
#                 "Muvaffaqiyatli o'chirildi! ✅",
#                 reply_markup=main_menu
#             )
#         else:
#             await callback_query.answer("Element topilmadi! ⚠️")
#             await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#     except Exception as e:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)

# # Handler for "Orqaga" (Back)
# @dp.callback_query(lambda c: c.data == "back_to_main")
# async def process_back(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await callback_query.answer()
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Asosiy menyuga qaytdingiz! 🎉",
#         reply_markup=main_menu
#     )

# # Run the bot with error logging to super admin
# async def main():
#     try:
#         # Start Telethon client
#         await client.start()
#         await dp.start_polling(bot)
#     except Exception as e:
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"Error: {str(e)}\n")
#         if SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨Botda xatolik yuz berdi: {str(e)} ⚠️")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())


# import json
# import os
# from aiogram import Bot, Dispatcher
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# from aiogram.filters import CommandStart, Command
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from dotenv import load_dotenv
# from telethon import TelegramClient
# from telethon.tl.types import Channel

# # Load environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
# API_ID = os.getenv("API_ID")
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = "admin_session"
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# # Initialize Telethon client
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Initialize bot and dispatcher with FSM storage
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

# # Telegram message character limit
# MAX_MESSAGE_LENGTH = 4096

# # Define states for handling input
# class ConfigStates(StatesGroup):
#     ADDING_SOURCE = State()
#     ADDING_DESTINATION = State()
#     ADDING_KEYWORD = State()
#     ADDING_ADMIN = State()

# # Load and save config
# def load_config():
#     try:
#         with open('config.json', 'r') as file:
#             config = json.load(file)
#             # Ensure all IDs have -100 prefix
#             for key in ['sources', 'destinations']:
#                 config[key] = [int(f"-100{abs(id)}" if id >= 0 else str(id)) for id in config.get(key, [])]
#             # Initialize admins key if not present, using ADMIN_IDS from .env as fallback
#             if "admins" not in config:
#                 config["admins"] = ADMIN_IDS
#             return config
#     except FileNotFoundError:
#         config = {
#             "sources": [],
#             "destinations": [],
#             "keywords": [],
#             "admins": ADMIN_IDS
#         }
#         save_config(config)
#         return config

# def save_config(config):
#     with open('config.json', 'w') as file:
#         json.dump(config, file, indent=4)
#     # Create signal file to trigger reload in userbot
#     with open('reload_config.txt', 'w') as file:
#         file.write("reload")

# # Get group info (id, title, username/link) for a list of group IDs with monospace IDs
# async def get_group_info(group_ids):
#     group_info = []
#     async with client:
#         for group_id in group_ids:
#             try:
#                 # Strip -100 prefix for Telethon's get_entity
#                 entity_id = int(str(group_id).replace("-100", "-"))
#                 entity = await client.get_entity(entity_id)

#                 if isinstance(entity, Channel):
#                     if entity.username:
#                         link = f"@{entity.username}"
#                     else:
#                         stripped_id = str(abs(entity_id)).replace("-100", "")
#                         link = f"[Link](https://t.me/c/{stripped_id}/1)"
#                     group_info.append(f"`{group_id}` - {entity.title} {link}".strip())
#                 elif isinstance(entity, Chat):
#                     group_info.append(f"`{group_id}` - {entity.title} (Oddiy guruh — havola yo'q)")
#                 else:
#                     group_info.append(f"`{group_id}` - Noma'lum guruh turi")
#             except Exception as e:
#                 group_info.append(f"`{group_id}` - Noma'lum guruh (xato: {str(e)})")
#     print(f"get_group_info result for {group_ids}: {group_info}")  # Debug
#     return group_info

# # Get all groups the user is part of, excluding those in specified IDs, with monospace IDs
# async def get_available_groups(exclude_ids):
#     groups = []
#     async with client:
#         async for dialog in client.iter_dialogs():
#             if isinstance(dialog.entity, Channel) and dialog.entity.megagroup:
#                 group_id = -dialog.entity.id
#                 formatted_id = int(f"-100{abs(group_id)}")
#                 if formatted_id not in exclude_ids:
#                     entity = dialog.entity
#                     username = f"@{entity.username}" if entity.username else ""
#                     groups.append(f"`{formatted_id}` - {entity.title} {username}".strip())
#     return groups

# # Split a long message into parts
# def split_message(text, max_length=MAX_MESSAGE_LENGTH):
#     lines = text.split('\n')
#     messages = []
#     current_message = []
#     current_length = 0
#     for line in lines:
#         if current_length + len(line) + 1 > max_length:
#             messages.append('\n'.join(current_message))
#             current_message = [line]
#             current_length = len(line) + 1
#         else:
#             current_message.append(line)
#             current_length += len(line) + 1
#     if current_message:
#         messages.append('\n'.join(current_message))
#     return messages

# # Initial config load
# config = load_config()
# ADMIN_IDS = config.get("admins", ADMIN_IDS)

# # Inline keyboard markup for main menu
# main_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Ko'rish 📊", callback_data="view")],
#     [InlineKeyboardButton(text="Qo'shish ➕", callback_data="add")],
#     [InlineKeyboardButton(text="O'chirish ❌", callback_data="delete")]
# ])

# # Inline keyboard for selecting category to add
# add_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="add_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="add_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="add_keywords")],
#     [InlineKeyboardButton(text="Admin qo'shish 👮", callback_data="add_admin")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Inline keyboard for selecting category to delete
# delete_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="delete_select_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="delete_select_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="delete_select_keywords")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Handler for /start command
# @dp.message(CommandStart())
# async def send_welcome(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await message.reply("Admin botga xush kelibsiz! 😊 Quyidagi opsiyalardan birini tanlang:", reply_markup=main_menu)

# # Handler for /addadmin command
# @dp.message(Command("addadmin"))
# async def process_add_admin(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id != SUPERADMIN:
#         await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.set_state(ConfigStates.ADDING_ADMIN)
#     await message.reply("Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")

# # Handler for adding admin ID
# @dp.message(ConfigStates.ADDING_ADMIN)
# async def add_admin(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id != SUPERADMIN:
#         await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#         return
#     global config, ADMIN_IDS
#     new_admin_id = message.text.strip()
#     try:
#         new_admin_id = int(new_admin_id)
#         if new_admin_id not in config["admins"]:
#             config["admins"].append(new_admin_id)
#             ADMIN_IDS = config["admins"]
#             save_config(config)
#             await message.reply(f"✅ Yangi admin ID `{new_admin_id}` qo'shildi! 👮", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{new_admin_id}` allaqachon admin! 👮", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, 123456789)! 👮", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "Ko'rish" (View)
# @dp.callback_query(lambda c: c.data == "view")
# async def process_view(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     config = load_config()
#     print(f"Config loaded: {config}")  # Debug
#     sources = await get_group_info(config['sources']) or ["Hech narsa yo'q"]
#     destinations = await get_group_info(config['destinations']) or ["Hech narsa yo'q"]
#     keywords = config['keywords'] or ["Hech narsa yo'q"]
#     sources_text = '\n'.join(sources)
#     destinations_text = '\n'.join(destinations)
#     keywords_text = '\n'.join(keywords)
#     full_message = f"**Manbalar 📋**:\n{sources_text}\n\n**Manzillar 🏠**:\n{destinations_text}\n\n**Kalit so'zlar 🔍**:\n{keywords_text}"
#     print(f"Full message: {full_message}")  # Debug
#     messages = split_message(full_message)
#     await callback_query.answer()
#     if not messages:
#         await bot.send_message(callback_query.from_user.id, "Hech narsa topilmadi! 😔", reply_markup=main_menu, parse_mode="Markdown")
#         return
#     for i, msg in enumerate(messages):
#         reply_markup = main_menu if i == len(messages) - 1 else None
#         await bot.send_message(callback_query.from_user.id, msg, reply_markup=reply_markup, parse_mode="Markdown")

# # Handler for "Qo'shish" (Add)
# @dp.callback_query(lambda c: c.data == "add")
# async def process_add(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(callback_query.from_user.id, "Nima qo'shmoqchisiz? 😊 Kategoriyani tanlang:", reply_markup=add_category_menu)

# # Handler for selecting category to add
# @dp.callback_query(lambda c: c.data.startswith("add_"))
# async def process_add_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     category = callback_query.data.replace("add_", "")
#     category_map = {
#         "sources": ("manbalar", ConfigStates.ADDING_SOURCE),
#         "destinations": ("manzillar", ConfigStates.ADDING_DESTINATION),
#         "keywords": ("kalit so'zlar", ConfigStates.ADDING_KEYWORD),
#         "admin": ("admin", ConfigStates.ADDING_ADMIN)
#     }
#     category_key, state_name = category_map.get(category, ("", None))
#     if not state_name:
#         return
#     await callback_query.answer()
#     await state.set_state(state_name)
#     if category_key in ["manbalar", "manzillar"]:
#         exclude_ids = set(config['sources'] if category_key == "manbalar" else config['destinations'])
#         available_groups = await get_available_groups(exclude_ids)
#         groups_text = '\n'.join(available_groups) or "Mavjud guruhlar yo'q"
#         prompt = f"Iltimos, **{category_key.capitalize()} 📋** qo'shish uchun guruh ID sini kiriting (masalan, -1001234567890). 😊\nSizning mavjud guruhlaringiz:\n\n{groups_text}"
#         messages = split_message(prompt)
#         for i, msg in enumerate(messages):
#             reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]) if i == len(messages) - 1 else None
#             await bot.send_message(callback_query.from_user.id, msg, reply_markup=reply_markup, parse_mode="Markdown")
#     else:
#         if category_key == "admin":
#             if user_id != SUPERADMIN:
#                 await bot.send_message(user_id, "Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#                 return
#             await bot.send_message(user_id, "Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")
#         else:
#             prompt = f"**{category_key.capitalize()} 🔍** qo'shish uchun qiymat yuboring (masalan, 'toshkent'): 😊"
#             await bot.send_message(callback_query.from_user.id, prompt, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]), parse_mode="Markdown")

# # Handler for adding sources
# @dp.message(ConfigStates.ADDING_SOURCE)
# async def add_source(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     try:
#         value = int(value)
#         # Ensure -100 prefix
#         if value >= 0:
#             value = int(f"-100{value}")
#         elif not str(value).startswith('-100'):
#             value = int(f"-100{abs(value)}")
#         if value not in config['sources']:
#             config['sources'].append(value)
#             save_config(config)
#             await message.reply(f"✅ **Manbalar 📋** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding destinations
# @dp.message(ConfigStates.ADDING_DESTINATION)
# async def add_destination(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     try:
#         value = int(value)
#         # Ensure -100 prefix
#         if value >= 0:
#             value = int(f"-100{value}")
#         elif not str(value).startswith('-100'):
#             value = int(f"-100{abs(value)}")
#         if value not in config['destinations']:
#             config['destinations'].append(value)
#             save_config(config)
#             await message.reply(f"✅ **Manzillar 🏠** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding keywords
# @dp.message(ConfigStates.ADDING_KEYWORD)
# async def add_keyword(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     value = message.text.strip()
#     if value not in config['keywords']:
#         config['keywords'].append(value)
#         save_config(config)
#         await message.reply(f"✅ **Kalit so'zlar 🔍** ga '{value}' qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#     else:
#         await message.reply(f"⚠️ '{value}' allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "O'chirish" (Delete)
# @dp.callback_query(lambda c: c.data == "delete")
# async def process_delete(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(callback_query.from_user.id, "Nimani o'chirmoqchisiz? 😊 Kategoriyani tanlang:", reply_markup=delete_category_menu)

# # Handler for selecting category to delete
# @dp.callback_query(lambda c: c.data.startswith("delete_select_"))
# async def process_delete_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     config = load_config()
#     category = callback_query.data.replace("delete_select_", "")
#     category_map = {"sources": "manbalar", "destinations": "manzillar", "keywords": "kalit so'zlar"}
#     category_key = category_map.get(category)
#     if not category_key:
#         return
#     await callback_query.answer()
#     items = config[category]
#     if not items:
#         await bot.send_message(callback_query.from_user.id, f"⚠️ **{category_key.capitalize()} 📋🏠🔍** da hech narsa yo'q!", reply_markup=main_menu, parse_mode="Markdown")
#         return
#     delete_menu = InlineKeyboardMarkup(inline_keyboard=[])
#     if category_key in ["manbalar", "manzillar"]:
#         item_texts = await get_group_info(items)
#         for item_text in item_texts:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=item_text, callback_data=f"delete_{category}_{item_text.split('`')[1].strip('`')}")])
#     else:
#         for item in items:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=str(item), callback_data=f"delete_{category}_{item}")])
#     delete_menu.inline_keyboard.append([InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")])
#     await bot.send_message(callback_query.from_user.id, f"**{category_key.capitalize()} 📋🏠🔍** dan o'chirish uchun tanlang: 😊", reply_markup=delete_menu, parse_mode="Markdown")

# # Handler for deleting items
# @dp.callback_query(lambda c: c.data.startswith("delete_"))
# async def process_delete_item(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     global config
#     parts = callback_query.data.split("_")
#     if len(parts) != 3:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#         return
#     _, category, item = parts
#     try:
#         item = int(item) if category in ["sources", "destinations"] else item
#         if item in config[category]:
#             config[category].remove(item)
#             save_config(config)
#             category_map = {"sources": "Manbalar", "destinations": "Manzillar", "keywords": "Kalit so'zlar"}
#             category_name = category_map.get(category, category)
#             await callback_query.answer(f"✅ {category_name} dan `{item}` o'chirildi!")
#             await bot.send_message(callback_query.from_user.id, "Muvaffaqiyatli o'chirildi! ✅", reply_markup=main_menu)
#         else:
#             await callback_query.answer("Element topilmadi! ⚠️")
#             await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#     except Exception as e:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)

# # Handler for "Orqaga" (Back)
# @dp.callback_query(lambda c: c.data == "back_to_main")
# async def process_back(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await callback_query.answer()
#     await bot.send_message(callback_query.from_user.id, "Asosiy menyuga qaytdingiz! 🎉", reply_markup=main_menu)

# # Run the bot with error logging to super admin
# async def main():
#     try:
#         await client.start()
#         await dp.start_polling(bot)
#     except Exception as e:
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"Error: {str(e)}\n")
#         if SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨Botda xatolik yuz berdi: {str(e)} ⚠️")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())



# import json
# import os
# import asyncio
# from aiogram import Bot, Dispatcher
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# from aiogram.filters import CommandStart, Command
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from dotenv import load_dotenv
# from telethon import TelegramClient
# from telethon.tl.types import Channel, Chat
# from telethon.errors import SessionPasswordNeededError

# # Load environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
# API_ID = os.getenv("API_ID")
# API_HASH = os.getenv("API_HASH")
# SESSION_NAME = "admin_session"
# SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# # Initialize Telethon client
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# # Initialize bot and dispatcher with FSM storage
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

# # Telegram message character limit
# MAX_MESSAGE_LENGTH = 4096

# # Caches
# group_info_cache = {}  # Cache for group info
# available_groups_cache = None  # Cache for available groups
# cache_refresh_task = None

# # Define states for handling input
# class ConfigStates(StatesGroup):
#     ADDING_SOURCE = State()
#     ADDING_DESTINATION = State()
#     ADDING_KEYWORD = State()
#     ADDING_ADMIN = State()

# # Load and save config
# def load_config():
#     try:
#         with open('config.json', 'r') as file:
#             config = json.load(file)
#             for key in ['sources', 'destinations']:
#                 config[key] = [int(f"-100{abs(id)}" if id >= 0 else str(id)) for id in config.get(key, [])]
#             if "admins" not in config:
#                 config["admins"] = ADMIN_IDS
#             return config
#     except FileNotFoundError:
#         config = {
#             "sources": [],
#             "destinations": [],
#             "keywords": [],
#             "admins": ADMIN_IDS
#         }
#         save_config(config)
#         return config

# def save_config(config):
#     try:
#         print(f"Saving config: {config}")
#         with open('config.json', 'w') as file:
#             json.dump(config, file, indent=4)
#         with open('reload_config.txt', 'w') as file:
#             file.write("reload")
#     except Exception as e:
#         print(f"Error saving config: {str(e)}")
#         raise

# # Refresh available groups cache in background
# async def refresh_available_groups_cache():
#     global available_groups_cache
#     while True:
#         try:
#             async with client:
#                 groups = []
#                 async for dialog in client.iter_dialogs():
#                     if isinstance(dialog.entity, Channel) and dialog.entity.megagroup:
#                         group_id = -dialog.entity.id
#                         formatted_id = int(f"-100{abs(group_id)}")
#                         entity = dialog.entity
#                         username = f"@{entity.username}" if entity.username else ""
#                         groups.append(f"`{formatted_id}` - {entity.title} {username}".strip())
#                     elif isinstance(dialog.entity, Chat):
#                         group_id = -dialog.entity.id
#                         formatted_id = int(f"-100{abs(group_id)}")
#                         entity = dialog.entity
#                         groups.append(f"`{formatted_id}` - {entity.title} (Oddiy guruh — havola yo'q)".strip())
#                 available_groups_cache = groups
#                 print(f"Refreshed available groups cache: {available_groups_cache}")
#         except Exception as e:
#             print(f"Error refreshing cache: {str(e)}")
#         await asyncio.sleep(300)  # Refresh every 5 minutes

# # Get group info (id, title, username/link) for a list of group IDs with monospace IDs
# async def get_group_info(group_ids):
#     group_info = []
#     tasks = []

#     async def fetch_group_info(group_id):
#         if group_id in group_info_cache:
#             return group_info_cache[group_id]
#         try:
#             # Ensure client is connected
#             if not client.is_connected():
#                 await client.connect()
#             # Strip -100 prefix for Telethon's get_entity
#             entity_id = int(str(group_id).replace("-100", "-"))
#             entity = await client.get_entity(entity_id)
#             if isinstance(entity, Channel):
#                 if entity.username:
#                     link = f"@{entity.username}"
#                 else:
#                     stripped_id = str(abs(entity_id))
#                     link = f"[Link](https://t.me/c/{stripped_id}/1)"
#                 result = f"`{group_id}` - {entity.title} {link}".strip()
#             elif isinstance(entity, Chat):
#                 result = f"`{group_id}` - {entity.title} (Oddiy guruh — havola yo'q)"
#             else:
#                 result = f"`{group_id}` - Noma'lum guruh turi"
#             group_info_cache[group_id] = result
#             return result
#         except Exception as e:
#             result = f"`{group_id}` - Noma'lum guruh (xato: {str(e)})"
#             group_info_cache[group_id] = result
#             return result

#     for group_id in group_ids:
#         tasks.append(fetch_group_info(group_id))
    
#     results = await asyncio.gather(*tasks, return_exceptions=True)
#     for result in results:
#         if isinstance(result, str):
#             group_info.append(result)
#         else:
#             group_info.append(f"`{group_id}` - Noma'lum guruh (xato: {str(result)})")
    
#     print(f"get_group_info result for {group_ids}: {group_info}")
#     return group_info

# # Get available groups from cache
# def get_available_groups(exclude_ids):
#     global available_groups_cache
#     if available_groups_cache is None:
#         print("Available groups cache not ready yet")
#         return ["Guruhlar ro'yxati yuklanmadi, ID ni qo'lda kiriting"]
#     return [group for group in available_groups_cache if int(group.split('`')[1].strip('`')) not in exclude_ids]

# # Split a long message into parts
# def split_message(text, max_length=MAX_MESSAGE_LENGTH):
#     lines = text.split('\n')
#     messages = []
#     current_message = []
#     current_length = 0
#     for line in lines:
#         if current_length + len(line) + 1 > max_length:
#             messages.append('\n'.join(current_message))
#             current_message = [line]
#             current_length = len(line) + 1
#         else:
#             current_message.append(line)
#             current_length += len(line) + 1
#     if current_message:
#         messages.append('\n'.join(current_message))
#     return messages

# # Initial config load
# config = load_config()
# ADMIN_IDS = config.get("admins", ADMIN_IDS)

# # Inline keyboard markup for main menu
# main_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Ko'rish 📊", callback_data="view")],
#     [InlineKeyboardButton(text="Qo'shish ➕", callback_data="add")],
#     [InlineKeyboardButton(text="O'chirish ❌", callback_data="delete")]
# ])

# # Inline keyboard for selecting category to add
# add_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="add_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="add_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="add_keywords")],
#     [InlineKeyboardButton(text="Admin qo'shish 👮", callback_data="add_admin")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Inline keyboard for selecting category to delete
# delete_category_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Manbalar 📋", callback_data="delete_select_sources")],
#     [InlineKeyboardButton(text="Manzillar 🏠", callback_data="delete_select_destinations")],
#     [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="delete_select_keywords")],
#     [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
# ])

# # Handler for /start command
# @dp.message(CommandStart())
# async def send_welcome(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await message.reply("Admin botga xush kelibsiz! 😊 Quyidagi opsiyalardan birini tanlang:", reply_markup=main_menu)

# # Handler for /addadmin command
# @dp.message(Command("addadmin"))
# async def process_add_admin(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id != SUPERADMIN:
#         await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.set_state(ConfigStates.ADDING_ADMIN)
#     await message.reply("Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")

# # Handler for adding admin ID
# @dp.message(ConfigStates.ADDING_ADMIN)
# async def add_admin(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id != SUPERADMIN:
#         await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     new_admin_id = message.text.strip()
#     try:
#         new_admin_id = int(new_admin_id)
#         if new_admin_id not in config["admins"]:
#             config["admins"].append(new_admin_id)
#             save_config(config)
#             await message.reply(f"✅ Yangi admin ID `{new_admin_id}` qo'shildi! 👮", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{new_admin_id}` allaqachon admin! 👮", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, 123456789)! 👮", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "Ko'rish" (View)
# @dp.callback_query(lambda c: c.data == "view")
# async def process_view(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     print(f"Config loaded: {config}")
#     sources = await get_group_info(config['sources']) or ["Hech narsa yo'q"]
#     destinations = await get_group_info(config['destinations']) or ["Hech narsa yo'q"]
#     keywords = config['keywords'] or ["Hech narsa yo'q"]
#     sources_text = '\n'.join(sources)
#     destinations_text = '\n'.join(destinations)
#     keywords_text = '\n'.join(keywords)
#     full_message = f"**Manbalar 📋**:\n{sources_text}\n\n**Manzillar 🏠**:\n{destinations_text}\n\n**Kalit so'zlar 🔍**:\n{keywords_text}"
#     print(f"Full message: {full_message}")
#     messages = split_message(full_message)
#     await callback_query.answer()
#     if not messages:
#         await bot.send_message(callback_query.from_user.id, "Hech narsa topilmadi! 😔", reply_markup=main_menu, parse_mode="Markdown")
#         return
#     for i, msg in enumerate(messages):
#         reply_markup = main_menu if i == len(messages) - 1 else None
#         await bot.send_message(callback_query.from_user.id, msg, reply_markup=reply_markup, parse_mode="Markdown")

# # Handler for "Qo'shish" (Add)
# @dp.callback_query(lambda c: c.data == "add")
# async def process_add(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(callback_query.from_user.id, "Nima qo'shmoqchisiz? 😊 Kategoriyani tanlang:", reply_markup=add_category_menu)

# # Handler for selecting category to add
# @dp.callback_query(lambda c: c.data.startswith("add_"))
# async def process_add_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     category = callback_query.data.replace("add_", "")
#     category_map = {
#         "sources": ("manbalar", ConfigStates.ADDING_SOURCE),
#         "destinations": ("manzillar", ConfigStates.ADDING_DESTINATION),
#         "keywords": ("kalit so'zlar", ConfigStates.ADDING_KEYWORD),
#         "admin": ("admin", ConfigStates.ADDING_ADMIN)
#     }
#     category_key, state_name = category_map.get(category, ("", None))
#     if not state_name:
#         return
#     await callback_query.answer()
#     await state.set_state(state_name)
#     if category_key in ["manbalar", "manzillar"]:
#         config = load_config()
#         exclude_ids = set(config['sources'] if category_key == "manbalar" else config['destinations'])
#         available_groups = get_available_groups(exclude_ids)
#         groups_text = '\n'.join(available_groups)
#         prompt = f"Iltimos, **{category_key.capitalize()} 📋** qo'shish uchun guruh ID sini kiriting (masalan, -1001234567890). 😊\nSizning mavjud guruhlaringiz:\n\n{groups_text}"
#         messages = split_message(prompt)
#         for i, msg in enumerate(messages):
#             reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]) if i == len(messages) - 1 else None
#             await bot.send_message(callback_query.from_user.id, msg, reply_markup=reply_markup, parse_mode="Markdown")
#     else:
#         if category_key == "admin":
#             if user_id != SUPERADMIN:
#                 await bot.send_message(user_id, "Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
#                 return
#             await bot.send_message(user_id, "Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")
#         else:
#             prompt = f"**{category_key.capitalize()} 🔍** qo'shish uchun qiymat yuboring (masalan, 'toshkent'): 😊"
#             await bot.send_message(callback_query.from_user.id, prompt, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]), parse_mode="Markdown")

# # Handler for adding sources
# @dp.message(ConfigStates.ADDING_SOURCE)
# async def add_source(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     value = message.text.strip()
#     try:
#         value = int(value)
#         if value >= 0:
#             value = int(f"-100{value}")
#         elif not str(value).startswith('-100'):
#             value = int(f"-100{abs(value)}")
#         if value not in config['sources']:
#             config['sources'].append(value)
#             print(f"Adding source {value}, new sources: {config['sources']}")
#             save_config(config)
#             await message.reply(f"✅ **Manbalar 📋** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding destinations
# @dp.message(ConfigStates.ADDING_DESTINATION)
# async def add_destination(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     value = message.text.strip()
#     try:
#         value = int(value)
#         if value >= 0:
#             value = int(f"-100{value}")
#         elif not str(value).startswith('-100'):
#             value = int(f"-100{abs(value)}")
#         if value not in config['destinations']:
#             config['destinations'].append(value)
#             print(f"Adding destination {value}, new destinations: {config['destinations']}")
#             save_config(config)
#             await message.reply(f"✅ **Manzillar 🏠** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#         else:
#             await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     except ValueError:
#         await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
#     await state.clear()

# # Handler for adding keywords
# @dp.message(ConfigStates.ADDING_KEYWORD)
# async def add_keyword(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id not in ADMIN_IDS:
#         await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     value = message.text.strip()
#     if value not in config['keywords']:
#         config['keywords'].append(value)
#         save_config(config)
#         await message.reply(f"✅ **Kalit so'zlar 🔍** ga '{value}' qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
#     else:
#         await message.reply(f"⚠️ '{value}' allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
#     await state.clear()

# # Handler for "O'chirish" (Delete)
# @dp.callback_query(lambda c: c.data == "delete")
# async def process_delete(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await callback_query.answer()
#     await bot.send_message(callback_query.from_user.id, "Nimani o'chirmoqchisiz? 😊 Kategoriyani tanlang:", reply_markup=delete_category_menu)

# # Handler for selecting category to delete
# @dp.callback_query(lambda c: c.data.startswith("delete_select_"))
# async def process_delete_category(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     category = callback_query.data.replace("delete_select_", "")
#     category_map = {"sources": "manbalar", "destinations": "manzillar", "keywords": "kalit so'zlar"}
#     category_key = category_map.get(category)
#     if not category_key:
#         return
#     await callback_query.answer()
#     items = config[category]
#     if not items:
#         await bot.send_message(callback_query.from_user.id, f"⚠️ **{category_key.capitalize()} 📋🏠🔍** da hech narsa yo'q!", reply_markup=main_menu, parse_mode="Markdown")
#         return
#     delete_menu = InlineKeyboardMarkup(inline_keyboard=[])
#     if category_key in ["manbalar", "manzillar"]:
#         item_texts = await get_group_info(items)
#         for item_text in item_texts:
#             item_id = item_text.split('`')[1].strip('`')
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=item_text, callback_data=f"delete_{category}_{item_id}")])
#     else:
#         for item in items:
#             delete_menu.inline_keyboard.append([InlineKeyboardButton(text=str(item), callback_data=f"delete_{category}_{item}")])
#     delete_menu.inline_keyboard.append([InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")])
#     await bot.send_message(callback_query.from_user.id, f"**{category_key.capitalize()} 📋🏠🔍** dan o'chirish uchun tanlang: 😊", reply_markup=delete_menu, parse_mode="Markdown")

# # Handler for deleting items
# @dp.callback_query(lambda c: c.data.startswith("delete_"))
# async def process_delete_item(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     config = load_config()
#     parts = callback_query.data.split("_")
#     if len(parts) != 3:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#         return
#     _, category, item = parts
#     try:
#         item = int(item) if category in ["sources", "destinations"] else item
#         if item in config[category]:
#             config[category].remove(item)
#             print(f"Deleting {item} from {category}, new {category}: {config[category]}")
#             save_config(config)
#             if item in group_info_cache:
#                 del group_info_cache[item]
#             category_map = {"sources": "Manbalar", "destinations": "Manzillar", "keywords": "Kalit so'zlar"}
#             category_name = category_map.get(category, category)
#             await callback_query.answer(f"✅ {category_name} dan `{item}` o'chirildi!")
#             await bot.send_message(callback_query.from_user.id, "Muvaffaqiyatli o'chirildi! ✅", reply_markup=main_menu)
#         else:
#             await callback_query.answer("Element topilmadi! ⚠️")
#             await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
#     except Exception as e:
#         await callback_query.answer("Xatolik yuz berdi! ⚠️")
#         await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)

# # Handler for "Orqaga" (Back)
# @dp.callback_query(lambda c: c.data == "back_to_main")
# async def process_back(callback_query: CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
#         return
#     await state.clear()
#     await callback_query.answer()
#     await bot.send_message(callback_query.from_user.id, "Asosiy menyuga qaytdingiz! 🎉", reply_markup=main_menu)

# # Run the bot with error logging to super admin
# async def main():
#     global cache_refresh_task
#     try:
#         await client.start()
#         # Start cache refresh task
#         cache_refresh_task = asyncio.create_task(refresh_available_groups_cache())
#         await dp.start_polling(bot)
#     except SessionPasswordNeededError:
#         print("2FA required. Please handle 2FA authentication manually.")
#         await client.disconnect()
#     except Exception as e:
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"Error: {str(e)}\n")
#         if SUPERADMIN:
#             await bot.send_message(SUPERADMIN, f"🚨Botda xatolik yuz berdi: {str(e)} ⚠️")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())




import json
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat
from telethon.errors import SessionPasswordNeededError

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "admin_session"
SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# Initialize Telethon client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Initialize bot and dispatcher with FSM storage
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Telegram message character limit
MAX_MESSAGE_LENGTH = 4096
MAX_GROUPS_DISPLAY = 20  # Limit to avoid entity parsing errors

# Caches
group_info_cache = {}  # Cache for group info
available_groups_cache = None  # Cache for available groups
cache_refresh_task = None

# Define states for handling input
class ConfigStates(StatesGroup):
    ADDING_SOURCE = State()
    ADDING_DESTINATION = State()
    ADDING_KEYWORD = State()
    ADDING_ADMIN = State()

# Load and save config
def load_config():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            for key in ['sources', 'destinations']:
                config[key] = [int(f"-100{abs(id)}" if id >= 0 else str(id)) for id in config.get(key, [])]
            if "admins" not in config:
                config["admins"] = ADMIN_IDS
            return config
    except FileNotFoundError:
        config = {
            "sources": [],
            "destinations": [],
            "keywords": [],
            "admins": ADMIN_IDS
        }
        save_config(config)
        return config

def save_config(config):
    try:
        print(f"Saving config: {config}")
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)
        with open('reload_config.txt', 'w') as file:
            file.write("reload")
    except Exception as e:
        print(f"Error saving config: {str(e)}")
        raise

# Refresh available groups cache in background
async def refresh_available_groups_cache():
    global available_groups_cache
    while True:
        try:
            async with client:
                groups = []
                async for dialog in client.iter_dialogs(limit=100):  # Limit to 100 to avoid overload
                    if isinstance(dialog.entity, Channel) and dialog.entity.megagroup:
                        group_id = -dialog.entity.id
                        formatted_id = int(f"-100{abs(group_id)}")
                        entity = dialog.entity
                        username = f"@{entity.username}" if entity.username else ""
                        groups.append(f"`{formatted_id}` - {entity.title} {username}".strip())
                    elif isinstance(dialog.entity, Chat):
                        group_id = -dialog.entity.id
                        formatted_id = int(f"-100{abs(group_id)}")
                        entity = dialog.entity
                        groups.append(f"`{formatted_id}` - {entity.title} (Oddiy guruh — havola yo'q)".strip())
                available_groups_cache = groups
                print(f"Refreshed available groups cache: {available_groups_cache[:5]}... (total {len(groups)})")
        except Exception as e:
            print(f"Error refreshing cache: {str(e)}")
        await asyncio.sleep(300)  # Refresh every 5 minutes

# Get group info (id, title, username/link) for a list of group IDs with monospace IDs
async def get_group_info(group_ids):
    group_info = []
    tasks = []

    async def fetch_group_info(group_id):
        if group_id in group_info_cache:
            return group_info_cache[group_id]
        try:
            if not client.is_connected():
                await client.connect()
            entity_id = int(str(group_id).replace("-100", "-"))
            entity = await client.get_entity(entity_id)
            if isinstance(entity, Channel):
                if entity.username:
                    link = f"@{entity.username}"
                else:
                    stripped_id = str(abs(entity_id))
                    link = f"[Link](https://t.me/c/{stripped_id}/1)"
                result = f"`{group_id}` - {entity.title} {link}".strip()
            elif isinstance(entity, Chat):
                result = f"`{group_id}` - {entity.title} (Oddiy guruh — havola yo'q)"
            else:
                result = f"`{group_id}` - Noma'lum guruh turi"
            group_info_cache[group_id] = result
            return result
        except Exception as e:
            result = f"`{group_id}` - Noma'lum guruh (xato: {str(e)})"
            group_info_cache[group_id] = result
            return result

    for group_id in group_ids:
        tasks.append(fetch_group_info(group_id))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, str):
            group_info.append(result)
        else:
            group_info.append(f"`{group_id}` - Noma'lum guruh (xato: {str(result)})")
    
    print(f"get_group_info result for {group_ids}: {group_info}")
    return group_info

# Get available groups from cache
def get_available_groups(exclude_ids):
    global available_groups_cache
    if available_groups_cache is None:
        print("Available groups cache not ready yet")
        return ["Guruhlar ro'yxati yuklanmadi, ID ni qo'lda kiriting (-1001234567890 formatida)"]
    return [group for group in available_groups_cache[:MAX_GROUPS_DISPLAY] if int(group.split('`')[1].strip('`')) not in exclude_ids]

# Split a long message into parts
def split_message(text, max_length=MAX_MESSAGE_LENGTH):
    lines = text.split('\n')
    messages = []
    current_message = []
    current_length = 0
    for line in lines:
        if current_length + len(line) + 1 > max_length:
            messages.append('\n'.join(current_message))
            current_message = [line]
            current_length = len(line) + 1
        else:
            current_message.append(line)
            current_length += len(line) + 1
    if current_message:
        messages.append('\n'.join(current_message))
    return messages

# Initial config load
config = load_config()
ADMIN_IDS = config.get("admins", ADMIN_IDS)

# Inline keyboard markup for main menu
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ko'rish 📊", callback_data="view")],
    [InlineKeyboardButton(text="Qo'shish ➕", callback_data="add")],
    [InlineKeyboardButton(text="O'chirish ❌", callback_data="delete")]
])

# Inline keyboard for selecting category to add
add_category_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Manbalar 📋", callback_data="add_sources")],
    [InlineKeyboardButton(text="Manzillar 🏠", callback_data="add_destinations")],
    [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="add_keywords")],
    [InlineKeyboardButton(text="Admin qo'shish 👮", callback_data="add_admin")],
    [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
])

# Inline keyboard for selecting category to delete
delete_category_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Manbalar 📋", callback_data="delete_select_sources")],
    [InlineKeyboardButton(text="Manzillar 🏠", callback_data="delete_select_destinations")],
    [InlineKeyboardButton(text="Kalit so'zlar 🔍", callback_data="delete_select_keywords")],
    [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
])

# Handler for /start command
@dp.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    await state.clear()
    await message.reply("Admin botga xush kelibsiz! 😊 Quyidagi opsiyalardan birini tanlang:", reply_markup=main_menu)

# Handler for /addadmin command
@dp.message(Command("addadmin"))
async def process_add_admin(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != SUPERADMIN:
        await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
        return
    await state.set_state(ConfigStates.ADDING_ADMIN)
    await message.reply("Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")

# Handler for adding admin ID
@dp.message(ConfigStates.ADDING_ADMIN)
async def add_admin(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != SUPERADMIN:
        await message.reply("Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    new_admin_id = message.text.strip()
    try:
        new_admin_id = int(new_admin_id)
        if new_admin_id not in config["admins"]:
            config["admins"].append(new_admin_id)
            save_config(config)
            await message.reply(f"✅ Yangi admin ID `{new_admin_id}` qo'shildi! 👮", reply_markup=main_menu, parse_mode="Markdown")
        else:
            await message.reply(f"⚠️ `{new_admin_id}` allaqachon admin! 👮", reply_markup=main_menu, parse_mode="Markdown")
    except ValueError:
        await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, 123456789)! 👮", reply_markup=main_menu, parse_mode="Markdown")
    await state.clear()

# Handler for "Ko'rish" (View)
@dp.callback_query(lambda c: c.data == "view")
async def process_view(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    print(f"Config loaded: {config}")
    sources = await get_group_info(config['sources']) or ["Hech narsa yo'q"]
    destinations = await get_group_info(config['destinations']) or ["Hech narsa yo'q"]
    keywords = config['keywords'] or ["Hech narsa yo'q"]
    sources_text = '\n'.join(sources)
    destinations_text = '\n'.join(destinations)
    keywords_text = '\n'.join(keywords)
    full_message = f"**Manbalar 📋**:\n{sources_text}\n\n**Manzillar 🏠**:\n{destinations_text}\n\n**Kalit so'zlar 🔍**:\n{keywords_text}"
    print(f"Full message: {full_message}")
    messages = split_message(full_message)
    await callback_query.answer()
    if not messages:
        await bot.send_message(callback_query.from_user.id, "Hech narsa topilmadi! 😔", reply_markup=main_menu, parse_mode="Markdown")
        return
    for i, msg in enumerate(messages):
        reply_markup = main_menu if i == len(messages) - 1 else None
        await bot.send_message(callback_query.from_user.id, msg, reply_markup=reply_markup, parse_mode="Markdown")

# Handler for "Qo'shish" (Add)
@dp.callback_query(lambda c: c.data == "add")
async def process_add(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Nima qo'shmoqchisiz? 😊 Kategoriyani tanlang:", reply_markup=add_category_menu)

# Handler for selecting category to add
@dp.callback_query(lambda c: c.data.startswith("add_"))
async def process_add_category(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    category = callback_query.data.replace("add_", "")
    category_map = {
        "sources": ("manbalar", ConfigStates.ADDING_SOURCE),
        "destinations": ("manzillar", ConfigStates.ADDING_DESTINATION),
        "keywords": ("kalit so'zlar", ConfigStates.ADDING_KEYWORD),
        "admin": ("admin", ConfigStates.ADDING_ADMIN)
    }
    category_key, state_name = category_map.get(category, ("", None))
    if not state_name:
        return
    await callback_query.answer()
    await state.set_state(state_name)
    if category_key in ["manbalar", "manzillar"]:
        config = load_config()
        exclude_ids = set(config['sources'] if category_key == "manbalar" else config['destinations'])
        available_groups = get_available_groups(exclude_ids)
        groups_text = '\n'.join(available_groups) if available_groups else "Guruhlar ro'yxati mavjud emas"
        prompt = f"Iltimos, **{category_key.capitalize()} 📋** qo'shish uchun guruh ID sini kiriting (masalan, -1001234567890). 😊\nSizning mavjud guruhlaringizning bir qismi (maksimum {MAX_GROUPS_DISPLAY} ta):\n\n{groups_text}"
        try:
            messages = split_message(prompt)
            for i, msg in enumerate(messages):
                reply_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]) if i == len(messages) - 1 else None
                await bot.send_message(callback_query.from_user.id, msg, reply_markup=reply_markup, parse_mode="Markdown")
        except TelegramBadRequest as e:
            print(f"TelegramBadRequest: {str(e)}")
            await bot.send_message(callback_query.from_user.id, f"Xatolik yuz berdi: {str(e)}. Iltimos, ID ni qo'lda kiriting (-1001234567890 formatida).", reply_markup=reply_markup, parse_mode="Markdown")
    else:
        if category_key == "admin":
            if user_id != SUPERADMIN:
                await bot.send_message(user_id, "Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
                return
            await bot.send_message(user_id, "Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")
        else:
            prompt = f"**{category_key.capitalize()} 🔍** qo'shish uchun qiymat yuboring (masalan, 'toshkent'): 😊"
            await bot.send_message(callback_query.from_user.id, prompt, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]]), parse_mode="Markdown")

# Handler for adding sources
@dp.message(ConfigStates.ADDING_SOURCE)
async def add_source(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    value = message.text.strip()
    try:
        value = int(value)
        if value >= 0:
            value = int(f"-100{value}")
        elif not str(value).startswith('-100'):
            value = int(f"-100{abs(value)}")
        if value not in config['sources']:
            config['sources'].append(value)
            print(f"Adding source {value}, new sources: {config['sources']}")
            save_config(config)
            await message.reply(f"✅ **Manbalar 📋** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
        else:
            await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
    except ValueError:
        await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
    await state.clear()

# Handler for adding destinations
@dp.message(ConfigStates.ADDING_DESTINATION)
async def add_destination(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    value = message.text.strip()
    try:
        value = int(value)
        if value >= 0:
            value = int(f"-100{value}")
        elif not str(value).startswith('-100'):
            value = int(f"-100{abs(value)}")
        if value not in config['destinations']:
            config['destinations'].append(value)
            print(f"Adding destination {value}, new destinations: {config['destinations']}")
            save_config(config)
            await message.reply(f"✅ **Manzillar 🏠** ga `{value}` qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
        else:
            await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
    except ValueError:
        await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu)
    await state.clear()

# Handler for adding keywords
@dp.message(ConfigStates.ADDING_KEYWORD)
async def add_keyword(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    value = message.text.strip()
    if value not in config['keywords']:
        config['keywords'].append(value)
        save_config(config)
        await message.reply(f"✅ **Kalit so'zlar 🔍** ga '{value}' qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
    else:
        await message.reply(f"⚠️ '{value}' allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
    await state.clear()

# Handler for "O'chirish" (Delete)
@dp.callback_query(lambda c: c.data == "delete")
async def process_delete(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Nimani o'chirmoqchisiz? 😊 Kategoriyani tanlang:", reply_markup=delete_category_menu)

# Handler for selecting category to delete
@dp.callback_query(lambda c: c.data.startswith("delete_select_"))
async def process_delete_category(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    category = callback_query.data.replace("delete_select_", "")
    category_map = {"sources": "manbalar", "destinations": "manzillar", "keywords": "kalit so'zlar"}
    category_key = category_map.get(category)
    if not category_key:
        return
    await callback_query.answer()
    items = config[category]
    if not items:
        await bot.send_message(callback_query.from_user.id, f"⚠️ **{category_key.capitalize()} 📋🏠🔍** da hech narsa yo'q!", reply_markup=main_menu, parse_mode="Markdown")
        return
    delete_menu = InlineKeyboardMarkup(inline_keyboard=[])
    if category_key in ["manbalar", "manzillar"]:
        item_texts = await get_group_info(items)
        for item_text in item_texts:
            item_id = item_text.split('`')[1].strip('`')
            delete_menu.inline_keyboard.append([InlineKeyboardButton(text=item_text, callback_data=f"delete_{category}_{item_id}")])
    else:
        for item in items:
            delete_menu.inline_keyboard.append([InlineKeyboardButton(text=str(item), callback_data=f"delete_{category}_{item}")])
    delete_menu.inline_keyboard.append([InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")])
    await bot.send_message(callback_query.from_user.id, f"**{category_key.capitalize()} 📋🏠🔍** dan o'chirish uchun tanlang: 😊", reply_markup=delete_menu, parse_mode="Markdown")

# Handler for deleting items
@dp.callback_query(lambda c: c.data.startswith("delete_"))
async def process_delete_item(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config()
    parts = callback_query.data.split("_")
    if len(parts) != 3:
        await callback_query.answer("Xatolik yuz berdi! ⚠️")
        await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
        return
    _, category, item = parts
    try:
        item = int(item) if category in ["sources", "destinations"] else item
        if item in config[category]:
            config[category].remove(item)
            print(f"Deleting {item} from {category}, new {category}: {config[category]}")
            save_config(config)
            if item in group_info_cache:
                del group_info_cache[item]
            category_map = {"sources": "Manbalar", "destinations": "Manzillar", "keywords": "Kalit so'zlar"}
            category_name = category_map.get(category, category)
            await callback_query.answer(f"✅ {category_name} dan `{item}` o'chirildi!")
            await bot.send_message(callback_query.from_user.id, "Muvaffaqiyatli o'chirildi! ✅", reply_markup=main_menu)
        else:
            await callback_query.answer("Element topilmadi! ⚠️")
            await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)
    except Exception as e:
        await callback_query.answer("Xatolik yuz berdi! ⚠️")
        await bot.send_message(callback_query.from_user.id, "Qayta urining! 😊", reply_markup=main_menu)

# Handler for "Orqaga" (Back)
@dp.callback_query(lambda c: c.data == "back_to_main")
async def process_back(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    await state.clear()
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Asosiy menyuga qaytdingiz! 🎉", reply_markup=main_menu)

# Run the bot with error logging to super admin
async def main():
    global cache_refresh_task
    try:
        await client.start()
        cache_refresh_task = asyncio.create_task(refresh_available_groups_cache())
        await dp.start_polling(bot)
    except SessionPasswordNeededError:
        print("2FA required. Please handle 2FA authentication manually.")
        await client.disconnect()
    except Exception as e:
        with open('error.log', 'a') as log_file:
            log_file.write(f"Error: {str(e)}\n")
        if SUPERADMIN:
            await bot.send_message(SUPERADMIN, f"🚨Botda xatolik yuz berdi: {str(e)} ⚠️")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())