模板笔记
２０１６年０３月２８日１６：４５：３６


把页面内容放在中间的class为     text-center。

url_for() 函数是在模板里用的

flask示例３－１０定义收藏夹图标
来http://www.w3cplus.com/css/understand-the-favicon.html

在base模板里放time失败
报错　TemplateSyntaxError: expected name or number

刚在模板又报错

发现是继承的命令extends 写成了extern　但是继承部分没问题　自己后加的东西报server error的错误

虽然有点像是废话，但是jinja2可以控制html元素

现在进度到第４章　　发现一bug。。。。当我使用网页的button属性进行页面跳转的时候。。
比如:
    ０　　127.0.0.1/user/
    １  　127.0.0.1/user/base/　　这一步找不到页面　因为前面一步的网址还在。。。
找到解决方法了...　　templates/base.html里 <a href="base">　在base前加一个/。。
也就是　a href="/base"。。。完美解决

wtf.巴拉巴拉函数　必须在{% block page_content %} 里　{% endblock %}

记录　刚才在表单类里放了中文折腾半天都报错 换成英文就好了

笔记　python代码里的 url_for() 括号里的参数是函数名　　（一开始还以为是html文件的名字╮（╯＿╰）╭
笔记　刚才忘记import flash　然后flash那一步一直失败也不报错　
