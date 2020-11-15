import config
import sqlite3

con = sqlite3.connect(config.db, check_same_thread=False)


def get_data(): return con.execute("SELECT * FROM USER").fetchall()


def get_count(): return con.execute("SELECT COUNT(*) FROM USER").fetchone()[0]


def delete_data(username):
    con.execute("DELETE FROM USER WHERE name = ?", (username,))
    con.commit()


def set_data(username):
    data = get_data()
    con.executemany('INSERT INTO USER (id, name) values(?, ?)',
                    [(data[get_count()-1][0]+1, username)])
    con.commit()
