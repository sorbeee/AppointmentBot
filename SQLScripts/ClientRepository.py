import psycopg2
from SQLScripts import db_client
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


async def AddUser(ClientId, ClientName, ClientPhone):
    try:
        with connection.cursor() as cursor:
            insert_query = \
                'INSERT INTO ' + db_client.TABLE_NAME + ' (' +\
                db_client.ID + ', ' +\
                db_client.NAME + ', '+\
                db_client.PHONE_NUMBER + ') VALUES (' +\
                ClientId + ', ' + '\' ' +\
                ClientName + '\', ' +\
                ClientPhone + ');'

            cursor.execute(insert_query)
            connection.commit()

            return True
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def GetClientById(client_id):
    try:
        with connection.cursor() as cursor:
            select_query = \
                'SELECT * FROM ' + db_client.TABLE_NAME + ' WHERE ' + db_client.ID + ' = ' + str(client_id) + ';'

            cursor.execute(select_query)
            data = cursor.fetchall()

            return len(data) > 0
    except Exception as _ex:
        print("[INFO] error database", _ex)