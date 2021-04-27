emojis = {
    'robot': u'\U0001F916',
    'smiling': u'\U0000263A',
    'sun': u'\U00002600',
    'numbers': u'\U0001F522',
    'thinking': u'\U0001F914',
    'grinning_face': u'\U0001F600',
    'unamused_face': u'\U0001F612',
    'cityscape': u'\U0001F3D9',
    'hand_single_finger': u'\U0001F448',
    'thunderstorm': u'\U0001F4A8',  # Code: 200's, 900, 901, 902, 905
    'drizzle': u'\U0001F4A7',      # Code: 300's
    'rain': u'\U00002614',         # Code: 500's
    'snowflake': u'\U00002744',    # Code: 600's snowflake
    'snowman': u'\U000026C4',      # Code: 600's snowman, 903, 906
    'atmosphere': u'\U0001F301',   # Code: 700's foogy
    'clear_sky': u'\U00002600',    # Code: 800 clear sky
    'few_clouds': u'\U000026C5',   # Code: 801 sun behind clouds
    'clouds': u'\U00002601',       # Code: 802-803-804 clouds general
    'hot': u'\U0001F525',          # Code: 904
    'default_emoji': u'\U0001F300'  # default emojis
}


def get_emoji(weather_id):
    if weather_id:
        if str(weather_id)[0] == '2' or weather_id == 900 or weather_id == 901 or weather_id == 902 or weather_id == 905:
            return emojis['thunderstorm']
        elif str(weather_id)[0] == '3':
            return emojis['drizzle']
        elif str(weather_id)[0] == '5':
            return emojis['rain']
        elif str(weather_id)[0] == '6' or weather_id == 903 or weather_id == 906:
            return emojis['snowflake'] + ' ' + emojis['snowman']
        elif str(weather_id)[0] == '7':
            return emojis['atmosphere']
        elif weather_id == 800:
            return emojis['clear_sky']
        elif weather_id == 801:
            return emojis['few_clouds']
        elif weather_id == 802 or weather_id == 803 or weather_id == 803:
            return emojis['clouds']
        elif weather_id == 904:
            return emojis['hot']
        else:
            return emojis['default_emoji']

    else:
        return emojis['default_emoji']
