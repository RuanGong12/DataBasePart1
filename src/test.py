from DatabasePort import DatabasePort
import pymysql
import time

db = DatabasePort()


# message = db.signup("Hellwfdd", "sddawdwa", "temp")
# print(message)
message = db.add_rate(100012, 1, 4)
print(message)
