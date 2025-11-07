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