import sqlite3
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from creator import *

social = [
    'youtube',
    'vk',
    'facebook',
    'twitter',
    'x',
    'instagram',
    'ok',
    'mail',
    'gmail',
    'telegram',
]

word_array = []
url_array = []
between_aray = []


class Crawler:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # 1. Индексирование одной страницы
    def addToIndex(self, soup, url_id):
        word_list = self.separateWords(self.getTextOnly(soup))
        for i, word in enumerate(word_list):
            if len(word) <= 3:
                continue
            word = word.lower()
            word_id = self.getEntryId('word_list', word=word)
            query = "INSERT INTO word_location (fk_word_id, fk_url_id, location) VALUES (?, ?, ?)"
            self.cursor.execute(query, (word_id, url_id, i))
        self.conn.commit()

    def getEntryId(self, table, **kwargs):
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        conditions = " AND ".join([f"{key}=? " for key in kwargs.keys()])
        query = f"SELECT * FROM {table} WHERE {conditions}"
        values = tuple(kwargs.values())
        self.cursor.execute(query, values)
        row = self.cursor.fetchone()
        if row is None:
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.lastrowid
        return row[0]

    # 2. Получение текста страницы
    def getTextOnly(self, soup):
        return soup.getText()

    # 3. Разбиение текста на слова
    def separateWords(self, text):
        return re.findall(r'[a-zA-Zа-яА-Я0-9ёЁ]+', text)

    # 4. Проиндексирован ли URL (проверка наличия URL в БД)
    def isIndexed(self, url):
        query = "SELECT * FROM url_list WHERE url=?"
        self.cursor.execute(query, (url,))
        row = self.cursor.fetchone()
        if row is None:
            return False

        query2 = "SELECT * FROM link_between_url WHERE fk_from_url_id=?"
        self.cursor.execute(query2, (row[0],))
        row2 = self.cursor.fetchone()
        if row2 is None:
            return False

        return True

    # 5. Добавление ссылки с одной страницы на другую
    def addLinkRef(self, urlFromId, urlToId, linkText):
        query = "INSERT INTO link_between_url (fk_from_url_id, fk_to_url_id) VALUES (?, ?)"
        self.cursor.execute(query, (urlFromId, urlToId))
        link_id = self.cursor.lastrowid
        for word in self.separateWords(linkText):
            if len(word) <= 3:
                continue
            word = word.lower()
            word_id = self.getEntryId('word_list', word=word)
            query = "INSERT INTO link_word (fk_word_id, fk_link_id) VALUES (?, ?)"
            self.cursor.execute(query, (word_id, link_id))
        self.conn.commit()

    def crawl(self, url_list, max_depth=1):
        newPagesSet = []
        for url in url_list:
            url = url.rstrip('/')
            self.getEntryId('url_list', url=url)
        self.conn.commit()

        for curr_depth in range(0, max_depth):
            for url in url_list:
                url = url.rstrip('/')
                if self.isIndexed(url):
                    continue
                curr_url_id = self.getEntryId('url_list', url=url)
                try:
                    html_doc = requests.get(url).text
                except:
                    print("except", url)
                    continue
                soup = BeautifulSoup(html_doc, "html.parser")
                tags = soup.find_all('a')
                for tag in tags:
                    href = tag.get('href')
                    if href is None:
                        continue
                    href = href.split('#')[0].lower()
                    if not href.startswith('http'):
                        href = urljoin(url, href)
                    if self.isSocial(href):
                        continue
                    href = href.rstrip('/')
                    link_text = tag.text.strip()
                    href_url_id = self.getEntryId('url_list', url=href)
                    newPagesSet.append(href)
                    self.addLinkRef(curr_url_id, href_url_id, link_text)
                self.addToIndex(soup, curr_url_id)

                self.add_info()
            url_list = newPagesSet
            newPagesSet = []

    def initDB(self):
        create_tables(self.conn, self.cursor)

    def isSocial(self, href):
        domain = urlparse(href).hostname
        if domain is None:
            return True
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            return True
        second_domain = domain.split('.')[-2]
        for soc in social:
            if second_domain == soc:
                return True
        return False

    def clear_db(self):
        self.cursor.execute("DELETE FROM link_word")
        self.cursor.execute("DELETE FROM link_between_url")
        self.cursor.execute("DELETE FROM word_location")
        self.cursor.execute("DELETE FROM word_list")
        self.cursor.execute("DELETE FROM url_list")
        self.conn.commit()

    def add_info(self):
        words = self.cursor.execute(
            "SELECT COUNT(*) FROM word_list").fetchone()[0]
        betweens = self.cursor.execute(
            "SELECT COUNT(*) FROM link_between_url").fetchone()[0]
        urls = self.cursor.execute(
            "SELECT COUNT(*) FROM url_list").fetchone()[0]
        word_array.append(words)
        between_aray.append(betweens)
        url_array.append(urls)


if __name__ == '__main__':
    db_filename = 'pzvsii_lr2.db'
    url_list = [
        'https://exponenta.ru/news/pobediteli-konkursa-vkr-sredi-studentov-elektroenergetikov',
        'https://ngs.ru/text/transport/2024/10/06/74177057/'
    ]
    crawler = Crawler(db_filename)
    crawler.initDB()
    crawler.clear_db()
    print('wordList\tlinkBetweenUrl\turlList')
    crawler.crawl(url_list, 2)
    for a, b, c in zip(word_array, between_aray, url_array):
        print(f'{a}\t{b}\t{c}')
