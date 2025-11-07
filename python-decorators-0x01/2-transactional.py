#!/usr/bin/env python3
import sqlite3
import functools

def with_db_connection(func):
    """Decorator to automatically handle opening and closing the database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def transactional(func):
    """Decorator that manages transactions: commit if successful, rollback if an error occurs."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[TRANSACTION] Commit successful.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[TRANSACTION] Rolled back due to error: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"[UPDATE] Updated user {user_id} email to {new_email}")


if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
