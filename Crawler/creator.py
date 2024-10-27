import sqlite3

db_name = 'pzvsii_lr2.db'


def create_tables(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_list (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_list (
            id INTEGER PRIMARY KEY,
            word TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_location (
            id INTEGER PRIMARY KEY,
            fk_word_id INTEGER,
            fk_url_id INTEGER,
            location INTEGER,
            FOREIGN KEY (fk_word_id) REFERENCES word_list (id),
            FOREIGN KEY (fk_url_id) REFERENCES url_list (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS link_between_url (
            id INTEGER PRIMARY KEY,
            fk_from_url_id INTEGER,
            fk_to_url_id INTEGER,
            FOREIGN KEY (fk_from_url_id) REFERENCES url_list (id),
            FOREIGN KEY (fk_to_url_id) REFERENCES url_list (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS link_word (
            id INTEGER PRIMARY KEY,
            fk_word_id INTEGER,
            fk_link_id INTEGER,
            FOREIGN KEY (fk_word_id) REFERENCES word_list (id),
            FOREIGN KEY (fk_link_id) REFERENCES link_between_url (id)
        )
    ''')

    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    create_tables(conn, cursor)
    conn.close()
