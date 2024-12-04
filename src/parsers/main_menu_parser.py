import asyncio
import time

import httpx
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

cookies = {
    '_ym_uid': '1712062070396684790',
    'UTMcookie': 'McD_App',
    'cookies-agreement': 'true',
    'x-client-verison': '73c68',
    'PHPSESSID': 'a196fgqt77ocab4g1m12qrqkd8',
    'client_define': 'mcd-user-66e9a165b33450.66892865',
    'selected-menu-category': 'burgery-i-rolly',
    'selected-subcategory': 'vse-burgery-i-rolly',
    'confirmed-city': 'true',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,ja;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_ym_uid=1712062070396684790; UTMcookie=McD_App; cookies-agreement=true; x-client-verison=73c68; PHPSESSID=a196fgqt77ocab4g1m12qrqkd8; client_define=mcd-user-66e9a165b33450.66892865; selected-menu-category=burgery-i-rolly; selected-subcategory=vse-burgery-i-rolly; confirmed-city=true',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://vkusnoitochka.ru/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
}

url = 'https://vkusnoitochka.ru/menu/'

EXTRA_PAGES = ['cuper-boks',
               'kidz-kombo',
               'sety-menee-600-kkal',
               'tolko-v-dostavke',
               'vygodno-dlya-megakompanii',
               'kombo-obed',
               'sety-i-pary',
               'zimniy-kombo']

CATEGORIES = {'novinki': 'new',
              'populyarnoe': 'popular',
              'napitki': 'drink',
              'burgery-i-rolly': 'burger',
              'kartofel-startery-i-salaty': 'snack',
              'kafe': 'cafe',
              'deserty_2': 'dessert',
              'sousy': 'other'}

TYPES = {'default': 'default',
         'Горячие напитки': 'hot',
         'Прохладительные напитки': 'cold',
         'Соки': 'juice',
         'Коктейли Молочные': 'milkshake',
         'Говядина': 'beef',
         'Курица': 'chicken',
         'Роллы': 'roll',
         'Морепродукты': 'fish',
         'Картофель': 'fries',
         'Стартеры': 'starter',
         'Салаты': 'salad',
         'Десерты и выпечка': 'dessert',
         'Напитки': 'drink',
         'Мороженое': 'icecream',
         'Десерты': 'dessert'}

TYPES_IDS = {
    'new': {'default': 1},

    'popular': {'default': 2},

    'other': {'default': 3},

    'drink': {'hot': 4,
              'cold': 5,
              'juice': 6,
              'milkshake': 7},

    'dessert': {'dessert': 8,
                'icecream': 9},

    'snack': {'salad': 10,
              'starter': 11,
              'fries': 12},

    'cafe': {'dessert': 13,
             'drink': 14},

    'burger': {'chicken': 15,
               'beef': 16,
               'roll': 17,
               'fish': 18}
}

items = []
extra_titles = []
items_types = []


async def get_extra_items(page):
    async with httpx.AsyncClient() as session:
        req = await session.get(url + page, cookies=cookies, headers=headers)

    if req.status_code == 200:

        soup = BeautifulSoup(req.text, 'html.parser')

        for el in soup.find_all('a', 'product-card'):

            tit = el.find(itemprop='name').text.capitalize()

            title_split = tit.split(' ')
            if '.' in title_split[-1] or ',' in title_split[-1]:
                continue
            elif len(title_split) >= 2 and ',' in title_split[-2]:
                continue
            tit = tit.capitalize()

            if tit not in extra_titles:
                extra_titles.append(tit)


def parse(category, tip='default'):
    cards = driver.find_elements(By.CLASS_NAME, 'product-card')

    for card in cards:
        ActionChains(driver).scroll_to_element(card).perform()
        size = card.find_element(By.CLASS_NAME, "product-card__footer").text

        title = card.find_element(By.CLASS_NAME, 'product-card__title').text
        title_split = title.split(' ')
        if '.' in title_split[-1] or ',' in title_split[-1] or 'большой' in title_split[-1]:
            continue
        elif len(title_split) >= 2 and ',' in title_split[-2]:
            continue
        elif 'Комбо' in title_split[0] or 'Пара' in title_split[0]:
            continue
        title = title.capitalize()

        if title in extra_titles:
            continue

        card.click()
        time.sleep(3)

        sizes = driver.find_elements(By.CLASS_NAME, 'product-offer-tabs__offer')
        close = driver.find_element(By.CLASS_NAME, 'modal-abstraction__close')

        desc = driver.find_elements(By.CLASS_NAME, 'product-settings__text')
        desc = desc[1].text

        if sizes:
            for size in sizes:
                size.click()
                time.sleep(2)

                item = {'title': title,
                        'image': driver.find_element(
                            By.CLASS_NAME, 'product-top__img').find_element(
                            By.CLASS_NAME, 'common-image__img').get_attribute('src'),
                        'description': desc,
                        'price': driver.find_element(By.CLASS_NAME, 'product-bottom').text,
                        'size': size.text}

                item['price'] = item['price'].split('\n')[1].split(' ')[1]
                item['price'] = int(item['price'])

                if item not in items:
                    print('added', end='=    ')
                    items.append(item)

                items_types.append({"item_id": items.index(item) + 1,
                                    "type_id": TYPES_IDS[CATEGORIES[category]][TYPES[tip]]
                                    })

                print(f""
                      f"{item['title']}, type_id: {TYPES_IDS[CATEGORIES[category]][TYPES[tip]]}, id: {items.index(item) + 1}")

        else:
            item = {'title': title,
                    'image': driver.find_element(
                        By.CLASS_NAME, 'product-top__img').find_element(
                        By.CLASS_NAME, 'common-image__img').get_attribute('src'),
                    'description': desc,
                    'price': driver.find_element(By.CLASS_NAME, 'product-bottom').text,
                    'size': size.split('\n')[0]}

            item['price'] = item['price'].split('\n')[1].split(' ')[1]
            item['price'] = int(item['price'])

            if item not in items:
                print('added', end='=    ')
                items.append(item)

            items_types.append({"item_id": items.index(item) + 1,
                                "type_id": TYPES_IDS[CATEGORIES[category]][TYPES[tip]]
                                })

            print(
                f"{item['title']}, type_id: {TYPES_IDS[CATEGORIES[category]][TYPES[tip]]}, id: {items.index(item) + 1}")

        close.click()
        time.sleep(1)


async def get_pages():
    async with httpx.AsyncClient() as session:
        main_response = await session.get(url, cookies=cookies, headers=headers)

    if main_response.status_code == 200:
        main_soup = BeautifulSoup(main_response.text, "html.parser")

        return [el['href'].split('/')[-1] for el in main_soup.find_all('a', 'menu-category-item') if
                el['href'].split('/')[-1] not in EXTRA_PAGES]


async def main():
    await asyncio.gather(*[get_extra_items(page) for page in EXTRA_PAGES])

    categories = await get_pages()

    for category in categories[2:]:
        if category == 'zavtrak':
            continue

        print('###', category.upper())

        driver.get(url + category)
        time.sleep(5)

        types = driver.find_element(By.CLASS_NAME, 'menu-subcategories')
        types = types.find_elements(By.CLASS_NAME, 'font-type-6')
        wait = WebDriverWait(driver, timeout=4)

        if types:
            for tip in types[1:]:
                if 'Комбо' in tip.text.split(' ')[0]:
                    continue
                elif 'Боксы' in tip.text:
                    continue
                print('#####', TYPES[tip.text], TYPES_IDS[CATEGORIES[category]][TYPES[tip.text]])

                ActionChains(driver).scroll_by_amount(0, -3000).perform()
                wait.until(lambda d: tip.is_displayed())

                tip.click()
                time.sleep(5)

                parse(category, tip.text)
        else:
            parse(category)

    async with httpx.AsyncClient() as session:
        await session.post('http://localhost:8000/items/add/many', json={'items': items})

    async with httpx.AsyncClient() as session:
        await session.post('http://localhost:8000/items/add/types',
                           json={"items": items_types})


if __name__ == '__main__':
    asyncio.run(main())
