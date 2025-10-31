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
    

#create database ALX_prodev if not exists

def create_database(connection):

    try:
        curor=connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error creting database: {err}")


