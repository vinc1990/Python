import requests

from bs4 import BeautifulSoup

for i in range(0, 1):
    userCode  = str(201500004941 + i)
    postdata1 = {'menucode_current':'','sjxz':'sjxz3','ysyx':'yscj','userCode':userCode,'xn':'2015','xn1':'2016','xq':'1','ysyxS':'on','sjxzS':'on'}
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
    print(soup)
    number = soup.find(style="float:left;text-align:left;width: 12%;").text[3:]
    print(number)

