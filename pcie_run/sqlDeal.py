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
    sql = "insert into Task(version, type, caseType, ip, user, createtime, status) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', sysdate(), '0');" % (version, type, caseType, ip, user)
    cursor.execute(sql)
    conn.commit()   # 插入数据，要提交一下
    result = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return result

def insertKeyFrameTime(casename, starttime, finishtime, taskid):
    conn = pymysql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpassword, db=DBdb, charset=DBcharset)
    cursor = conn.cursor()
    sql = "insert into keyFrameTime(casename, starttime, finishtime, taskid) values(\'%s\', sysdate(), sysdate(), \'%s\');" % (casename, starttime, finishtime, taskid)
    cursor.execute(sql)
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
    time1 = "select starttime from keyFrameTime where id = %s;" % (id)
    time2 = "select finishtime from keyFrameTime where id = %s;" % (id)
    sql = "update keyFrameTime set costtime = time1 - time2;"
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