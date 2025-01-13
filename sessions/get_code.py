from telethon import TelegramClient
import time
from termcolor import colored
import os

api_id = input(colored("please enter your api id -> ", 'light_green'))
api_hash = input(colored("\nplease enter your api hash -> ", 'light_green'))
session_name = input(colored("\nplease enter your session file name (without .session) -> ", "light_green"))

if not os.path.exists(f"{session_name}.session"):
    print("File session not found. Please create a session first.")
else:
    ready = input("Enter the user number in Telegram to send the code, then press y to read the code to you, otherwise press n if you are not ready -> ")

    if ready == "y":
        client = TelegramClient(session_name, api_id, api_hash)

        async def main():
            await client.start()

            time.sleep(5)
            user_id = 777000  
            message = await client.get_messages(user_id, limit=1) 

            if message:
                print("\n\n", message[0].text)

        with client:
            client.loop.run_until_complete(main())
    elif ready == "n":
        print("OK, you are ready to come back again")
    else:
        print("only press y or n!")
