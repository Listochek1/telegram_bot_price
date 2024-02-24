from pybit.unified_trading import HTTP
from datetime import datetime
import telebot
from telebot import types
from auth_token import TOKEN


def price_btc():
    """Используя API Bybit узнаем цену BTC"""
    session = HTTP(testnet=True)
    response = session.get_tickers(category="inverse",symbol="BTCUSD")
    price = response['result']['list']
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nBTC price: {price[0]['lastPrice']} (USDT)") #Используя документацию API Bybit выбираем последнию цену BTC/USD


#Создаем бота в телеграмм и импортируем токен
def telegram_bot(token):
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=["start"])
    def start_message(message):
        """Данная функция будет выводить текст на экран после того как будет испьзована команда /start"""
        bot.send_message(message.chat.id,"Чтобы узнать текущую цену введите 'Price'") 

    @bot.message_handler(content_types = ['text'])    
    def send_text(message):

        """Данная функция выводит на экран цену BTC после ввода 'Price' """
        if message.text.lower() == 'price': 
            try:
                session = HTTP(testnet=True)
                response = session.get_tickers(category="inverse",symbol="BTCUSD")
                price = response['result']['list']
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nBTC price: {price[0]['lastPrice']} (USDT)" #текущую дату,время и цену биткоина 
                )
            except Exception as ex: #срабатывает если произошла ошибка
                price(ex)
                bot.send.message(
                    message.chat.id,'Что то пошло не так...'
                )
        else:           #срабатывает если пользователь ввел неверную команду 
            bot.send_message(message.chat.id,'Неправильно введенная комманда!')

                

    bot.polling()

if __name__ == '__main__':
    #price_btc()
    telegram_bot(TOKEN)
