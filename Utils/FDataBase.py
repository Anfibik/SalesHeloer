import math
import sqlite3
import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_info_lead(self):
        sql = '''SELECT * FROM lead'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")

        return []

    def set_new_lead(self, company, name, job_title, phone, mail, project, price, profit, status):
        try:
            self.__cur.execute(
                "INSERT INTO lead (company, name, job_title, phone, mail, project, price, profit, status)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (company, name, job_title, phone, mail, project, price, profit, status))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def get_lead(self, alias):
        try:
            self.__cur.execute(f"SELECT * FROM lead WHERE company = '{alias}'")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return False, False

    def del_lead(self, ids_lead):
        ids_lead = tuple(map(int, ids_lead))
        try:
            if len(ids_lead) > 1:
                self.__cur.execute(f"DELETE FROM lead WHERE id in {ids_lead}")
            else:
                ids_lead = ids_lead[0]
                self.__cur.execute(f"DELETE FROM lead WHERE id = {ids_lead}")
            print('внутри удаления')
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

    def add_user(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()

            print(name, email, hpsw)

            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (name, email, hpsw))
            print("Accept")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
