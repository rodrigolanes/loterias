import json
import sqlite3

database_name = '/home/rodrigo/projetos/loterias/bot.db'


def add_concurso(concurso):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT count(concurso_id) FROM concursos WHERE concurso_id=?", [concurso["concurso"]])
        if c.fetchone()[0] == 1:
            c.execute("delete from concursos where concurso_id=?", [
                concurso['concurso']])
        c.execute("insert into concursos values (?, ?)", [
            concurso['concurso'], json.dumps(concurso)])

        conn.commit()


def add_usuario(user_id):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT count(user_id) FROM users WHERE user_id=?", [user_id])
        if c.fetchone()[0] == 0:
            c.execute("insert into users values (?)", [user_id])
            conn.commit()


def remove_usuario(user_id):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(
            "delete FROM users WHERE user_id=?", [user_id])
        conn.commit()


def get_all_usuarios():
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT user_id FROM users;")

        rows = c.fetchall()

        users = []

        for row in rows:
            users.append(row[0])

        return users


def get_last_concurso():
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()

        c.execute(
            "SELECT max(concurso_id) FROM concursos;")

        numero_ultimo_concurso = c.fetchone()[0]

        c.execute(
            "SELECT data FROM concursos where concurso_id=?", [numero_ultimo_concurso])

        return json.loads(c.fetchone()[0])
