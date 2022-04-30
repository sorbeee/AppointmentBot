from datetime import timedelta
from SQLScripts import db_worker, db_records, db_client
import psycopg2
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


async def AddWorker(state):
    try:
        async with state.proxy() as data:
            with connection.cursor() as cursor:
                insert_query = \
                    'INSERT INTO ' + db_worker.TABLE_NAME + ' (' \
                    + db_worker.ID + ', ' \
                    + db_worker.BUSINESS_ID + ', ' \
                    + db_worker.NAME + ', ' \
                    + db_worker.LASTNAME + ', ' \
                    + db_worker.PHOTO_ID + ', ' \
                    + db_worker.PHONE_NUMBER + ', ' \
                    + db_worker.TIME_OF_WORK + ', ' \
                    + db_worker.DESCRIPTION + \
                    ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s );'

                cursor.execute(insert_query, data)
                connection.commit()
                return True
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def GetWorkers(business_id):
    try:
        with connection.cursor() as cursor:
            select_query = \
                'SELECT * FROM ' + db_worker.TABLE_NAME + ' WHERE ' + db_worker.BUSINESS_ID + ' = ' + str(
                    business_id) + ';'

            cursor.execute(select_query)

            return cursor.fetchall()

    except Exception as _ex:
        print("[INFO] error database", _ex)


async def GetWorkerById(worker_id):
    try:
        with connection.cursor() as cursor:
            select_query = \
                'SELECT * FROM ' + db_worker.TABLE_NAME + ' WHERE ' + db_worker.ID + ' = ' + str(worker_id) + ';'

            cursor.execute(select_query)

            return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def DeleteWorker(worker_id):
    try:
        with connection.cursor() as cursor:
            delete_query = \
                'DELETE FROM ' + db_worker.TABLE_NAME + ' WHERE ' + db_worker.ID + ' = ' + str(worker_id) + ';'

            cursor.execute(delete_query)
            connection.commit()
            return True

    except Exception as _ex:
        print("[INFO] error database", _ex)



async def GetThisDatSchedule(Date, WorkerId):
    try:
        with connection.cursor() as cursor:
            select_query = \
                'SELECT * FROM ' + db_records.TABLE_NAME  + \
                ' JOIN ' + db_client.TABLE_NAME + ' ON ' + db_records.VISITOR_ID + ' = visitor.id' + \
                ' WHERE ' + db_records.WORKER_ID + ' = ' + str(WorkerId) + \
                 ' AND ' + db_records.TIME + ' BETWEEN ' + f'\'{Date}\'' + ' AND ' + f'\'{Date + timedelta(days=1)}\'' + \
                ' ORDER BY ' + db_records.TIME + ';'
                #' JOIN ' + db_worker.TABLE_NAME  + ' ON ' + db_records.WORKER_ID + ' = ' + 'employees.id' + \

            cursor.execute(select_query)

            return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] error database", _ex)

# SELECT * FROM Records JOIN employees ON employee_id = employees.id JOIN Visitor ON visitor_id = visitor.id WHERE start_time BETWEEN '2020-04-29 00:00:00' AND '2020-05-06 00:00:00';