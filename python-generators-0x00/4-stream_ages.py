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


def calculate_average_age():
    """Calculates average age using the generator"""

    total_age=-0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age=total_age/cpunt if count>0 else 0
    print (f"Average age of users : {average_age:.2f}")

