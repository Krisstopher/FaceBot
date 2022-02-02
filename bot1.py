import telebot
import random
import cv2
import requests as rq
from code import start

token = '640773264:AAF8ZOAo7Hgi0Q3ZAJIX_CTwkeTiTIi5isk'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text", "photo"])

def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    if (message.content_type == 'photo') :
        k = random.randint(0, 2)
        if (k == 0) :
            bot.send_message(message.chat.id, 'Ищу двойников...')
        if (k == 1) :
            bot.send_message(message.chat.id, 'Изображение обрабатывается...')
        if (k == 2) :
            bot.send_message(message.chat.id, 'Подождите, ищу похожих людей...')
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        print(file_info)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('new_file.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
       # raw = message.photo[2].file_id
       # name = raw + ".jpg"
       # finf = bot.get_file(raw)
       # file = rq.get('https://api.telegram.org/file/bot' + token + '/' + finf.file_path)
       # file.show()
       # with open(name, 'wb') as new_file:
       #     new_file.write(file)
       # img = cv2.imread(name)
        img = cv2.imread('new_file.jpg')
        facelist = start(img)
        if (len(facelist) > 0) :
            bot.send_message(message.chat.id, str(int((1 - facelist[0][0])*100)) + '% сходства лиц')
            bot.send_photo(message.chat.id, open(facelist[0][1], 'rb'))
            bot.send_message(message.chat.id, str(int((1 - facelist[1][0])*100)) + '% сходства лиц')
            bot.send_photo(message.chat.id, open(facelist[1][1], 'rb'))
            bot.send_message(message.chat.id, str(int((1 - facelist[2][0])*100)) + '% сходства лиц')
            bot.send_photo(message.chat.id, open(facelist[2][1], 'rb'))
            bot.send_message(message.chat.id, str(int((1 - facelist[3][0])*100)) + '% сходства лиц')
            bot.send_photo(message.chat.id, open(facelist[3][1], 'rb'))
            bot.send_message(message.chat.id, str(int((1 - facelist[4][0])*100)) + '% сходства лиц')
            bot.send_photo(message.chat.id, open(facelist[4][1], 'rb'))
        else :
            bot.send_message(message.chat.id, 'Не могу найти лицо на фото.')

    else :
        k = random.randint(0, 7)
        if (k == 0) :
            bot.send_message(message.chat.id, 'Это не изображение.')
        if (k == 1) :
            bot.send_message(message.chat.id, 'Пришли мне фотографию лица.')
        if (k == 2) :
            bot.send_message(message.chat.id, 'Лучше отошли мне изображение лица.')
        if (k == 3) :
            bot.send_message(message.chat.id, 'Я работаю только с изображениями.')
        if (k == 4) :
            bot.send_message(message.chat.id, 'Отправь мне фото лица, и я найду в своей базе данных похожего человека.')
        if (k == 5) :
            bot.send_message(message.chat.id, 'Я - бот для распознавания лица, а не чатбот.')
        if (k == 6) :
            bot.send_message(message.chat.id, 'Скинь сюда изображение своего лица.')
        if (k == 7) :
            bot.send_message(message.chat.id, 'Я могу найти похожего человека, если отправишь мне фото.')


if __name__ == '__main__':
     bot.polling(none_stop=True)