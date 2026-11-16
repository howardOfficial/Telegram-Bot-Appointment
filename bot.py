import telebot
from telebot import types
import json
import os

#Сюда вставляем токен который мы получим от @BotFather
TOKEN = 'ТВОЙ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

# Файл для хранения данных (имитация БД)
DB_FILE = 'requests.json'

def save_request(user_id, name, phone):
    # Загружаем старые данные
    data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                data = []
    
    # Добавляем новую заявку
    data.append({'user_id': user_id, 'name': name, 'phone': phone})
    
    # Сохраняем
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📝 Оставить заявку')
    btn2 = types.KeyboardButton('ℹ️ О нас')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, 
                     f"Здравствуйте, {message.from_user.first_name}!\n"
                     "Это демо-бот для записи на консультацию.\n"
                     "Выберите действие:", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'ℹ️ О нас')
def about(message):
    bot.send_message(message.chat.id, "Этот бот создан для демонстрации навыков разработки.")

@bot.message_handler(func=lambda message: message.text == '📝 Оставить заявку')
def ask_name(message):
    bot.send_message(message.chat.id, "Отлично! Как вас зовут?")
    bot.register_next_step_handler(message, ask_phone)

def ask_phone(message):
    name = message.text
    bot.send_message(message.chat.id, f"{name}, укажите ваш номер телефона:")
    bot.register_next_step_handler(message, save_data, name)

def save_data(message, name):
    phone = message.text
    user_id = message.chat.id
    save_request(user_id, name, phone)
    
    bot.send_message(message.chat.id, 
                     f"Спасибо! Ваша заявка сохранена:\n"
                     f"Имя: {name}\nТелефон: {phone}\n"
                     f"Я свяжусь с вами в ближайшее время.")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
