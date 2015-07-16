#/usr/bin/python
import requests,re,json,time,os,os.path
#模拟知乎登陆，主要是获取验证码登陆
_zhihu_url='http://www.zhihu.com'
_login_url=_zhihu_url+'/login/email'
_captcha_url=_zhihu_url+'/captcha.gif?r='
_session=None
email=None,
password=None,
xsrf=None
favor_data=100
question_url=None
header_data={'Accept':'*/*',
'Accept-Encoding':'gzip,deflate,sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Content-Length':'108',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
,'Host':'www.zhihu.com'
,'Origin':'http://www.zhihu.com'
,'Referer':'http://www.zhihu.com/'
,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
,'X-Requested-With':'XMLHttpRequest'
}

def get_captcha():
    return _captcha_url+str(int(time.time()*1000))

def save_captcha(url):
    global _session
    r=_session.get(url)
    with open("code.gif",'wb') as f:
        f.write(r.content)

def input_data():
    global email
    global password
    global question_url
    email=input('plesae input your email:')
    password=input('please input your password:')
    question_url=input('please input the question\'s url:')
      
def login():
    global _session
    global header_data
    global xsrf
    input_data()
    r=_session.get('http://www.zhihu.com')
    xsrf=re.findall('xsrf(.*)',r.text)[0][8:42]
    captcha=save_captcha(get_captcha())#下载验证码
    captcha=input('check the captcha and input captcha:')
    login_data = {' _xsrf':xsrf,'email':email,'password':password,'rememberme':'true'
    ,'captcha':captcha}
    r=_session.post(_login_url,data=login_data,headers=header_data)
    j=r.json()
    c=int(j['r'])
    if c==0:
        print('sign in successful')
        save_cookies()
        get_answer(question_url)
        os.remove("code.gif")
    else:
        print('登陆出现问题。。。。')
        

import  pickle
def save_cookies():
    global _session
    with open("cookiefile",'bw')as f:
        pickle.dump(_session.cookies.get_dict(),f)


def read_cookies():
    global _session,question_url
    with open('cookiefile','rb')as f:
        cookie=pickle.load(f)
        _session.cookies.update(cookie)
    question_url=input('please input the url of question:')
    

      
def get_answer(url):
    '''
该方法主要用于确定获赞前十的答案
'''
    global _session
    global favor_data
    r=_session.get(url)
    pat=re.compile('"count">(.*?)</span>')
    _list=re.findall(pat,r.text)
    favor_list=[int(k) for k in _list]
    favor_list.sort(reverse=True)
    if len(favor_list)>11:
        favor_data=favor_list[10]
    else:
        favor_data=0
    save_answer(r)


def save_answer(r):
    '''
该方法主要用于正则表达式获取内容
'''
    pattern_title=re.compile('<h2 class="zm-item-title zm-editable-content">\n\n([\s\S]*?)\n\n<\/h2>')
    pattern_desc=re.compile('<div class="zm-editable-content">([\s\S]*?)<\/div>')
    pattern=re.compile('div [\S\s]*?"count">(.*?)</span>[\s\S]*?clearfix">(.*)[\s\S]*?<\/div>')
    title=re.findall(pattern_title,r.text)
    desc=re.findall(pattern_desc,r.text)
    #print(title,desc)
    answer_favor_list=re.findall(pattern,r.text)
    with open(title[0]+'.txt','w') as f:
        f.write('问题：'+title[0]+'\n\n')
        f.write('描述：'+desc[0]+'\n\n')
        i=0
        for answer in answer_favor_list:
            i+=1
            if(int(answer[0])>favor_data):
                f.write('答案'+str(i)+'(赞同：'+answer[0]+')-->'+answer[1])
                f.write('-----------------------\n\n\n')

_session=requests.session()
if os.path.exists('cookiefile'):
    print('have cookies')
    read_cookies()
    get_answer(question_url)
else:
    login()
