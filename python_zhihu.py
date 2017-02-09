#/usr/bin/python
import requests,re,json,time,os,os.path,sys
#显示验证码
from PIL import Image
import traceback
import json
#模拟知乎登陆，主要是获取验证码登陆
_zhihu_url='https://www.zhihu.com'
_captcha_url=_zhihu_url+'/captcha.gif?r='
_captcha_url_end="&type=login";
header_data={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0'
    ,'Host':'www.zhihu.com'
    ,'Upgrade-Insecure-Requests':'1'
    ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'

    }


class ZhiHu():

    _session=None

    favor_data=100

    def __init__(self):
        self.do_first()
    def get_captcha(self):
        return _captcha_url+str(int(time.time()*1000))+_captcha_url_end
    def show_or_save_captcha(self,url):
        global _session
        r=_session.get(url,headers=header_data,verify=True)
        with open("code.gif",'wb') as f:
            f.write(r.content)
        #显示验证码
        try:
            print("haha")
            im = Image.open("code.gif")
            im.show()
        except:
            print("请打开下载的验证码文件code.gif")

    def input_data(self):
        global email
        global password
        global question_url
        self.username=input('请输入用户名:')
        self.password=input('请输入密码:')
        self.show_or_save_captcha(self.get_captcha())
        self.captcha=input('请输入验证码:')

      
    def login(self):
        global _session
        global header_data
        global xsrf
        r=_session.get('https://www.zhihu.com',headers=header_data,verify=True)
        self.xsrf=re.findall('name="_xsrf" value="([\S\s]*?)"',r.text)[0]

        self.input_data()
        #确定用户名类型
        if re.search(r'^1\d{10}$', self.username):
            _type='phone_num'
            _login_type='/login/phone_num'
        elif re.search(r'(.+)@(.+)', self.username):
            _login_type='/login/email'
            _type='email'
        else:
            print('用户名格式不正确')
            sys.exit(1)
        
        
        login_data = {' _xsrf':self.xsrf,_type:self.username,'password':self.password,'rememberme':'true'
        ,'captcha':self.captcha}
        r=_session.post(_zhihu_url+_login_type,data=login_data,headers=header_data,verify=True)
        j=r.json()
        c=int(j['r'])
        if c==0:
            print('sign in successful')
            
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
 
    def get_answer_text(self,url,answers=15):
        global _session
        global favor_data
        r=_session.get(url,headers=header_data,verify=True)
        pat=re.compile('"count">[\s]*?(.*?)</span>')
       
        _list=re.findall(pat,r.text)
        #print(_list);
        #favor_list=[int(k) for k in _list]
        favor_list=[]
        #下面主要是将以“K”为单位的赞同数转化为数字
        for i in _list:
            if 'K' in i:
                #print('k in'+i)
                i = i.replace('K','000')
                favor_list.append(int(i))
            else:
                #print(i)
                favor_list.append(int(i))
                
        favor_list.sort(reverse=True)
        if len(favor_list)>=answers:
            favor_data=favor_list[answers-1]
        else:
            favor_data=0
        self.save_text(r)

    def get_answer_img(self,url):
        global  _session
        r=_session.get(url,headers=header_data,verify=True).text
        item_pattern=re.compile('<div tabindex="-1" class="zm-item-answer  zm-item-expanded"([\S\s]*?)class="meta-item zu-autohide js-noHelp">')
        img_pattern=re.compile('<img[\s\S]*? src="([\s\S]*?)"')
        pattern_title=re.compile('<span class="zm-editable-content">([\s\S]*?)</span>')
        #author_pattern=re.compile('<a class="author-link"[\s\S]*?href="([\S\s]*?)"')
        author_pattern=re.compile('<a class="author-link"[\s\S]*?>([\S\s]*?)</a>')
        items=re.findall(item_pattern,r)
        title=re.findall(pattern_title,r)
        authors=[]
        img_list=[]
        i=0
        try :

            for item in items:

                i+=1
                authors.append(re.findall(author_pattern,item))
 
                img_list.append(re.findall(img_pattern,item))
                
               
        except :
            print('查找出了一点问题')
            traceback.print_exc()
        try:
            #print(authors)
            j=0
            for author in authors:
                img_urls=img_list[j]
                #print(len(img_urls))
                if len(img_urls) == 0:
                    continue
                title_text=title[0];
                author_text=''
                if len(author)>0:
                    author_text=author[0]
                    path=self.createPathIfNotExist(title_text+'\\'+author[0])
                j+=1
                k=0
                for url in img_urls:
                    if 'https' not in url:
                        #print('坏图：'+url)
                        continue
                    print(url)
                    temp=url.split('.')
                    suffix='jpg'
                    if len(temp)>0:
                        
                        suffix=temp[len(temp)-1]
                        #print('suffix=  '+suffix)
                    
                    k+=1
                    with open(path+author_text+str(k)+'.'+suffix,'bw')as f:
                        print('下载第'+str(j)+'个人'+'第'+str(k)+'照片')
                        f.write(_session.get(url,verify=True).content)

                
                
        except:
            print('下载图片出了一点问题')
            traceback.print_exc()
                
    def createPathIfNotExist(self,path):
        root_path=os.path.abspath('.')
        p=root_path+'\\'+path+'\\'
        if not os.path.exists(p):
            os.makedirs(p)   
        return p

    #def getAnswerByPage(self):
        #t='include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        #r=_session.get('https://www.zhihu.com/api/v4/questions/'+'48337357'+'/answers?+'+t+'&offset=0&limit=20&sort_by=default',headers=header_data,verify=True)
        #jdata=json.loads(r.text);
        #return jdata

            
    def save_text(self,r):
        global path_for
        pattern_title=re.compile('<span class="zm-editable-content">([\s\S]*?)</span>')
        pattern_desc=re.compile('<div class="zm-editable-content">([\s\S]*?)</div>')
        pattern_answer=re.compile('<span class="count">[\s]*?([\S]*?)</span>[\s\S]*?<div class="zm-editable-content clearfix">([\s\S]*?)</div>')
        
        title=re.findall(pattern_title,r.text)
        #print('title:'+title[0]);
        desc=re.findall(pattern_desc,r.text)
        #print(title,desc)
        #a=re.sub(re.compile('<br>'),'\n',r.text)
        answer_favor_list=re.findall(pattern_answer,r.text)
        pat_sub=re.compile('<br>')
        with open('./'+title[0]+'.txt','w',encoding='utf-8') as f:
            try:
                
                f.write('问题：'+title[0]+'\n\n')
                f.write('描述：'+desc[0]+'\n\n')
                #按赞同数多少对答案排序
                answer_favor_list = sorted(answer_favor_list, reverse=True, key=self.get_int_list)
                for i,answer in enumerate(answer_favor_list):
                    #print('answer[0]--->'+answer[0])
                    if(self.get_int(answer[0])>favor_data):
                        f.write('\n-------------------''答案'+str(i+1)+'(赞同：'+answer[0]+')''---------------------\n')
                        f.write('\n答案'+str(i+1)+'(赞同：'+answer[0]+')-->'+re.sub(pat_sub,'\n',answer[1]))
                        f.write('\n++++++++++++++++++++++++this answer is over++++++++++++++++++++++++++++++')
                        f.write('\n\n')
            except Exception as e:
                print('可能在文件读写的时候出了一点问题。。。')
                traceback.print_exc()
    def get(self,url):
        return _session.get(url,headers=header_data,verify=True)
    def get_int(self ,s):
        if 'K' in s:
            return int(s.replace('K','000'))
        return int(s)
    def get_int_list(self, answer_list):
        return self.get_int(answer_list[0])
    def do_first(self):
        global _session
        _session=requests.session()
        if os.path.exists('cookiefile'):
            #print('have cookies')
            self.read_cookies()
            #self.get_text(question_url)
        else:
            self.login()
        
