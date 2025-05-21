import asyncio
import random
from datetime import datetime
from bot_admin import main as admin_bot_main
from user_bot import user_bot_main
from aiogram import Bot
from dotenv import load_dotenv
import os
import telethon
import aiohttp

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPERADMIN = int(os.getenv("SUPERADMIN", "0"))

# Initialize bot for sending error notifications
bot = None
if BOT_TOKEN and SUPERADMIN:
    bot = Bot(token=BOT_TOKEN)

async def retry_with_backoff(func, max_retries=5, initial_delay=1, max_delay=60):
    """
    Retry a function with exponential backoff on network errors.
    """
    for attempt in range(max_retries):
        try:
            return await func()
        except (telethon.errors.rpcerrorlist.TimeoutError, aiohttp.ClientError, ConnectionError) as e:
            if attempt == max_retries - 1:
                raise  # Re-raise on last attempt
            delay = min(initial_delay * (2 ** attempt) + random.uniform(0, 0.1), max_delay)
            print(f"Network error: {str(e)}. Retrying in {delay:.2f} seconds (attempt {attempt + 1}/{max_retries})...")
            await asyncio.sleep(delay)
    raise Exception("Max retries reached for network operation")

async def run_bots():
    while True:  # Loop to restart bots on recoverable errors
        try:
            # Create tasks for both bots
            admin_task = asyncio.create_task(admin_bot_main())
            user_task = asyncio.create_task(user_bot_main())
            
            # Wait for both tasks to complete
            await retry_with_backoff(
                lambda: asyncio.gather(admin_task, user_task, return_exceptions=True),
                max_retries=5,
                initial_delay=1,
                max_delay=60
            )
        except (telethon.errors.rpcerrorlist.TimeoutError, aiohttp.ClientError, ConnectionError) as e:
            error_msg = f"Network error in main_bot: {str(e)}"
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()} {error_msg}\n")
            print(error_msg)
            if bot and SUPERADMIN:
                try:
                    await bot.send_message(SUPERADMIN, f"🚨 MainBot: {error_msg} ⚠️")
                except Exception as notify_error:
                    print(f"Failed to notify SUPERADMIN: {notify_error}")
            await asyncio.sleep(5)  # Wait before retrying
            continue  # Retry running both bots
        except telethon.errors.FloodWaitError as e:
            error_msg = f"Flood wait error in main_bot: Must wait {e.seconds} seconds."
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()} {error_msg}\n")
            print(error_msg)
            if bot and SUPERADMIN:
                try:
                    await bot.send_message(SUPERADMIN, f"🚨 MainBot: {error_msg} ⚠️")
                except Exception as notify_error:
                    print(f"Failed to notify SUPERADMIN: {notify_error}")
            await asyncio.sleep(e.seconds)
            continue  # Retry after waiting
        except telethon.errors.AuthKeyUnregisteredError as e:
            error_msg = f"Session invalid in main_bot: {str(e)}. Regenerating session..."
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()} {error_msg}\n")
            print(error_msg)
            if bot and SUPERADMIN:
                try:
                    await bot.send_message(SUPERADMIN, f"🚨 MainBot: {error_msg} ⚠️")
                except Exception as notify_error:
                    print(f"Failed to notify SUPERADMIN: {notify_error}")
            # Note: Session regeneration should be handled in user_bot.py
            await asyncio.sleep(5)
            continue  # Retry
        except asyncio.exceptions.CancelledError:
            error_msg = "Main bot cancelled."
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()} {error_msg}\n")
            print(error_msg)
            if bot and SUPERADMIN:
                try:
                    await bot.send_message(SUPERADMIN, f"🚨 MainBot: {error_msg} ⚠️")
                except Exception as notify_error:
                    print(f"Failed to notify SUPERADMIN: {notify_error}")
            break  # Exit on cancellation
        except Exception as e:
            error_msg = f"Unexpected error in main_bot: {str(e)}"
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()} {error_msg}\n")
            print(error_msg)
            if bot and SUPERADMIN:
                try:
                    await bot.send_message(SUPERADMIN, f"🚨 MainBot: {error_msg} ⚠️")
                except Exception as notify_error:
                    print(f"Failed to notify SUPERADMIN: {notify_error}")
            await asyncio.sleep(5)
            continue  # Retry on unexpected errors
        finally:
            # Ensure proper cleanup
            if bot:
                try:
                    await bot.close()
                except Exception as close_error:
                    print(f"Failed to close bot session: {close_error}")

if __name__ == "__main__":
    print("Starting both AdminBot and UserBot...")
    try:
        asyncio.run(run_bots())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        with open('error.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now()} Bot stopped by user.\n")
    except Exception as e:
        error_msg = f"Fatal error in main: {str(e)}"
        print(error_msg)
        with open('error.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now()} {error_msg}\n")
        raise