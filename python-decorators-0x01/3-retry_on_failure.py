#!/usr/bin/env python3
import time
import sqlite3
import functools

# Reutilizar o decorador do task anterior
def with_db_connection(func):
    """Decorator to automatically handle database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    print(f"[RETRY] Attempt {attempt + 1}/{retries}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[ERROR] {e}. Retrying in {delay}s...")
                    attempt += 1
                    time.sleep(delay)
            # If all retries fail, raise the last error
            raise Exception(f"Operation failed after {retries} retries.")
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
