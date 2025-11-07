#!/usr/bin/env python3
import time
import sqlite3
import functools

# Cache global (poderia ser um dicionário de instância também)
query_cache = {}

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


def cache_query(func):
    """Decorator that caches the result of SQL queries."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extrai a query de kwargs ou args
        query = kwargs.get('query')
        if query is None and len(args) > 1:
            query = args[1]  # assume conn é o primeiro argumento

        # Verifica se já existe no cache
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing and caching query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # Primeira chamada — executa e guarda no cache
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Segunda chamada — usa o cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
