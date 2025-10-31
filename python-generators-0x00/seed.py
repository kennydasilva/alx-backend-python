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


#connect directly to alx_prodev database

def connect_to_prodev():

    try:
        connection= mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
#create table user_data
def create_table(connection):

    try:
        cursor=connection.cursor()
        query="""
        CREATE TABLE IF NOT EXISTS user_data(
            user_id char(36) PRIMARY KEY NOT NULL,
            name VARCHAR (100) NOT NULL,
            email VARCHAR (100) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
            );
            """
        cursor.execute(query)
        cursor.commit()
        print("Table user_data created successfully")
        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

