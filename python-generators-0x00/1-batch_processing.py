#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):

    # connect database
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )

        cursor =connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        batch=[]

        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch=[]

        if batch:
            yield batch
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    

def batch_processing(batch_size):

    for batch in stream_users_in_batches(batch_size):

        filtered_users=[user for user in batch if user['age']>25]

        for user in filtered_users:
            print(user)