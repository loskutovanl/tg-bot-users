import sqlite3
import os
import datetime
from typing import List


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT_DIR, 'database.db')


def insert(nickname: str, user_name: str, chat_name: str, user_number: int, dtime=datetime.datetime.now().isoformat()) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO 'users' (nickname, user_name, chat_name, congr_number, dtime_connetion) VALUES (?, ?, ?, ?,?);
        """, (nickname, user_name, chat_name, user_number, dtime))


def insert2(nickname: str,
            user_name: str,
            chat_id: int,
            user_id: int,
            chat_name: str,
            congr_number: int,
            is_winner: int,
            dtime: datetime = datetime.datetime.now().isoformat()) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO 'users' (nickname, user_name, chat_name,
                            congr_number, chat_id, user_id, 
                            dtime_connetion, is_winner) 
                            VALUES (?, ?, ?, ?,?,?,?,?);
        """, (nickname, user_name, chat_name, congr_number, chat_id, user_id, dtime, is_winner))

"блок функций для вывода всех кто в юбилейном списке"

def select_lucky(moderator_id: int):

    with sqlite3.connect(( DB )) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT chat_name, user_name, nickname, congr_number, dtime_connetion, is_winner, chat_id
                           FROM 'users' JOIN 'groups_relation'
                           ON chat_id = group_id AND moderator_id = abs({moderator_id});""")
    result = cursor.fetchall()
    return result

def select_lucky_id(idd: int):

    with sqlite3.connect(( DB )) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT *
                           FROM 'users'
                           WHERE chat_id = {idd};""")
    result = cursor.fetchall()
    return result


"Блок функций для поздравления последних непоздравленных начало"

def select_last_uncongratulate(moderator_id: int):
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT chat_id, congr_number, nickname, user_name, chat_name, dtime_connetion, id, is_winner
                           FROM 'users' JOIN 'groups_relation'
                           ON chat_id = group_id AND moderator_id = abs({moderator_id}) AND is_winner = 0
                           ORDER BY chat_id, congr_number;""")
    result = cursor.fetchall()
    return result


def select_group_id(moderator_id: int):
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT chat_id, COUNT(*)
                           FROM 'users' JOIN 'groups_relation'
                           ON chat_id = group_id AND moderator_id = abs({moderator_id}) AND is_winner = 0
                           GROUP BY chat_id;""")
    result = cursor.fetchall()
    return result

def temp_save_unceleb(
            chat_id: int,
            record_id: int,
            bot_message_id: int
            ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO 'temp_unceleb' (chat_id, record_id, bot_message_id) VALUES (?, ?, ?);
        """, (chat_id, record_id, bot_message_id))

def temp_cleaner():
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''DELETE FROM 'temp_unceleb';''')

def get_chat_id_unceleb(bot_message_id):
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id FROM 'temp_unceleb' WHERE bot_message_id={bot_message_id}")
        result = cursor.fetchall()
        return result[0][0]

def is_winner_id_select_unceleb(
        bot_message_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f'''SELECT id FROM users Join temp_unceleb ON id=record_id
                        WHERE bot_message_id={bot_message_id};''')
        id = []
        for i in result:
            id.append(i)

        return id[0][0]

def buttons_remover_unceleb(
        chat_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT bot_message_id FROM 'temp_unceleb' WHERE chat_id={chat_id}")
        result = cursor.fetchall()
        delete_list = []
        for i in result:
            delete_list.extend(i)
        return delete_list

def storage_cleaner_unceleb(
        chat_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''DELETE FROM 'temp_unceleb' WHERE chat_id={chat_id};''')

def record_cleaner_unceleb(bot_message_id: int) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''DELETE FROM 'temp_unceleb' WHERE bot_message_id={bot_message_id};''')
"Конец блока функций unceleb"

def winner_check(id):
    with sqlite3.connect(( DB )) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id={id} AND is_winner=1")
        result = cursor.fetchall()
        return result


def insert_to_groups(moderator_id: int, group_id: int) -> None:
    """
    Функция, которая записывает id группы модераторов и групп пользователей в таблицу groups_relation (по связи многие
    ко многим; одной записи соответствует одна пара).
    :param moderator_id: id группы модераторов
    :param group_id: id группы пользователей
    :return: None
    """
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO 'groups_relation' (moderator_id, group_id) 
            VALUES (?, ?);""",
            (moderator_id, group_id)
        )


def select_from_groups() -> List[tuple]:
    """
    Генератор, который из таблицы groups_relation возвращает данные о записях id групп модераторов и пользователей,
    сгруппированные по id групп модераторов.
    :return List[tuple]: id групп модераторов и пользователей
    """
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT moderator_id "
                       "FROM 'groups_relation'")
        moderator_id_list = cursor.fetchall()
        for moderator_id in moderator_id_list:
            cursor.execute(f"SELECT moderator_id, group_id "
                           f"FROM 'groups_relation'"
                           f"WHERE moderator_id={moderator_id[0]}")
            result = cursor.fetchall()
            yield result


def delete_from_groups() -> None:
    """
    Функция, которая полностью очищает таблицу groups_relation.
    :return: None
    """
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'groups_relation'")


def get_moderator_id() -> List[int]:
    """
    Функция, которая возвращает список id групп модераторов из таблицы groups_relation.
    :return List[int]: список id групп модераторов
    """
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT moderator_id FROM 'groups_relation'")
        moderator_id_list = cursor.fetchall()
        result = []
        for moderator_id in moderator_id_list:
            result.append(moderator_id[0])
        return result

def select_id_from_users(user_id) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM 'users' WHERE user_id={user_id}")
        record_id = cursor.fetchall()
        return record_id[-1][0]



def temp_save(
            chat_id: int,
            record_id: int,
            bot_message_id: int
            ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO 'temp_storage' (chat_id, record_id, bot_message_id) VALUES (?, ?, ?);
        """, (chat_id, record_id, bot_message_id))



def buttons_remover(
        chat_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT bot_message_id FROM 'temp_storage' WHERE chat_id={chat_id}")
        result = cursor.fetchall()
        delete_list = []
        for i in result:
            delete_list.extend(i)
        return delete_list

def record_cleaner(bot_message_id: int) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''DELETE FROM 'temp_storage' WHERE bot_message_id={bot_message_id};''')


def get_chat_id(bot_message_id):
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id FROM 'temp_storage' WHERE bot_message_id={bot_message_id}")
        result = cursor.fetchall()
        return result[0][0]


def storage_cleaner(
        chat_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''DELETE FROM 'temp_storage' WHERE chat_id={chat_id};''')


def is_winner_id_select(
        bot_message_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f'''SELECT id FROM users Join temp_storage ON id=record_id
                        WHERE bot_message_id={bot_message_id};''')
        id = []
        for i in result:
            id.append(i)

        return id[0][0]


def is_winner_record(winner_id: int,
        ) -> None:
    with sqlite3.connect((DB)) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''UPDATE users set is_winner = '1' 
                        WHERE id={winner_id}''')

