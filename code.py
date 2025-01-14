import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import os
def fetch_fanfiction(fandom, pairing, tags, kudos):
    # Кодируем параметры для URL
    fandom_encoded = quote(fandom)
    pairing_encoded = quote(pairing)
    tags_encoded = quote(','.join(tags))
    kudos_encoded = quote(str(kudos))

    # Формируем URL для поиска
    url = (
        f"https://archiveofourown.org/works/search?"
        f"commit=Search&work_search%5Bquery%5D=&work_search%5Btitle%5D=&"
        f"work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&"
        f"work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&"
        f"work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=&"
        f"work_search%5Blanguage_id%5D=&work_search%5Bfandom_names%5D={fandom_encoded}&"
        f"work_search%5Brating_ids%5D=&work_search%5Bcharacter_names%5D=&"
        f"work_search%5Brelationship_names%5D={pairing_encoded}&"
        f"work_search%5Bfreeform_names%5D={tags_encoded}&"
        f"work_search%5Bhits%5D=&work_search%5Bkudos_count%5D={kudos_encoded}&"
        f"work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&"
        f"work_search%5Bsort_column%5D=_score&work_search%5Bsort_direction%5D=desc"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("Ошибка при получении данных")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    works = []

    for work in soup.find_all('li', class_='work'):
        # Извлечение id фанфика
        work_id = work.get('id', '').replace('work_', '')
        title_tag = work.find('h4', class_='heading')
        title_text = title_tag.get_text(strip=True) if title_tag else "Без названия"

        # Извлечение имени автора
        author_match = re.search(r'by(.+?)(?: \(|$)', title_text)
        author = author_match.group(1).strip() if author_match else "Неизвестный автор"
        title_cleaned = title_text.split('by')[0].strip()

        # Формируем полную ссылку на фанфик
        full_link = f"https://archiveofourown.org/works/{work_id}?view_full_work=true" if work_id else "Нет ссылки"

        # Переход к странице фанфика для получения описания
        fanfic_response = requests.get(full_link)
        fanfic_soup = BeautifulSoup(fanfic_response.text, 'html.parser')

        # Извлечение описания из <blockquote class="userstuff">
        description_block = fanfic_soup.find('blockquote', class_='userstuff')
        description = description_block.get_text(strip=True) if description_block else "Описание отсутствует"

        works.append({
            'title': title_cleaned,
            'author': author,
            'link': full_link,
            'description': description,  # Добавляем описание в словарь
            'work_id': work_id  # Добавляем work_id в словарь
        })

    return works
def save_to_txt(works, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for work in works:
            f.write(f"Title: {work['title']}\n")
            f.write(f"Author: {work['author']}\n")
            f.write(f"Link: {work['link']}\n")
            f.write(f"Description: {work['description']}\n")  # Сохраняем описание
            f.write("\n")

def download_fanfic(work_id):
    # Формируем полный URL для получения страницы фанфика
    full_download_link = f"https://archiveofourown.org/works/{work_id}?view_full_work=true"
    response = requests.get(full_download_link)

    if response.status_code == 200:
        fanfic_soup = BeautifulSoup(response.text, 'html.parser')

        # Извлечение содержимого из <div class="userstuff module" role="article">
        userstuff_div = fanfic_soup.find('div', class_='userstuff module', role='article')

        if userstuff_div:
            # Получаем текстовое содержимое
            fanfic_content = userstuff_div.get_text(separator='\n', strip=True)

            # Сохраняем содержимое в файл fanfic.txt
            with open('fanfic.txt', 'w', encoding='utf-8') as f:
                f.write(fanfic_content)
            print(f"Фанфик успешно сохранен в 'fanfic.txt'.")
        else:
            print("Содержимое фанфика не найдено.")
    else:
        print(f"Не удалось получить страницу фанфика. Статус: {response.status_code}.")

if __name__ == "__main__":
    fandom = input("Введите фандом: ")
    pairing = input("Введите пейринг (формат Имя/Имя): ")
    tags_input = input("Введите теги через запятую (например, Angst, Fluff): ")
    tags = [tag.strip() for tag in tags_input.split(',')]  # Преобразуем строку в список
    kudos = input("Введите максимальное количество оценок (kudos): ")

    # Получаем список фанфиков
    fanfics = fetch_fanfiction(fandom, pairing, tags, kudos)

    if fanfics:
        # Сохраняем информацию о фанфиках в текстовый файл
        save_to_txt(fanfics, 'fanfics.txt')
        print("Фанфики сохранены в fanfics.txt")

    else:
        print("Фанфики не найдены.")