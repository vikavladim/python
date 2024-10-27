import colorsys
import re
import sqlite3
import random

import requests

from creator import db_name
import time
from bs4 import BeautifulSoup


class Seacher:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def getWordsIds(self, queryWordsList):
        """
        Получение идентификаторов для каждого слова в queryString
        :param queryString: поисковый запрос пользователя
        :return: список wordlist.rowid искомых слов
        """

        rowidList = []

        for word in queryWordsList:
            query = "SELECT id FROM word_list WHERE word =? LIMIT 1"
            result_row = self.conn.execute(query, (word,)).fetchone()
            if result_row != None:
                word_row_id = result_row[0]
                rowidList.append(word_row_id)
            else:
                raise Exception(
                    "Одно из слов поискового запроса не найдено:" + word)
        return rowidList

    def getMatchRows(self, queryString):
        """
        Поиск комбинаций из всезх искомых слов в проиндексированных url-адресах
        :param queryString: поисковый запрос пользователя
        :return: 1) список вхождений формата (urlId, loc_q1, loc_q2, ...) loc_qN позиция на странице Nго слова из поискового запроса  "q1 q2 ..."
        """

        queryString = queryString.lower()
        wordsList = queryString.split(' ')

        wordsidList = self.getWordsIds(wordsList)

        columns = []
        joins = []
        conditions = []

        # Созать переменную для полного SQL-запроса
        sql_template = """
            SELECT {columns}
            FROM word_location t0
            {joins}
            WHERE {conditions}
        """

        columns.append('t0.fk_url_id url_id')

        for i in range(len(wordsList)):
            columns.append(f't{i}.location w{i}_loc')
            if i > 0:
                joins.append(f'cross join word_location t{
                             i} on t0.fk_url_id=t{i}.fk_url_id ')
            conditions.append(f't{i}.fk_word_id=?')

        sql_query = sql_template.format(
            columns=', '.join(columns),
            joins='\n'.join(joins),
            conditions=' and '.join(conditions)
        )

        self.conn.execute('drop table if exists match_rows')
        self.conn.execute(f'CREATE TABLE IF NOT EXISTS match_rows as {
                          sql_query}', (*wordsidList,))
        self.conn.commit()

        return wordsidList

    def indexation(self):
        # Для некоторых столбцов в таблицах БД укажем команду создания объекта "INDEX" для ускорения поиска в БД
        self.conn.execute("DROP INDEX   IF EXISTS wordidx;")
        self.conn.execute("DROP INDEX   IF EXISTS urlidx;")
        self.conn.execute("DROP INDEX   IF EXISTS wordurlidx;")
        self.conn.execute("DROP INDEX   IF EXISTS urltoidx;")
        self.conn.execute("DROP INDEX   IF EXISTS urlfromidx;")
        self.conn.execute("DROP INDEX   IF EXISTS rankurlididx;")
        self.conn.execute(
            'CREATE INDEX IF NOT EXISTS wordidx       ON word_list(word)')
        self.conn.execute(
            'CREATE INDEX IF NOT EXISTS urlidx        ON url_list(url)')
        self.conn.execute(
            'CREATE INDEX IF NOT EXISTS wordurlidx    ON word_location(fk_word_id)')
        self.conn.execute(
            'CREATE INDEX IF NOT EXISTS urltoidx      ON link_between_url(fk_to_url_id)')
        self.conn.execute(
            'CREATE INDEX IF NOT EXISTS urlfromidx    ON link_between_url(fk_from_url_id)')
        self.conn.execute(
            'CREATE INDEX IF NOT EXISTS rankurlididx  ON page_rank(url_id)')
        self.conn.execute("REINDEX wordidx;")
        self.conn.execute("REINDEX urlidx;")
        self.conn.execute("REINDEX wordurlidx;")
        self.conn.execute("REINDEX urltoidx;")
        self.conn.execute("REINDEX urlfromidx;")
        self.conn.execute("REINDEX rankurlididx;")

    def calculatePageRank(self, iterations=5):
        # Подготовка БД ------------------------------------------
        # стираем текущее содержимое таблицы PageRank
        self.conn.execute('DROP TABLE IF EXISTS pagerank')
        self.conn.execute("""CREATE TABLE  IF NOT EXISTS  page_rank(
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            url_id INTEGER,
                                            score REAL
                                        );""")
        self.indexation()
        # в начальный момент ранг для каждого URL равен 1
        self.conn.execute(
            'INSERT INTO page_rank (url_id, score) SELECT id, 1.0 FROM url_list')
        self.conn.commit()

        # Цикл Вычисление PageRank в несколько итераций
        for i in range(iterations):
            print("Итерация %d" % (i))

            for row in self.conn.execute('SELECT id FROM url_list'):
                url_id = row[0]
                pr = 0.15

                pages_from = self.conn.execute(
                    'SELECT distinct fk_from_url_id FROM link_between_url WHERE fk_to_url_id=?', (url_id,))
                for page in pages_from:
                    old_rank = self.conn.execute(
                        'SELECT score FROM page_rank WHERE url_id=?', (page[0],)).fetchone()
                    total_count_pages = self.conn.execute(
                        'SELECT count(*) FROM link_between_url WHERE fk_from_url_id=?',
                        (page[0],)).fetchone()
                    pr += (1 - pr) * (old_rank[0] / total_count_pages[0])

                self.conn.execute(
                    'UPDATE page_rank SET score=? WHERE url_id=?', (pr, url_id,))

            self.conn.commit()

    def geturlname(self, id):
        """
        Получает из БД текстовое поле url-адреса по указанному urlid
        :param id: целочисленный urlid
        :return: строка с соответствующим url
        """
        return self.conn.execute('SELECT url FROM url_list WHERE id=?', (id,)).fetchone()[0]

    def getSortedList(self, queryString):
        """
        На поисковый запрос формирует список URL, вычисляет ранги, выводит в отсортированном порядке
        :param queryString:  поисковый запрос
        :return:
        """

        wordsidList = self.getMatchRows(queryString)

        self.calculatePageRank()
        self.distanceScore(wordsidList)

        self.normalizeScores('page_rank', 0)
        self.normalizeScores('distance_score', 1)

        self.conn.execute("drop table if exists metrics")
        self.conn.execute("""create table if not exists metrics as
                                SELECT distinct url_list.id,
                                 page_rank.normalized_score m1, 
                                 distance_score.normalized_score m2, 
                                 (page_rank.normalized_score+distance_score.normalized_score)/2 m3,
                                 url
                                 FROM distance_score 
                                 join page_rank on distance_score.url_id = page_rank.url_id
                                 join url_list  on url_list.id = distance_score.url_id
                                 ORDER BY m3 DESC """)

    def normalizeScores(self, table_name, smallIsBetter=0):
        columns = [row[1] for row in self.conn.execute(
            f"PRAGMA table_info({table_name})").fetchall()]
        if 'normalized_score' not in columns:
            self.conn.execute(
                f"ALTER TABLE {table_name} ADD COLUMN normalized_score float")
        vsmall = 1e-6
        minscore, maxscore = self.conn.execute(
            f'SELECT min(score),max(score) FROM {table_name}').fetchone()

        if smallIsBetter:  # Режим МЕНЬШЕ вх. значение => ЛУЧШЕ
            self.conn.execute(f'UPDATE {
                              table_name} SET normalized_score = ?*1.0 / max(score, ?)', (minscore, vsmall))
        else:
            self.conn.execute(f'UPDATE {
                              table_name} SET normalized_score = score*1.0/ max(?, ?)', (maxscore, vsmall))
        self.conn.commit()

    def distanceScore(self, wordsidList):
        self.conn.execute('DROP TABLE IF EXISTS distance_score')
        if (len(wordsidList) < 2):
            self.conn.execute(
                'create table distance_score as SELECT id, 1.0 FROM url_list')
            self.conn.commit()
        else:
            columns = []
            expression = []
            sql_template = """
                select url_id, {columns}, min({expression}) score
                from match_rows
                group by url_id
            """
            for i in range(len(wordsidList)):
                columns.append(f'w{i}_loc')
                for j in range(i + 1, len(wordsidList)):
                    expression.append(f'abs(w{i}_loc - w{j}_loc)')

            full_query = sql_template.format(
                columns=','.join(columns),
                expression='+'.join(expression)
            )

            self.conn.execute(
                f'create table if not exists distance_score as {full_query}')
            self.conn.commit()

    def generate_random_color(self):
        h = random.random()
        s = random.uniform(0.5, 1.0)
        v = random.uniform(0.5, 1.0)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    def createMarkedHtmlFile(self, markedHTMLFilename, url_html, query_words):
        soup = BeautifulSoup(requests.get(url_html).text, 'html.parser')
        html_words = soup.getText()
        # Приобразование текста к нижнему регистру
        html_words = html_words.lower()
        colors = []
        for i in range(len(query_words)):
            query_words[i] = query_words[i].lower()
            colors.append(self.generate_random_color())

        for i in range(len(query_words)):
            html_words = html_words.replace(query_words[i], f'<span style="background-color:{
                                            colors[i]}; font-weight: bold;">{query_words[i]}</span>')

        # сохранить html-код в файл с указанным именем
        file = open(markedHTMLFilename, 'w', encoding="utf-8")
        file.write(html_words)
        file.close()


if __name__ == '__main__':
    seacher = Seacher(db_name)

    mySearchQuery = "моделирование обработка"

    start_time = time.time()
    seacher.getSortedList(mySearchQuery)
    end_time = time.time()
    print('time: ', end_time - start_time)

    limit = 3
    for row in seacher.conn.execute('select * from metrics limit ?', (limit,)):
        seacher.createMarkedHtmlFile('_'.join(re.split('/|:| ', row[4]))+'.html', row[4],
                                     mySearchQuery.lower().split(' '))
