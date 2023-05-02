import tkinter as tk
import threading
from time import sleep
import tkinter.filedialog
from PIL import Image,ImageTk
import random
import socket
from threading import Thread
from server import run_server
import subprocess


event = threading.Event()
class GUI:

    def __init__(self,id):

        self.ipv4s = socket.gethostbyname_ex(socket.gethostname())[2]
        self.rule_page = 0
        self.id = id
        self.root = tk.Tk()
        self.root.title('败喜胜欣心醉矣             忘忧清乐久棋中           用户名：'+str(id)+'      ip:'+str(self.ipv4s[2]))
        self.root.geometry("1200x800+200+120")
        self.interface()


    def interface(self):
        """"界面编写位置"""
        self.Button_rule = tk.Button(self.root, text="规则介绍", command=self.rule_start,font=('华文仿宋', 14, "bold"))
        self.Button_rule.place(x=50, y=120, width=100, height=80)

        self.Button1 = tk.Button(self.root, text="人机对弈", command=self.rule_start,font=('华文仿宋', 14, "bold"))
        self.Button1.place(x=50, y=240, width=100, height=80)

        self.Button2 = tk.Button(self.root, text="本地双人", command=self.TWO_PLAYER,font=('华文仿宋', 14, "bold"))
        self.Button2.place(x=50, y=360, width=100, height=80)

        self.Button3 = tk.Button(self.root, text="在线对战", command=self.rule_start,font=('华文仿宋', 14, "bold"))
        self.Button3.place(x=50, y=480, width=100, height=80)

        self.Button4 = tk.Button(self.root, text="对局回溯", command=self.rule_start,font=('华文仿宋', 14, "bold"))
        self.Button4.place(x=50, y=600, width=100, height=80)

        self.Button5 = tk.Button(self.root, text="棋子与音乐", command=self.change_start, font=('华文仿宋', 14, "bold"))
        self.Button5.place(x=40, y=720, width=120, height=50)

        self.main_title = tk.Label(self.root, text="藏族“久”棋 对战平台",font=('华文新魏', 36, "bold"))
        self.main_title.place(x=400, y=20)

        random.seed()
        mainpic_num = random.randint(1,6)
        path = 'main_pic/' + str(mainpic_num) + '.png'
        print(path)
        img_open = Image.open(path)
        img = ImageTk.PhotoImage(img_open.resize((1000, 800)))
        self.mainpic = tk.Label(self.root, width=1000, height=800)
        self.mainpic.place(x=200, y=80)
        self.mainpic.config(image=img)
        self.mainpic.image = img

    def TWO_PLAYER(self):
        process1 = subprocess.Popen(['python', 'server_local.py'])
        process2 = subprocess.Popen(['python', 'player_local1.py'])
        process3 = subprocess.Popen(['python', 'player_local2.py'])

    def change_start(self):


        self.mainpic.destroy()
        self.main_title.destroy()

        path1 = r'C:\Users\chiya\PycharmProjects\qjh\chess\material\blackChess.png'
        img_open1 = Image.open(path1)
        img1 = ImageTk.PhotoImage(img_open1.resize((70,70)))

        path2 = r'C:\Users\chiya\PycharmProjects\qjh\chess\material\whiteChess.png'
        img_open2 = Image.open(path2)
        img2 = ImageTk.PhotoImage(img_open2.resize((70, 70)))

        path3 = r'C:\Users\chiya\PycharmProjects\qjh\chess\material\1.jpg'
        img_open3 = Image.open(path3)
        img3 = ImageTk.PhotoImage(img_open3.resize((300, 300)))

        # self.label_img.winfo_exists()
        try :
            self.label_img.destroy()
            self.Button_rule_last.destroy()


            self.label_img = tk.Label()
            self.label_img.place(x=500, y=150)
            self.label_img.config(image=img1)
            self.label_img.image = img1

            self.Button_rule_last = tk.Button(self.root, text="切换黑子皮肤", command=self.rule_last,font=('SimHei', 15, "bold"))
            self.Button_rule_last.place(x=470, y=240, width=150, height=40)


        except:
            self.label_img = tk.Label()
            self.label_img.place(x=500, y=150)
            self.label_img.config(image=img1)
            self.label_img.image = img1

            self.Button11 = tk.Button(self.root, text="切换黑子皮肤", command=self.rule_last,font=('SimHei', 15, "bold"))
            self.Button11.place(x=470, y=240, width=150, height=40)

            self.label_img2 = tk.Label()
            self.label_img2.place(x=500, y=400)
            self.label_img2.config(image=img2)
            self.label_img2.image = img2

            self.Button22 = tk.Button(self.root, text="切换白子皮肤", command=self.rule_last,
                                              font=('SimHei', 15, "bold"))
            self.Button22.place(x=470, y=490, width=150, height=40)

            self.label_img3 = tk.Label()
            self.label_img3.place(x=750, y=150)
            self.label_img3.config(image=img3)
            self.label_img3.image = img3

            self.Button33 = tk.Button(self.root, text="切换棋盘皮肤", command=self.rule_last,
                                              font=('SimHei', 15, "bold"))
            self.Button33.place(x=820, y=490, width=150, height=40)

            self.Button44 = tk.Button(self.root, text="退出", command=self.rule_quit11, font=('SimHei', 15, "bold"))
            self.Button44.place(x=1005, y=740, width=70, height=40)

    def rule_quit11(self):
        self.label_img.destroy()
        self.label_img2.destroy()
        self.label_img3.destroy()
        self.Button11.destroy()
        self.Button22.destroy()
        self.Button33.destroy()
        self.Button44.destroy()


        self.main_title = tk.Label(self.root, text="藏族“久”棋 对战平台", font=('华文新魏', 36, "bold"))
        self.main_title.place(x=400, y=20)


        random.seed()
        mainpic_num = random.randint(1,6)
        path = 'main_pic/' + str(mainpic_num) + '.png'
        img_open = Image.open(path)
        img = ImageTk.PhotoImage(img_open.resize((1000, 800)))
        self.mainpic = tk.Label(self.root, width=1000, height=800)
        self.mainpic.place(x=200, y=80)
        self.mainpic.config(image=img)
        self.mainpic.image = img



    def rule_start(self):


        self.mainpic.destroy()
        self.main_title.destroy()

        path = 'rule/'+str(self.rule_page)+'.png'
        img_open = Image.open(path)
        img = ImageTk.PhotoImage(img_open.resize((700,700)))

        # self.label_img.winfo_exists()
        try :
            self.label_img.destroy()
            self.Button_rule_last.destroy()
            self.Button_rule_quit.destroy()
            self.Button_rule_next.destroy()
            self.Button_rule_fast_change1.destroy()
            self.Button_rule_fast_change2.destroy()
            self.Button_rule_fast_change3.destroy()
            self.Button_rule_fast_change4.destroy()
            self.Button_rule_fast_change5.destroy()
            self.Button_rule_fast_change6.destroy()
            self.Button_rule_fast_change7.destroy()

            self.label_img = tk.Label()
            self.label_img.place(x=460, y=25)
            self.label_img.config(image=img)
            self.label_img.image = img

            self.Button_rule_last = tk.Button(self.root, text="上一页", command=self.rule_last,font=('SimHei', 15, "bold"))
            self.Button_rule_last.place(x=450, y=740, width=90, height=40)

            self.Button_rule_fast_change1 = tk.Button(self.root, text="棋具", command=lambda: self.rule_fast_change(1),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change1.place(x=545, y=740, width=60, height=40)

            self.Button_rule_fast_change2 = tk.Button(self.root, text="久棋下法", command=lambda: self.rule_fast_change(2),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change2.place(x=610, y=740, width=60, height=40)

            self.Button_rule_fast_change3 = tk.Button(self.root, text="行棋规则", command=lambda: self.rule_fast_change(3),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change3.place(x=675, y=740, width=60, height=40)

            self.Button_rule_fast_change4 = tk.Button(self.root, text="胜负", command=lambda: self.rule_fast_change(15),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change4.place(x=740, y=740, width=60, height=40)

            self.Button_rule_fast_change5 = tk.Button(self.root, text="纪律", command=lambda: self.rule_fast_change(18),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change5.place(x=805, y=740, width=60, height=40)

            self.Button_rule_fast_change6 = tk.Button(self.root, text="权利与义务",command=lambda: self.rule_fast_change(19),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change6.place(x=870, y=740, width=65, height=40)

            self.Button_rule_fast_change7 = tk.Button(self.root, text="裁判法", command=lambda: self.rule_fast_change(20),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change7.place(x=940, y=740, width=60, height=40)

            self.Button_rule_quit = tk.Button(self.root, text="退出", command=self.rule_quit,font=('SimHei', 15, "bold"))
            self.Button_rule_quit.place(x=1005, y=740, width=70, height=40)

            self.Button_rule_next = tk.Button(self.root, text="下一页", command=self.rule_next,font=('SimHei', 15, "bold"))
            self.Button_rule_next.place(x=1080, y=740, width=90, height=40)
        except:
            self.label_img = tk.Label()
            self.label_img.place(x=460, y=25)
            self.label_img.config(image=img)
            self.label_img.image = img

            self.Button_rule_last = tk.Button(self.root, text="上一页", command=self.rule_last,font=('SimHei', 15, "bold"))
            self.Button_rule_last.place(x=450, y=740, width=90, height=40)

            self.Button_rule_fast_change1 = tk.Button(self.root, text="棋具", command=lambda :self.rule_fast_change(1),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change1.place(x=545, y=740, width=60, height=40)

            self.Button_rule_fast_change2 = tk.Button(self.root, text="久棋下法", command=lambda :self.rule_fast_change(2),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change2.place(x=610, y=740, width=60, height=40)

            self.Button_rule_fast_change3 = tk.Button(self.root, text="行棋规则", command=lambda :self.rule_fast_change(3),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change3.place(x=675, y=740, width=60, height=40)

            self.Button_rule_fast_change4 = tk.Button(self.root, text="胜负", command=lambda :self.rule_fast_change(15),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change4.place(x=740, y=740, width=60, height=40)

            self.Button_rule_fast_change5 = tk.Button(self.root, text="纪律", command=lambda :self.rule_fast_change(18),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change5.place(x=805, y=740, width=60, height=40)

            self.Button_rule_fast_change6 = tk.Button(self.root, text="权利与义务", command=lambda :self.rule_fast_change(19),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change6.place(x=870, y=740, width=65, height=40)

            self.Button_rule_fast_change7 = tk.Button(self.root, text="裁判法", command=lambda :self.rule_fast_change(20),font=('SimHei', 9, "bold"))
            self.Button_rule_fast_change7.place(x=940, y=740, width=60, height=40)

            self.Button_rule_quit = tk.Button(self.root, text="退出", command=self.rule_quit,font=('SimHei', 15, "bold"))
            self.Button_rule_quit.place(x=1005, y=740, width=70, height=40)

            self.Button_rule_next = tk.Button(self.root, text="下一页", command=self.rule_next,font=('SimHei', 15, "bold"))
            self.Button_rule_next.place(x=1080, y=740, width=90, height=40)

    def rule_fast_change(self,i):
        self.rule_page = i
        path = 'rule/' + str(self.rule_page) + '.png'
        img_open = Image.open(path)
        img = ImageTk.PhotoImage(img_open.resize((700, 700)))
        self.label_img.config(image=img)
        self.label_img.image = img

    def rule_next(self):
        self.rule_page += 1
        path = 'rule/' + str(self.rule_page) + '.png'
        try:
            img_open = Image.open(path)
            img = ImageTk.PhotoImage(img_open.resize((700, 700)))
            self.label_img.config(image=img)
            self.label_img.image = img
        except:
            self.rule_page -= 1
            print('超页')

    def rule_last(self):
        self.rule_page -= 1
        path = 'rule/' + str(self.rule_page) + '.png'
        try:
            img_open = Image.open(path)
            img = ImageTk.PhotoImage(img_open.resize((700, 700)))
            self.label_img.config(image=img)
            self.label_img.image = img
        except:
            self.rule_page += 1
            print('超页')

    def rule_quit(self):
        self.rule_page = 0
        self.Button_rule_last.destroy()
        self.Button_rule_quit.destroy()
        self.Button_rule_next.destroy()
        self.Button_rule_fast_change1.destroy()
        self.Button_rule_fast_change2.destroy()
        self.Button_rule_fast_change3.destroy()
        self.Button_rule_fast_change4.destroy()
        self.Button_rule_fast_change5.destroy()
        self.Button_rule_fast_change6.destroy()
        self.Button_rule_fast_change7.destroy()
        self.label_img.destroy()

        self.main_title = tk.Label(self.root, text="藏族“久”棋 对战平台", font=('华文新魏', 36, "bold"))
        self.main_title.place(x=400, y=20)


        random.seed()
        mainpic_num = random.randint(1,6)
        path = 'main_pic/' + str(mainpic_num) + '.png'
        img_open = Image.open(path)
        img = ImageTk.PhotoImage(img_open.resize((1000, 800)))
        self.mainpic = tk.Label(self.root, width=1000, height=800)
        self.mainpic.place(x=200, y=80)
        self.mainpic.config(image=img)
        self.mainpic.image = img



if __name__ == '__main__':
    a = GUI('chiya')
    a.root.mainloop()

