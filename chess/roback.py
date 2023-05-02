import tkinter as tk
import tkinter.messagebox  # 弹窗库
import numpy as np
import os
import json



class chess_roback:

    def __init__(self):
        self.root = tk.Tk()  # 创建窗口
        self.root.title("棋局回溯")  # 窗口名字
        self.root.geometry("700x700+200+120")
        self.record = []
        self.record_entey()
        self.interface()
        self.page = 0



    def record_entey(self):
        f4 = open("11.txt", encoding='utf-8')
        contents2 = f4.readline()
        i = 0
        record1 = []
        list_old = []
        # 利用循环全部读出
        while contents2:
            list = json.loads(contents2)
            if list != list_old:
                record1.append(list)
            list_old = list
            contents2 = f4.readline()
            i = i + 1
        f4.close()

        self.record = record1

    def interface(self):
        self.chessrecord_now = tk.Canvas(self.root, width=560, height=560, background='lightcyan')
        self.chessrecord_now.place(x=0, y=0)

        self.Button_last = tk.Button(self.root, text="上一页", command=self.last_record)
        self.Button_last.place(x=0, y=560, width=90, height=40)

        self.Button_next = tk.Button(self.root, text="下一页",command=self.next_record)
        self.Button_next.place(x=100, y=560, width=90, height=40)

        self.Button_ai = tk.Button(self.root, text="Ai预测", command=self.aihelp)
        self.Button_ai.place(x=200, y=560, width=90, height=40)

        self.chess_text = tk.Text(self.root,font=('华文新魏', 15))
        self.chess_text.place(x=560, y=0, width=140, height=560)
        self.chess_text.insert('1.0','棋局分析\n')
        self.chess_text.insert('2.0', '')


        self.chessrecord_now_refresh()
        self.callback(self.record[0])

    def chessrecord_now_refresh(self):
        for i in range(0, 14):
            self.chessrecord_now.create_line(i * 40 + 20, 20, i * 40 + 20, 540)
            self.chessrecord_now.create_line(20, i * 40 + 20, 540, i * 40 + 20)

    def aihelp(self):
        record_now = self.record[self.page]
        str1 = self.chess_text.get('3.0')
        str2 = self.chess_text.get('5.0')
        if str2 != '吃':
            list = []
            for i in range(0,14):
                for j in range(0,14):
                    if record_now[i][j] == 0:
                        if len(list) == 0:
                            print(1)
                            list.append([i,j])
                        elif abs(list[0][0] - 6.5)>abs(i-6.5) and abs(list[0][1] - 6.5)>abs(j-6.5):
                            print(2)
                            list = []
                            list.append([i,j])
                        elif abs(list[0][0] - 6.5)==abs(i-6.5) and abs(list[0][1] - 6.5)==abs(j-6.5):
                            print(3)
                            list.append([i,j])
            str3 = ''
            for item in list:
                str3 =str3+ chr(item[0] + 65) + str(item[1] + 1)+','

            self.chess_text.insert('6.0', '\n下一步推荐：'+str3)
        
        else:
            list = []
            if str1 == '白':
                for i in range(0,14):
                    for j in range(0,14):
                        if record_now[i][j]==1:
                            print(i,j)
                            choice = []
                            if i + 1 < 14 and record_now[i + 1][j] == 0:
                                choice.append([i + 1, j,1])
                            if i + 2 < 14 and record_now[i + 1][j] == 2 and record_now[i + 2][j] == 0:
                                choice.append([i + 2, j,11])
                                if i + 4 < 14 and record_now[i + 3][j] == 2 and record_now[i + 4][j] == 0:
                                    choice.append([i + 4, j,21])
                                    if i + 6 < 14 and record_now[i + 5][j] == 2 and record_now[i + 6][j] == 0:
                                        choice.append([i + 6, j,31])
                                        if i + 8 < 14 and record_now[i + 7][j] == 2 and record_now[i + 8][j] == 0:
                                            choice.append([i + 8, j,41])
                                            if i + 10 < 14 and record_now[i + 9][j] == 2 and record_now[i + 10][j] == 0:
                                                choice.append([i + 10, j,51])
                                                if i + 12 < 14 and record_now[i + 11][j] == 2 and record_now[i + 12][j] == 0:
                                                    choice.append([i + 12, j,61])

                            if i - 1 > -1 and record_now[i - 1][j] == 0:
                                choice.append([i - 1, j,1])
                            if i - 2 > -1 and record_now[i - 1][j] == 2 and record_now[i - 2][j] == 0:
                                choice.append([i - 2, j,11])
                                if i - 4 > -1 and record_now[i - 3][j] == 2 and record_now[i - 4][j] == 0:
                                    choice.append([i - 4, j,21])
                                    if i - 6 > -1 and record_now[i - 5][j] == 2 and record_now[i - 6][j] == 0:
                                        choice.append([i - 6, j,31])
                                        if i - 8 > -1 and record_now[i - 7][j] == 2 and record_now[i - 8][j] == 0:
                                            choice.append([i - 8, j,41])
                                            if i - 10 > -1 and record_now[i - 9][j] == 2 and record_now[i - 10][j] == 0:
                                                choice.append([i - 10, j,51])
                                                if i - 12 > -1 and record_now[i - 11][j] == 2 and record_now[i - 12][j] == 0:
                                                    choice.append([i - 12, j,61])

                            if j + 1 < 14 and record_now[i][j + 1] == 0:
                                choice.append([i, j + 1,1])
                            if j + 2 < 14 and record_now[i][j + 1] == 2 and record_now[i][j + 2] == 0:
                                choice.append([i, j + 2,11])
                                if j + 4 < 14 and record_now[i][j + 3] == 2 and record_now[i][j + 4] == 0:
                                    choice.append([i, j + 4,21])
                                    if j + 6 < 14 and record_now[i][j + 5] == 2 and record_now[i][j + 6] == 0:
                                        choice.append([i, j + 6,31])
                                        if j + 8 < 14 and record_now[i][j + 7] == 2 and record_now[i][j + 8] == 0:
                                            choice.append([i, j + 8,41])
                                            if j + 10 < 14 and record_now[i][j + 9] == 2 and record_now[i][j + 10] == 0:
                                                choice.append([i, j + 10,51])
                                                if j + 12 < 14 and record_now[i][j + 11] == 2 and record_now[i][j + 12] == 0:
                                                    choice.append([i, j + 12,61])

                            if j - 1 > -1 and record_now[i][j - 1] == 0:
                                choice.append([i, j - 1,1])
                            if j - 2 > -1 and record_now[i][j - 1] == 2 and record_now[i][j - 2] == 0:
                                choice.append([i, j - 2,11])
                                if j - 4 > -1 and record_now[i][j - 3] == 2 and record_now[i][j - 4] == 0:
                                    choice.append([i, j - 4,21])
                                    if j - 6 > -1 and record_now[i][j - 5] == 2 and record_now[i][j - 6] == 0:
                                        choice.append([i, j - 6,31])
                                        if j - 8 > -1 and record_now[i][j - 7] == 2 and record_now[i][j - 8] == 0:
                                            choice.append([i, j - 8,41])
                                            if j - 10 > -1 and record_now[i][j - 9] == 2 and record_now[i][j - 10] == 0:
                                                choice.append([i, j - 10,51])
                                                if j - 12 > -1 and record_now[i][j - 11] == 2 and record_now[i][j - 12] == 0:
                                                    choice.append([i, j - 12,61])

                            for item in choice:
                                try:
                                    I = item[0]
                                    J = item[1]
                                    if (record_now[I - 1][J - 1] == 1 and record_now[I - 1][J] == 1 and record_now[I][J - 1] == 1) or (
                                        record_now[I - 1][J + 1] == 1 and record_now[I - 1][J] == 1 and record_now[I][J + 1] == 1) or (
                                        record_now[I + 1][J - 1] == 1 and record_now[I + 1][J] == 1 and record_now[I][J - 1] == 1) or (
                                        record_now[I + 1][J + 1] == 1 and record_now[I + 1][J] == 1 and record_now[I][J + 1] == 1):
                                        item[2] += 100
                                except:
                                    pass

                            choice.sort(key=lambda x: x[2], reverse=True)
                            for item in choice:
                                if item[2]== choice[0][2]:
                                    list.append([i,j,item[0],item[1],item[2]])
            else:
                for i in range(0,14):
                    for j in range(0,14):
                        if record_now[i][j]==2:
                            print(i,j)
                            choice = []
                            if i + 1 < 14 and record_now[i + 1][j] == 0:
                                choice.append([i + 1, j,1])
                            if i + 2 < 14 and record_now[i + 1][j] == 1 and record_now[i + 2][j] == 0:
                                choice.append([i + 2, j,11])
                                if i + 4 < 14 and record_now[i + 3][j] == 1 and record_now[i + 4][j] == 0:
                                    choice.append([i + 4, j,21])
                                    if i + 6 < 14 and record_now[i + 5][j] == 1 and record_now[i + 6][j] == 0:
                                        choice.append([i + 6, j,31])
                                        if i + 8 < 14 and record_now[i + 7][j] == 1 and record_now[i + 8][j] == 0:
                                            choice.append([i + 8, j,41])
                                            if i + 10 < 14 and record_now[i + 9][j] == 1 and record_now[i + 10][j] == 0:
                                                choice.append([i + 10, j,51])
                                                if i + 12 < 14 and record_now[i + 11][j] == 1 and record_now[i + 12][j] == 0:
                                                    choice.append([i + 12, j,61])

                            if i - 1 > -1 and record_now[i - 1][j] == 0:
                                choice.append([i - 1, j,1])
                            if i - 2 > -1 and record_now[i - 1][j] == 1 and record_now[i - 2][j] == 0:
                                choice.append([i - 2, j,11])
                                if i - 4 > -1 and record_now[i - 3][j] == 1 and record_now[i - 4][j] == 0:
                                    choice.append([i - 4, j,21])
                                    if i - 6 > -1 and record_now[i - 5][j] == 1 and record_now[i - 6][j] == 0:
                                        choice.append([i - 6, j,31])
                                        if i - 8 > -1 and record_now[i - 7][j] == 1 and record_now[i - 8][j] == 0:
                                            choice.append([i - 8, j,41])
                                            if i - 10 > -1 and record_now[i - 9][j] == 1 and record_now[i - 10][j] == 0:
                                                choice.append([i - 10, j,51])
                                                if i - 12 > -1 and record_now[i - 11][j] == 1 and record_now[i - 12][j] == 0:
                                                    choice.append([i - 12, j,61])

                            if j + 1 < 14 and record_now[i][j + 1] == 0:
                                choice.append([i, j + 1,1])
                            if j + 2 < 14 and record_now[i][j + 1] == 1 and record_now[i][j + 2] == 0:
                                choice.append([i, j + 2,11])
                                if j + 4 < 14 and record_now[i][j + 3] == 1 and record_now[i][j + 4] == 0:
                                    choice.append([i, j + 4,21])
                                    if j + 6 < 14 and record_now[i][j + 5] == 1 and record_now[i][j + 6] == 0:
                                        choice.append([i, j + 6,31])
                                        if j + 8 < 14 and record_now[i][j + 7] == 1 and record_now[i][j + 8] == 0:
                                            choice.append([i, j + 8,41])
                                            if j + 10 < 14 and record_now[i][j + 9] == 1 and record_now[i][j + 10] == 0:
                                                choice.append([i, j + 10,51])
                                                if j + 12 < 14 and record_now[i][j + 11] == 1 and record_now[i][j + 12] == 0:
                                                    choice.append([i, j + 12,61])

                            if j - 1 > -1 and record_now[i][j - 1] == 0:
                                choice.append([i, j - 1,1])
                            if j - 2 > -1 and record_now[i][j - 1] == 1 and record_now[i][j - 2] == 0:
                                choice.append([i, j - 2,11])
                                if j - 4 > -1 and record_now[i][j - 3] == 1 and record_now[i][j - 4] == 0:
                                    choice.append([i, j - 4,21])
                                    if j - 6 > -1 and record_now[i][j - 5] == 1 and record_now[i][j - 6] == 0:
                                        choice.append([i, j - 6,31])
                                        if j - 8 > -1 and record_now[i][j - 7] == 1 and record_now[i][j - 8] == 0:
                                            choice.append([i, j - 8,41])
                                            if j - 10 > -1 and record_now[i][j - 9] == 1 and record_now[i][j - 10] == 0:
                                                choice.append([i, j - 10,51])
                                                if j - 12 > -1 and record_now[i][j - 11] == 1 and record_now[i][j - 12] == 0:
                                                    choice.append([i, j - 12,61])

                            for item in choice:
                                try:
                                    I = item[0]
                                    J = item[1]
                                    if (record_now[I - 1][J - 1] == 2 and record_now[I - 1][J] == 2 and record_now[I][J - 1] == 2) or (
                                        record_now[I - 1][J + 1] == 2 and record_now[I - 1][J] == 2 and record_now[I][J + 1] == 2) or (
                                        record_now[I + 1][J - 1] == 2 and record_now[I + 1][J] == 2 and record_now[I][J - 1] == 2) or (
                                        record_now[I + 1][J + 1] == 2 and record_now[I + 1][J] == 2 and record_now[I][J + 1] == 2):
                                        item[2] += 100
                                except:
                                    pass

                            choice.sort(key=lambda x: x[2], reverse=True)
                            for item in choice:
                                if item[2]== choice[0][2]:
                                    list.append([i,j,item[0],item[1],item[2]])

            list2 = sorted(list, key=lambda x: x[4], reverse=True)
            choices = []
            for item in list2:
                if item[4] == list2[0][4]:
                    choices.append(item)
            print(choices)
            str3 = ''
            for item in choices:
                str3 = str3 + chr(item[0] + 65) + str(item[1] + 1) + '->' + chr(item[2] + 65) + str(item[3] + 1)+'\n'

            self.chess_text.insert('6.0', '\n下一步推荐：\n' + str3)

    def last_record(self):
        if self.page > 0:
            self.page -= 1
        self.chessrecord_now.delete("all")
        self.chessrecord_now_refresh()
        self.callback(self.record[self.page])

        self.chess_text.delete('2.0', 'end')
        if self.page > 1:
            pass



    def next_record(self):
        if self.page < len(self.record)-1:
            self.page += 1
        self.chessrecord_now.delete("all")
        self.chessrecord_now_refresh()
        self.callback(self.record[self.page])

        if self.page  > 0:
            self.chess_text.delete('2.0','end')
            black_show = []
            black_delete = []
            white_show = []
            white_delete = []
            record_now = self.record[self.page]
            record_last = self.record[self.page-1]
            for j in range(0, 14):
                for i in range(0, 14):
                    if record_now[i][j] - record_last[i][j] == 1:
                        black_show.append(chr(i+65)+str(j+1))
                    if record_now[i][j] - record_last[i][j] == -1:
                        black_delete.append(chr(i + 65) + str(j + 1))
                    if record_now[i][j] - record_last[i][j] == 2:
                        white_show.append(chr(i + 65) + str(j + 1))
                    if record_now[i][j] - record_last[i][j] == -2:
                        white_delete.append(chr(i + 65) + str(j + 1))


            str_pos = ''
            try:
                if len(black_show)>len(white_show):
                    self.chess_text.insert('3.0', '\n\n黑棋'+black_delete[0]+'->'+black_show[0]+'\n')
                    for pos in white_delete:
                        str_pos += pos+','
                    self.chess_text.insert('4.0', '\n吃白棋:'+str_pos+'\n')
                else:
                    self.chess_text.insert('3.0', '\n\n白棋' + white_delete[0] + '->' + white_show[0] + '\n')
                    for pos in black_delete:
                        str_pos += pos + ','
                    self.chess_text.insert('4.0', '\n吃黑棋:' + str_pos + '\n')
            except:
                try:
                    if (black_delete[0] == 'H7' and white_delete[0] == 'G8') or (black_delete[0] == 'G8' and white_delete[0] == 'H7'):
                        self.chess_text.insert('3.0', '\n\n布局结束\n')
                except:
                    pass
                if len(black_show)>len(white_show):
                    self.chess_text.insert('3.0', '\n\n黑棋->'+black_show[0]+'\n')
                else:
                    self.chess_text.insert('3.0', '\n\n白棋->' + white_show[0] + '\n')




    def callback(self,A):
        for j in range(0, 14):
            for i in range(0, 14):
                if A[i][j] == 1:
                    globals()['x' + str(i) + "_" + str(j)] = self.chessrecord_now.create_oval(40 * j + 5, 40 * i + 5, 40 * j + 35,
                                                                            40 * i + 35, fill='black')
                elif A[i][j] == 2:
                    globals()['x' + str(i) + "_" + str(j)] = self.chessrecord_now.create_oval(40 * j + 5, 40 * i + 5, 40 * j + 35,
                                                                            40 * i + 35, fill='white')



if __name__ == '__main__':
    a = chess_roback()



    a.root.mainloop()