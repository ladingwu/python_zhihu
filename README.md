# python_zhihu
一个知乎爬虫（最新），模拟登陆，获取答案，

下载文件到某个文件夹，然后运行，根据提示执行程序，

[如下](https://github.com/ladingwu/python_zhihu/blob/master/example.jpg)

**验证码问题**：程序会下载验证码到文件目录下，你需要手动填写验证码，登陆一次之后，会记录你的cookies下次可以直接登陆，无需填写密码等，cookies文件也在程序文件目录下。

实例化：

from python_zhihu import ZhiHu

zh=ZhiHu()

下载某个问题下的高赞答案：

zh.get_answer_text('某问题的url')

下载某个问题下所有的图片：

zh,get_answer_img('某问题的url')
