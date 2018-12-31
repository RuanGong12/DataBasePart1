# avator是前端传来一个字符串，不用管是什么存数据库里就好
import pymysql
import time
from Database import Database

database = Database()

_host = database.gethost()
_port = database.getport()
_sql_user = database.getuser()
_sql_password = database.getpassword()
_database = database.getdatabase()


class DatabasePort(object):
    def signup(self, name, password, avator):  # 注册账号，成功返回账号id，不成功返回-1
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                sql1 = "INSERT INTO `Auth` (`login_name`,`password`)  VALUES (%s, %s)"
                cursor.execute(sql1, (name, password))
                sql2 = "INSERT INTO `User` (`user_name`, `avator`) VALUES (%s, %s)"
                cursor.execute(sql2, (name, avator))

            # !connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as e:
            print("Wrong", e)
            return -1
        finally:
            connection.close()

    def login(self, userId, password):  # 登录，成功返回1，账号或密码错误返回0
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT Auth.`user_id` FROM `Auth` WHERE `Auth.user_id` = %d AND Auth.`password` = %s"
                cursor.execute(sql, (userId, password))
                result = cursor.fetchone()
                if result != None:
                    return 1
                # TODO return user_id

        except Exception as e:
            print("Wrong", e)
            return 0
        finally:
            connection.close()

    # userId的用户评论id的课程，内容为comment  成功返回0失败返回1
    def add_comment(self, userId, act_id, comment):
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                localtime = time.asctime(time.localtime(time.time()))
                sql = "INSERT INTO `Comments` (`message`, `auth_id`,`act_id`,`date`) VALUES (%s, %d, %d,%s)"
                cursor.execute(sql, (comment, userId, act_id, localtime))

            # !connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            return 0
        except Exception as e:
            print("Wrong", e)
            return 1
        finally:
            connection.close()

    def add_rate(self, userId, id, rate):  # ! userId的用户评分id的课程，分数为rate(0-5)  成功返回0失败返回1
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                sql = "UPDATE  SET field1=new-value1, field2=new-value2"
                cursor.execute(sql, (id))
                # cursor.execute(sql, (message, userID, act_id))

            # !connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            return 0
        except Exception as e:
            print("Wrong", e)
            return 1
        finally:
            connection.close()

    def courselike(self, userId, id):  # ! 收藏功能  改变状态，即没收藏变为收藏，收藏变为取消收藏
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                sql = "SELECT Collection.id FROM Collection WHERE Collection.user_id = %d AND Collection.activity_id = %d"
                cursor.execute(sql, (userId, id))
                # cursor.execute(sql, (message, userID, act_id))
                resualts = cursor.fetchall()
                if resualts != None:
                    for row in resualts:
                        Collection_id = row[0]
                    sql = "DELETE FROM Collection WHERE id = %d;"
                    cursor.execute(sql, (Collection_id))
                else:
                    sql = "INSERT INTO `Collection` (`user_id`, `activity_id`) VALUES (%d, %d)"
                    cursor.execute(sql, (userId, id))
            # !connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            return 0
        except Exception as e:
            print("Wrong", e)
            return 1
        finally:
            connection.close()

    def ask_course(self, userId, id):  # userId询问id课程相关信息，返回格式示例为：
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `Activity` WHERE `Activity.id`=%d"
                cursor.execute(sql, (id))
                # TODO their must a bug because time problem
                results = cursor.fetchall()
                for row in results:
                    name = row[1]
                    time = row[2]
                    level = row[3]
                    location = row[4]
                    introduction = row[5]
                    teacher = row[6]
                    school = row[7]
                    cover = row[8]
                    tags = row[9]

                sql = "SELECT time.start_time, time.end_time, time.`repeat` FROM time WHERE time.id = %d "
                cursor.execute(sql, (time))
                results = cursor.fetchall()
                for row in results:
                    start_time = row[0]
                    end_time = row[1]
                timeLocation = [start_time, end_time]
                return {"id": id, "title": name, "school": school, "location": location, "teacher": teacher, "cover": cover, "timeLocation": timeLocation, "tags": tags, "rate": level, "isLike": 1, "hasRated": 0, "description": [introduction]}

        except Exception as e:
            print("Wrong", e)
        finally:
            connection.close()
            # 这里我想加入location
            # return {
            #     "id" : "0232",
            #     "title": "神奇的材料世界",
            #     "school": "材料学院",
            #     "teachers": ["文进", "赵春霞", "丁瑶"],
            #     "cover": "http://edu-image.nosdn.127.net/8282FBC079673EA3A28339617E2F69E5.jpg?imageView&thumbnail=510y288&quality=100&thumbnail=223x125&quality=100",
            #     "timeLocation": ["1-13周", "周三 第一大节 2A 102", "周五 第三大节 2A 202"],
            #     "tags": ["材料", "物理"],
            #     "rate": 4,
            #     "isLike": 1,
            #     "hasRated": 0,
            #     "description": ["形形色色的材料构成了丰富多彩的物质世界，为我们创造了美好的生活,推进了人类文明的发展，影响和改变了我们的生活。玻璃、陶瓷、金属和塑料…….这些神奇物质是如何改变我们的世界？新材料的出现会给我们带来哪些惊喜？想知道背后精彩的科学故事和相关科学原理吗？让我们一起走进神奇的材料世界。"]
            # }

    def ask_comment(self, id):  # 查询id课程的评论  返回格式示例为：
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `*` FROM `Comments` WHERE `Comments.act_id` = %d"
                cursor.execute(sql, (id))
                results = cursor.fetchall()
                for row in results:
                    message = row[1]
                    auth_id = row[2]
                    date = row[4]
                # TODO return user_id
                sql = "SELECT `User`.user_name FROM `User` WHERE `User`.id = %d"
                cursor.execute(sql, (id))
                results = cursor.fetchall()
                for row in results:
                    user_name = row[0]
                return {"id": auth_id, "userName": user_name, "date": date, "content": message}
        except Exception as e:
            print("Wrong", e)
        finally:
            connection.close()
        # return [{
        #     "id": "23469872",  # (评论人id)
        #     "userName": "double7",
        #     "date" : "2018-12-30 15:23",
        #     "content": "软件工程这门课对我相当有帮助，老师上课讲的很详细，完全不像很多经验不足的老师，讲课像念紧箍咒一样，一说到紧箍咒，我就想到了西游记。今年下半年，中美合拍的西游记即将正式开机，我继续扮演美猴王孙悟空，我会用美猴王艺术形象努力创造一个正能量的形象，文体两开花，弘扬中华文化，希望大家能多多关注。"
        # },
        # {
        #     "id": "23469873",
        #     "userName": "加拿大电鳗",
        #     "date" : "2018-12-30 15:26",
        #     "content": "几天后，期末考试正式开始，我将继续表演挂科，文理两爆炸，继续以学渣的形象让各位笑话，请大家多多关注。"
        # }
        # ]

    def userinf(self, userId):  # 查询用户相关信息  返回格式为
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `*` FROM `User` WHERE `User`.id = %d"
                cursor.execute(sql, (userId))
                results = cursor.fetchall()
                for row in results:
                    user_id = row[0]
                    user_name = row[1]
                    avator = row[2]
                    like = row[3]
                like = []
                sql = "SELECT Collection.activity_id FROM Collection WHERE Collection.activity_id = %d"
                cursor.execute(sql, (userId))
                results = cursor.fetchall()
                for row in results:
                    like.append(row[0])
                return {"id": user_id, "name": user_name, "avator": avator, "like": like}

        except Exception as e:
            connection.close()
            print("Wrong", e)
        finally:
            connection.close()
            # return {
            #     "id": "334452",
            #     "name": "double7",
            #     "avatar": "/static/img/user_head_img.png",
            #     "like": ["233333", "66666"]  # (收藏的课程id)
            # }
