import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from yt_dlp import YoutubeDL

# DIQQAT: BotFather bergan tokenni pastdagi qo'shtirnoq ichiga yozing
TOKEN = "8302492091:AAG1_qGJt077FjnwsZtU0U7LxAafRJ1UXjM"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Salom! Video yuklash uchun Instagram, TikTok yoki YouTube linkini yuboring.")

@dp.message_handler()
async def download(message: types.Message):
    if "http" in message.text:
        msg = await message.answer("⏳ Video tahlil qilinmoqda, kuting...")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'noplaylist': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([message.text])
            
            with open('video.mp4', 'rb') as video:
                await message.reply_video(video, caption="Tayyor! ✅")
            
            os.remove('video.mp4')
            await msg.delete()
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: {str(e)}")
    else:
        await message.answer("Iltimos, video havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
