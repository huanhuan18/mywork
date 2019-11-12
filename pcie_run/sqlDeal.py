import pymysql

DBhost = "10.196.168.40"
DBport = 3306
DBuser = "huanhuan18"
DBpassword = "123456"
DBdb = "pcie"
DBcharset = "utf-8"

def insertTask(version, type, caseType, ip, user):
    conn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpassword, db=DBdb, charset=DBcharset)
    cursor = conn.cursor()
    sql1 = "insert into Task(version, type, caseType, ip, user, createtime, status) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', sysdate(), '0');" % (version, type, caseType, ip, user)
    sql2 = "(select @@identity);"
    cursor.execute(sql1)
    cursor.execute(sql2)
    conn.commit()   # 插入数据，要提交一下
    result = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

def insertKeyFrameTime(casename, starttime, taskid):
    conn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpassword, db=DBdb, charset=DBcharset)
    cursor = conn.cursor()
    sql1 = "insert into keyFrameTime(casename, starttime, taskid) values(\'%s\', sysdate(), \'%s\');" % (casename, taskid)
    sql2 = "(select @@identity);"
    cursor.execute(sql1)
    cursor.execute(sql2)
    conn.commit()
    result = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

def updatetime(id):
    conn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpassword, db=DBdb, charset=DBcharset)
    cursor = conn.cursor()
    sql = "update keyFrameTime set finishtime = sysdate() where id = %s;" % (id)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

def keyframeCosttime(id):
    conn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpassword, db=DBdb, charset=DBcharset)
    cursor = conn.cursor()
    result = "select starttime,finishtime from keyFrameTime where id = \'%s\;'" % (id)
    costtime = (result[1] - result[0]).seconds
    sql = "update keyFrameTime set costtime = \'%s\' where id = \'%s\';" % (costtime, id)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

def updateTask(id):
    conn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpassword, db=DBdb, charset=DBcharset)
    cursor = conn.cursor()
    sql = "update Task set status = \'1\', finishtime = sysdate() where id = \'%s\';" % (id)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result