import psycopg2
from db_names import db_estimate
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



async def AddEstimation(Estimate, BusinessId, VisitorId):
    try:
        cursor = connection.cursor()
        insert_query = \
                'INSERT INTO ' + db_estimate.TABLE_NAME + ' (' + \
                db_estimate.ESTIMATE + ', ' + \
                db_estimate.BUSINESS_ID + ', ' + \
                db_estimate.VISITOR_ID + \
                ') VALUES ( ' + \
                str(Estimate) + ', ' + str(BusinessId) + ', ' + str(VisitorId) + ');'

        cursor.execute(insert_query)
        connection.commit()
        return True
    except Exception as _ex:
        print("[INFO] error database", _ex)


async def UpdateEstimation(Estimate, BusinessId, VisitorId):
    try:
        cursor = connection.cursor()
        select_query = \
            'UPDATE  ' + db_estimate.TABLE_NAME + \
            ' SET ' + db_estimate.ESTIMATE + ' = ' + str(Estimate) + \
            ' WHERE ' + \
            db_estimate.VISITOR_ID + ' = ' + str(VisitorId) + ' AND ' + \
            db_estimate.BUSINESS_ID + ' = ' + str(BusinessId) + ';'

        cursor.execute(select_query)
        connection.commit()
        return True

    except Exception as _ex:
        print("[INFO] error database", _ex)


async def IsEstimated(BusinessId, VisitorId):
    try:
        cursor = connection.cursor()
        select_query = \
            'SELECT * FROM ' + db_estimate.TABLE_NAME + ' WHERE ' + \
            db_estimate.VISITOR_ID + ' = ' + str(VisitorId) + ' AND ' + \
            db_estimate.BUSINESS_ID + ' = ' + str(BusinessId) + ';'

        cursor.execute(select_query)
        return len(cursor.fetchall()) == 0

    except Exception as _ex:
        print("[INFO] error database", _ex)


async def GetEstimation(BusinessId):
    try:
        cursor = connection.cursor()
        select_query = \
            'SELECT round(AVG(' + db_estimate.ESTIMATE + '),2) ' + \
            'FROM ' + db_estimate.TABLE_NAME + \
            ' WHERE ' + db_estimate.BUSINESS_ID + ' = ' + str(BusinessId) + ';'
        cursor.execute(select_query)
        return cursor.fetchall()

    except Exception as _ex:
        print("[INFO] error database", _ex)
