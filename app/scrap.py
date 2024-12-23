import requests
from bs4 import BeautifulSoup
import sqlite3
from functools import wraps

urls = {"wine": "https://simplewine.ru/catalog/vino/page",
        "champagne": "https://simplewine.ru/catalog/shampanskoe_i_igristoe_vino/page",
        "whiskey": "https://simplewine.ru/catalog/ksn/viski/page"}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def scrapp_wine(pages):
    drinks = []
    for cnt in range(1, pages + 1):
        link = urls["wine"] + str(cnt)
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        wines = soup.find_all("div", {"class": "catalog-grid__item"})
        for i in wines:
            try:
                winelink = "https://simplewine.ru" + \
                           i.find_all("a", {"class": "swiper-container js-toggle-group js-dy-slot-click"})[0]["href"]
                response2 = requests.get(winelink, headers=headers)
                response2.raise_for_status()
                soup = BeautifulSoup(response2.text, 'html.parser')
                data = soup.find_all("dd", {"class": "product-brief__value"})

                drinktype = "Вино"
                name = i.find_all("div", {"id": "snippet-buy-block"})[0]["data-product-name"]
                price = float(soup.find_all("meta", {"itemprop": "price"})[0]["content"])
                color, region, sugar, grape, manufacture = list(map(lambda x: x.strip(), [data[j].text for j in range(5)]))
                strength = float(data[5].text.strip()[0:-1])
                volume = float(data[6].text.strip()[0:-2])
                whiskey_type = "-"
                drinks.append((drinktype, name, price, color, region, sugar, grape, manufacture, strength,
                               volume, whiskey_type, volume * strength / 100, price / volume, winelink))
            except Exception:
                pass
    return drinks

def scrapp_champagne(pages):
    drinks = []
    for cnt in range(1, pages + 1):
        link = urls["champagne"] + str(cnt)
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        wines = soup.find_all("div", {"class": "catalog-grid__item"})
        for i in wines:
            try:
                winelink = "https://simplewine.ru" + \
                       i.find_all("a", {"class": "swiper-container js-toggle-group js-dy-slot-click"})[0]["href"]
                response2 = requests.get(winelink, headers=headers)
                response2.raise_for_status()
                soup = BeautifulSoup(response2.text, 'html.parser')
                data = soup.find_all("dd", {"class": "product-brief__value"})

                drinktype = "Игристое вино"
                name = i.find_all("div", {"id": "snippet-buy-block"})[0]["data-product-name"]
                price = float(soup.find_all("meta", {"itemprop": "price"})[0]["content"])
                color, region, sugar, grape, manufacture = list(map(lambda x: x.strip(), [data[j].text for j in range(5)]))
                strength = float(data[5].text.strip()[0:-1])
                volume = float(data[6].text.strip()[0:-2])
                whiskey_type = "-"
                drinks.append((drinktype, name, price, color, region, sugar, grape, manufacture, strength,
                               volume, whiskey_type, volume * strength / 100, price / volume, winelink))
            except Exception:
                pass
    return drinks

def scrapp_whiskey(pages):
    drinks = []
    for cnt in range(1, pages + 1):
        link = urls["whiskey"] + str(cnt)
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        wines = soup.find_all("div", {"class": "catalog-grid__item"})
        for i in wines:
            try:
                winelink = "https://simplewine.ru" + \
                       i.find_all("a", {"class": "swiper-container js-toggle-group js-dy-slot-click"})[0]["href"]
                response2 = requests.get(winelink, headers=headers)
                response2.raise_for_status()
                soup = BeautifulSoup(response2.text, 'html.parser')
                data = soup.find_all("dd", {"class": "product-brief__value"})

                drinktype = "Виски"
                name = i.find_all("div", {"id": "snippet-buy-block"})[0]["data-product-name"]
                price = float(soup.find_all("meta", {"itemprop": "price"})[0]["content"])
                color = "-"
                region = data[0].text.strip()
                sugar = "-"
                grape = "-"
                strength = float(data[1].text.strip()[0:-1])
                volume = float(data[2].text.strip()[0:-2])
                whiskey_type = data[3].text.strip()
                manufacture = data[4].text.strip()
                drinks.append((drinktype, name, price, color, region, sugar, grape, manufacture, strength,
                               volume, whiskey_type, volume * strength / 100, price / volume, winelink))
            except Exception:
                pass
    return drinks


def create_table():
    connection = sqlite3.connect('drinks.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Drinks (
    id INTEGER PRIMARY KEY,
    drinktype TEXT,
    name TEXT,
    price REAL,
    color TEXT,
    region TEXT,
    sugar TEXT,
    grape TEXT,
    manufacture TEXT,
    strength REAL,
    volume REAL,
    whiskey_type TEXT,
    alcohol REAL,
    priceforliter REAL,
    linktodrink TEXT
    )
    ''')
    drinks = scrapp_champagne(1) + scrapp_wine(0) + scrapp_whiskey(0)
    cursor.executemany('''INSERT INTO Drinks (drinktype, name, price, color, region, sugar, grape, manufacture, strength,
                              volume, whiskey_type, alcohol, priceforliter, linktodrink) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       drinks)
    connection.commit()
    connection.close()

def get_data(query):
    connection = sqlite3.connect('drinks.db')
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    if not data:
        return [(0, )]
    return data
