#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):

    """Fetch one page of users from the database"""

    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):

    """Generator that lazily loads paginated data from the database"""
    offset = 0

    while True:
        page = paginate_users(page_size, offset)

        if not page:
            break
        yield page
        offset += page_size
