
import json
import requests
from bs4 import BeautifulSoup

URL = 'https://upl.uz'

response = requests.get(URL)
response.raise_for_status()
response_html = response.text

print(response_html)
print(type(response_html))


soup = BeautifulSoup(response_html, 'html.parser')
print(soup)

wrapper = soup.find('div', id='upl-content')
items = wrapper.find_all('div', class_='sh-news')
print(len(items))

result = []

for item in items:
    title = item.find('h2').get_text()
    print(title)
    img = item.find('img').get('data-src')
    img_name = img.split('/')[-1]
    img_content = requests.get(img).content
    with open(img_name, mode='wb') as file:
        file.write(img_content)
    print(img)
    description = item.find('div', class_='sh-text').next.get_text(strip=True)
    print(description)
    side_date = item.find('div', class_='side-date').find_all('span')
    time = side_date[0].get_text()
    if len(side_date) == 2:
        comments = side_date[-1].get_text(strip=True)
    else:
        comments = '0'

    result.append({
        'title': title,
        'img': img,
        'description': description,
        'time': time,
        'comments': comments
    })

with open('data.json', mode='w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

import json
import requests
from bs4 import BeautifulSoup

URL = 'https://upl.uz'

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

categories_wrapper = soup.find('div', class_='nav_row')
categories_list = categories_wrapper.find('ul')

categories = []

for category_item in categories_list.find_all('li'):
    a = category_item.find('a')
    if a is None:
        continue

    categories.append({
        'name': a.get_text(strip=True),
        'link': a.get('href')
    })

with open('categories.json', mode='w', encoding='utf-8') as file:
    json.dump(categories, file, ensure_ascii=False, indent=4)

print(categories)