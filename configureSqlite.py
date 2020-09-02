import sqlite3

conn = sqlite3.connect('bot.db')

c = conn.cursor()

c.execute(
    ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
if c.fetchone()[0] == 0:
    c.execute("CREATE TABLE users (user_id varchar(10))")

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='concursos' ''')
if c.fetchone()[0] == 0:
    c.execute("CREATE TABLE concursos (concurso_id integer, data json)")

conn.close()
