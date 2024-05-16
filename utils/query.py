from django.db import connection
from collections import namedtuple

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def query(query_str: str):
    hasil = []
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO 'MARMUT'")

        try:
            cursor.execute(query_str)

            if query_str.strip().lower().startswith("select"):
                hasil = map_cursor(cursor)
            else:
                hasil = cursor.rowcount
        except Exception as e:
            hasil = e

    return hasil
