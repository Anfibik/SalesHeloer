import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_info_records(self, name_tabl, user_email):
        sql = f"SELECT * FROM {name_tabl} WHERE user_email = '{user_email}'"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")

        return []

    def set_new_lead(self, company, name, phone, mail, project, user_email, job_title='', price='', profit=''):
        try:
            self.__cur.execute(
                "INSERT INTO lead (company, name, phone, mail, project, job_title, price, profit, user_email)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (company, name, phone, mail, project, job_title, price, profit, user_email))
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
            print("Ошибка получения лида из БД " + str(e))

        return False, False

    def del_records(self, db_name, ids_record=None):
        if ids_record is None:
            try:
                self.__cur.execute(f"DELETE FROM {db_name}")
                self.__db.commit()
                return True
            except sqlite3.Error as e:
                print("Ошибка удаления всех записей БД " + str(e))
                return False

        if type(ids_record) in (int, str):
            ids_record = [ids_record]
        ids_record = tuple(map(int, ids_record))
        try:
            if len(ids_record) > 1:
                self.__cur.execute(f"DELETE FROM {db_name} WHERE id in {ids_record}")
            else:
                ids_record = ids_record[0]
                self.__cur.execute(f"DELETE FROM {db_name} WHERE id = {ids_record}")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

    def add_user(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (name, email, hpsw))
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

    # =================================================================================================

    def add_record(self, name_table, dict_records=None, **kwargs):
        """Добавление записи в выбранную таблицу по выбранным столбцам"""
        if dict_records is None:
            title_table = tuple(kwargs.keys())
            values = tuple(kwargs.values())
        else:
            title_table = []
            values = []
            for t, v in dict_records.items():
                title_table.append(t)
                values.append(v)
            title_table = tuple(title_table)
            values = tuple(values)
        try:
            self.__cur.execute(f"INSERT INTO {name_table} {title_table} VALUES {values}")
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"Ошибка добавления в БД:{name_table} записи {kwargs} " + str(e))
            return False
        return True

    def get_last_record(self, name_table):
        try:
            self.__cur.execute(f"SELECT * FROM {name_table} ORDER BY id DESC LIMIT 1;")
            last_record = self.__cur.fetchone()
            return last_record
        except sqlite3.Error as e:
            print("Ошибка получения последней записи из БД " + str(e))
            return False

    def update_record_by_id(self, name_table, id_record, columns_values):
        new_val = ''
        for title, values in columns_values.items():
            new_val = new_val + title
            if type(values) == int:
                new_val = new_val + '=' + str(values) + ', '
            else:
                new_val = new_val + '=' + f"'{values}'" + ', '
        new_val = new_val.rstrip(', ')
        try:
            self.__cur.execute(f"UPDATE {name_table} SET {new_val} WHERE id={id_record}")
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка обновления записи {id_record} в БД {name_table} " + str(e))
            return False

    def save_warehouse(self):
        try:
            self.__cur.execute(f"INSERT INTO my_warehouse "
                               f"SELECT * FROM warehouse WHERE id = {self.get_last_record('warehouse')['id']}")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка копирования склада в БД " + str(e))
            return False
        return True

    def check_records(self, name_table):
        try:
            check = self.__cur.execute(f"SELECT EXISTS(SELECT 1 FROM {name_table} LIMIT 1);")
            check = check.fetchone()[0]
            return check
        except sqlite3.Error as e:
            print("Ошибка проверки записей в таблице " + str(e))
            return False

    def get_record(self, name_table, *args):
        query = ''
        for column, value in args:
            query += f"{column} = '{value}' AND "
        query = query.rstrip(' AND')
        try:
            self.__cur.execute(f"SELECT * FROM {name_table} WHERE {query};")
            res = self.__cur.fetchone()
            if not res:
                print("Запись не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
