import psycopg2
from db_names import db_records
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


async def IsBusy(WorkerId, Date):
    try:
        with connection.cursor() as cursor:
            select_query = 'SELECT * FROM ' + db_records.TABLE_NAME + \
                           ' WHERE ' + db_records.WORKER_ID + ' = ' + str(WorkerId) + \
                           ' AND ' + db_records.TIME + ' = ' + f'\'{str(Date)}\'' + ';'

            cursor.execute(select_query)
            data = cursor.fetchall()

            return len(data) <= 0
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def AddAppointment(WorkerId, BusinessId, VisitorId, Time):
    try:
        with connection.cursor() as cursor:
            insert_query = \
                'INSERT INTO ' + db_records.TABLE_NAME + ' (' + \
                db_records.BUSINESS_ID + ', ' + \
                db_records.VISITOR_ID + ', ' + \
                db_records.WORKER_ID + ', ' + \
                db_records.TIME + \
                ') VALUES ( ' + \
                str(BusinessId) + ', ' + \
                str(VisitorId) + ', ' + \
                str(WorkerId) + ', ' + \
                f'\'{Time}\'' + ');'

            cursor.execute(insert_query)
            connection.commit()
            return True

    except Exception as _ex:
        print("[INFO] error database", _ex)
