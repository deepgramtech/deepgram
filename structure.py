import telebot
from Task import Task
import parser
from telebot import types
import qrcode
import os
from PIL import Image
from io import BytesIO
import pprint
import requests
#main variables
TOKEN = 'PUT-HERE-YOUR-TOKEN'
bot = telebot.TeleBot (TOKEN)
task = Task ()
positive = 'Yes, please.'
negative = 'No, thanks.'
ticket = 'Book a free ticket'
info = 'Just info'
channel_to_forward_id = '@experimenting1'

user = bot.get_me()
def binary_markup(first_choice, second_choice):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    first = types.KeyboardButton(first_choice)
    second = types.KeyboardButton(second_choice)
    markup.row(first, second)
    return markup
def forward_message_to(channel_to_forward_id, message):
    from_chat_id = message.chat.id
    message_id = message.message_id
    bot.forward_message(channel_to_forward_id, from_chat_id, message_id)

@ bot.message_handler (commands = ['cnn'])
def start_handler (message):
    if not task.cnn:
        chat_id = message.chat.id
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("MNIST", callback_data="mnist"))
        keyboard.add(types.InlineKeyboardButton("CIFAR10", callback_data="cifar10"))
        msg = bot.send_message (chat_id, 'Choose a dataset', reply_markup = keyboard)
        #bot.register_next_step_handler (msg, askInfo)
        task.cnn = True

@bot.callback_query_handler(lambda dataset: dataset.data in ["mnist"])
def train_mnist(dataset):
  chat_id = dataset.message.chat.id
  print('mnist')
  bot.send_message(chat_id, 'You chose mnist')



@bot.callback_query_handler(lambda dataset: dataset.data in ["cifar10"])
def train_mnist(dataset):
  chat_id = dataset.message.chat.id
  print('cifar10')
  bot.send_message(chat_id, 'You chose cifar10')




@ bot.message_handler (commands = ['help'])
def help_function (message):
    chat_id = message.chat.id
    print(message)
    forward_message_to(channel_to_forward_id, message)
    msg = bot.send_message (chat_id, 'The commands you can try are /start for info, /qrcoder to encode a message and /flip to rotate an image.')
    return
#handlers
@ bot.message_handler (commands = ['start', 'go'])
def start_handler (message):
    if not task.isRunning:
        chat_id = message.chat.id
        msg = bot.send_message (chat_id, 'Hey, do you want to know more about DeepGram?', reply_markup = binary_markup(positive, negative))
        bot.register_next_step_handler (msg, askInfo)

        task.isRunning = True


def askInfo (message):
    chat_id = message.chat.id
    text = message.text
    if text == '/start':
        task.isRunning = False
        bot.register_next_step_handler (message, start_handler)
    if text == positive:
        msg = bot.send_message (chat_id, 'Do you want to book a free ticket for the next event or just info?', reply_markup = binary_markup(ticket,info))
        bot.register_next_step_handler (msg, info_or_meetup)
    elif text == negative:
        msg = bot.send_message (chat_id, 'Ok, eventually you can type /start to start over.')
        task.isRunning = False
        #bot.register_next_step_handler (msg, start_handler)
    else:
        msg = bot.send_message (chat_id, 'Enter the section correctly.')
        bot.register_next_step_handler (msg, askInfo)
        return

def info_or_meetup (message):
    chat_id = message.chat.id
    text = message.text
    if text == '/start':
        bot.register_next_step_handler (message, start_handler)
    if text == ticket:
        msg = bot.send_message (chat_id, 'You are doing right! Book it here: https://www.eventbrite.it/e/biglietti-deepgram4-creiamo-un-bot-per-il-deep-learning-79733094833')
        task.isRunning = False
        #bot.register_next_step_handler (msg, start_handler)
    elif text == info:
        msg = bot.send_message (chat_id, 'Great! It is a Meetup we take every two weeks at Digital Tree (https://digitaltree.ai) to create a Telegram Bot to perform Deep Learning! Interesting, right? Learn more at deepgram.tech.')
        task.isRunning = False
        #bot.register_next_step_handler (msg, start_handler)
    else:
        msg = bot.send_message (chat_id, 'Enter the section correctly.')
        task.isRunning = False
        bot.register_next_step_handler (msg, info_or_meetup)
    return

@ bot.message_handler (commands = ['qrcode', 'qrcoder'])
def qrcoder_handle(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Insert the message to encode or type or type "no" to undo.')
    bot.register_next_step_handler (msg, qrcoder_send)

def qrcoder_send(message):
    chat_id = message.chat.id
    if message.content_type == 'text':
            msg_text = message.text
            print(msg_text)
    else:
        msg = bot.send_message(chat_id, 'You can encode only strings. Send a message again')
        bot.register_next_step_handler (msg, qrcoder_send)
    if msg_text.lower() == 'no':
        return 0
    if msg_text.lower() == '/qrcoder':
        msg = bot.send_message(chat_id, 'Sorry you cannot do it now. Type "no" if you want to undo and start again.')
        bot.register_next_step_handler (msg, qrcoder_send)

    img=qrcode.make(msg_text)
    name_file = "qrcode_" + str(chat_id) + ".png"
    img.save(name_file)
    img_output=open(name_file,"rb")
    #invio il qrcode
    try:
        bot.send_photo(chat_id,img_output)
    except:
        msg = bot.send_message(chat_id, 'Something went wrong. Try again, please.')
        bot.register_next_step_handler (msg, qrcoder_send)
    try:
        os.remove(name_file)
        print("File Removed!")
    except:
        return 0

def photo_message(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file = bot.get_file(fileID)
    print('file.file_path =', file.file_path)
    ffile_photo = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file.file_path)
    print(ffile_photo)
    response = requests.get(ffile_photo)
    return response

@ bot.message_handler(commands = ['flip'])
def flip_handler(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Send here a picture that you want to flip')
    bot.register_next_step_handler (msg, flip_image)

def flip_image(message):
    chat_id = message.chat.id
    content_type = message.content_type
    if content_type=='photo':
        response = photo_message(message)
        img = Image.open(BytesIO(response.content))
        print('img type is:')
        print(type(img))
        img_modified=img.rotate(180)
        name_file = "flipped_" + str(chat_id) + ".png"
        img_modified.save(name_file)
        #download_photo(ffile_photo)
        img_loaded = open(name_file, 'rb')
        bot.send_photo(chat_id, img_loaded)
        try:
            os.remove(name_file)
            print("File Removed!")
        except:
            return 0
    else:
        msg = bot.send_message(chat_id, 'Only photos are accepted. Start again.')
        bot.register_next_step_handler (msg, flip_image)

    return 0

@bot.message_handler (content_types=["photo","document","text","audio"])
def file_info(message):
    content_type=message.content_type
    chat_id=message.chat.id
    user_name=message.chat.username
    print("message type: %s\nmessagge from: %s(%s)"%(content_type,user_name,chat_id))
    if content_type=="photo":
        file_size=message.photo[0].file_size
        file_id=message.photo[0].file_id

        print("size:",file_size,"b\nid file:",file_id)

    elif content_type=="document":
        file_name=message.document.file_name
        file_size=message.document.file_size
        file_id=message.document.file_id

        print("name: %s\nsize: %sb\nid: %s"%(file_name,file_size,file_id))

    elif content_type=="audio":
        title=message.audio.title
        file_size=message.audio.file_size
        mime_type=message.audio.mime_type
        artist=message.audio.performer
        print("title: %s\nsize: %sb\nmime_type: %s\nartist: %s"%(title,file_size,mime_type,artist))

    elif content_type=="text":
        print("message: %s"%message.text)


bot.polling (none_stop = True)
