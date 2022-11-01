import requests
import json
import re


# url = 'https://www.wildberries.ru/catalog/97565916/detail.aspx?targetUrl=BP'


# Вариант получения нужной ссылки через регулярные выражения
# url_fix= [int(s) for s in re.findall(r'-?\d+\.?\d*', url)]
#
# card_detail_json = f'https://card.wb.ru/cards/detail?nm={url_fix[0]}'
# print(card_detail_json)
# Вариант получения ссылки через список
def page_parce(url):
    new_url = url.split('/')[-2]
    json_url = f'https://card.wb.ru/cards/detail?nm={new_url}'
    req = requests.get(url=json_url)
    # with open('req.json', 'w') as file:
    #     json.dump(req.json(), file, indent=4, ensure_ascii=False)
    #

    package_card = req.json()
    items = package_card['data']['products']
    for item in items:
        item_name = item["name"]
        item_brand = item['brand']
        item_price = item['salePriceU'] / 100
        item_price = item_price.__round__()
        item_raiting = item['rating']
        # print(f"Название: {item_name}\nБренд: {item_brand}\nЦена: {item_price} рублей\nРейтинг товара: {item_raiting} звезд(ы)")
        return(item_name[0:50])




