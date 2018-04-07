#-*- coding: UTF-8 -*-
#__author__ = 'Awu'
#__data__ = '2018/1/18'
#__lastModified__ = '2018/2/2'

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import urllib.request
import http.cookiejar
import urllib.parse
import re
import os
import sys
from PIL import Image
from PIL import ImageTk	
from PIL import ImageEnhance	
from PIL import ImageFilter
import pytesseract
from importlib import reload
from bs4 import BeautifulSoup
import io
import requests
import random
import time
import json


CET ="http://www.chsi.com.cn/cet/"
CaptchaUrl = "http://jwxt.xtu.edu.cn/jsxsd/verifycode.servlet"
PostUrl = "http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk"
GradeUrl="http://jwxt.xtu.edu.cn/jsxsd/kscj/cjcx_list?xq="
RKpostUrl="http://jwxt.xtu.edu.cn/jsxsd/kscj/cjjd_list"
EvaluationUrl = "http://jwxt.xtu.edu.cn/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ"
FlagUrl = "http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk?flag=sess"

def getRank(opener):
	li=[]
	li1=[]
	li2=[]
	postData = [
		('kksj','2017-2018-1'),
		('kksj','2016-2017-2'),
		('kksj','2016-2017-1'),
		('kksj','2015-2016-2'),
		('kksj','2015-2016-1'),
		('kclb', '1'),
		('kclb', '7'),
		('zsb', '0'),
	]
	postData1 = [
		('kksj','2017-2018-1'),
		('kksj','2016-2017-2'),
		('kksj','2016-2017-1'),
		('kksj','2015-2016-2'),
		('kksj','2015-2016-1'),
		('kclb', '1'),
		('zsb', '0'),
	]
	postData2 = [
		('kksj','2017-2018-1'),
		('kksj','2016-2017-2'),
		('kksj','2016-2017-1'),
		('kksj','2015-2016-2'),
		('kksj','2015-2016-1'),
		('kclb', '7'),
		('zsb', '0'),
	]
	headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Connection': 'keep-alive',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
	}
	data=urllib.parse.urlencode(postData).encode(encoding='UTF-8')
	request=urllib.request.Request(RKpostUrl,data,headers)
	try:
		response=opener.open(request)
		soup=BeautifulSoup(response.read().decode('UTF-8'),'lxml')
		for tabb in soup.find_all('tr'):
			for trr in tabb.find_all('td'):
				if trr.get_text()!='':
					li.append(trr.get_text())
	except urllib.request.HTTPError as e:
		print(e.code())

	data1=urllib.parse.urlencode(postData1).encode(encoding='UTF-8')
	request1=urllib.request.Request(RKpostUrl,data1,headers)
	try:
		response1=opener.open(request1)
		soup1=BeautifulSoup(response1.read().decode('UTF-8'),'lxml')
		for tabb in soup1.find_all('tr'):
			for trr in tabb.find_all('td'):
				if trr.get_text()!='':
					li1.append(trr.get_text())
	except urllib.request.HTTPError as e:
		print(e.code())

	data2=urllib.parse.urlencode(postData2).encode(encoding='UTF-8')
	request2=urllib.request.Request(RKpostUrl,data2,headers)
	try:
		response2=opener.open(request2)
		soup2=BeautifulSoup(response2.read().decode('UTF-8'),'lxml')
		for tabb in soup2.find_all('tr'):
			for trr in tabb.find_all('td'):
				if trr.get_text()!='':
					li2.append(trr.get_text())
	except urllib.request.HTTPError as e:
		print(e.code())
	RankGUI=Tk()
	RankGUI.title("排名")
	RankGUI.geometry('350x300+700+400')
	tree=ttk.Treeview(RankGUI,show="headings",height=300)
	tree["columns"]=("课程属性","平均分","平均成绩","班级排名","专业排名")
	tree.column("课程属性",width=70)
	tree.column("平均分",width=70)
	tree.column("平均成绩",width=70)
	tree.column("班级排名",width=70)
	tree.column("专业排名",width=70)
	tree.heading("课程属性",text="课程属性")
	tree.heading("平均分",text="平均学分")  #显示表头
	tree.heading("平均成绩",text="平均成绩")
	tree.heading("班级排名",text="班级排名")
	tree.heading("专业排名",text="专业排名")
	tree.insert("",0,values=("全部成绩",li[0],li[1],li[2],li[3]))
	tree.insert("",1,values=("必修成绩",li1[0],li1[1],li1[2],li1[3]))
	tree.insert("",2,values=("选修成绩",li2[0],li2[1],li2[2],li2[3]))
	tree.pack(side='left')
	RankGUI.mainloop()

def ChoseSocre(opener):
	main=Tk()
	main.title("查询成绩")
	main.geometry('500x300+500+200')
	choose=Frame(main,height=30,width=200)
	def print_item(event):
		for i in tree.get_children():
			tree.delete(i)
		global year
		year=yearChosen.get(yearChosen.curselection())
		li=[]
		global GradeUrl
		GradeUrl=GradeUrl+year
		grade = opener.open(GradeUrl).read()
		grade=grade.decode('UTF-8')
		GradeUrl="http://jwxt.xtu.edu.cn/jsxsd/kscj/cjcx_list?xq="
		fo=''
		exp1 = re.compile("(?isu)<tr[^>]*>(.*?)</tr>")
		exp2 = re.compile("(?isu)<td[^>]*>(.*?)</td>")
		exp3 = re.compile("(?isu)<td[^>]*><a[^>]*>(.*?)</a></td>")
		for row in exp1.findall(grade)[2:14]:
			i=0
			for col in exp2.findall(row):
				if i==3:
					col=exp3.findall(row)[0]
				fo=fo+col+','
				i+=1
			li.append(fo)
			fo=''
		i=0
		for z in li:
			str=z.split(',')
			tree.insert("",i,text=str[2],values=(str[2],str[3],str[4],str[7])) #插入数据，
			i+=1

	var = StringVar()
	yearChosen = Listbox(choose, height=10, selectmode=BROWSE, listvariable = var)
	yearChosen.bind('<ButtonRelease-1>', print_item)
	list_item = ['2015-2016-1','2015-2016-2','2016-2017-1','2016-2017-2','2017-2018-1','2017-2018-2']
	list_item.reverse()
	for item in list_item:
		yearChosen.insert(END, item)
	scrl = Scrollbar(choose)
	scrl.pack(side=RIGHT, fill=Y)
	yearChosen.configure(yscrollcommand = scrl.set) #停在拉取的位置
	scrl['command'] = yearChosen.yview #显示list的Y轴的值
	yearChosen.pack(side=LEFT, fill=BOTH)
	choose.pack(side=LEFT)
	ScoreGui=Frame(main,width=320,height=200)
	tree=ttk.Treeview(ScoreGui,show="headings",height=300)#表格
	tree["columns"]=("科目","成绩","学分","课程属性")
	tree.column("科目",width=150)   #表示列,不显示
	tree.column("成绩",width=50)
	tree.column("学分",width=50)
	tree.column("课程属性",width=70)
	tree.heading("科目",text="科目")  #显示表头
	tree.heading("成绩",text="成绩")
	tree.heading("学分",text="学分")
	tree.heading("课程属性",text="课程属性")
	scrl = Scrollbar(ScoreGui)
	scrl.pack(side=RIGHT, fill=Y)
	tree.configure(yscrollcommand = scrl.set) #停在拉取的位置
	scrl['command'] = tree.yview #显示list的Y轴的值
	tree.pack(side='left',fill=BOTH)
	ScoreGui.pack(side='right')
	main.mainloop()

def getcookie():
	cookie = http.cookiejar.CookieJar()
	handler = urllib.request.HTTPCookieProcessor(cookie)
	opener = urllib.request.build_opener(handler)
	# 将cookies绑定到一个opener cookie由import http.cookiejar自动管理
	return opener

def download():
	global opener
	opener=getcookie()
	code = opener.open(CaptchaUrl).read()
	# 用openr访问验证码地址,获取cookie
	tempIm = io.BytesIO(code)
	# 保存验证码到内存
	codepic=Image.open(tempIm)
	img_open =ImageTk.PhotoImage(codepic)
	codeLabel=Label(mainGui,image=img_open)
	codeLabel.image=img_open
	codeLabel.place(x=210,y=228)
	def retry(event):
		download()
	codeLabel.bind('<ButtonRelease-1>', retry)

def start(user,pas,codenum):
	if len(user)==0 or len(pas)==0:
		messagebox.showinfo('提示','请填写用户名或密码。')
	else:
		reload(sys)
		username = user
		password = pas
		# 用户名和密码
		flagData = {
			'flag':'sess',
		}
		headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
		}
		# 根据抓包信息 构造headers
		DData = urllib.parse.urlencode(flagData).encode(encoding='UTF-8')
		flag = urllib.request.Request(FlagUrl, DData, headers)
		try:
			responseFlag = opener.open(flag)
			hjson = json.loads(responseFlag.read())['data']
			scode = hjson.split('#')[0]
			sxh = hjson.split('#')[1]
			code = username + "%%%" + password
			encoded = ''
			for i in range(len(code)):
				if i < 20:
					encoded = encoded + code[i: i+1] + scode[0: int(sxh[i: i+1])]
					scode = scode[int(sxh[i: i+1]): len(scode)]
				else:
					encoded = encoded+code[i: len(code)]
					break
		except urllib.request.HTTPError as e:
			print(e)
		SecretCode = codenum
		# 打开保存的验证码图片 输入
		postData = {
		'USERNAME': username,
		'PASSWORD': password,
		'encoded':encoded,
		'RANDOMCODE': SecretCode,
		}
		# 根据抓包信息 构造表单
		data = urllib.parse.urlencode(postData).encode(encoding='UTF-8')
		# 生成post数据 ?key1=value1&key2=value2的形式
		request = urllib.request.Request(PostUrl, data, headers)
		# 构造request请求
		try:
			response = opener.open(request)
			if response.geturl()=="http://jwxt.xtu.edu.cn/jsxsd/framework/xsMain.jsp":
				clearent1()
				clearent2()
				clearent3()
				result = response.read().decode('UTF-8')
				soupp = BeautifulSoup(result,'lxml')
				namee = soupp.find("div",id="Top1_divLoginName").get_text()
				main(opener,username,namee)
			else:
				result = response.read().decode('gbk')
				if len(re.findall('用户名或密码错误,请联系本院教务老师!',result)) >0:
					messagebox.showinfo('提示','账号或密码错误！！！')
					clearent1()
					clearent2()
					clearent3()
				else:
					messagebox.showinfo('提示','验证码错误！！！')
					download()
					clearent3()
		except urllib.request.HTTPError as e:
			print (e.code)
		# 利用之前存有cookie的opener登录页面
	

def main(opener,username,name):
	mainGui.destroy()
#	mainGui.withdraw()
	def returnLogin(event):
		root.destroy()
#		mainGui.deiconify()
	def inn(event):
		lab1['fg'] ='red'
	def lev(event):
		lab1['fg'] ='black'
	root = Tk()
	root.title("Getit")
	root.geometry("300x300+500+200")
	root.iconbitmap('ico\\图标.ico')
	b1 =Button(root,text="查成绩",command = lambda: ChoseSocre(opener),width=10,height=1,bg='#1d6bb6',fg='white')
	b2 =Button(root,text="发送满意度",command = lambda: PostGui(opener,username),width=10,height=1,bg='#1d6bb6',fg='white')
	b3 =Button(root,text="查询排名",command=lambda: getRank(opener),width=10,height=1,bg='#1d6bb6',fg='white')
	b4 =Button(root,text="发送教评",command=lambda: TeachDo(opener),width=10,height=1,bg='#1d6bb6',fg='white')
	b5 =Button(root,text="...",width=10,height=1,bg='#1d6bb6',fg='white')
	b6 =Button(root,text="...",width=10,height=1,bg='#1d6bb6',fg='white')
	lab =Label(root,text="当前用户：%s"%name)
	lab1 =Label(root,text="注销登录",fg='black')
	bag = Image.open('ico\\背景图片.png')
	img_bac = ImageTk.PhotoImage(bag)
	backage =Label(root,image=img_bac)
	backage.image=img_bac
	lab1.bind('<Enter>',inn)
	lab1.bind('<Leave>',lev)
	lab1.bind('<ButtonRelease-1>', returnLogin)
	b1.place(x=15, y=40)
	b2.place(x=110, y=40)
	b3.place(x=205, y=40)
	b4.place(x=15, y=80)
	b5.place(x=110, y=80)
	b6.place(x=205, y=80)
	lab.place(x=0,y=0)
	lab1.place(x=250,y=0)
	backage.place(x=100,y=140)
	root.mainloop()

def TeachDo(opener):
	def doing(opener):
		headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
		}
		text.insert(END,"查找网页信息...."+'\n'+"请等待...."+'\n')
		text.see(END)
		text.update()
		Evaluation = opener.open(EvaluationUrl).read()
		soup = BeautifulSoup(Evaluation, 'lxml')
		for trr in soup.find_all('tr'):
			for a in trr.find_all('a'):
				url = "http://jwxt.xtu.edu.cn"
				ss = opener.open(url + a['href']).read()
				if len(ss) > 9000:
					print("找到教评网页："+url + a['href'])
					text.insert(END,"找到教评网页："+url + a['href']+'\n')
					text.see(END)
					text.update()
					time.sleep(3)
					Teacherdo = BeautifulSoup(ss.decode('utf-8'), 'lxml')
					for trrr in Teacherdo.find_all('tr'):
						for aa in trrr.find_all('a'):
							if aa.get_text() == '查看':
								print("已评价")
								text.insert(END,"已评价"+'\n')
								text.see(END)
								text.update()
								time.sleep(1)
								continue
							elif aa.get_text() == '评价':
								str1 = aa['href']
								done = opener.open(url + str1[18:-11]).read()
								if len(done) < 7000:
									time.sleep(3)
									text.insert(END,"没有数据信息"+'\n')
									text.see(END)
									text.update()
									continue
								else:
									time.sleep(3)
									print("开始处理:"+url + str1[18:-11])
									text.insert(END,"开始处理:"+url + str1[18:-11]+'\n')
									text.see(END)
									text.update()
									donee = BeautifulSoup(done.decode('utf-8'), 'lxml')
									TeacherdoPost = []
									for inn in donee.find_all('input'):
										if inn['name'] == 'issubmit':
											TeacherdoPost.append((inn['name'], '1'))
											continue
										elif inn['name'] == 'pj06xh':
											break
										else:
											TeacherdoPost.append((inn['name'], inn['value']))
									for trrrr in donee.find_all('tr'):
										choice = ''
										randd = str(random.randint(1, 2))
										for td in trrrr.find_all('td'):
											for inn in td.find_all('input'):
												if inn['name'] == "pj06xh":
													choice = 'pj0601id_'+inn['value']
													TeacherdoPost.append((inn['name'], inn['value']))
												else:
													if inn['name'] == choice:
														if inn['id'] == choice+'_'+randd:
															TeacherdoPost.append((inn['name'], inn['value']))
													elif inn['type'] == 'hidden':
														TeacherdoPost.append((inn['name'], inn['value']))
									TeacherdoPost.append(('jynr', ''))
									print("发送表单数据！！")
									text.insert(END,"发送表单数据！！"+'\n')
									text.see(END)
									text.update()
									time.sleep(5)
									dataUrl = 'http://jwxt.xtu.edu.cn/jsxsd/xspj/xspj_save.do'
									data = urllib.parse.urlencode(TeacherdoPost).encode(encoding="UTF-8")
									request1 = urllib.request.Request(dataUrl, data, headers=headers)
									try:
										response = opener.open(request1)
									except:
										print("出错，请重试，")
										text.insert(END,"出错，请重试，"+'\n')
										text.see(END)
										text.update()
					print("处理完成。请等待查询网址。")
					text.insert(END,"处理完成。请等待查询网址。"+'\n')
					text.see(END)
					text.update()
				else:
					print("无效网址。")
					text.insert(END,"无效网址。"+'\n')
					text.see(END)
					text.update()

	console = Tk()
	console.title("控制台")
	console.iconbitmap('ico\\图标.ico')
	text = Text(console,width=20,height=20)
	text.pack(fill=X,side=LEFT)
	scrl = Scrollbar(console)
	scrl.pack(side=RIGHT, fill=Y)
	text.configure(yscrollcommand = scrl.set) #停在拉取的位置
	scrl['command'] = text.yview #显示list的Y轴的值
	doing(opener)
	text.insert(END,"处理完成。"+'\n')
	console.mainloop()


def PostGui(opener,username):
	PostGui = Tk()
	PostGui.title("writer ：xiaowu")
	PostGui.geometry("270x255+500+200")
	PostGui.iconbitmap('ico\\图标.ico')
	def getText():
		solution = text.get("0.0","end")
		if solution == '\n':
			solution ="教学硬件希望加强，生活质量希望提高。"
		if post(solution,opener,username):
			messagebox.showinfo('提示','发送成功！！！')
			PostGui.destroy()
		else :
			messagebox.showinfo('提示','发送失败！！！')
	b1=Button(PostGui,width = 15,text="确认",command = getText)
	lab2 = Label(PostGui,fg='red',text="如果不填写的话，会默认为我的建议！！！")
	lab1 = Label(PostGui,text="题写你对改进学校教育教学工作的看法和建议")
	lab1.place(x=20,y=70)
	lab2.place(x=20,y=20)
	text = Text(PostGui,width = 30 , height = 6)
	text.place(x=20,y=103)
	b1.place(x=80,y=200)
	PostGui.mainloop()

def post(solution,opener,username):
	PostUrl = "http://jwxt.xtu.edu.cn/jsxsd/mydgl/doSavePsNew?psfs=2&mydpcid=0B5EF67FD3B048E19F8C31554E3F213B&xs0101id=%s&xnxq01id=2017-2018-1"%username
	postData = [
	('hiddenj11','2C32E57802EE4771A9941A4CB9908F09'),
	('hiddenj11radio','711B10DCD39146259AD13F28DB3D99D4'),
	('hiddenj12','677E54163D9941D6BEC5205824242A41'),
	('hiddenj12radio','4EA52B12CDE842E9A7EBDEFA3BFA3ADC'),
	('hiddenj13','D9DC66C94CD442DEA22A1B33DBC89578'),
	('hiddenj13radio','FA452BADABEF49D088F0445CA508010E'),
	('hiddenj14','BB2A1555423F4D68B9697E303B4FACB2'),
	('hiddenj14radio','3281610530AA42BF8C3EB819AF1CF788'),
	('hiddenj15','42B38CD111D54056AA1792B5E24FC4EB'),
	('hiddenj15radio','BEA44B9FCA6E425BABA185D2D339C589'),
	('hiddenj16','50F387EB0C864D67BC35FCFF21C0541F'),
	('hiddenj16radio','229641DD21D44246AF2DE4CC1C88ED23'),
	('hiddenj17','DFD3F06E42624C6C9AEFD661E5DF8B9E'),
	('hiddenj17radio','23095578C2AB40DCA0CED0D2BA2A0BDE'),
	('hiddenj18','44D7EFE96C4F4FE096FE249831886125'),
	('hiddenj18radio','31DDE2C773D544D39435C311198828C0'),
	('hiddenj19','9111D74168B548A58FC04E87871369EB'),
	('hiddenj19radio','4A15906796F14BC6ABE896DA36C84C39'),
	('hiddenj110','6E1113CF0955490EAE8442AF6F366658'),
	('hiddenj110radio','575B520863114FE79C6C2B241ED3673A'),
	('hiddenj111','7D1ECDCC22B64FC89C1FB8CBD34AF3DB'),
	('hiddenj111radio','66EEE8FD4DE34E129DB6A45B3E5C889C'),
	('hiddenj112','D7EBA233BA79416DBEA452CE3D492064'),
	('hiddenj112radio','FD233FEB96B742379F573CE56F64C992'),
	('hiddenj113','618DA0E95FF14F97B4D3642B5431C411'),
	('hiddenj113radio','315D315F28484EF297B3BEA3880949A0'),
	('hiddenj114','8A66B8312FD747088E3C89D32A34B5E3'),
	('hiddenj114radio','B63B134954224EF39E2BF5DDFE03E8F6'),
	('hiddenj115','83AF571133494D5FB21E18907A4A86D4'),
	('hiddenj115radio','CD4D8A900E4242F4A97EA44D73F3C201'),
	('hiddenj116','2C709673BC9343F7B6E56067D33B7855'),
	('hiddenj116radio','F534B5044AC7471989FA81CF63C878FE'),
	('hiddenj117','F2AE5ED126A64A928726AEF5B161FF34'),
	('hiddenj117radio','1B463C67E2EE4AAFAB2DE30696EB4FE6'),
	('hiddenj118','A4972EF707664BDD850D475BC5B009B8'),
	('hiddenj118radio','75E97DD53EF84AE69610EF5ECF85A254'),
	('hiddenj119','B4273CB4FEB54790AB91C8EBB7033767'),
	('hiddenj119radio','6B63AA4958C14DFC969CC31D63EFDB33'),
	('hiddenj120','A3193B2BFEE14F49ABB371ECAB00A705'),
	('hiddenj120radio','740E24A952AE44BDBDB554B2A20ACAE6'),
	('hiddenj121','F0B10583BBBB41A5907934B808472452'),
	('hiddenj121radio','ACDF935AECCD498D96167818E91F5BE4'),
	('hiddenj122','B633FA701520429EAAF42B32410AAAF6'),
	('hiddenj122radio','51CC541BE59C453BB402E0880CD34FA6'),
	('hiddenj123','7F129D3F920F4DD38B48992FDC543871'),
	('hiddenj123radio','B82A85BD3DC249828D275C69E8C8D30C'),
	('hiddenj124','AC98C6C829AC4788906758A99734984A'),
	('hiddenj124radio','CA77EB69BF924C92ACF0F79DE36EFA0B'),
	('hiddenj125','3167DB88125B40FC9E9F6417C51AD80E'),
	('hiddenj125radio','69A55E4290C14CD2B5508EE3C4FA9903'),
	('hiddenj126','8CD44478E7664D609D3E62235C0B906E'),
	('hiddenj126radio','3B74AE81576C48AAA021EF9D033B19A0'),
	('hiddenj127','8CA6C84944B74954AA16DFFF79F7E762'),
	('hiddenj127radio','DBAE800C9F3746B4A6F3E59B4BDB4954'),
	('hiddenj128','569782963F704A70ADDFD0CC906726F1'),
	('hiddenj128radio','F4B4B125F2F64F1C8BBA645C21CC8514'),
	('hiddenj129','C6A81CA7632643ABB5E27BF3EB36BA9E'),
	('hiddenj129radio','BC0F46E16CBC439F90AA661DCA4B62D3'),
	('hiddenj130','3D4C75B1C84B4DE696DAB0B0E07074DE'),
	('hiddenj130radio','D41284FDF37B4A339945C04F8F906A41'),
	('hiddenj131','1F1CC6BED987467AAD4D712BD44A442A'),
	('hiddenj131radio','97F1B3B814544A20A8C0F08A32BC8BE8'),
	('hiddenj132','8D7B38B846C24F41A8007BE1440B31D2'),
	('hiddenj132radio','9EFBBCAD81A943A6B5E18C988E866012'),
	('hiddenj133','18E3C1F0A3B5428892DF5764207CE3B2'),
	('hiddenj133radio','2D71F8A813DE4D4FB21F3DEF97B87BA7'),
	('hiddenj134','999E3C125E484E009144A64E1E944BBB'),
	('hiddenj134radio','1CF20459703E47FDBFCC445C5991BFEC'),
	('hiddenj135','650D8D3312B2426DB67325729BB481D3'),
	('hiddenj135radio','36572742B6DA4BBFA2AA00A0070AA151'),
	('hiddenj136','8D7D1EAC56EF4433AAB2524EF05804E2'),
	('hiddenj136radio','385741E1E2704378B61B6E3B66D645FB'),
	('hiddenj137','9A02062434D04AC49F95496C292CA66E'),
	('hiddenj137radio','33BEDD25B5454BB2BDDD5B223FEAEBEC'),
	('hiddenj138','A39D6EA16CB2461BBCF0753730B6BA01'),
	('hiddenj138radio','2CA59463868C4581B56332BD2C892B75'),
	('hiddenj139','8D84381AF8604B47921AC87094C44A61'),
	('hiddenj139radio','835024A8BD4744BBA20427816AE5DB69'),
	('hiddenj140','65B6B7DDFE324335A53C70F52A794298'),
	('hiddenj140radio','B833A80540C04F1BB30A55B66D13A749'),
	('hiddenj141','7CC0CE037AE94F1889218A4F4D5B80CD'),
	('hiddenj141radio','5C44B4BD90584C4D8FFCCFF7A75708EC'),
	('hiddenj142','5BEADA898E07426BA386A5E5A5E364BD'),
	('hiddenj142radio','5315064575EC4B86AA03A57DD6B6B7D1'),
	('hiddenj143','7936AF8171F5480CB9324316CB6A6CF4'),
	('hiddenj143radio','CB5DFF65D6904CEE919764DFEB153994'),
	('hiddenj144','EDEFBC94DB9946EF97F8958FA8EB394D'),
	('hiddenj144radio','5C723F7E39764146920436268BA71927'),
	('hiddenj145','6864A71DA7EE4C7C9AF561BEB91E0C09'),
	('hiddenj145radio','60AF9F9D24C04DD681540360730D66DF'),
	('hiddenj146','AA61966AF3FC4BA48CD90B82D23FFA45'),
	('hiddenj146radio','C768DBD9B47448DB846665CE9DA339DE'),
	('hiddenj147','5AD0F7F632AB472C9F7B441EF65A9BC9'),
	('hiddenj147radio','03C0367622D449A2BC2ABFE7A1371193'),
	('hiddenj148','72928C5D879A476281F506D30918B663'),
	('hiddenj148radio','DC7E9505E0F94301A998CD41EFBBFAA8'),
	('hiddenN11','829502B34D1E43E9A181CF5FA150392D'),
	('hiddenN11checkbox','948D25D23C414258A9E2D3471DBCF27F'),
	('hiddenN11checkbox','CDCEAF8C81FF4C6BB57C34FA1EB61F2D'),
	('hiddenN11checkbox','1EFA0AE0443C45C08820AF6D05646744'),
	('hiddenN11checkbox','A1F970982238410989344E972FE17E5F'),
	('hiddenN12','1C4FF67B504443A981DC8E4F498A9DA0'),
	('hiddenN12checkbox','7E2CBBE29FA1440CB5D99E2ABDF51A5E'),
	('hiddenN12checkbox','58E7C0F3000343F4845355E59060E80C'),
	('hiddenN13','090FF9143E8C44C0A05863E4FFF6CBDD'),
	('hiddenN13checkbox','BA33A3289A7A401DB5D43B95FAFFCBF1'),
	('hiddenN13checkbox','BE1AB5EC2CE043888514A7A2DD86A495'),
	('hiddenN13checkbox','940623FD80444F0BA88B44CC3985F955'),
	('hiddenN14','DF4C0E0322074AEFA299550100B9570B'),
	('hiddenN14checkbox','A64E1BA212494057AAB2D4AF59667D6F'),
	('hiddenN14checkbox','CAD64AD8C686455A9DF0285268C8A788'),
	('hiddenN14checkbox','D1C8E0A21EF64301B4BD3D69C8FA5ED5'),
	('hiddenN15','3494BF98A0224BA2805BD3EE73A1F781'),
	('hiddenN15checkbox','896BF93715724175A0DE444CDE3D9489'),
	('hiddenN15checkbox','C914AD643B71449392B773F3A06DFEEE'),
	('hiddenN15checkbox','4E8CEC12AB9842319F628E76BD18E83E'),
	('hiddenN15checkbox','731DBD4520CE469CBB36B4095FDA2199'),
	('hiddenN16','06904338938042C0B2CE16C1CF5DA113'),
	('hiddenN16checkbox','B76FB024054B43F78CF4B4C96CD19BD6'),
	('hiddenN16checkbox','8CC2A7CC11E14A0D911CCADE7702D4EA'),
	('hiddenT11','80C4D853A30340CA8F14E7080D5CB904'),
	('T11',solution),
	('stlx1stlb1j','48'),
	('stlx1stlb2L','0'),
	('stlx2stlb1N','6'),
	('stlx2stlb2R','0'),
	('stlx3stlb1T','1'),
	('erzbIdx','55'),
	]
	headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Connection': 'keep-alive',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
	}
	data = urllib.parse.urlencode(postData).encode(encoding="UTF-8")
	request = urllib.request.Request(PostUrl,data,headers)
	try:
		response = opener.open(request)
	except urllib.request.HTTPError as e:
		return False
	return True

def clearent1():
	ent1.delete(0,END)

def clearent2():
	ent2.delete(0,END)

def clearent3():
	ent3.delete(0,END)

if __name__ == '__main__':
	mainGui=Tk()
	mainGui.title("Login")
	mainGui.geometry('400x300+500+200')
	mainGui.iconbitmap('ico\\图标.ico')
	cvFrame = Frame(mainGui)
	cv = Canvas(cvFrame,bg='#626669',width=400,height=155)
	cv.create_polygon((0,0,0,155,155,155),fill='#78797a')
	cv.create_polygon((0,0,155,0,77.5,77.5),fill='#909090')
	cv.create_polygon((400,40,400,155,285,155),fill='#4e545a')
	cv.create_text((170,77.5),text="Getit",anchor=W,font = "time 25 bold",fill='white')
	cv.pack()
	# 小图标.png
	ico = Image.open('ico\\小图标.png')
	ico_open=ImageTk.PhotoImage(ico)
	label = Label(cvFrame,image=ico_open,width=45,height=45,bg='#626669')
	label.image=ico_open
	cv.create_window((115,75),window = label,anchor=W)
	cvFrame.pack()
	lab1=Label(mainGui,text="账号:")
	ent1=Entry(mainGui)
	lab2=Label(mainGui,text="密码:")
	ent2=Entry(mainGui,show="*")
	lab4=Label(mainGui,text="验证码:")
	ent3=Entry(mainGui,width=8)
	b1=Button(mainGui,text="登陆",command=lambda : start(ent1.get(),ent2.get(),ent3.get()),width=15,bg='#a4a3a3')
	def login(event):
		start(ent1.get(),ent2.get(),ent3.get())
	mainGui.bind('<Return>',login)
	download()
	ent1.place(x=140,y=171)
	ent2.place(x=140,y=201)
	ent3.place(x=140,y=231)
	lab1.place(x=105,y=170)
	lab2.place(x=105,y=200)
	lab4.place(x=95,y=230)
	b1.place(x=140,y=260)
	mainGui.resizable(0, 0)
	mainGui.mainloop()