import telebot
from random import *
from telebot import types  # Кнопки тг импорт
import os #Картинки из папок)
import emoji
import requests
from googletrans import Translator, constants
from pprint import pprint
import database
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from database import SQLite
bot = telebot.TeleBot("5618060312:AAFKPwJBIHbbK4unvjLJem_22cm5Ck5vago")
app_id = '6752774e07260308a55a41713b6715ad'

db = SQLite("user_telebot.db")
sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                                        id integer,
                                        name TEXT ,
                                        surname text ,
                                        age integer );'''
db.execute(sqlite_create_table_query)
sqlite_create_table_admin = '''CREATE TABLE IF NOT EXISTS admin (
                                        id integer,
                                        name TEXT);'''
db.execute(sqlite_create_table_admin)
# db.add_admin_execut(345092919, "Марго")

main_keyboard = types.ReplyKeyboardMarkup(True)  # Кнопки
main_keyboard.row("Магический шар", 'Помощь', "Погода")
main_keyboard.row("Меню", "Регистрация", "Переводчик")
main_keyboard.row("Игра угадай число", "Получить фото")
main_keyboard.row("Стикер", "Калькулятор", "Криптовалюта")

no_keyboard = types.ReplyKeyboardMarkup(True)
no_keyboard.row("Нет")

yes_no_keyboatd = types.ReplyKeyboardMarkup(True)
yes_no_keyboatd.row("Да", "Нет")

cryptocurrency_keyboard = types.ReplyKeyboardMarkup(True)
cryptocurrency_keyboard.row('Bitcoin', 'Ethereum')
cryptocurrency_keyboard.row('EUR', 'RUB', 'USD')

crypto_keyboard = types.ReplyKeyboardMarkup(True)
crypto_keyboard.row('Bitcoin', 'Ethereum')

currency_keyboard = types.ReplyKeyboardMarkup(True)
currency_keyboard.row('EUR', 'RUB', 'USD')

admin_keyboard = types.ReplyKeyboardMarkup(True)
admin_keyboard.row('users bd', 'del user', 'add admin')
admin_keyboard.row("del admin", "check admin")

calculator_keyboard = types.ReplyKeyboardMarkup(True)
calculator_keyboard.row("Простые вычисления", "Дроби", "Степени")

id_admins = [345092919]

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, я бот помощник. Буду помогать тебе!",
                     reply_markup=main_keyboard)  # Кнопка клавиатура


@bot.message_handler(commands=["помощь"])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Пока не могу помочь, меня разрабатывают",
                     reply_markup=main_keyboard)  # Кнопка клавиатура


@bot.message_handler(commands=["magic_ball"])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, я магический шар! Напиши свой вопрос!")
    bot.register_next_step_handler(message, game_play)


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Пока не могу помочь, меня разрабатывают")

@bot.message_handler(commands=["guess_the_number"])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Добро пожаловать в игру 'Угадай число'!")
    start_game(message)

@bot.message_handler(content_types=["text"])
def send_message(message):
    text = message.text.lower()
    if text == "помощь":
        bot.send_message(message.from_user.id, "Пока не могу помочь, меня разрабатывают")
    elif text == "магический шар" or text == "game":
        bot.send_message(message.from_user.id, "Привет, я магический шар! Напиши свой вопрос!")
        bot.register_next_step_handler(message, game_play)
    elif text == "меню" or text == "/menu":
        bot.send_message(message.from_user.id, "Ты можешь выбрать нужное тебе действие: \n " +
                         "/help - Помощь \n" + "/magic_ball - Игра магический шар \n" + "/guess_the_number - Игра угадай число \n")
    elif text == "регистрация":
        bot.send_message(message.from_user.id, "Напишите Ваше имя")
        bot.register_next_step_handler(message, get_name)
    elif text == "игра угадай число":
        bot.send_message(message.from_user.id, "Добро пожаловать в игру 'Угадай число'!")
        start_game(message)
    elif text == "получить фото":
        bot.send_photo(message.from_user.id, open("тт.jpg", "rb"))
        bot.send_photo(message.from_user.id, "https://i.imgur.com/77YeKfh.jpeg")
        bot.send_video(message.from_user.id, 'https://i.imgur.com/URY3Wd4.mp4')
    elif text == "получить мем":
        get_files_names_memes(message)
    elif text == "стикер":
        stikers = ["CAACAgIAAxkBAAEF_OxjOryYP3pX0KWxfRwqC3s-11YWOwACLgADN7ORFJ6m-GsXdZUWKgQ",
                   "CAACAgIAAxkBAAEF_OpjOryW4Lx5aDVRTWOBR4jB_cgc6QACLwADN7ORFF5aVpEyrfDtKgQ",
                   "CAACAgIAAxkBAAEF_OhjOryUB34CR-BIscbForTnEgvDpwACog8AAjx1GEi-eZ90LVK_IioE",
                   "CAACAgIAAxkBAAEF_OZjOryS1m2GbgQJEIQuUKzmjaz-RgACEA4AAniAGEigRfnK2vZrjyoE",
                   "CAACAgIAAxkBAAEF_ORjOryPXhTl3TXlX9mo7wrJgptcsAACbRIAAsvG0UhbxGS4C108yyoE",
                   "CAACAgIAAxkBAAEF_OJjOryNFaP4moyVKvqwPf8hdRLp-wACLxYAAnujyEirRjCqmOc1uyoE",
                   "CAACAgIAAxkBAAEF_OBjOryLtYJs8pj55xlyhH2UhQzQowACgBkAAr0ByUjmqj-AiCmidyoE",
                   "CAACAgIAAxkBAAEF_N5jOryIoEu0tG4bp343JT6I5B6g_AACqBIAAlCHyEgmu776I8ZkVSoE",
                   "CAACAgIAAxkBAAEF_NRjOrvwhRsE7SmIQ1PUdGJh0sI9qAACCxEAAnv90Ug6UurudObDbyoE"]
        stiker = choice(stikers)
        bot.send_sticker(message.from_user.id, stiker)
    elif text == "смайлик":
        bot.send_message(message.from_user.id, emoji.emojize(":thumbs_up:"))
    elif text == 'погода':
        bot.send_message(message.from_user.id, "Напишите нужный Вам город!)")
        bot.register_next_step_handler(message, weather)
    elif text == "переводчик":
        bot.send_message(message.from_user.id, "Вы хотите получить список всех языков? Напишите 'Да' или  'Нет' ;)", reply_markup= yes_no_keyboatd)
        bot.register_next_step_handler(message, translate_yes_no)
    elif text == "криптовалюта":
        bot.send_message(message.from_user.id, "Нажмите на нужную Вам валюту:3", reply_markup=cryptocurrency_keyboard)
        bot.register_next_step_handler(message, cryptocurrency_get)
    elif text == "админ панель":
        if db.check_admin_execut(message.from_user.id):
            bot.send_message(message.from_user.id, "Привет, Админ!", reply_markup=admin_keyboard)
            bot.register_next_step_handler(message, admin_bd)
        else:
            bot.send_message(message.from_user.id, "ТЫ НЕ ПРОЙДЕШЬ!", reply_markup=main_keyboard)



# сделать перевод только из крипты в долабы, и т.д и наоборот




def admin_del_admin(message):
    id_admin = message.text
    if int(id_admin) in id_admins:
        bot.send_message(message.from_user.id, "Его нельзя удалить", reply_markup=main_keyboard)
    else:
        if db.del_admin_execut(id_admin):
            bot.send_message(message.from_user.id, "Вы успешно удалили Админа", reply_markup=main_keyboard)
        else:
            bot.send_message(message.from_user.id, "Произошла ошибка:(", reply_markup=main_keyboard)

def admin_get_user_del(message):
    user_id = message.text
    if db.del_execut(user_id):
        bot.send_message(message.from_user.id, "Вы успешно удалили пользователя", reply_markup=main_keyboard)
    else:
        bot.send_message(message.from_user.id, "Произошла ошибка:(", reply_markup=main_keyboard)

def admin_add_admin(message):
    id_admin, name_admin = message.text.split()
    if db.add_admin_execut(id_admin, name_admin):
        bot.send_message(message.from_user.id, "Вы успешно добавили Админа", reply_markup=main_keyboard)
    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так..", reply_markup=main_keyboard)

def admin_bd(message):
    try:
        command = message.text.lower()
        if command == 'users bd':
            users = ""
            data_base_get_users = db.select_execute()
            for i in data_base_get_users:
                users += " " + str(i)
                users += "\n"
            bot.send_message(message.from_user.id, users, reply_markup=main_keyboard)
        elif command == 'del user':
            bot.send_message(message.from_user.id, "Напишите ID")
            bot.register_next_step_handler(message, admin_get_user_del)
        elif command == 'add admin':
            bot.send_message(message.from_user.id, 'Напишите id и Имя пользователя используя только пробел')
            bot.register_next_step_handler(message, admin_add_admin)
        elif command == "del admin":
            bot.send_message(message.from_user.id, "Напишите ID")
            bot.register_next_step_handler(message, admin_del_admin)
        elif command == "check admin":
            admins = ""
            data_base_get_admin = db.list_admin_execut()
            for i in data_base_get_admin:
                admins += " " + str(i)
                admins += "\n"
            bot.send_message(message.from_user.id, admins, reply_markup=main_keyboard)



    except:
        print('Бд пустая')
        bot.send_message(message.from_user.id, "Произошла ошибка", reply_markup=main_keyboard)

def cryptocurrency_output(message, currency, quantity):
    try:
        global cg
        output = message.text.lower()
        print(output, currency, quantity)
        crypto = ['bitcoin', 'ethereum']
        currency_money = ['eur', 'rub', 'usd']
        if currency in crypto:
            money = cg.get_price(ids=currency, vs_currencies=output)
            money_total = money[currency][output] * quantity
            bot.send_message(message.from_user.id, output + " = " + str(money_total), reply_markup=main_keyboard)
        elif currency in currency_money:
            money = cg.get_price(ids=output, vs_currencies=currency)
            money_total = quantity / money[output][currency]
            bot.send_message(message.from_user.id, output + " = " + str(money_total), reply_markup=main_keyboard)
    except Exception as error:
        print(Exception)
        bot.send_message(message.from_user.id, "Переводить можно только из крипты в валюту и наоборот. Попробуйте еще раз:)",
                         reply_markup=main_keyboard)
def cryptocurrency_quantity(message, currency):
    try:
        quantity = message.text
        if "," in quantity:
            quantity = quantity.replace(",", ".")
        quantity = float(quantity)
        crypto = ['bitcoin', 'ethereum']
        currency_money = ['eur', 'rub', 'usd']
        if currency in crypto:
            bot.send_message(message.from_user.id, "Нажмите на валюту в которую перевести:3", reply_markup=currency_keyboard)
            bot.register_next_step_handler(message, cryptocurrency_output, currency, quantity)
        elif currency in currency_money:
            bot.send_message(message.from_user.id, "Нажмите на валюту в которую перевести:3",
                             reply_markup=crypto_keyboard)
            bot.register_next_step_handler(message, cryptocurrency_output, currency, quantity)



    except Exception as error:
        bot.send_message(message.from_user.id, "Вам нужно написать число, попробуйте еще раз:((",
                         reply_markup=main_keyboard)
def cryptocurrency_get(message):

    currency = message.text.lower()
    bot.send_message(message.from_user.id, "Напишите количество:3")
    bot.register_next_step_handler(message, cryptocurrency_quantity, currency)

def translate_language(message, words):
    try:
        language = message.text
        print(words)
        print(language)
        translator = Translator()
        translation = translator.translate(words, dest=language)
        bot.send_message(message.from_user.id, translation.origin + ' ' + translation.src + "\n" + translation.text + ' ' + translation.dest, reply_markup=main_keyboard)
    except Exception as error:
        bot.send_message(message.from_user.id, "Вы неправильно ввели язык, посмотрите список языков", reply_markup=main_keyboard)
def translate(message):
    words = message.text

    bot.send_message(message.from_user.id, "Напишите нужный Вам язык в формате 'RU', 'EN'")
    bot.register_next_step_handler(message, translate_language, words)

def translate_language_full(message):
    language_full = ["ru - Русский", "en - Английский", "de - Немецкий", "af - Африканский", "am - Амхарский",
                     "ar - Арабский", "az - Азербайджанский", "be - Белорусский", "bg - Болгарский",
                     "bn - Бенгальский",
                     "bs - Боснийский", "ca - Каталанский", "ceb - Сербский", "co - Корсиканский",
                     "cs - Чешский", "cy - Валлийский",
                     "da - Датский", "el - Греческий", "eo - Эсперанто", "es - Испанский", "et - Эстонский",
                     "eu - Баскский", "fa - Персидский",
                     "fi - Финский", "fr - Французский", "fy - Фризский", "ga - Ирландский",
                     "gd - Шотландскийгэльский", "gl - Галисийский",
                     "gu - Гуджарати", "ha - Хауса", "haw - Гавайский", "he - Иврит", "hi - Хинди",
                     "hmn - Хмонг", "hr - Хорватский",
                     "ht - Гаитянскийкреольский", "hu - Венгерский", "hy - Армянский", "id - Индонезийский",
                     "ig - Игбо", "is - Исландский",
                     "it - Итальянский", "iw - Иврит", "ja - Японский", "jw - Яванский", "ka - Грузинский",
                     "kk - Казахский", "km - Кхмерский",
                     "kn - Каннада", "ko - Корейский", "ku - Курдский(курманджи)", "ky - Киргизский",
                     "la - Латинский", "lb - Люксембургский"]


    bot.send_message(message.from_user.id, '\n'.join(language_full))
    bot.send_message(message.from_user.id, "Напишите Ваш текст :3")
    bot.register_next_step_handler(message, translate)

def translate_yes_no(message):
    answer = message.text.lower()
    print(answer)
    if answer == "yes" or answer == "да":
        translate_language_full(message)
    else:
        bot.send_message(message.from_user.id, "Напишите Ваш текст :3")
        bot.register_next_step_handler(message, translate)




def check_weather_big_one(message, number, info):
    global app_id
    info_city = info["list"][number]
    id_city = info_city["id"]
    answer = requests.get("http://api.openweathermap.org/data/2.5/weather",
                          params={'id': id_city, 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
    info = answer.json()
    temp = int(info["main"]["temp"])
    temp_min_and_max = [int(info["main"]["temp_min"]), int(info["main"]["temp_max"])]
    weather = info["weather"][0]["description"]


    bot.send_message(message.from_user.id, "Температура: " + str(temp) + "\n" + "Минимальная температура " + str(temp_min_and_max[0]) + '\n' + 'Наибольшая темпепратура ' + str(temp_min_and_max[1]) + "\n" + "Погода: " + weather, reply_markup=main_keyboard)


def number_user_weather(message, info):
    number = message.text
    if number.isdigit() and 0 < int(number) <= (len(info)):
        number = int(number) - 1
        check_weather_big_one(message, number, info)
    else:
        bot.send_message(message.from_user.id,"Вы написани не правильный номер, повторите попытку!")
        bot.register_next_step_handler(message, number_user_weather, info)

def citi_big_one(message, info):
    global info_city
    for i in range(len(info["list"])):
        bot.send_message(message.from_user.id, str(i + 1) + ": " + info["list"][i]["name"]+ " " + info["list"][i]["sys"]["country"])
    bot.send_message(message.from_user.id, "Напишите номер: ")
    bot.register_next_step_handler(message, number_user_weather, info)

def weather(message):
    city = message.text
    global app_id
    try:
        answer = requests.get("http://api.openweathermap.org/data/2.5/find",
                              params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
        info = answer.json()
        number = 0
        if len(info["list"]) > 1:
            citi_big_one(message, info)
        else:
            check_weather_big_one(message, number, info)
    except Exception as error:
        bot.send_message(message.from_user.id, "Этот город не найден :(", reply_markup=main_keyboard)
    number = 0


def get_files_names_memes(message):
    files = os.listdir(path="./meme")
    mem = choice(files)
    bot.send_photo(message.from_user.id, open("./meme/" + mem, "rb"))
    files.remove(mem)
def Yes_no_check_quit(message):
    text = message.text.lower()
    total = 0
    if text == "да" or text == "lf" or text == "yes":
        start_game(message)
    else:
        bot.send_message(message.from_user.id, "Приходи еще!",
                         reply_markup=main_keyboard)



def process_game(message, random_num, total):
    numbers = message.text
    total += 1
    if numbers.isdigit() and 1 <= int(numbers) <= 100:
        numbers = int(numbers)
        if random_num == numbers:
            bot.send_message(message.from_user.id, "Вы угадали, поздравляем! Это была " + str(total) + " попытка!")
            bot.send_message(message.from_user.id, "Хотите сыграть еще? Напишите 'Да' или 'Нет' : ",
                             reply_markup=yes_no_keyboatd)
            bot.register_next_step_handler(message, Yes_no_check_quit)


        elif random_num < numbers:
            bot.send_message(message.from_user.id, "Попытка № " + str(total) + ": " + "Слишком много, попробуйте еще раз")
            bot.register_next_step_handler(message, process_game, random_num, total)

        else:
            bot.send_message(message.from_user.id, "Попытка № " + str(total) + " : " + ' Слишком мало, попробуйте еще раз')
            bot.register_next_step_handler(message, process_game, random_num, total)

    else:
        bot.send_message(message.from_user.id, "Введите корректное число от 1 до 100")
        bot.register_next_step_handler(message, process_game, random_num, total)


def start_game(message):
    bot.send_message(message.from_user.id, "Введи число от 1 до 100: ")
    random_num = randint(1, 100)
    total = 0
    bot.register_next_step_handler(message, process_game, random_num, total)




def get_name(message):
    name = message.text

    bot.send_message(message.from_user.id, "Напишите Вашу фамилию")
    bot.register_next_step_handler(message, get_surname, name)


def get_surname(message, name):
    surname = message.text

    bot.send_message(message.from_user.id, "Напишите Ваш возраст(Используйте только цифры)")
    bot.register_next_step_handler(message, get_number, name, surname)


def get_number(message, name, surname):
    age = message.text
    res = "Ваше имя: " + name + "\n"
    res += "Ваша фамилия: " + surname + "\n"
    res += "Ваш возраст: " + age + "\n"
    bot.send_message(message.from_user.id, "Ваши данные: " + "\n" + res)
    id_user = message.from_user.id
    sqlite_select_query = 'INSERT INTO users (id, name, surname, age) VALUES ( ' + str(
        id_user) + ', \'' + name + '\',' + ' \'' + surname + '\', ' + age + ');'
    if db.execute(sqlite_select_query):
        bot.send_message(message.from_user.id, "Вы успешно зарегистрировались :3", reply_markup=main_keyboard)
    else:
        bot.send_message(message.from_user.id, "Возникли какие-то неполадки, попробуйте еще раз:((", reply_markup=main_keyboard)



def game_play(message):
    text = message.text.lower()
    if text == "нет" or text == "ytn" or text == "no":
        bot.send_message(message.from_user.id,
                         "Жду тебя снова!", reply_markup=main_keyboard)

        return
    else:
        answer = ["Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да", "Можешь быть уверен в этом",
                  "Мне кажется - да",
                  "Вероятнее всего", "Хорошие перспективы", "Знаки говорят - да", "Да", "Пока неясно, попробуй снова",
                  "Спроси позже",
                  "Лучше не рассказывать", "Сейчас нельзя предсказать", "Сконцентрируйся и спроси опять",
                  "Даже не думай",
                  "Мой ответ - нет",
                  "По моим данным - нет", "Перспективы не очень хорошие", "Весьма сомнительно"]

    bot.send_message(message.from_user.id, choice(answer))
    bot.send_message(message.from_user.id,
                     "Ты хочешь еще что-то спросить? \n Напиши вопрос или 'Нет' если хочешь закончить ",
                     reply_markup=no_keyboard)
    bot.register_next_step_handler(message, game_play)



bot.polling(none_stop=True, timeout=123)