import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from GUI import GUI


import tkinter as tk
import sqlite3
from GUI import GUI

class LoginAndRegister(tk.Tk):
    def __init__(self, db_file):
        super().__init__()

        # 设置窗口标题和大小
        self.title('用户登录')
        self.geometry('300x200+500+240')

        # 连接数据库
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # 创建用户表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # 创建用户名和密码输入框
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # 创建登陆和注册按钮
        self.login_btn = tk.Button(self, text='Login', command=self.login)
        self.register_btn = tk.Button(self, text='Register', command=self.register)



        # 设置布局
        tk.Label(self, text='Username:').place(x=10, y=10)
        tk.Entry(self, textvariable=self.username_var).place(x=80, y=10, width=150, height=20)
        tk.Label(self, text='Password:').place(x=10, y=40)
        tk.Entry(self, textvariable=self.password_var, show='*').place(x=80, y=40, width=150, height=20)
        self.login_btn.place(x=15, y=80)
        self.register_btn.place(x=80, y=80)



        # 显示窗口
        self.mainloop()

    def login(self):
        # 从数据库中获取用户名和密码
        username = self.username_var.get()
        password = self.password_var.get()
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()

        # 如果找到匹配的用户，则登陆成功并打开另一个窗口
        if user:
            self.destroy()
            app = GUI(username)
        else:
            # 登陆失败，弹出提示框
            tk.messagebox.showerror('Error', 'Incorrect username or password')

    def register(self):
        # 获取用户名和密码
        username = self.username_var.get()
        password = self.password_var.get()

        try:
            # 将用户名和密码插入数据库中
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            tk.messagebox.showinfo('Success', 'Registration successful')
        except sqlite3.IntegrityError:
            # 如果用户名已经存在，则注册失败，弹出提示框
            tk.messagebox.showerror('Error', 'Username already exists')



if __name__ == '__main__':
    db_file = r'data\users.db'
    app = LoginAndRegister(db_file)
    #
    #     # 加载背景图片
    #     self.bg_image = Image.open(r"data\1.png")
    #     self.bg_image = ImageTk.PhotoImage(self.bg_image)
    #     self.bg_canvas = tk.Canvas(self, width=300, height=200)
    #     self.bg_canvas.pack(fill="both", expand=True)
    #
    #     # 在Canvas上显示背景图片
    #     self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
    #
    #     # 创建自定义透明样式
    #     style = ttk.Style()
    #     style.configure("TransparentEntry.TEntry", background="SystemButtonFace")
    #
    #     # 设置布局
    #     self.bg_canvas.create_window(60, 10, window=tk.Label(self, text='Username:'))
    #     self.bg_canvas.create_window(155, 10, window=ttk.Entry(self, textvariable=self.username_var, width=20, style='TransparentEntry.TEntry'))
    #     self.bg_canvas.create_window(60, 40, window=tk.Label(self, text='Password:'))
    #     self.bg_canvas.create_window(155, 40, window=ttk.Entry(self, textvariable=self.password_var, show='*', width=20, style='TransparentEntry.TEntry'))
    #     self.bg_canvas.create_window(45, 80, window=self.login_btn)
    #     self.bg_canvas.create_window(135, 80, window=self.register_btn)
    #
    #     # 监听窗口大小变化事件
    #     self.bind("<Configure>", self.on_resize)
    #
    #     # 显示窗口
    #     self.mainloop()
    #
    # def on_resize(self, event):
    #     # 加载背景图片
    #     image = Image.open("data\\1.png")
    #
    #     # 调整图片大小以匹配窗口大小
    #     resized_image = image.resize((event.width, event.height), Image.ANTIALIAS)
    #     self.bg_image = ImageTk.PhotoImage(resized_image)
    #
    #     # 在Canvas上显示背景图片
    #     self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
    #     self.bg_canvas.create_window(45, 80, window=self.login_btn)
    #     self.bg_canvas.create_window(135, 80, window=self.register_btn)
    #
    #

