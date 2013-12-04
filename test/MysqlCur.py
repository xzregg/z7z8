
import MySQLdb

def get_mysql_result(cursor,size=1000):
    while True:
        result = cursor.fetchmany(size)
        if not result:
            break
        for line in result:
            yield line
            