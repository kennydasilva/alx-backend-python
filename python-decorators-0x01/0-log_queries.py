#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime  


def log_queries(func):
    """Decorator to log SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Verifica se 'query' foi passada como argumento nomeado
        query = kwargs.get('query', None)

        # Caso não tenha sido, tenta obter o primeiro argumento posicional
        if query is None and len(args) > 0:
            query = args[0]

        # Faz o log da query antes da execução, com data e hora
        if query is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Executing query: {query}")

        # Executa a função original
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Exemplo de execução
users = fetch_all_users(query="SELECT * FROM users")
print(users)
