import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Masukkan API key Anda
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

async def get_weather(location="Jakarta"):
    """
    Fungsi untuk mendapatkan prediksi cuaca hari ini dari WeatherAPI.
    """
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=1&aqi=no&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        location_name = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        forecast = data["forecast"]["forecastday"][0]["day"]
        
        condition = forecast["condition"]["text"]
        avg_temp = forecast["avgtemp_c"]
        max_temp = forecast["maxtemp_c"]
        min_temp = forecast["mintemp_c"]
        humidity = forecast["avghumidity"]

        return (
            f"Prediksi Cuaca untuk Hari Ini di {location_name}, {region}, {country}:\n"
            f"- Kondisi: {condition}\n"
            f"- Suhu Rata-rata: {avg_temp}°C\n"
            f"- Suhu Maksimum: {max_temp}°C\n"
            f"- Suhu Minimum: {min_temp}°C\n"
            f"- Kelembapan: {humidity}%"
        )
    else:
        return "Gagal mendapatkan data cuaca. Silakan coba lagi."

async def hari_ini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler untuk perintah 'Hari ini'.
    """
    chat_id = update.effective_chat.id
    try:
        location = " ".join(context.args) if context.args else "Jakarta"
        weather_report = await get_weather(location)
        await context.bot.send_message(chat_id=chat_id, text=weather_report)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Terjadi kesalahan: " + str(e))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler untuk perintah 'start'.
    """
    await update.message.reply_text(
        "Halo! Saya adalah bot cuaca. Gunakan perintah /hari_ini untuk mendapatkan prediksi cuaca hari ini.\n"
        "Contoh: /hari_ini [lokasi]"
    )

def main():
    """
    Fungsi utama untuk menjalankan bot Telegram.
    """
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Menambahkan command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hari_ini", hari_ini))

    # Memulai bot
    application.run_polling()

if __name__ == "__main__":
    main()
