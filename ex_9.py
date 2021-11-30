import telebot
import random
from khayyam import JalaliDatetime
from gtts import gTTS
from qrcode import make

bot = telebot.TeleBot("T")

number = 0

@bot.message_handler(commands=['start'])
def salam(message):
    bot.reply_to(message , "سلام، خوش اومدی "  + message.from_user.first_name + '🙋🏻‍♀️')

@bot.message_handler(commands=['help'])
def Help(message):
    bot.reply_to(message ,'''
    /start ----- شروع ربات و خوش آمد گویی
    /game ----- بازی حدس عدد
    /age -----محاسبه سن شمسی
    /voice ----- تبدیل متن انگلیسی به صدا
    /max ----- پیدا کردن بزرگترین عدد
    /argmax ----- پیدا کردن اندیس بزرگترین عدد
    /qrcode ----- ساختن کد کیوآر
    /help ----- توضیحات همین پیام 
    ''')
#--------------------------------------------------------------------------------------#

@bot.message_handler(commands=['game'])
def Game(message):
    global number
    number = random.randint(1,100)
    user_guse = bot.send_message(message.chat.id,'یک عدد بین 1 تا 100 انتخاب شده، حدس بزن!' )
    bot.register_next_step_handler(user_guse, guseGame)
   
def guseGame(user_guse):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = telebot.types.KeyboardButton('New Game')
    markup.add(itembtn1)

    global number
    if user_guse.text == "New Game":
        user_guse = bot.send_message(user_guse.chat.id, 'بازی از اول شروع شد، دوباره حدس بزن',reply_markup=markup)
        number = random.randint(1,100)
        bot.register_next_step_handler(user_guse, guseGame)
    else:

        if int(user_guse.text)>100 or int(user_guse.text)<1:
            user_guse = bot.send_message(user_guse.chat.id, 'فقط عدد بین 1 تا 100 حدس بزن',reply_markup=markup)
            bot.register_next_step_handler(user_guse, guseGame)
        if int(user_guse.text)>number:
            user_guse = bot.send_message(user_guse.chat.id, 'بیا پایین تر',reply_markup=markup)
            bot.register_next_step_handler(user_guse, guseGame)
        elif int(user_guse.text)<number:
            user_guse = bot.send_message(user_guse.chat.id, 'برو بالاتر',reply_markup=markup)
            bot.register_next_step_handler(user_guse, guseGame)
        elif int(user_guse.text)==number:
            markup = telebot.types.ReplyKeyboardRemove(selective=True)
            user_guse = bot.send_message(user_guse.chat.id, 'آفرین، درست حدس زدی👏🏻\nبازی تمام شد.',reply_markup=markup)
        
#--------------------------------------------------------------------------------------#

@bot.message_handler(commands=['age'])
def Age(message):
    date = bot.send_message(message.chat.id, 'تاریخ تولدت رو به فرمت زیر وارد کن\n(1400/09/10)' )
    bot.register_next_step_handler(date, date_age)

def date_age(date):
    spl = (date.text).split("/")
    temp = JalaliDatetime.now() - JalaliDatetime(spl[0],spl[1],spl[2])
    year = temp.days // 365
    temp = temp.days%365
    month = temp //30
    day = temp%30

    bot.send_message(date.chat.id ,"سن شما " + str(year) + " سال و " + str(month) +'ماه و ' + str(day) + "روز ")

#--------------------------------------------------------------------------------------#

@bot.message_handler(commands=['voice'])
def Voice(message):
    user_text = bot.send_message(message.chat.id, 'لطفا یک متن به زبان انگلیسی تایپ کن:')
    bot.register_next_step_handler(user_text , text_to_voice)

def text_to_voice(user_text):
    convert = gTTS(text = user_text.text , lang = 'en' , slow = False)
    convert.save('voice.mp3')
    convert = open('voice.mp3' , 'rb')
    bot.send_voice(user_text.chat.id , convert )

#--------------------------------------------------------------------------------------#
@bot.message_handler(commands=['qrcode'])
def QRcode(message):
    u_txt = bot.send_message(message.chat.id, 'لینک، آیدی یا متنی که قراره براش کد qr درست کنی رو بفرست...')
    bot.register_next_step_handler(u_txt, imgQR)

def imgQR(u_txt):
    img = make(u_txt.text)
    img.save('qrcode.png')
    img = open('qrCode.png', 'rb')
    bot.send_photo(u_txt.chat.id, img)
#--------------------------------------------------------------------------------------#

@bot.message_handler(commands=['max'])
def Max(message):
    array = bot.send_message(message.chat.id, 'یک لیست از اعداد به فرمت زیر وارد کن\n14,7,78,15,8,19,20')
    bot.register_next_step_handler(array, maxArry)

def maxArry(array):
    numbers = list(map(int,array.text.split(',')))
    maximum = max(numbers)

    bot.send_message(array.chat.id, "بزرگترین عدد : " + str(maximum))

#--------------------------------------------------------------------------------------#

@bot.message_handler(commands=['argmax'])
def Argmax(message):
    array = bot.send_message(message.chat.id, 'یک لیست از اعداد به فرمت زیر وارد کن\n14,7,78,15,8,19,20')
    bot.register_next_step_handler(array, index_max)

def index_max(array):
    numbers = list(map(int,array.text.split(',')))
    index = numbers.index(max(numbers)) + 1

    bot.send_message(array.chat.id, str(index)+'مین عدد بزرگترین عدد است')

#--------------------------------------------------------------------------------------#


    



bot.infinity_polling()
