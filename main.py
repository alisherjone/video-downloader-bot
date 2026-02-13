import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from yt_dlp import YoutubeDL

# Bot tokeningizni shu yerga yozing
API_TOKEN = "8302492091:AAG1_qGJt077FjnwsZtU0U7LxAafRJ1UXjM"

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Video yuklash funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024, # 50MB gacha cheklov
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "video.mp4"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Instagram, TikTok yoki YouTube linkini yuboring, men uni yuklab beraman.")

@dp.message_handler()
async def handle_message(message: types.Message):
    if "http" in message.text:
        wait_msg = await message.answer("Video tayyorlanmoqda, iltimos kuting...")
        try:
            file_path = download_video(message.text)
            with open(file_path, 'rb') as video:
                await message.answer_video(video)
            os.remove(file_path) # Faylni o'chirish
            await wait_msg.delete()
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: {str(e)}")
    else:
        await message.answer("Iltimos, video linkini yuboring.")

# Render port xatosini olmaslik uchun asosiy qism
if __name__ == "__main__":
    # Render PORT o'zgaruvchisini talab qiladi
    from aiohttp import web
    
    # Portni aniqlash
    port = int(os.environ.get("PORT", 5000))
    
    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
    
