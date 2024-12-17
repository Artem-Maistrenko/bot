import telebot
from g4f.client import Client
import requests
from bs4 import BeautifulSoup
from textwrap import wrap

# Настройки бота
TOKEN = '7410295659:AAEk6Rb7GGsJ9mQ5mlv6KCnU07dRgmFqCkk'
bot = telebot.TeleBot(TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}')


# Обработка текстовых сообщений
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    # Получаем сообщение от пользователя
    user_input = message.text.strip().lower()

    # Если пользователь просит обработать страницу
    if user_input.startswith('/getinfo'):
        url = 'https://www.dota2.com/home'

        try:
            r = requests.get(url)

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, features='html.parser')
                title = soup.find('title').text
                news_items = soup.select('.news-item')

                result = f"Текст заголовка страницы: {title}\n\nПоследние новости:\n"
                for item in news_items[:3]:
                    header = item.find('h3').text
                    date = item.find('span', class_='date').text
                    link = item.find('a')['href'].replace('https://www.blackbox.ai', 'https://api.blackbox.ai')

                    result += f"{header} ({date})\n{link}\n\n"

                bot.send_message(message.chat.id, result)
            else:
                bot.send_message(message.chat.id, 'Ошибка при загрузке страницы.')
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

    # Обычное общение с пользователем
    else:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)


# Запуск бота
bot.polling()