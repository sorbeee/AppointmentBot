import psycopg2
from db_names import db_business
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


async def AddBusiness(state):
    try:
        async with state.proxy() as data:
            with connection.cursor() as cursor:
                insert_query = \
                    'INSERT INTO ' + db_business.TABLE_NAME + ' (' \
                    + db_business.OWNER_ID + ', ' \
                    + db_business.NAME + ', ' \
                    + db_business.PHOTO_ID + ', ' \
                    + db_business.DESCRIPTION + ', ' \
                    + db_business.TIME_OF_WORK + \
                    ') VALUES (%s, %s, %s, %s, %s );'

                cursor.execute(insert_query, data)
                connection.commit()
                print("[INFO] Data was added")
                return True
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def GetAllBusinesses():
    with connection.cursor() as cursor:
        select_query = 'SELECT * FROM ' + db_business.TABLE_NAME + ';'

        cursor.execute(select_query)

        return cursor.fetchall()


async def GetBusinessById(Id):
    with connection.cursor() as cursor:
        select_query = 'SELECT * FROM ' + db_business.TABLE_NAME + ' WHERE ' + db_business.OWNER_ID + ' = ' + str(
            Id) + ';'

        cursor.execute(select_query)

        return cursor.fetchall()


async def GetBusinessByBusinessId(Id):
    with connection.cursor() as cursor:
        select_query = 'SELECT * FROM ' + db_business.TABLE_NAME + ' WHERE ' + db_business.ID + ' = ' + str(
            Id) + ';'

        cursor.execute(select_query)

        return cursor.fetchall()


async def DeleteBusiness(business_id):
    try:
        with connection.cursor() as cursor:
            delete_query = \
            'DELETE FROM ' + db_business.TABLE_NAME + ' WHERE ' + db_business.ID + ' = ' + str(business_id) + ';'

            cursor.execute(delete_query)
            connection.commit()
            return True

    except Exception as _ex:
        print("[INFO] error database", _ex)