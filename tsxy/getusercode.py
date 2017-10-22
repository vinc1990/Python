import requests
import pymysql
from bs4 import BeautifulSoup

def connectdb():
    db = pymysql.connect("localhost", "root", "", "stu_tsxy", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    return db,cursor

def closedb(db,cursor):
    cursor.close()
    db.close()

def get_score(x, db, cursor):
    userCode  = str(201500004941 + x)
    stu_score_list = []
    number = ""
    label = True
    #label = False
    for y in range(2):
        xn = str(2015 + y)
        xn1 = str(2016 + y)
        for z in range(2):
            xq = str(z)
            postdata1 = {'menucode_current':'','sjxz':'sjxz3','ysyx':'yscj','userCode':userCode,'xn':xn,'xn1':xn1,'xq':xq,'ysyxS':'on','sjxzS':'on'}
            headers1 = {'Host':'jiaowu.tsc.edu.cn',\
                                'Connection':'keep-alive',\
                                'Content-Length':'100',\
                                'Cache-Control':'max-age=0',\
                                'Origin':'http://jiaowu.tsc.edu.cn',\
                                'Upgrade-Insecure-Requests':'1',\
                                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',\
                                'Content-Type':'application/x-www-form-urlencoded',\
                                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',\
                                'Referer':'http://jiaowu.tsc.edu.cn/tscjw/student/xscj.stuckcj.jsp?menucode=JW130706',\
                                'Accept-Encoding':'gzip, deflate',\
                                'Accept-Language':'zh-CN,zh;q=0.8'} 
            s = requests.session()
            res = s.post('http://jiaowu.tsc.edu.cn/tscjw/student/xscj.stuckcj_data.jsp', data = postdata1, headers=headers1)
            soup = BeautifulSoup(res.text, 'html.parser')
         
            if label:
                try:
                    number = soup.find(style="float:left;text-align:left;width: 12%;").text[3:]
          
                except AttributeError:  
                    return
                #将学生信息传入数据库
                stu_info = []
                stu_info.append(userCode)
                stu_info.append(number)
                stu_info.append(soup.find(style="float:left;text-align:left;width: 22%;").text[7:])
                stu_info.append(soup.find(style="float:left;text-align:left;width: 20%").text[5:])
                stu_info.append(soup.find(style="float:left;text-align:left;width: 14%;").text[3:])
                
                # SQL 插入语句
                info_sql = "insert into stu_info(usercode, number, college, grade, name) values (%s, %s, %s, %s, %s)" 
                try:
                    # 执行sql语句
                    cursor.execute(info_sql, tuple(stu_info))
                    # 提交到数据库执行
                    db.commit()
                    label = False
                except:
                    # 如果发生错误则回滚
                    db.rollback()
            #number = '3153106225'
            #将学生成绩插入数据库
            for i in range(int((len(soup.select('tr td'))-10) / 9)):
                stu_score = []
                stu_score.append(number)
                for j in range(7):
                        stu_score.append(soup.select('tr td')[i * 9 + j + 11].text.strip())
                stu_score.append(xn)
                stu_score.append(xn1)
                stu_score.append(xq)
                stu_score_list.append(tuple(stu_score))
    score_sql = "insert into stu_score(number, course, credit, category, study, assessment, gain, score, xn, xn1, xq) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  
    try:
        cursor.executemany(score_sql, stu_score_list)
        db.commit()
    except:
        db.rollback()

(db,cursor) = connectdb()
for x in range(3):  
    get_score(x, db, cursor)
closedb(db,cursor)


