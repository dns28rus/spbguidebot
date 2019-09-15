# -*- coding: utf-8 -*-

import telebot
import requests
import config
import dbworker
import time
from telebot import TeleBot, types

bot = telebot.TeleBot(config.token)

#добавить кнопки "Получить координаты", "Начать" и "Написать отзыв"
keyboard1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboard1.add('Получить координаты', 'Начать', 'Оставить отзыв')

#добавить клавиатуру для перекрёстка
keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboard2.add('Пошли на граффити посмотреть', 'Иду по основному пути!')

#добавить кнопку, чтобы запускать состояния подквестов
keyboard3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
keyboard3.add('Пойдём дальше!')


@bot.message_handler(commands=['start'])
def start_message(message):
    dbworker.set_state(message.chat.id, config.States.S_MENU.value)
    bot.send_message(message.chat.id, 'Привет! Спасибо за доверие ;) Здесь ты сможешь пройти интересные и небанальные маршруты по любимому нами Петербургу! Готов двинуться дальше? Напиши \"да\" (или что угодно вообще, не важно ;) )')
   
#отправить мп-3 (вместе с метаданными)
    #audio = open('./media/otbivka.mp3', 'rb')
    #bot.send_audio(message.chat.id, audio)

# отправить "голосовуху"
    #voice = open('./media/otbivka.ogg', 'rb')
    #bot.send_voice(message.chat.id, voice)  

#@bot.message_handler(content_types=['sticker'])
#def sticker_id(message):
#    print(message)

@bot.message_handler(content_types=['text'],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_MENU.value)
def quest_menu(message):
    # Выбор квеста или написать отзыв
    # Уберем клавиатуру с вариантами ответа.
    keyboard_hider = telebot.types.ReplyKeyboardRemove()
    # Проверяем, отправлен пункт меню или меню вызвано в первый раз

    if message.text == 'Получить координаты':
        bot.send_message(message.chat.id, 'Квест начинается у часовни Александра Невского (ул. Блохина, 26а). Нужно подойти ко входу и встать к нему спиной. Вот точные координаты начала квеста:')
        bot.send_location(message.chat.id, 59.952515, 30.290786)
        #bot.delete_message(message.chat.id, message.message_id)

    elif message.text == 'Начать':
        # запуск квеста, первые аудиофайлы
        dbworker.set_state(message.chat.id, config.States.S_QUEST_1.value)
        bot.send_message(message.chat.id, 'Для начала путешествия отправь любое сообщение или нажми на команду /letsgo', reply_markup=keyboard_hider)

    elif message.text == 'Пошли на граффити посмотреть':
        # Ответвление про граффити
        dbworker.set_state(message.chat.id, config.States.S_QUEST_2.value)
        bot.send_message(message.chat.id, 'Принято! Нажми на кнопку для продолжения экскурсии', reply_markup=keyboard3)

    elif message.text == 'Иду по основному пути!':
        # Путь на Камчатку
        dbworker.set_state(message.chat.id, config.States.S_QUEST_3.value)
        bot.send_message(message.chat.id, 'Окей! Нажми на кнопку для продолжения экскурсии', reply_markup=keyboard3)
       
    elif message.text == 'Оставить отзыв':
        # Оставляем отзыв
        dbworker.set_state(message.chat.id, config.States.S_REVIEW.value)
        bot.send_message(message.chat.id, 'Теперь можно написать или \"наговорить\" голосовым сообщением отзыв. Как тебе? Что понравилось? Что добавить?', reply_markup=keyboard_hider)
        
    else:
        #Написать про меню и отзывы
        bot.send_message(message.chat.id, "Что ж, благодарим за участие в тестовом запуске нашего Гида по интересным местам Питера. На данный момент у нас только 1 маршрут. Для его прохождения нужно нажать на \"Начать\", чтобы узнать где место старта, нажми на \"Получить координаты\". Чтобы оставить отзыв, нажми на соответствующую кнопку", reply_markup=keyboard1)
    
@bot.message_handler(commands=['letsgo'],
                     content_types=['text'],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_QUEST_1.value)
def start_quest(message):
    bot.send_message(message.chat.id, 'Ну, поехали! Надевай наушники и готовься к увлекательному путешествию. Сейчас отправлю первый аудиофайл. Он достаточно длинный, поэтому отправиться может не моментально. Возможно, придётся немного подождать)')

    # отправить "голосовуху"
    #bot.send_message(message.chat.id, 'Первая МП3')
    audio = open('./media/kino-1.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)  
    time.sleep(365)
    #задержка 365 секунд

    #bot.send_message(message.chat.id, 'Вторая МП3')
    audio = open('./media/kino-2.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)
    time.sleep(110)
    #задержка 110 секунд
    
    bot.send_message(message.chat.id, "Твой выбор?", reply_markup=keyboard2)
    # устанавливаем состояние вызова меню
    dbworker.set_state(message.chat.id, config.States.S_MENU.value)


@bot.message_handler(content_types=['text'],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_QUEST_2.value)
def start_quest(message):
    # отправить "голосовуху"
    #bot.send_message(message.chat.id, 'МП3, которая про граффити')
    audio = open('./media/kino-2-1.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)  
    time.sleep(120)
    #задержка 120 секунд
    bot.send_message(message.chat.id, "Нажми на кнопку, когда вернёшься к перекрестку у дома 17 по ул. Блохина", reply_markup=keyboard3)
    # устанавливаем состояние вызова меню
    dbworker.set_state(message.chat.id, config.States.S_QUEST_3.value)

@bot.message_handler(content_types=['text'],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_QUEST_3.value)
def start_quest(message):
    # отправить "голосовуху"
    #bot.send_message(message.chat.id, 'МП3 про Камчатку')
    audio = open('./media/kino-3.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)  
    time.sleep(180)
    #задержка 180 секунд
    bot.send_message(message.chat.id, "Благодарим тебя ещё раз! Не забывай оставить отзыв ;)", reply_markup=keyboard1)
    # устанавливаем состояние вызова меню
    dbworker.set_state(message.chat.id, config.States.S_MENU.value)

    
# если боту отправляют голосовое сообщение или аудиозапись   
@bot.message_handler(content_types=['voice', 'text'],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_REVIEW.value)
def get_review(message):
    if message.text == 'Закончить отзыв':
        dbworker.set_state(message.chat.id, config.States.S_MENU.value)
        bot.send_message(message.chat.id, "Огромная благодарность! Нам очень важна твоя обратная связь!", reply_markup=keyboard1)
        return
    if message.voice != None:
        file_info = bot.get_file(message.voice.file_id)
        voice_file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.token, file_info.file_path))
        with open('voice'+str(message.date)+'.ogg', 'wb') as file:
            file.write(voice_file.content)    
    #Перешлём сообщение в чат с орг.группой
    bot.forward_message(config.DiscussionId, message.chat.id, message.message_id)
    keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard2.add('Закончить отзыв')
    bot.send_message(message.chat.id, "Спасибо! Если есть что добавить, можно это сделать сейчас. Если нет - нажми \"Закончить отзыв\".", reply_markup=keyboard2)
    

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, посетитель!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, посетитель')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


if __name__ == "__main__":
    bot.polling(none_stop=True)
