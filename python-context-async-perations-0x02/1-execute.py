#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    """Context manager to execute a query automatically"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()

    def __enter__(self):
        """Abre conexão e executa a query"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """Fecha a conexão"""
        self.conn.close()



if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery('users.db', query, (25,)) as results:
        print(results)
