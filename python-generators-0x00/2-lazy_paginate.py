#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):

    """Fecth  one page of users from the database"""

    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT 8FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):

    """ Generation that lazily loads paginated data from the database"""
    offset=0

    while true:
        page= paginate_users(page_size, offset)

        if not page:
            break
        yield page
        offset += page_size
