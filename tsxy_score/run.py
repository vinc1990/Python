
from flask import *
import warnings
warnings.filterwarnings("ignore")
import pymysql
from config import *


app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
def connectdb():
	db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, use_unicode=True, charset=CHARSET)
	db.autocommit(True)
	cursor = db.cursor()
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')
	return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
	db.close()
	cursor.close()

# 首页
@app.route('/')
def index():
	return render_template('index.html')

# 处理表单提交
@app.route('/getscore', methods=['POST'])
def handle():
	# 获取post数据
	data = request.form
	if data['xq']=='第一学期':
		xq = '0'
	else:
		xq = '1'
	# 连接数据库
	(db,cursor) = connectdb()

	# 获取学生信息
	cursor.execute("select * from stu_info where number=%s", data['stu_id'])
	stu_info = cursor.fetchall()[0]
	stu_info = stu_info[2:]
	
	# 获取学生成绩
	cursor.execute("select * from stu_score where number=%s and xn=%s and xq=%s", (data['stu_id'], data['xn'], xq))
	stu_score = cursor.fetchall()
	posts = []
	posts.append(stu_info)
	for L in stu_score:
		posts.append(L[2:-3])

	# 关闭数据库
	closedb(db,cursor)
	print(posts)
	return render_template('score.html', posts=posts)



if __name__ == '__main__':
	app.run(debug=True)