#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import bs4
from tkinter import *
from tkinter.filedialog import askdirectory
import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time
import threading  # 设置多线程,防止界面卡死,重要

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self):
        super().__init__()
        self.createUI()

    def createUI(self):
        self.time_sleep = 0.05
        self.window = tk.Tk()  # 创建window窗口
        self.window.title("中国地质大学(武汉) 罗大鹏图像视频课题组")  # 定义窗口名称
        # self.window.resizable(0,0)  # 禁止调整窗口大小
        self.menu = ttk.Combobox(self.window, width=10)
        self.path = StringVar()
        self.lab1 = tk.Label(self.window, text="目标路径:")
        self.lab2 = tk.Label(self.window, text="选择分类:")
        self.lab3 = tk.Label(self.window, text="爬取页数:")
        #self.page = tk.Entry(self.window, width=5)
        self.num_pages = tk.Entry(self.window, width=4)
        self.input = tk.Entry(self.window, textvariable=self.path, width=70)  # 创建一个输入框,显示图片存放路径
        self.info = tk.Text(self.window, height=20)  # 创建一个文本展示框，并设置尺寸
        self.menu['value'] = ('统一冰红茶', '统一绿茶', '脉动', '农夫山泉', '加多宝', '百事可乐')
        self.menu.current(0)
        # 添加一个按钮，用于选择图片保存路径
        self.t_button = tk.Button(self.window, text='图片保存路径', relief=tk.RAISED, width=10, height=1, command=self.select_Path)
        # 添加一个按钮，用于触发爬取功能
        self.t_button1 = tk.Button(self.window, text='开始爬取', relief=tk.RAISED, width=8, height=1, command=lambda: self.thread_it(self.get_menu,))
        # 添加一个按钮，用于触发清空输出框功能
        self.c_button2 = tk.Button(self.window, text='清空输出', relief=tk.RAISED, width=8, height=1, command=self.cle)
        self.s_button3 = tk.Button(self.window, text='退出程序', relief=tk.RAISED, width=8, height=1, command=self.window.quit)
    #def gui_arrange(self):
        """完成页面元素布局，设置各部件的位置"""
        self.lab1.grid(row=0,column=0)
        self.lab2.grid(row=1, column=0)
        self.menu.grid(row=1, column=1,sticky=W)
        self.lab3.grid(row=2, column=0,padx=5,pady=5,sticky=tk.W)
        self.num_pages.grid(row=2, column=1,sticky=W)
        self.input.grid(row=0,column=1)
        self.info.grid(row=3,rowspan=5,column=0,columnspan=3,padx=15,pady=15)
        self.t_button.grid(row=0,column=2,padx=5,pady=5,sticky=tk.W)
        self.t_button1.grid(row=1,column=2)
        self.c_button2.grid(row=0,column=3,padx=5,pady=5,sticky=tk.W)
        self.s_button3.grid(row =1, column=3)

    def select_Path(self):
        """选取本地路径"""
        path_ = askdirectory()
        self.path.set(path_)

    # 获取后缀名
    def get_suffix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取referrer，用于生成referrer
    def get_referrer(self, url):
        par = urllib.parse.urlparse(url)
        if par.scheme: #https
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

        # 保存图片
    def save_image(self, rsp_data, word):
        #这里需要修改
        #TODO
        root_dir = self.input.get()
        case_list = ['统一冰红茶', '统一绿茶', '脉动', '农夫山泉', '加多宝', '百事可乐']
        for t in case_list:
            if not os.path.exists(root_dir + '/images'):
                os.makedirs(root_dir + '/images')
            if not os.path.exists(root_dir + '/images/' + str(t)):
                os.makedirs(root_dir + '/images/' + str(t))

        if not os.path.exists(root_dir+ '/images/' + word):
            os.mkdir(root_dir + '/images/' + word)

        #if not os.path.exists(root_dir): #是否存在返回的是Boolean值,true或者false
            #os.mkdir(root_dir)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir(root_dir + '/images/' + word)) + 1
        for image_info in rsp_data['imgs']:

            try:
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(image_info['objURL'])
                # 指定UA和referrer，减少403
                refer = self.get_referrer(image_info['objURL'])
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', refer)
                ]
                urllib.request.install_opener(opener)
                # 保存图片
                #urllib.request.urlretrieve()函数作用是将远程数据下载到本地
                #参数urlretrieve(url, filename=None, reporthook=None, data=None)
                #url: 下载链接地址
                #filename: 指定了本地保存路径
                urllib.request.urlretrieve(image_info['objURL'], root_dir + '/images/'+word + '/' + str(self.__counter) + str(suffix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                #print("正在下载", url)
                #self.info.insert('end', "正在下载第:" +str(self.__counter) +"张图片"+ '\n')
                self.info.insert(END, "正在下载第: " + str(self.__counter) + "张图片" + '\n')
                #INSERT索引表示在光标处插入
                #END索引表示在最后插入
                print("图片数目+1,已经爬取" + str(self.__counter) + "张图")  # 控制台输出
                self.__counter += 1
        return

    # 开始获取
    def get_images(self, word='待爬取图片'):

        search = urllib.parse.quote(word)  # 这里search已经为str类型
        # pn int 图片数
        pn = self.__start_amount  # start_amount为整数类型
        while pn < self.__amount:

            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read().decode('unicode_escape')  #反向解码为字符
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else: #python中try except如果没有异常发生,会执行else语句
                # 解析json
                rsp_data = json.loads(rsp)
                self.save_image(rsp_data, word)
                # 读取下一页
                print("下载下一页")
                pn += 60
            finally: #finally是程序发不发生异常都会执行
                page.close()
        print("下载任务结束")
        return

    def start(self, word, spider_page_num=1, start_page=1):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """

        self.__start_amount = (start_page - 1) * 60
        spider_page_num = self.num_pages.get()  #这里返回的是字符类型,需要转换为整型
        spider_page_num = int(spider_page_num)
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.get_images(word)

    def cle(self):
        """定义一个函数，用于清空输出框的内容"""
        self.info.delete(1.0, "end")  # 从第一行清除到最后一行

    def stoprunning(self):
        pass

    def get_menu(self):
        word = self.menu.get()
        self.start(word)
        #self.get_images(word)

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

if __name__ == '__main__':
    crawler = Crawler()  # 抓取延迟为 0.05
    #crawler.gui_arrange()
    tk.mainloop()

