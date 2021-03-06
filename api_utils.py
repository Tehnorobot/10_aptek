import requests
import sys
import os
import pygame
from io import BytesIO
from PIL import Image

API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"
API_KEY_FIND_ORG = 'ebbc19e0-2f51-41bc-bb0a-4b882df65a8e'

# Получаем первый топоним из ответа геокодера
def get_toponim(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
    "apikey": API_KEY_GEOCODER,
    "geocode": toponym_to_find,
    "format": "json"}
    
    response = requests.get(
        geocoder_api_server,
        params=geocoder_params)
    
    if response:
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym

    # Ошибка выполнения запроса
    print("Ошибка выполнения запроса:")
    return None
    
# поиск_топонима_по_адресу
def get_coords(toponym_to_find):
    toponym = get_toponim(toponym_to_find)
    # Запрос успешно выполнен
    if toponym:
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        return(toponym_coodrinates)
    return None

# получить размер карты в градусах  
def get_degree_size(toponym_to_find):
    toponym = get_toponim(toponym_to_find)
    # Запрос успешно выполнен
    if toponym:
        # Координаты углов топонима:
        x1, y1 = map(float,
                     toponym["boundedBy"]["Envelope"]["lowerCorner"].split())
        x2, y2 = map(float,
                     toponym["boundedBy"]["Envelope"]["upperCorner"].split())
        return str(abs(x1 - x2)), str(abs(y1 - y2))
    return None
 
# Показать карту (pygame)
def show_map_pygame(params):
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    # Удаляем за собой файл с изображением.
    os.remove(map_file)

# Показать карту (BytesIO)
def show_map(params):
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        sys.exit(1)

    # Сформируем изображение из строки байт.
    Image.open(BytesIO(response.content)).show()