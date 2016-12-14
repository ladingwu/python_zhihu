# python_zhihu
一个知乎爬虫（最新），模拟登录，获取答案，

python环境：python3.X
依赖的包：requests


下载文件到某个文件夹，然后运行，根据提示执行程序，

![](https://github.com/ladingwu/python_zhihu/blob/master/example.jpg)

**验证码问题**：程序会下载验证码到文件目录下，你需要手动填写验证码，登录一次之后，会记录你的cookies下次可以直接登录，无需填写密码等，cookies文件也在程序文件目录下。

实例化：

from python_zhihu import ZhiHu

zh=ZhiHu()

下载某个问题下的高赞答案：

zh.get_answer_text('某问题的url')
> 这个方法会下载某个问题下的高赞文字答案，存储在一个txt文件中

下载某个问题下所有的图片：

zh.get_answer_img('某问题的url')
> 这个方法会下载某个问题下的答案中的所有图片，并且按照回答人的昵称归类

## 更新
通过不同的方式（邮箱或手机号）登陆

## 2016-12-14，继续更新
有同学提交了一点代码，可以自动打开验证码图片，并且可以按赞数排序，棒！

后期可能会加上更多功能,敬请期待....
