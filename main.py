import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from yt_dlp import YoutubeDL
from aiohttp import web

# BOT TOKENINGIZ
TOKEN = "8302492091:AAG1_qGJt077FjnwsZtU0U7LxAafRJ1UXjM"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Video yuklash funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'no_warnings': True,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "video.mp4"

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Salom! Video yuklash uchun link yuboring (Instagram, TikTok, YouTube).")

@dp.message_handler()
async def handle_docs(message: types.Message):
    if "http" in message.text:
        msg = await message.answer("⌛️ Yuklanmoqda, iltimos kuting...")
        try:
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, download_video, message.text)
            
            with open(file_path, 'rb') as video:
                await message.reply_video(video, caption="Tayyor! ✅")
            
            os.remove(file_path)
            await msg.delete()
        except Exception as e:
            await message.answer("❌ Xatolik: Video yuklab bo'lmadi. Linkni tekshiring.")
    else:
        await message.answer("Iltimos, video linkini yuboring.")

# --- RENDER UCHUN DUMMY WEB SERVER ---
async def web_handle(request):
    return web.Response(text="Bot is Live!")

app = web.Application()
app.router.add_get('/', web_handle)

async def on_startup(dp):
    # Botni alohida fonda yurgizish
    print("Bot ishga tushdi...")

if __name__ == "__main__":
    # Render PORT o'zgaruvchisini talab qiladi
    port = int(os.environ.get("PORT", 10000))
    
    # Bot pollingni boshlash
    loop = asyncio.get_event_loop()
    loop.create_task(executor.start_polling(dp, skip_updates=True))
    
    # Web serverni ishga tushirish (Render talabi)
    web.run_app(app, port=port)
    
