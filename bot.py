from g4f.client import Client as G4FClient
from colorama import Fore
import re
import telebot
from telebot import types
import threading

# Инициализация бота
bot = telebot.TeleBot('7897112705:AAFdWM5Odzdpw7r1htpYFNvUlckX23pIJb8')  # Замените на ваш токен

def AI_answer(text: str, prompt: str = '', request_theme: str = "Metro Exodus", model: str = 'gpt-4o', limit: int = 3, timeout: int = 100) -> str | None:
    def send_request():
        try:
            client = G4FClient()
            print(Fore.GREEN + f"Отправка запроса к модели {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"{prompt}\n{text}"}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(Fore.RED + f"Ошибка при отправке запроса: {e}")
            return None

    print(Fore.CYAN + "\n" + "=" * 15 + f"{request_theme}" + "=" * 15)

    for attempt in range(15):
        response = send_request()
        if response:
            clear_text = re.sub(r"[A-Za-z0-9]", "", response)
            clear_text = re.sub(r'\s+', ' ', clear_text.strip())
            if len(clear_text) > limit:
                print(Fore.GREEN + f"Ответ подходит, возвращаем результат.")
                print(Fore.CYAN + "=" * 15 + "="*len(request_theme) + "=" * 15)
                return response.strip()
        print(Fore.RED + f"Процесс прерван после {attempt+1} попытки.")
        print(Fore.CYAN + "=" * 15 + "="*len(request_theme) + "=" * 15 + "\n")

    return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("👋 Поздороваться"), types.KeyboardButton("❓ Задать вопрос"))
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Я бот, который поможет тебе в игре Metro Exodus.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, "Привет! Готов помочь тебе в игре Metro Exodus.")
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Где найти ресурсы?"), types.KeyboardButton("Как пройти сложные участки?"),
                   types.KeyboardButton("Информация о врагах"), types.KeyboardButton("Задать свой вопрос"),
                   types.KeyboardButton("Вернуться в главное меню"))
        bot.send_message(message.chat.id, "Задай мне вопрос", reply_markup=markup)
    elif message.text == "Где найти ресурсы?":
        bot.send_message(message.chat.id, "Ресурсы можно найти в различных локациях. Например, в Волге много медикаментов, а в Тайге много боеприпасов.")
    elif message.text == "Как пройти сложные участки?":
        bot.send_message(message.chat.id, "Для прохождения сложных участков рекомендуется использовать скрытность и экономить боеприпасы. В некоторых случаях можно обойти врагов.")
    elif message.text == "Информация о врагах":
        bot.send_message(message.chat.id, "В игре Metro Exodus есть различные типы врагов, включая мутантов и бандитов. Мутанты обычно слабее, но могут атаковать группами. Бандиты вооружены и могут быть опасны.")
    elif message.text == "Задать свой вопрос":
        bot.send_message(message.chat.id, "Пожалуйста, задайте свой вопрос, и я постараюсь помочь вам.")
    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("👋 Поздороваться"), types.KeyboardButton("❓ Задать вопрос"))
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=markup)
    else:
        # Обработка пользовательских вопросов с использованием AI
        context = "Все вопросы касаются игры Metro Exodus. Пожалуйста, ответьте в контексте этой игры."
        loading_message = bot.send_message(message.chat.id, "Загрузка...")

        def process_request():
            response = AI_answer(message.text, prompt=context, request_theme="Вопрос от пользователя о Metro Exodus")
            if response:
                bot.edit_message_text(response, message.chat.id, loading_message.message_id)
            else:
                bot.edit_message_text("Не понимаю ваш вопрос. Пожалуйста, попробуйте задать его по-другому или выберите один из предложенных вариантов.", message.chat.id, loading_message.message_id)

        threading.Thread(target=process_request).start()

bot.polling()