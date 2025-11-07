#!/usr/bin/env python3
import sqlite3
import functools

def with_db_connection(func):
    """Decorator that automatically opens and closes a database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Abre a conexão à base de dados
        conn = sqlite3.connect('users.db')
        try:
            # Passa a conexão para a função decorada
            result = func(conn, *args, **kwargs)
        finally:
            # Fecha a conexão (mesmo que ocorra erro)
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Teste
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
