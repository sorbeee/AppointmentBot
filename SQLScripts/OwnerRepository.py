import psycopg2
from SQLScripts import db_owner
from config import host, user, password, db_name


async def StartDB(_):
    try:
        global connection
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        print('[INFO] Connected to db')
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def IsOwner(Id):
    with connection.cursor() as cursor:
        select_query = 'SELECT * FROM ' + db_owner.TABLE_NAME + ' WHERE ' + db_owner.ID + ' = ' + str(Id) + ';'

        cursor.execute(select_query)
        data = cursor.fetchall()

        return len(data) > 0
