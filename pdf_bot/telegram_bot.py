import os
from dotenv import load_dotenv

from telebot import TeleBot
from pdf_converter import pdf_to_mp3

load_dotenv()

token = os.getenv('TOKEN')

bot = TeleBot(token)


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    bot.reply_to(message,
                 '''Отправте свой PDF файл для преобразования
в формат mp3''')


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = (message.document.file_name)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, 'Файл получен, идет обработка ...')
        pdf_to_mp3(file_path=src, language='ru')
        bot.reply_to(message, 'Файл обработан, осталось еще чуть-чуть')
        file_name = message.document.file_name.split('.')[0]
        bot.send_audio(chat_id=chat_id, audio=open(f'{file_name}.mp3',
                                                   'rb'))
    except Exception as error:
        print(f'Ошибка {error}')
        bot.reply_to(message, 'Что-то пошло не так(, повторите попытку')
    os.remove(src)
    os.remove(f'{file_name}.mp3')


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
