import requests
from api_utils import get_degree_size, get_toponim, get_coords, show_map_pygame, show_map

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "ebbc19e0-2f51-41bc-bb0a-4b882df65a8e"

address_ll = "37.604063,55.756386"
param_point = ''

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass
res = []
res_2 = []
# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
for i in range(10):
    organization = json_response["features"][i]
    # Название организации.
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    text = organization["properties"]["CompanyMetaData"]["Hours"]['text']
    
    # Получаем координаты ответа.
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    delta = "0.02"
    res.append((org_point, text))
    # Собираем параметры для запроса к StaticMapsAPI:
for i in res:
    if i[1][0:9] == 'ежедневно':
        color = 'pm2dgl'
    else:
        color = 'pm2lbl'
    param_point += f'{i[0]},{color}~'

map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": param_point[0:-1]
}
show_map(map_params)