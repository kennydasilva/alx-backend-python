#!/usr/bin/python3
import mysql.connector
import csv

## kenny Dasilva Mangue
## connect to Msyql server  

def connect_db():

    try:
        connection= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
        )

        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None