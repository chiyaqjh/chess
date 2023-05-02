from tkinter import *
import tkinter.messagebox  # 弹窗库
import numpy as np

root = Tk()                       #创建窗口
root.title("棋")                  #窗口名字
w1 = Canvas(root, width=600,height=600,background='lightcyan')
w1.pack()



#button = tkinter.Button(w1, text='回合结束', bg='#7CCD7C', width=20, height=5, command=switch_button).pack()


for i in range(0, 14):
    w1.create_line(i * 40 + 20, 20, i * 40 + 20, 540)
    w1.create_line(20, i * 40 + 20, 540, i * 40 + 20)

num=0
A=np.full((14,14),0)
#B=np.full((14,14),'')
#B=np.full((14,14),0)
loc=[1,0,0]
def callback(event):
    global num ,A
    if num<30:
        for j in range (0,14):
            for i in range (0,14):
                if (event.y - 20 - 40 * i) ** 2 + (event.x - 20 - 40 * j) ** 2 <= 2 * 20 ** 2:
                    break
            if (event.y - 20 - 40 * i) ** 2 + (event.x - 20 - 40 * j) ** 2 <= 2*20 ** 2:
                break
        if num % 2 == 0 and A[i][j] == 0:
            globals()['x'+str(i)+"_"+str(j)]=w1.create_oval(40*j+5, 40*i+5, 40*j+35, 40*i+35,fill='black')
            A[i][j] = 1
            num += 1
        if num % 2 != 0 and A[i][j] == 0 :
            globals()['x'+str(i)+"_"+str(j)]=w1.create_oval(40*j+5, 40*i+5, 40*j+35, 40*i+35,fill='white')
            A[i][j] = 2
            num += 1
    else:
        if loc[0]==1:
            for j in range (0,14):
                for i in range (0,14):
                    if (event.y - 20 - 40 * i) ** 2 + (event.x - 20 - 40 * j) ** 2 <= 2 * 20 ** 2:
                        break
                if (event.y - 20 - 40 * i) ** 2 + (event.x - 20 - 40 * j) ** 2 <= 2*20 ** 2:
                    break
            loc[0]=2
            loc[1]=i
            loc[2]=j
            #w1.delete(globals()['x'+str(i)+"_"+str(j)])
        elif loc[1]==2:
            for j in range (0,14):
                for i in range (0,14):
                    if (event.y - 20 - 40 * i) ** 2 + (event.x - 20 - 40 * j) ** 2 <= 2 * 20 ** 2:
                        break
                if (event.y - 20 - 40 * i) ** 2 + (event.x - 20 - 40 * j) ** 2 <= 2*20 ** 2:
                    break

    print(A)



w1.bind("<Button -1>",callback)
w1.pack()

def quit():
    root.quit()

u=Button(root,text="退出",width=10,height=1,command=quit,font=('楷体',14))
u.pack()

def switch_hanshu(switch):
    if switch[0]=='b':
      switch[0]='w'
    elif switch[0]=='w':
      switch[0]='b'
    print(switch[0])
switch = ['b']
#print(list1[0])
#flag=1
#flag=switch_hanshu(flag)
B = Button(root, text="回合结束", command=lambda : switch_hanshu(switch))
B.pack()
#sw=Button(root, text='回合结束', bg='#7CCD7C', width=20, height=5, command=switch_button(flag))
mainloop()