import json
import os
import re
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

from user_bot import get_groups_dict
MAX_MESSAGE_LENGTH = 4096  # Telegram's max message length


# Load environment variables
load_dotenv()
BOT_TOKEN = "7607758454:AAF0xFJPgqi1sgjfHPsCH9Qj-CZXd65mLTw"
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "admin_session"  
SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))
CONFIG_FILE = "groups_config.json"

# Initialize bot and dispatcher with FSM storage
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def send_to_group(group_id, sender_id, formatted_message):
    # Create the inline button
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kilent lichkasi", url=f"tg://user?id={sender_id}")]
    ])
    try:
        await bot.send_message(
            chat_id=group_id,
            text=formatted_message,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=inline_keyboard
        )
        print(f"Message sent to group {group_id}")
    except Exception as e:
        print(f"Failed to send message to group {group_id}: {e}")

def escape_md(text: str) -> str:
    """
    Escape Markdown V1 special characters and clean unwanted characters.
    Removes square brackets and trailing slashes if needed.
    """
    if not isinstance(text, str):
        text = str(text)

    # Remove brackets [] and trailing backslashes
    text = re.sub(r"[\[\]]", "", text)
    text = text.replace("\\", "")

    # Escape Markdown characters (_ * `)
    return re.sub(r"([_*`])", r"\\\1", text)

# Get available groups from cache
def get_available_groups():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"❌ Error loading groups config: {str(e)}")
        return {}

# Define states for handling input
class ConfigStates(StatesGroup):
    ADDING_SOURCE = State()
    ADDING_DESTINATION = State()
    ADDING_KEYWORD = State()
    ADDING_ADMIN = State()
    
# Load and save config
def load_config(file_name: str):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            config = json.load(file)
            # Ensure consistent structure
            if not isinstance(config.get("sources"), dict):
                config["sources"] = {}
            if not isinstance(config.get("destinations"), dict):
                config["destinations"] = {}
            if not isinstance(config.get("keywords"), list):
                config["keywords"] = []
            if "admins" not in config:
                config["admins"] = ADMIN_IDS
            return config
    except FileNotFoundError:
        config = {
            "sources": {},
            "destinations": {},
            "keywords": [],
            "admins": ADMIN_IDS
        }
        save_config(config)
        return config
    except Exception as e:
        print(f"❌ Error loading config: {str(e)}")
        return None
    
def save_config(config):
    try:
        print("Saving config to 'config.json'...")
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)

        with open('reload_config.txt', 'w', encoding='utf-8') as file:
            file.write("reload")

        print("✅ Config saved successfully.")
        return True
    except Exception as e:
        print(f"❌ Error saving config: {str(e)}")
        if SUPERADMIN:
            asyncio.create_task(bot.send_message(SUPERADMIN, f"🚨 Config saqlashda xatolik: {str(e)} ⚠️"))
        return False  # Indicate failure

def split_message(text: str, max_length: int = 4096) -> list:
    """Split a message into parts that fit within Telegram's max message length."""
    try:
        if len(text) <= max_length:
            return [text]
        
        messages = []
        current_message = ""
        lines = text.split("\n")
        
        for line in lines:
            if len(current_message) + len(line) + 1 > max_length:
                messages.append(current_message.strip())
                current_message = line + "\n"
            else:
                current_message += line + "\n"
        
        if current_message.strip():
            messages.append(current_message.strip())
        
        return messages
    except Exception as e:
        print(f"error at split message: {e}")
        
# Initial config load
config = load_config("config.json")
ADMIN_IDS = config.get("admins", ADMIN_IDS) 

# Inline keyboard markup for main menu
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ko'rish 📊", callback_data="view")],
    [InlineKeyboardButton(text="Qo'shish ➕", callback_data="add")],
    [InlineKeyboardButton(text="O'chirish ❌", callback_data="delete")],
    [InlineKeyboardButton(text="Guruhlarim 👥", callback_data="groups")]
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
    config = load_config("config.json")
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
    
@dp.callback_query(lambda c: c.data == "view")
async def process_view(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id

    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return

    await callback_query.answer("⏳ Ma'lumotlar yuklanmoqda...")

    try:
        config = load_config("config.json")

        sources_dict = config.get("sources", {})
        destinations_dict = config.get("destinations", {})
        keywords_list = config.get("keywords", [])

        sources = '\n'.join(
            f"`{k}` - {escape_md(v)}" for k, v in sources_dict.items()
        ) if sources_dict else "Hech narsa yo'q"

        destinations = '\n'.join(
            f"`{k}` - {escape_md(v)}" for k, v in destinations_dict.items()
        ) if destinations_dict else "Hech narsa yo'q"

        keywords = '\n'.join(escape_md(k) for k in keywords_list) if keywords_list else "Hech narsa yo'q"

        text = (
            f"📋 **Manbalar:**\n{sources}\n\n"
            f"🏠 **Manzillar:**\n{destinations}\n\n"
            f"🔍 **Kalit so'zlar:**\n{keywords}"
        )

        messages = split_message(text, max_length=MAX_MESSAGE_LENGTH)

        for i, msg in enumerate(messages):
            reply_markup = main_menu if i == len(messages) - 1 else None
            await bot.send_message(
                chat_id=user_id,
                text=msg,
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )

    except Exception as e:
        print("❌ Ma'lumotlarni yuklashda xatolik:", e)
        await bot.send_message(
            user_id,
            "⚠️ Ma'lumotlarni olishda xatolik yuz berdi!",
            parse_mode="Markdown",
            reply_markup=main_menu
        )

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
        await callback_query.answer("Noto'g'ri kategoriya! ⚠️")
        await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)
        return

    await callback_query.answer()
    await state.set_state(state_name)

    if category_key in ["manbalar", "manzillar"]:
        # Fetch all groups from cache (no filtering)
        try:
            available_groups = get_available_groups() or {}
            if available_groups:
                groups_text = '\n'.join(f"`{group_id}` - {escape_md(group_name)}" for group_id, group_name in available_groups.items())
            else:
                groups_text = (
                    "📂 Guruhlar ro'yxati mavjud emas.\n\n"
                    "Iltimos, guruhlar ro'yxatini yangilash uchun **bosh menyudan** "
                    "**Guruhlarim 📂** tugmasini bosing."
                )

            prompt = (
                f"Iltimos, **{category_key.capitalize()} 📋** qo'shish uchun guruh ID sini kiriting "
                f"(masalan, -1001234567890). 😊\n\nMavjud guruhlar ro'yxati:\n\n{groups_text}"
            )
        except Exception as e:
            print(e)

        try:
            messages = split_message(prompt)
            for i, msg in enumerate(messages):
                reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
                ]) if i == len(messages) - 1 else None

                await bot.send_message(
                    callback_query.from_user.id,
                    msg,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )

        except TelegramBadRequest as e:
            print(f"TelegramBadRequest: {str(e)}")
            await bot.send_message(
                callback_query.from_user.id,
                f"Xatolik yuz berdi: {str(e)}. Iltimos, ID ni qo'lda kiriting (-1001234567890 formatida).",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
                ]),
                parse_mode="Markdown"
            )

    else:
        if category_key == "admin":
            if user_id != SUPERADMIN:
                await bot.send_message(user_id, "Sizda bu amalni bajarish uchun ruxsat yo'q! ⚠️")
                return
            await bot.send_message(user_id, "Iltimos, yangi admin ID sini kiriting (masalan, 123456789): 😊")
        else:
            prompt = (
                f"**{category_key.capitalize()} 🔍** qo'shish uchun qiymat yuboring "
                f"(masalan, 'toshkent'): 😊"
            )
            await bot.send_message(
                callback_query.from_user.id,
                prompt,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")]
                ]),
                parse_mode="Markdown"
            )
            
# Handler for adding sources
@dp.message(ConfigStates.ADDING_SOURCE)
async def add_source(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return

    config = load_config("config.json")
    if not config:
        await message.reply("⚠️ Config yuklashda xato yuz berdi!", reply_markup=main_menu, parse_mode="Markdown")
        return

    value = message.text.strip()
    try:
        value = int(value)
        value = str(value)  # Store as string key

        if value in config.get("sources", {}):
            await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
        else:
            available_groups = get_available_groups()
            group_name = available_groups.get(value, "Noma'lum guruh")
            config["sources"][value] = group_name
            if save_config(config) or 1:
                print(f"Added source {value}: {group_name}")
                await message.reply(f"✅ **Manbalar 📋** ga `{value}` - *{escape_md(group_name)}* qo‘shildi!", reply_markup=main_menu, parse_mode="Markdown")
            else:
                await message.reply("⚠️ Config saqlashda xato yuz berdi!", reply_markup=main_menu, parse_mode="Markdown")
    except ValueError:
        await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu, parse_mode="Markdown")
    await state.clear()
    
@dp.message(ConfigStates.ADDING_DESTINATION)
async def add_destination(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return

    config = load_config("config.json")
    if not config:
        await message.reply("⚠️ Config yuklashda xato yuz berdi!", reply_markup=main_menu, parse_mode="Markdown")
        return

    value = message.text.strip()
    try:
        value = int(value)
        value = str(value)  # Store as string key

        if value in config.get("destinations", {}):
            await message.reply(f"⚠️ `{value}` allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
        else:
            available_groups = get_available_groups()
            group_name = available_groups.get(value, "Noma'lum guruh")
            config["destinations"][value] = group_name
            save_config(config)
            print(f"Added destination {value}: {group_name}")
            await message.reply(f"✅ **Manbalar 📋** ga `{value}` - *{escape_md(group_name)}* qo‘shildi!", reply_markup=main_menu, parse_mode="Markdown")
    except ValueError:
        await message.reply("⚠️ Iltimos, to'g'ri ID kiriting (masalan, -1001234567890)!", reply_markup=main_menu, parse_mode="Markdown")
    await state.clear()
    
# Handler for adding keywords
@dp.message(ConfigStates.ADDING_KEYWORD)
async def add_keyword(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.reply("Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return
    config = load_config("config.json")
    if not config:
        await message.reply("⚠️ Config yuklashda xato yuz berdi!", reply_markup=main_menu, parse_mode="Markdown")
        return
    value = message.text.strip()
    if not value:
        await message.reply("⚠️ Kalit so'z bo'sh bo'lmasligi kerak!", reply_markup=main_menu, parse_mode="Markdown")
        await state.clear()
        return
    try:
        value = value.encode('utf-8').decode('utf-8', errors='ignore')
        if value not in config["keywords"]:
            config["keywords"].append(value)
            if save_config(config) or 1:
                await message.reply(f"✅ **Kalit so'zlar 🔍** ga '{escape_md(value)}' qo'shildi!", reply_markup=main_menu, parse_mode="Markdown")
            else:
                await message.reply("⚠️ Config saqlashda xato yuz berdi!", reply_markup=main_menu, parse_mode="Markdown")
        else:
            await message.reply(f"⚠️ '{escape_md(value)}' allaqachon mavjud!", reply_markup=main_menu, parse_mode="Markdown")
    except UnicodeEncodeError as e:
        print(f"Error encoding keyword: {e}")
        await message.reply("⚠️ Kalit so'zda xato yuz berdi, iltimos qayta urining!", reply_markup=main_menu, parse_mode="Markdown")
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

    config = load_config("config.json")
    category = callback_query.data.replace("delete_select_", "")
    category_map = {"sources": "manbalar", "destinations": "manzillar", "keywords": "kalit so'zlar"}
    category_key = category_map.get(category)

    if not category_key:
        await callback_query.answer("Noto'g'ri kategoriya! ⚠️")
        await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)
        return

    delete_menu = InlineKeyboardMarkup(inline_keyboard=[])
    empty_message = f"⚠️ **{category_key.capitalize()} 📋🏠🔍** da hech narsa yo'q!"

    if category in ["sources", "destinations"]:
        items_dict = config.get(category, {})
        if not items_dict:
            await callback_query.answer()
            await bot.send_message(callback_query.from_user.id, empty_message, reply_markup=main_menu, parse_mode="Markdown")
            return
        for group_id, group_name in items_dict.items():
            btn_text = f"{escape_md(group_name)} [`{group_id}`]"
            delete_menu.inline_keyboard.append([
                InlineKeyboardButton(text=btn_text, callback_data=f"delete_{category}_{group_id}")
            ])
    elif category == "keywords":
        items = config.get("keywords", [])
        if not items:
            await callback_query.answer()
            await bot.send_message(callback_query.from_user.id, empty_message, reply_markup=main_menu, parse_mode="Markdown")
            return
        for keyword in items:
            delete_menu.inline_keyboard.append([
                InlineKeyboardButton(text=escape_md(keyword), callback_data=f"delete_{category}_{keyword}")
            ])

    delete_menu.inline_keyboard.append([
        InlineKeyboardButton(text="Orqaga 🎉", callback_data="back_to_main")
    ])

    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        f"**{category_key.capitalize()} 📋🏠🔍** dan o'chirish uchun tanlang: 😊",
        reply_markup=delete_menu,
        parse_mode="Markdown"
    )
    
# Handler for deleting items
@dp.callback_query(lambda c: c.data.startswith("delete_"))
async def process_delete_item(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return

    config = load_config("config.json")
    parts = callback_query.data.split("_", 2)  # "delete_sources_-1001234567890" or "delete_keywords_someword"
    if len(parts) != 3:
        await callback_query.answer("Xatolik yuz berdi! ⚠️")
        await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)
        return

    _, category, item = parts
    category_map = {"sources": "Manbalar", "destinations": "Manzillar", "keywords": "Kalit so'zlar"}
    category_name = category_map.get(category, category)

    try:
        if category in ["sources", "destinations"]:
            item_id = str(item)
            if item_id in config[category]:
                del config[category][item_id]
                print(f"Deleted {item_id} from {category}. New data: {config[category]}")
                save_config(config)
                await callback_query.answer(f"✅ {category_name} dan `{item_id}` o'chirildi!")
                await bot.send_message(user_id, "Muvaffaqiyatli o'chirildi! ✅", reply_markup=main_menu)
            else:
                await callback_query.answer("Element topilmadi! ⚠️")
                await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)

        elif category == "keywords":
            if item in config["keywords"]:
                config["keywords"].remove(item)
                print(f"Deleted keyword: {item}")
                save_config(config)
                await callback_query.answer(f"✅ {category_name} dan `{item}` o'chirildi!")
                await bot.send_message(user_id, "Muvaffaqiyatli o'chirildi! ✅", reply_markup=main_menu)
            else:
                await callback_query.answer("Kalit so'z topilmadi! ⚠️")
                await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)

        else:
            await callback_query.answer("Noto'g'ri kategoriya! ⚠️")
            await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)

    except Exception as e:
        print(f"Xatolik: {e}")
        await callback_query.answer("Xatolik yuz berdi! ⚠️")
        await bot.send_message(user_id, "Qayta urining! 😊", reply_markup=main_menu)

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

# Handler for Guruhlarim
@dp.callback_query(lambda c: c.data == "groups")
async def show_my_groups(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id not in ADMIN_IDS:
        await bot.send_message(user_id, "Sizda bu botni ishlatish uchun ruxsat yo'q! ⚠️")
        return

    await callback_query.answer("⏳ Guruhlar yangilanmoqda...")

    try:
        groups = await get_groups_dict()

        # Save to groups_config.json
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(groups, f, ensure_ascii=False, indent=2)

        if not groups:
            await bot.send_message(user_id, "📂 Hech qanday guruh topilmadi!", reply_markup=main_menu, parse_mode="Markdown")
            return

        text_lines = ["📂 **Sizdagi guruhlar ro'yxati:**\n"]
        for group_id, display in groups.items():
            text_lines.append(f"• `{group_id}` - {display}")

        text = "\n".join(text_lines)
        messages = split_message(text, max_length=MAX_MESSAGE_LENGTH)

        # Send each message part
        for i, msg in enumerate(messages):
            # Only include reply_markup on the last message
            reply_markup = main_menu if i == len(messages) - 1 else None
            await bot.send_message(
                user_id,
                msg,
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )

    except Exception as e:
        print("❌ Guruhlarni olishda xatolik:", e)
        await bot.send_message(user_id, "⚠️ Guruhlarni olishda xatolik yuz berdi!", reply_markup=main_menu, parse_mode="Markdown")

   
async def main():
    try:
        # Start the bot polling
        print("Starting bot...")
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        # Log error to file
        print(f"ERROR: {e}")
        with open('error.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"Error: {str(e)}\n")
        # Notify superadmin
        if SUPERADMIN and "argument of type 'NoneType'" not in str(e):
            try:
                await bot.send_message(SUPERADMIN, f"🚨 Botda xatolik yuz berdi: {str(e)} ⚠️")
            except Exception as notify_error:
                print(f"Failed to notify superadmin: {notify_error}")
        raise  # Re-raise to stop the bot on critical errors

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())