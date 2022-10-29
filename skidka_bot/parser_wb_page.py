import requests
import json
import re

url = 'https://www.wildberries.ru/catalog/73118021/detail.aspx?targetUrl=GP'
# Вариант получения нужной ссылки через регулярные выражения
# url_fix= [int(s) for s in re.findall(r'-?\d+\.?\d*', url)]
#
# card_detail_json = f'https://card.wb.ru/cards/detail?nm={url_fix[0]}'
# print(card_detail_json)
# Вариант получения ссылки через список
new_url = url.split('/')[-2]
print(f'https://card.wb.ru/cards/detail?nm={new_url}')

