#!/usr/bin/env python3
import sqlite3
import functools


#Decorator to log sql queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        #check if 'query' was passed either possitionalty or as a keyword argument
        query =kwargs.get('query',None)

        if query is None and len(args) > 0:
            query = args[0]

            print(f"Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn=sqlite3.connect('users.db')
    cursor=conn.cursor()
    cursor.execute(query)
    reults=cursor.fetchall()
    conn.close()
    return reults

#Example execution
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT*FROM users")
    print(users)



