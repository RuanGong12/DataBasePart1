from zxnDatabase import DatabasePort
import pymysql
import time

db = DatabasePort()


# message = db.signup("Hellwfdd", "sddawdwa", "temp")
# print(message)
# message = db.add_comment(100013, 1, "Helswd")
# message = db.courselike(100013, 1)
message = db.ask_course(100013, 1)
print(message)
