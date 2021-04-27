"""
@iasimov_bot 🤖 Isaac Asimov

Bot para consultar el clima de una ciudad y contar.

"""

import telebot
import requests
import math
from decouple import config
from helpers import get_emoji, emojis

# Variables de configuración
token = config('BOT_TOKEN')
api_key = config('OPEN_WEATHER_KEY')
api_url = config('OPEN_WEATHER_URL')
bot_name = config('BOT_NAME')

# Instancia del telgram Bot
bot = telebot.TeleBot(token, parse_mode=None)

menu_buttons = {
    'clima': '¡Quiero saber el clima! ' + emojis['sun'],
    'contar': '¡Quiero contar! ' + emojis['numbers']
}

back_button_text = emojis['hand_single_finger'] + ' Volver'


# Creo el teclado para el menú principal
markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
for button_text in menu_buttons.values():
    button = telebot.types.KeyboardButton(button_text)
    markup.add(button_text)

i = 0  # contador
is_counter = False  # determina si el contador esta activo


def get_main_message(message):
    """
        Mensaje de Bienvenida
    """
    msg = "¡Hola {}! mi nombre es {} {}.\n".format(
        message.chat.first_name, bot_name, emojis['robot'])
    msg += "Aquí puedes informarte acerca del clima de una ciudad o si quieres simplemente contar!\n"
    msg += "\nDime, ¿Qué quieres hacer {}?\n".format(emojis['smiling'])
    msg += "\n/clima - Consultar el clima {}\n".format(emojis['sun'])
    msg += "\n/contar - Contar {}".format(emojis['numbers'])
    return msg


def reply_markup_404(message):
    """
        Muestra el mensaje de respuesta a una ciudad no existente.
        Código de estado HTTP 404 devuelto por la API de OpenWeather
    """
    msg = 'Al parecer esa ciudad no existe {}. ¿Quieres volverlo a intentar?'.format(
        emojis['thinking'])

    keyboard = [
        [
            telebot.types.InlineKeyboardButton(
                emojis['grinning_face'] + " Si, claro! ", callback_data='contar'),
            telebot.types.InlineKeyboardButton(
                emojis['unamused_face'] + " No, tal vez déspues", callback_data='NO'),
        ]
    ]
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, msg, reply_markup=reply_markup)


def create_weather_message(data):
    """
        Muestra la información del estado del tiempo de una ciudad.
    """
    current_temp = math.ceil(int(data['main']['temp']))
    feels_like = math.ceil(data['main']['feels_like'])
    weather_description = data['weather'][0]['description']
    weather_description = weather_description[0].upper(
    ) + weather_description[1:]
    wind_speed = round(data['wind']['speed'], 1)
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    visibility = math.ceil(data['visibility'] / 1000)
    emoji = get_emoji(data['weather'][0]['id'])

    msg = "Los datos del clima en {}, {} son los siguientes:\n\n".format(
        data['name'], data['sys']['country'])
    msg += "{} Temperatura actual {}°C \n".format(emoji, current_temp)
    msg += "Sensación térmica {}°C. {}\n".format(
        feels_like, weather_description)
    msg += "Viento: {}m/s\n".format(wind_speed)
    msg += "Humedad: {}%\n".format(humidity)
    msg += "Presión atmosférica: {}hPa\n".format(pressure)
    msg += "Visibilidad: {}km".format(visibility)
    return msg


def get_city_input_user(message):
    """
        Solicita al usuario el nombre de la ciudad.
    """
    msg = "OK, Dime el nombre de la ciudad {}".format(emojis['cityscape'])

    btn = telebot.types.KeyboardButton(back_button_text)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(btn)

    message = bot.reply_to(
        message, msg, reply_markup=keyboard)
    bot.register_next_step_handler(message, check_weather)


def increase_show_couter(message):
    """
        Inicia e incrementa el contador y envia su valor al usuario.
    """
    if message.text != back_button_text:
        global i
        global is_counter

        is_counter = True
        i += 1

        btn = telebot.types.KeyboardButton(back_button_text)
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
        keyboard.add(btn)

        message = bot.reply_to(
            message, i, reply_markup=keyboard)
        bot.register_next_step_handler(message, menu)
    else:
        send_welcome(message)


def check_weather(message):
    """
        Consulta a la API de OpenWeather para obtener el clima de la ciudad
        ingresada por el usuario.
    """
    user_input = message.text.strip('/')
    if user_input != back_button_text:
        params = dict(
            q=message.text,
            appid=api_key,
            lang='es',
            units='metric'
        )

        response = requests.get(url=api_url, params=params)
        data = response.json()

        if data['cod'] == '404':
            reply_markup_404(message)
        else:
            msg = create_weather_message(data)
            bot.send_message(message.chat.id, msg)
    else:
        send_welcome(message)


@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda m: m.text == back_button_text)
def send_welcome(message):
    """
        Inicia la interación con el bot
    """
    msg = get_main_message(message)
    bot.send_message(message.chat.id, msg, reply_markup=markup)


@bot.message_handler(func=lambda m: True)
@bot.message_handler(commands=['clima', 'contar'])
def menu(message):
    """
        Evalua la opción ingresada por el usuario y despacha a la acción correspondiente.
    """
    global is_counter

    user_input = message.text.strip('/')

    if user_input in [menu_buttons['clima'], 'clima']:
        is_counter = False
        get_city_input_user(message)
    elif user_input in [menu_buttons['contar'], 'contar'] or is_counter:
        increase_show_couter(message)
    else:
        bot.send_message(message.chat.id, get_main_message(message))


@bot.callback_query_handler(func=lambda query: True)
def query_handler(query):
    """
        Evalua la opción ingresada por el usuario a través del teclado en linea.
    """
    if query.data == 'NO':
        bot.send_message(query.from_user.id,
                         'Ok, No hay problema. Estaré aquí si me necesitas {}'.format(emojis['smiling']))
    else:
        get_city_input_user(query.message)


bot.polling()
