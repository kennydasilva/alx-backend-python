#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for automatic database connection handling"""

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        """Estabelece a conexão e retorna o objecto da base de dados"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Fecha a conexão automaticamente, mesmo que ocorra erro"""
        self.conn.close()


# Exemplo de uso
if __name__ == "__main__":
    with DatabaseConnection('users.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
