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

#insert from CSV
def insert_data(coconnection, csv_file):

    try:
        cursor = connection.cursor()

        with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:

                    #check if user already exit
                    cursor.execute("SELECT * FROM user_data where user_id=%s", (row['user_id'],))
                    result =cursor.fetchone()

                    if not result:
                        if not result:
                            cursor.execute("""
                                INSERT INTO user_data(user_id, name,emil,age)
                                VALUES(%s,%s,%s,%s)""",
                                (row['user_id'], row['name'], row['email'], row['age']))
                
        connection.commit()
        print("data inserted sucessfully")
        cursor.close()
    
    except FileNotFoundError:
        print(f"csv file '{csv_file}' not found.")

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

    
