import requests
from bs4 import BeautifulSoup

# Ваши данные
file_id = "0198e8d8-721d-71ae-a2c7-e798025a07fc"
url = f'https://www.zamzar.com/files/{file_id}/?from=mp4&to=srt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Создаем сессию
session = requests.Session()
print("Загружаем страницу Zamzar...")
page_response = session.get(url, headers=headers)

if page_response.status_code != 200:
    print(f"Ошибка! Не удалось загрузить страницу. Код: {page_response.status_code}")
    exit()

print("Страница успешно загружена. Ищем способ скачать файл...")

# СПОСОБ 1: Пробуем прямой URL (самый частый вариант)
print("\n[Попытка 1] Пробуем прямой линк для скачивания...")
# Формируем URL, по которому скорее всего лежит файл
direct_url = f"https://www.zamzar.com/files/{file_id}/H1_S1E4_IG.srt"
file_response = session.get(direct_url, headers=headers)

if file_response.status_code == 200 and 'application/octet-stream' in file_response.headers.get('Content-Type', ''):
    filename = "H1_S1E4_IG.srt"
    with open(filename, "wb") as f:
        f.write(file_response.content)
    print(f"✅ УСПЕХ! Файл сохранен как '{filename}'")
    exit()
else:
    print("❌ Прямая ссылка не сработала.")

# СПОСОБ 2: Ищем скрытую ссылку в HTML-коде страницы
print("\n[Попытка 2] Ищем ссылку в коде страницы...")
soup = BeautifulSoup(page_response.text, 'html.parser')

# Ищем все возможные элементы, которые могут содержать ссылку на скачивание
potential_links = []
# Ищем по тексту ссылки
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if '.srt' in href or 'download' in href.lower():
        potential_links.append(href)
# Ищем по кнопкам (они могут быть в data-атрибутах)
for btn in soup.find_all('button'):
    if btn.get('data-url'):
        potential_links.append(btn['data-url'])

# Пробуем все найденные подходящие ссылки
download_link = None
for link in potential_links:
    if file_id in link:  # Самая вероятная ссылка будет содержать ID вашего файла
        download_link = link
        break

if not download_link and potential_links:
    download_link = potential_links[0]

if download_link:
    # Если ссылка относительная (начинается с /), добавляем домен
    if download_link.startswith('/'):
        download_link = 'https://www.zamzar.com' + download_link
    elif not download_link.startswith('http'):
        download_link = 'https://www.zamzar.com/' + download_link

    print(f"Найдена ссылка: {download_link}")
    print("Пытаемся скачать...")

    file_response = session.get(download_link, headers=headers)
    if file_response.status_code == 200:
        filename = "H1_S1E4_IG.srt"
        with open(filename, "wb") as f:
            f.write(file_response.content)
        print(f"✅ УСПЕХ! Файл сохранен как '{filename}'")
    else:
        print(f"❌ Скачивание по найденной ссылке не удалось. Код ошибки: {file_response.status_code}")
else:
    print("❌ В коде страницы не найдено явных ссылок для скачивания.")
    print("Вот что удалось найти:")
    for link in potential_links:
        print(f" - {link}")

    # Выведем код страницы для ручного анализа, если нужно
    # with open("zamzar_page.html", "w", encoding="utf-8") as f:
    #    f.write(page_response.text)
    # print("Код страницы сохранен в файл 'zamzar_page.html' для анализа.")