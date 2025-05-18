# import asyncio
# from admin_bot import main as admin_bot_main
# from user_bot import user_bot_main

# async def run_bots():
#     try:
#         # Create tasks for both bots
#         admin_task = asyncio.create_task(admin_bot_main())
#         user_task = asyncio.create_task(user_bot_main())
        
#         # Wait for both tasks to complete (they won't unless an error occurs)
#         await asyncio.gather(admin_task, user_task)
#     except Exception as e:
#         # Log any unhandled errors
#         with open('error.log', 'a') as log_file:
#             log_file.write(f"Error in main_bot: {str(e)}\n")
#         raise

# if __name__ == "__main__":
#     print("Starting both AdminBot and UserBot...")
#     asyncio.run(run_bots())

# import asyncio
# import logging
# from admin_bot import main as admin_bot_main
# from user_bot import user_bot_main

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# async def run_bots():
#     try:
#         logging.info("Starting AdminBot...")
#         await admin_bot_main()  # Run admin bot first
#         logging.info("Starting UserBot...")
#         await user_bot_main()  # Run user bot after admin bot completes (though it won't due to run_until_disconnected)
#     except Exception as e:
#         error_msg = f"Error in main_bot: {str(e)}"
#         logging.error(error_msg)
#         with open('data/error.log', 'a') as log_file:
#             log_file.write(f"{error_msg}\n")
#         raise

# if __name__ == "__main__":
#     print("Starting both AdminBot and UserBot...")
#     asyncio.run(run_bots())

import asyncio
from admin_bot import main as admin_bot_main
from user_bot import user_bot_main

async def run_bots():
    try:
        # Create tasks for both bots
        admin_task = asyncio.create_task(admin_bot_main())
        user_task = asyncio.create_task(user_bot_main())
        
        # Wait for both tasks to complete (they won't unless an error occurs)
        await asyncio.gather(admin_task, user_task)
    except Exception as e:
        # Log any unhandled errors
        with open('error.log', 'a') as log_file:
            log_file.write(f"Error in main_bot: {str(e)}\n")
        raise

if __name__ == "__main__":
    print("Starting both AdminBot and UserBot...")
    asyncio.run(run_bots())