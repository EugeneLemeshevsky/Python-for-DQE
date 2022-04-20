import sqlite3
import os

class NewsfeedSQLiteRepository:
    def __init__(self, filename):
        self.create = not os.path.exists(filename)
        self.filename = filename
        self.tables = ['News', 'PrivateAd', 'Product']

    def __enter__(self):
        self.db = sqlite3.connect(self.filename)
        if self.create:
            cursor = self.db.cursor()
            for table in self.tables:
                trans = f"CREATE TABLE {table} ('text'	TEXT, 'additional_info'	TEXT);"
                cursor.execute(trans)
        self.db.commit()
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.db.close()

    def add_record(self, table, text, additional_info):
        if not self.duplicate_check(table, text, additional_info):
            cursor = self.db.cursor()
            req = f"INSERT INTO {table} (text, additional_info) VALUES(?, ?)"
            cursor.execute(req, (text, additional_info))
            self.db.commit()

    def duplicate_check(self, table, text, additional_info):
        cursor = self.db.cursor()
        req = f"SELECT * FROM {table} WHERE text = :text AND additional_info=:additional_info"
        cursor.execute(req, {'text': text, 'additional_info': additional_info})
        result = True if cursor.fetchone() else False
        return result
