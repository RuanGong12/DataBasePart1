# avator是前端传来一个字符串，不用管是什么存数据库里就好
import pymysql
# import synonyms
import time

_host = "129.204.75.9"
_port = 3306
_sql_user = "root"
_sql_password = "mysql123456"
_database = "DataSQL"


class DatabasePort(object):
    def signup(self, name, password, avator):  # * OK 注册账号，成功返回账号id，不成功返回-1
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                sql = "INSERT INTO `User` (`user_name`,`password`,`avator`)  VALUES (%s, %s,%s)"
                cursor.execute(sql, (name, password, avator))
                connection.commit()
                sql = "SELECT User.`id` FROM `User` WHERE User.`user_name` = %s AND User.`password` = %s"
                cursor.execute(sql, (name, password))
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            print("Wrong", e)
            return -1
        finally:
            connection.close()

    def login(self, userId, password):  # *Ok 登录，成功返回1，账号或密码错误返回0
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT User.`id` FROM User WHERE User.`id` = %s AND User.`password` = %s"
                cursor.execute(sql, (userId, password))
                result = cursor.fetchone()
                if result != None:
                    return 1
                else:
                    return 0

        except Exception as e:
            print("Wrong", e)
            return 0
        finally:
            connection.close()

    # userId的用户评论id的课程，内容为comment  成功返回0失败返回1
    def add_comment(self, userId, act_id, comment):  # *OK
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                localtime = time.asctime(time.localtime(time.time()))
                sql = "INSERT INTO `Comments` (`message`, `auth_id`,`act_id`,`date`) VALUES (%s, %s, %s,%s)"
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

    def add_rate(self, userId, id, rate):  # userId的用户评分id的课程，分数为rate(0-5)  成功返回0失败返回1
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                if rate > 5 or rate < 0:
                    print("Wrong rate number")
                    return 1
                # TODO add sql line in here
                sql = "UPDATE Collection SET rate = %s WHERE Collection.`user_id` = %s AND Collection.`activity_id` = %s"
                cursor.execute(sql, (rate, userId, id))
                # cursor.execute(sql, (message, userID, act_id))
            # your changes.
            connection.commit()
            return 0
        except Exception as e:
            print("Wrong", e)
            return 1
        finally:
            connection.close()

    def courselike(self, userId, id):  # *Ok 收藏功能  改变状态，即没收藏变为收藏，收藏变为取消收藏
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # TODO add sql line in here
                sql = "SELECT Collection.id FROM Collection WHERE Collection.user_id = %s AND Collection.activity_id = %s"
                cursor.execute(sql, (userId, id))
                # cursor.execute(sql, (message, userID, act_id))
                resualts = cursor.fetchall()
                if len(resualts) != 0:
                    for row in resualts:
                        Collection_id = row[0]
                    sql = "DELETE FROM Collection WHERE id = %s"
                    cursor.execute(sql, (Collection_id))
                else:
                    sql = "INSERT INTO Collection (`user_id`, `activity_id`) VALUES (%s, %s)"
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
                sql = "SELECT * FROM Activity WHERE Activity.`id`=%s"
                cursor.execute(sql, (id))
                # TODO their must a bug because time problem
                results = cursor.fetchall()
                for row in results:
                    name = row[1]
                    # time = row[2]
                    # level = row[3]
                    # location = row[4]
                    introduction = row[5]
                    teacher = row[6]
                    school = row[7]
                    cover = row[8]
                    tags = row[9]
                    date = row[10]
                    # type = row[11]
                # sql = "SELECT time.`start_time`, time.`end_time`, time.`repeat` FROM time WHERE time.id = %s"
                # cursor.execute(sql, (time))
                # results = cursor.fetchall()
                # for row in results:
                #     start_time = row[0]
                #     end_time = row[1]
                # timeLocation = [start_time, end_time]
                timeLocation = str(date)
                sql = "SELECT rate FROM Collection WHERE user_id = %s AND activity_id = %s"
                cursor.execute(sql, (userId, id))
                rate = cursor.fetchone()
                if rate != None:
                    rate = rate
                    isRated = 1
                else:
                    rate = 0
                    isRated = 0
                sql = "SELECT id FROM Collection WHERE user_id = %s AND activity_id = %s"
                cursor.execute(sql, (userId, id))
                results = cursor.fetchone()
                if results == None:
                    isLiked = 0
                else:
                    isLiked = 1

                return {"id": id, "title": name, "school": school, "teacher": teacher, "cover": cover, "timeLocation": timeLocation, "tags": tags, "rate": rate, "isLike": isLiked, "hasRated": isRated, "description": [introduction]}

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

    def ask_comment(self, id):  # *Ok 查询id课程的评论  返回格式示例为：
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM Comments WHERE Comments.`act_id` = %s"
                cursor.execute(sql, (id))
                results = cursor.fetchall()
                ans = []
                for row in results:
                    message = row[1]
                    auth_id = row[2]
                    date = row[4]
                    sql = "SELECT User.`user_name` FROM User WHERE User.`id` = %s"
                    cursor.execute(sql, (id))
                    results = cursor.fetchall()
                    for row in results:
                        user_name = row[0]
                    ans.append({"id": auth_id, "userName": user_name,
                                "date": date, "content": message})
                # TODO return user_id
                # sql = "SELECT `User`.user_name FROM `User` WHERE `User`.id = %s"
                # cursor.execute(sql, (id))
                # results = cursor.fetchall()
                # for row in results:
                #     user_name = row[0]
                return ans
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

    def userinf(self, userId):  # *OK 查询用户相关信息  返回格式为
        connection = pymysql.connect(
            db=_database, user=_sql_user, passwd=_sql_password, host=_host, port=_port)
        # End
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `*` FROM `User` WHERE `User`.id = %s"
                cursor.execute(sql, (userId))
                results = cursor.fetchall()
                for row in results:
                    user_id = row[0]
                    user_name = row[1]
                    avator = row[2]
                    like = row[3]
                like = []
                sql = "SELECT Collection.activity_id FROM Collection WHERE Collection.activity_id = %s"
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

#     def search(self, keywords, fuzzy):
#         '''
#         keywords为字符串，包含若干关键词，以空格分隔；
#         fuzzy为bool，代表是否进行模糊搜索
#         '''
#         keywordslist = keywords.split()
#         pastlen = len(keywordslist)
#         if (fuzzy):
#             for i in range(pastlen):
#                 keywordslist += synonyms.nearby(keywordslist[i])[0][1:4]

#         connection = pymysql.connect(host=_host, user=_sql_user, password=_sql_password,
#                                      db=_database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, port=_port)

#         results = []
#         indexs = set()
#         try:
#             with connection.cursor() as cursor:
#                 for i in range(pastlen):
#                     sql = "select * from course where name=%s or teacher=%s"
#                     cursor.execute(sql, (keywordslist[i], keywordslist[i]))
#                     result = cursor.fetchall()
#                     for one in result:
#                         # results[one['id']]=one
#                         if one['id'] not in indexs:
#                             # 新的，去重
#                             indexs.add(one['id'])
#                             results.append(one)
#                 for i in range(pastlen):
#                     sql = "select * from course where intro like '%" + \
#                         keywordslist[i]+"%'"
#                     cursor.execute(sql)
#                     result = cursor.fetchall()
#                     for one in result:
#                         # results[one['id']]=one
#                         if one['id'] not in indexs:
#                             # 新的，去重
#                             indexs.add(one['id'])
#                             results.append(one)
#                 for i in range(pastlen+1, len(keywordslist)):
#                     sql = "select * from course where name=%s"
#                     cursor.execute(sql, (keywordslist[i], keywordslist[i]))
#                     result = cursor.fetchall()
#                     for one in result:
#                         # results[one['id']]=one
#                         if one['id'] not in indexs:
#                             # 新的，去重
#                             indexs.add(one['id'])
#                             results.append(one)
#                 for i in range(pastlen+1, len(keywordslist)):
#                     sql = "select * from course where intro like '%" + \
#                         keywordslist[i]+"%'"
#                     cursor.execute(sql)
#                     result = cursor.fetchall()
#                     for one in result:
#                         # results[one['id']]=one
#                         if one['id'] not in indexs:
#                             # 新的，去重
#                             indexs.add(one['id'])
#                             results.append(one)
#         finally:
#             connection.close()

#         return results

#     def classify(self, classifyargs):
#         '''
#         classifyargs类型为classifyArgs，用于传分类的参数，各个参数为字符串，传递分类的标准，不需要某类分类则置None。
#         classifyArgs类记得检查是否import了，这是自己定义的数据结构
#         '''
#         sql = "select * from Activity where"
#         first = True

#         if classifyargs.school != None:
#             if not first:
#                 sql += " and"
#             sql += ' school=' + classifyargs.school
#         elif classifyargs.time != None:
#             if not first:
#                 sql += " and"
#             sql += ' time=' + classifyargs.time
#         elif classifyargs.level != None:
#             if not first:
#                 sql += " and"
#             sql += ' level=' + classifyargs.level

#         connection = pymysql.connect(host=_host, user=_sql_user, password=_sql_password,
#                                      db=_database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, port=_port)

#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(sql)
#                 result = cursor.fetchall()
#         finally:
#             connection.close()

#         return result


# class classifyArgs():
#     # campus = None
#     time = None
#     school = None
#     level = None
