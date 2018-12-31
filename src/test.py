import DatabasePort
import pymysql
import time
from Database import Database

database = Database()

_host = database.gethost()
_port = database.getport()
_sql_user = database.getuser()
_sql_password = database.getpassword()
_database = database.getdatabase()


def signup(name, password, avator):  # 注册账号，成功返回账号id，不成功返回-1
    connection = pymysql.connect(
        db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            # TODO add sql line in here
            sql1 = "INSERT INTO `Auth` (`login_name`,`password`)  VALUES (%s, %s)"
            cursor.execute(sql1, (name, password))
            connection.commit()
            sql2 = "INSERT INTO `User` (`user_name`, `avator`) VALUES (%s, %s)"
            cursor.execute(sql2, (name, avator))
            connection.commit()

    except Exception as e:
        print("Wrong", e)
        return -1
    finally:
        connection.close()


message = signup("hello", "xxxx", "temp")
