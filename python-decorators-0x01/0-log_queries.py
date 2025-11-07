#!/usr/bin/env python3
import sqlite3
import functools


#Decorator to log sql queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, 88kwargs):

        #check if 'query' was passed either possitionalty or as a keyword argument