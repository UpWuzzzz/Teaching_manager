# 教务系统爬取
做一个可视化界面帮助同学们查看成绩以及完成一些体力活。

#### 本项目使用的库
+ Thinter
+ urllib2
+ cookieJar
+ re
+ PIL
+ tesseract

#### 实现的功能
+ 成绩查询
+ 排名查询
+ 一键教评

#### 流程
```flow
st=>start: 开始
op=>operation: 输入用户名密码以及验证码
cond=>condition: 是否登陆成功
gd=>operation: 查询成绩
e=>end
st->op->cond
cond(yes)->gd
cond(no)->op
&```
