import datetime
import random
from requests import get
from io import BytesIO
from os import listdir
from PIL import (Image, ImageDraw, ImageFont)


def get_coinmarketcap_data():
    dict_of_cryptocurrency = {}
    data = get('https://api.coinmarketcap.com/v2/ticker/?limit=6')
    Json_data = data.json()

    for i in list(Json_data['data'].values()):
        answer = [i['id'], i['quotes']['USD']['percent_change_24h']]
        dict_of_cryptocurrency[i['name']] = answer

    return dict_of_cryptocurrency


def get_coinmarketcap_img(url):
    response = get(url)
    i = Image.open(BytesIO(response.content)).convert("RGBA")
    return i


def get_img_name():
    list_of_images = listdir('news/images')
    return random.choice(list_of_images)


def get_newspaper_image(image_name=get_img_name()):
    RED = (240, 67, 58)
    GREEN = (58, 240, 128)
    DATE = str(datetime.date.today())
    color_number = 0

    fontlight = ImageFont.truetype("news/fonts/Roboto_Slab/RobotoSlab-Light.ttf", 70)
    fontbold = ImageFont.truetype("news/fonts/Roboto_Slab/RobotoSlab-Bold.ttf", 120)
    fontroboto = ImageFont.truetype("news/fonts/Roboto/Roboto-Regular.ttf", 36)

    im = Image.open(f'news/images/{image_name}').resize((2000, 1000), Image.ANTIALIAS)
    fl = Image.open('news/system_img/filter1.jpg')
    im.size
    filtered_image = Image.blend(im, fl, 0.4)
    draw = ImageDraw.Draw(filtered_image)

    coinmarketcap_data = get_coinmarketcap_data()
    list_of_coinmarketdata_values = list(coinmarketcap_data.values())

    distance = filtered_image.size[0] / 6

    for i in list_of_coinmarketdata_values:
        url = f'https://s2.coinmarketcap.com/static/img/coins/128x128/{i[0]}.png'
        img = get_coinmarketcap_img(url)

        img_nyumber = list_of_coinmarketdata_values.index(i)
        x = int(distance * img_nyumber + 100)
        y = filtered_image.size[1] - 150
        filtered_image.paste(img, (x, y))

        h24_changes = i[1]

        if h24_changes < 0:
            color = RED
            color_number += 1
        else:
            color = GREEN

        draw.text((x + 135, y + 42), str(h24_changes),
        color, font=fontroboto)

    if color_number > 3:
        color = RED
    else:
        color = GREEN

    draw.text((100, 250), DATE,
    color, font=fontlight)

    draw.text((100, 100), "CryptoNews",
    (255, 255, 255), font=fontbold)

    imgByteArr = BytesIO()
    filtered_image.save(imgByteArr, format='PNG')
    return imgByteArr.getvalue()
