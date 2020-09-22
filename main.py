# імпортуємо бібліотеку gTTS і telebot
import telebot
from telebot import types
import config
from gtts import gTTS
import os

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    about_bot = bot.get_me()

    mess_bot = f"Привіт {message.from_user.first_name}."
    bot.send_message(message.chat.id, mess_bot, parse_mode='html')

    mess_about_bot = f"""
    Я {about_bot.first_name}🤖,  виберіть нижче 👇 один з пунктів 👀
    """

    inline_markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Про мене🤖', callback_data = 'about')
    item2 = types.InlineKeyboardButton('Розпочнемо🗂', callback_data = '/languages')
    item3 = types.InlineKeyboardButton('Як користуватись? 🤔', callback_data= 'how')
    inline_markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, mess_about_bot, parse_mode='html', reply_markup=inline_markup)

@bot.message_handler(commands=['languages'])
def chose_language(message):

    text_mess = f'Виберіть мову нижче 👇'

    markup_languages = types.ReplyKeyboardMarkup(resize_keyboard=50, row_width=2)
    gb = types.KeyboardButton('🇬🇧')
    us = types.KeyboardButton('🇺🇸')
    de = types.KeyboardButton('🇩🇪')
    pl = types.KeyboardButton('🇵🇱')
    markup_languages.add(gb, us, de, pl)

    bot.send_message(message.chat.id, text_mess, reply_markup=markup_languages)

lang = ''
flag = ''

@bot.message_handler(content_types=['text'])
def text(message):
    get_lang = message.text
    global lang, flag
    if get_lang == '🇬🇧':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=50)
        item1 = types.KeyboardButton('Назад⏮')
        markup.add(item1)

        bot.send_message(message.chat.id,
                         "Вибрали мову 'Британська англійська🇬🇧', напишіть слово. Щоб повернутись до вибору мови тицьніть 'Назад⏮' ",
                         reply_markup=markup)
        lang = 'en-gb'
        flag = '🇬🇧'
        bot.register_next_step_handler(message, speech_lang)

    elif get_lang == '🇩🇪':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=50)
        item1 = types.KeyboardButton('Назад⏮')
        markup.add(item1)

        bot.send_message(message.chat.id,
                         "Вибрали мову 'Німецька🇩🇪', напишіть слово. Щоб повернутись до вибору мови тицьніть 'Назад⏮'",
                         reply_markup=markup)

        lang = 'de'
        flag = '🇩🇪'
        bot.register_next_step_handler(message, speech_lang)

    elif get_lang == '🇺🇸':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=50)
        item1 = types.KeyboardButton('Назад⏮')
        markup.add(item1)

        bot.send_message(message.chat.id,
                         "Вибрали мову 'Американська англійсьа🇺🇸', напишіть слово. Щоб повернутись до вибору мови тицьніть 'Назад⏮'",
                         reply_markup=markup)

        lang = 'en-us'
        flag = '🇺🇸'
        bot.register_next_step_handler(message, speech_lang)

    elif get_lang == '🇵🇱':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=50)
        item1 = types.KeyboardButton('Назад⏮')
        markup.add(item1)

        bot.send_message(message.chat.id,
                         "Вибрали мову 'Польська'🇵🇱', напишіть слово. Щоб повернутись до вибору мови тицьніть 'Назад⏮'",
                         reply_markup=markup)

        lang = 'pl'
        flag = '🇵🇱'
        bot.register_next_step_handler(message, speech_lang)

def speech_lang(message):
    global lang, flag
    if message.text == 'Назад⏮':
        #можна вернути попередню функцію, будь яку яку написав перед тим
        chose_language(message)

    elif not message.text:
        bot.send_message(message.chat.id, f'Введіть будь - ласка слово 👿👿')
        bot.register_next_step_handler(message, speech_lang)

    else:
        bot.send_message(message.chat.id, f'Мені потрібно декілька секунд...{flag}')

        #зберігає текст в mp3 файлі
        speech_fast = gTTS(message.text, lang=lang)
        speech_slow = gTTS(message.text, lang=lang, slow=True)
        speech_fast.save(f'speech_fast/{message.text}-fast.mp3')
        speech_slow.save(f'speech_slow/{message.text}-slow.mp3')

        #відкриває аудіо файли
        audio_fast = open(f'speech_fast/{message.text}-fast.mp3', 'rb')
        audio_slow = open(f'speech_slow/{message.text}-slow.mp3', 'rb')

        # Надсилає повідомлення
        bot.send_message(message.chat.id, 'Швидка вимова 🚀')
        bot.send_audio(message.chat.id, audio_fast)
        bot.send_message(message.chat.id, 'Помала вимова 🐌')
        bot.send_audio(message.chat.id, audio_slow)

        # Видалення записів з папки
        # os.remove(f'speech_fast/{message.text}-fast.mp3')
        # os.remove(f'speech_slow/{message.text}-slow.mp3')

        # Повторяє цю функцію
        bot.register_next_step_handler(message, speech_lang)


# Обробка інлайн клавіатури!!!!!!!!
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'about':
            bot.send_message(call.message.chat.id,
                             f'Привіт щераз 🖖. Я поможу тобі правильно вимовляти слова іноземними мовами 🗣')

        if call.data == '/languages':
            chose_language(call.message)

        if call.data == 'how':
            bot.send_message(call.message.chat.id,
                             '1. Нажміть на Розпочнемо🗂. 2. Виберіть мову 🗂. 3. Я🤖 вам верну вимову цього слова')
            photo = open('Attachments/how?.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo)

bot.polling(none_stop=False)


