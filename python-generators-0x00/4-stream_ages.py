#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    try:
        """Generator that yields user ages one by one from the database"""
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for(age,) in cursor:
            yield age
        cursor.close()
        connection.close()
    
    except Exception as e:
        print(f"Error: {e}")
        return None

