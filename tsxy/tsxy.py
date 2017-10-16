import hashlib
import requests
from bs4 import BeautifulSoup
import pandas
import des
import b64

class Tsxy:
    def __init__(self):
        self.login_url = 'http://jiaowu.tsc.edu.cn/tscjw/cas/logon.action'
        self.code_url = 'http://jiaowu.tsc.edu.cn/tscjw/cas/genValidateCode'
        self.score_url = 'http://jiaowu.tsc.edu.cn/tscjw/student/xscj.stuckcj_data.jsp'
        self.deskey_url = 'http://jiaowu.tsc.edu.cn/tscjw/custom/js/SetKingoEncypt.jsp'
        self.baseinfo_url = 'http://jiaowu.tsc.edu.cn/tscjw/STU_BaseInfoAction.do'
        self.response = requests.session()
        r = self.response.get(self.deskey_url)
        self.deskey = r.text[19:38]
        self.timestamp = r.text[58:77]
        self.cookie = r.cookies['JSESSIONID']
        
    def get_code(self):
        r = self.response.get(self.code_url)
        with open('code.jpg', 'wb') as f:  
            f.write(r.content)
            f.close()
        code = input('请输入验证码:')
        return code
    
    def get_md5(self, passwd):
        passwd = passwd.encode(encoding='utf-8')
        md5 = hashlib.md5()
        md5.update(passwd)
        return md5.hexdigest()

    def login(self, username='4154301125', password='swh110119114hws'):
           code = self.get_code()
           username = b64.base64encode(username + ";;" + self.cookie)
           password = self.get_md5(self.get_md5(password) + self.get_md5(code))
           params = '_u' + code + '='+username +'&_p' + code + '=' + password + '&randnumber=' + code + '&isPasswordPolicy=1'
           token = self.get_md5(self.get_md5(params) + self.get_md5(self.timestamp))
           _params =  b64.base64encode(b64.utf16to8(des.strEnc(params, self.deskey, None, None)))
           postdata = {'params':_params, 'token':token, 'timestamp':self.timestamp}
           headers = {'Accept':'text/plain, */*; q=0.01',
                     'Accept-Encoding':'gzip, deflate',
                     'Accept-Language':'zh-CN,zh;q=0.8',
                     'Connection':'keep-alive',
                     'Content-Length':'844',
                     'content-type':'application/x-www-form-urlencoded',
                     'Cookie':'JSESSIONID=' + self.cookie,
                     'Host':'jiaowu.tsc.edu.cn',
                     'Origin':'http://jiaowu.tsc.edu.cn',
                     'Referer':'http://jiaowu.tsc.edu.cn/tscjw/cas/login.action',
                     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
           self.response.post(self.login_url, data = postdata, headers=headers)

    def get_baseinfo(self):
        postdata = {'hidOption':'InitData', 'menucode_current':'JW13020101'}
        headers = {'Accept':'*/*',
                   'Accept-Encoding':'gzip, deflate',
                   'Accept-Language':'zh-CN,zh;q=0.8',
                   'Connection':'keep-alive',
                   'Content-Length':'0',
                   'content-type':'application/x-www-form-urlencoded',
                   'Cookie':'JSESSIONID=' + self.cookie,
                   'Host':'jiaowu.tsc.edu.cn',
                   'Origin':'http://jiaowu.tsc.edu.cn',
                   'Referer':'http://jiaowu.tsc.edu.cn/tscjw/student/stu.xsxj.xjda.jbxx.html?menucode=JW13020101',
                   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

        res = self.response.post(self.baseinfo_url, data = postdata, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        print(soup)
        
    def get_score(self, usercode = '201500001868', xn = '2015', xn1 = '2016', xq = '0'):
           postdata = {'menucode_current':'','sjxz':'sjxz3','ysyx':'yscj','userCode':usercode,'xn':xn,'xn1':xn1,'xq':xq,'ysyxS':'on','sjxzS':'on'}
           headers = {'Host':'jiaowu.tsc.edu.cn',
                      'Connection':'keep-alive',
                      'Content-Length':'100',
                      'Cache-Control':'max-age=0',
                      'Origin':'http://jiaowu.tsc.edu.cn',
                      'Upgrade-Insecure-Requests':'1',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                      'Content-Type':'application/x-www-form-urlencoded',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Referer':'http://jiaowu.tsc.edu.cn/tscjw/student/xscj.stuckcj.jsp?menucode=JW130706',
                      'Accept-Encoding':'gzip, deflate',
                      'Accept-Language':'zh-CN,zh;q=0.8'} 
           res = self.response.post(self.score_url, data = postdata, headers=headers)
           soup = BeautifulSoup(res.text, 'html.parser')
           name = soup.find(style="float:left;text-align:left;width: 14%;").text[3:]
           student_id = soup.find(style="float:left;text-align:left;width: 12%;").text[3:]
           admin_class = soup.find(style="float:left;text-align:left;width: 20%").text[5:]
           college = soup.find(style="float:left;text-align:left;width: 22%;").text[7:]
           print('学院：%s\n班级：%s\n姓名：%s\n学号：%s' % (college, admin_class, name, student_id))
           result=[]
           for i in range(10):
               score = {}
               score['课程/环节'] = soup.select('tr td')[11 + i * 9].text
               score['学分'] = soup.select('tr td')[12 + i * 9].text
               score['类别'] = soup.select('tr td')[13 + i * 9].text
               score['修读性质'] = soup.select('tr td')[14 + i * 9].text
               score['考核方式'] = soup.select('tr td')[15 + i * 9].text
               score['取得方式'] = soup.select('tr td')[16 + i * 9].text
               score['成绩'] = soup.select('tr td')[17 + i * 9].text
               score['备注'] = soup.select('tr td')[18 + i * 9].text
               result.append(score)
           df = pandas.DataFrame(result, index=['1','2','3','4','5','6','7','8','9','10'], columns=['课程/环节','学分','类别','修读性质','考核方式','取得方式','成绩','备注'])   
           print(df.head(10))

if __name__ == '__main__':
    student = Tsxy()
    student.login()
    #student.get_baseinfo()
    student.get_score()
