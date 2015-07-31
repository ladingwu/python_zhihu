#/usr/bin/python
import requests,re,json,time,os,os.path
#模拟知乎登陆，主要是获取验证码登陆
_zhihu_url='http://www.zhihu.com'
_login_url=_zhihu_url+'/login/email'
_captcha_url=_zhihu_url+'/captcha.gif?r='
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
class ZhiHu():

    _session=None
    #email=None,
    #password=None,
    #xsrf=None
    favor_data=100
    #question_url='http://www.zhihu.com/question/32120582'
    #path_for=None
    def __init__(self):
        self.do_first()
    def get_captcha(self):
        return _captcha_url+str(int(time.time()*1000))
    def save_captcha(self,url):
        global _session
        r=_session.get(url)
        with open("code.gif",'wb') as f:
            f.write(r.content)

    def input_data(self):
        global email
        global password
        global question_url
        self.email=input('plesae input your email:')
        self.password=input('please input your password:')
        self.captcha=self.save_captcha(self.get_captcha())
        captcha=input('check the captcha and input captcha:')

      
    def login(self):
        global _session
        global header_data
        global xsrf
        r=_session.get('http://www.zhihu.com')
        self.xsrf=re.findall('xsrf(.*)',r.text)[0][8:42]
        #print(xsrf)
        self.input_data()
        
        
        login_data = {' _xsrf':self.xsrf,'email':self.email,'password':self.password,'rememberme':'true'
        ,'captcha':self.captcha}
        r=_session.post(_login_url,data=login_data,headers=header_data)
        j=r.json()
        print(j)
        c=int(j['r'])
        if c==0:
            print('sign in successful')
            #print(_session.cookies.get_dict())
            self.save_cookies()
            os.remove("code.gif")
        
        else:
            print('登陆出现问题。。。。')
        
    import  pickle,json
    def save_cookies(self):
        global _session,path_for
        with open('./'+"cookiefile",'w')as f:
            json.dump(_session.cookies.get_dict(),f)
            #_session.cookies.save()

    def read_cookies(self):
        global _session,path_for
        #_session.cookies.load()
        #_session.headers.update(header_data)
        with open('./'+'cookiefile')as f:
            cookie=json.load(f)
            _session.cookies.update(cookie)
 
    def get_text(self,url,answers=15):
        global _session
        global favor_data
        r=_session.get(url)
        pat=re.compile('"count">(.*?)</span>')
        _list=re.findall(pat,r.text)
        favor_list=[int(k) for k in _list]
        favor_list.sort(reverse=True)
        if len(favor_list)>=answers:
            favor_data=favor_list[answers-1]
        else:
            favor_data=0
        self.save_text(r)

    def get_img(self,url):
        global  _session
        r=_session.get(url).text
        pat_img=re.compile('<noscript><img src="([\s\S]*?)"')
        url_list=re.findall(pat_img,r.text)
        i=0
        try :   
            for img_url in url_list:
                i+=1
                with open(str(i)+'.jpg','bw')as f:
                    print('下载第'+str(i)+'张')
                    f.write(_session.get(img_url).content)
        except :
            print('可能出了一点问题。。。')
    
    def save_text(self,r):
        global path_for
        pattern_title=re.compile('<h2 class="zm-item-title zm-editable-content">\n\n([\s\S]*?)\n\n<\/h2>')
        pattern_desc=re.compile('<div class="zm-editable-content">([\s\S]*?)<\/div>')
        pattern=re.compile('div [\S\s]*?"count">(.*?)</span>[\s\S]*?clearfix">(.*)[\s\S]*?<\/div>')
        
        title=re.findall(pattern_title,r.text)
        desc=re.findall(pattern_desc,r.text)
        #print(title,desc)
        #a=re.sub(re.compile('<br>'),'\n',r.text)
        answer_favor_list=re.findall(pattern,r.text)
        pat_sub=re.compile('<br>')
        with open('./'+title[0]+'.txt','w') as f:
            try:
                
                f.write('问题：'+title[0]+'\n\n')
                f.write('描述：'+desc[0]+'\n\n')
                i=0
                for answer in answer_favor_list:
                    i+=1
                    if(int(answer[0])>favor_data):
                        f.write('\n-------------------''答案'+str(i)+'(赞同：'+answer[0]+')''---------------------\n')
                        f.write('\n答案'+str(i)+'(赞同：'+answer[0]+')-->'+re.sub(pat_sub,'\n',answer[1]))
                        f.write('\n++++++++++++++++++++++++this answer is over++++++++++++++++++++++++++++++')
                        f.write('\n\n')
            except Exception as e:
                print('可能在文件读写的时候出了一点问题。。。')

    def do_first(self):
        global _session
        _session=requests.session()
        if os.path.exists('cookiefile'):
            print('have cookies')
            self.read_cookies()
            #self.get_text(question_url)
        else:
            self.login()
        
