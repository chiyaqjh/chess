import pygame
import sys
import time
import numpy as np
import socket
import threading

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1020, 750), 0, 32)
font = pygame.font.SysFont("SimHei", 32)

# bgm
# pygame.mixer.init()
# pygame.mixer.music.load("music.mp3")
# pygame.mixer.music.play(-1)

# 加载相关素材
playerBackgroud = pygame.image.load(r"material/1.jpg")
mainBackground = pygame.image.load(r"material/mainScene.jpg")
startButton = pygame.image.load(r"material/startGame.png")
blackChess = pygame.image.load(r"material/blackChess.png")
whiteChess = pygame.image.load(r"material/whiteChess.png")
redChess = pygame.image.load(r"material/redChess.png")
redChess2 = pygame.image.load(r"material/redChess2.png")
# 当前场景
currentScene = "mainMenu"

# 当前状态
waitingForPlayer = False

mynumber = 0

# 黑方
blackPlayer = True

# 最近下子位置
latestX = -1
latestY = -1

# 棋盘
board = np.zeros((14, 14))

# 棋子位置
chessX = np.linspace(32, 690, 14)
chessY = np.linspace(32, 690, 14)

# 当前状态
waitingForElse = False

waitingForConnect = False

numblack = numwhite = 0
stepflag = 0
MES = ''
flag_num = 7
fly_num = 4
lose_num = 1

file1 = open("11.txt", 'w').close()
f1 = open('11.txt','a')

if blackPlayer:
    list = board.T.tolist()
    f1.write(str(list) + '\n')

# 创建一个socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 主动去连接局域网内IP为192.168.27.238，端口为6688的进程
#client.connect(('localhost', 6688))
# 此处填写服务器的公网ip
client.connect(('10.151.24.239', 6688))


def errorMessage():
    data = "Error"
    data = data.encode('utf-8')
    global client

    client.sendall(data)
    pygame.quit()
    sys.exit()


def sendMessage(data):
    try:
        global waitingForElse
        waitingForElse = True
        data = data.encode('utf-8')
        global client
        client.sendall(data)
        print(data)
        # 接收服务端的反馈数据
        if blackPlayer:
            list = board.T.tolist()
            f1.write(str(list) + '\n')
        while True:
            rec_data = client.recv(1024).decode(encoding='utf8')
            if len(rec_data) >= 3:
                rec_data = rec_data.split()

                # 获取服务器传回的信息
                global latestX, latestY
                latestX = int(rec_data[0])
                latestY = int(rec_data[1])

                try:
                    oldx = int(rec_data[2])
                    oldy = int(rec_data[3])

                    if blackPlayer:
                        board[int(rec_data[0]), int(rec_data[1])] = 2
                        board[int(rec_data[2]), int(rec_data[3])] = 0
                        if int(rec_data[0]) == int(rec_data[2]):
                            for t in range(min(int(rec_data[1]),int(rec_data[3])),max(int(rec_data[1]),int(rec_data[3]))):
                                if board[int(rec_data[0]), t] == 1:
                                    board[int(rec_data[0]), t] = 0
                        if int(rec_data[1]) == int(rec_data[3]):
                            for t in range(min(int(rec_data[0]),int(rec_data[2])),max(int(rec_data[0]),int(rec_data[2]))):
                                if board[t,int(rec_data[1])] == 1:
                                    board[t,int(rec_data[1])] = 0
                    else:
                        board[int(rec_data[0]), int(rec_data[1])] = 1
                        board[int(rec_data[2]), int(rec_data[3])] = 0
                        if int(rec_data[0]) == int(rec_data[2]):
                            for t in range(min(int(rec_data[1]),int(rec_data[3])),max(int(rec_data[1]),int(rec_data[3]))):
                                if board[int(rec_data[0]), t] == 2:
                                    board[int(rec_data[0]), t] = 0
                        if int(rec_data[1]) == int(rec_data[3]):
                            for t in range(min(int(rec_data[0]),int(rec_data[2])),max(int(rec_data[0]),int(rec_data[2]))):
                                if board[t,int(rec_data[1])] == 2:
                                    board[t,int(rec_data[1])] = 0

                    try:
                        oldx = int(rec_data[4])
                        oldy = int(rec_data[5])
                        board[int(rec_data[4]), int(rec_data[5])] = 0
                    except:
                        pass


                except:
                    if blackPlayer:
                        board[int(rec_data[0]), int(rec_data[1])] = 2
                    else:
                        board[int(rec_data[0]), int(rec_data[1])] = 1###################

                break
        if blackPlayer:
            list = board.T.tolist()
            f1.write(str(list) + '\n')
        waitingForElse = False
    except:
        errorMessage()


def firstMessage():
    try:
        global waitingForElse
        while True:
            print("i am waiting for the first message")
            rec_data = client.recv(1024).decode(encoding='utf8')
            print(rec_data)
            if len(rec_data) >= 3:
                rec_data = rec_data.split()
                # 获取服务器传回的信息
                if blackPlayer:
                    board[int(rec_data[0]), int(rec_data[1])] = 2
                else:
                    board[int(rec_data[0]), int(rec_data[1])] = 1
                break

        waitingForElse = False
    except:
        errorMessage()


def playerScene():
    try:
        global playerBackgroud
        global mainBackground
        global blackChess
        global whiteChess
        global chessX, chessY, board
        global numblack, numwhite, stepflag
        screen.fill((255, 255, 255))
        screen.blit(mainBackground, (0, 0))
        screen.blit(playerBackgroud, (20, 20))

        introduction = font.render("Your chess:", 1, (253, 177, 6))
        screen.blit(introduction, (720, 20))
        if blackPlayer:
            screen.blit(blackChess, (820, 100))
        else:
            screen.blit(whiteChess, (820, 100))

        introduction = font.render("black num:", 1, (253, 177, 6))
        screen.blit(introduction, (720, 120))

        introduction = font.render("white num:", 1, (253, 177, 6))
        screen.blit(introduction, (720, 220))


        # 绘制棋子
        numblack = numwhite = 0
        for i in range(14):
            for j in range(14):
                if board[i][j] == 1:
                    screen.blit(blackChess, (chessX[i] - 12, chessY[j] - 12))
                    numblack += 1
                elif board[i][j] == 2:
                    screen.blit(whiteChess, (chessX[i] - 12, chessY[j] - 12))
                    numwhite += 1
                elif board[i][j] == 3:
                    numblack += 1
                    screen.blit(redChess, (chessX[i] - 12, chessY[j] - 12))
                elif board[i][j] == 4:
                    numwhite += 1
                    screen.blit(redChess2, (chessX[i] - 12, chessY[j] - 12))

        # print(numwhite,numblack)
        if numwhite == flag_num and numblack == flag_num:
            stepflag = 1
            board[6][7] = board[7][6] = 0
            if blackPlayer:
                list = board.T.tolist()
                f1.write(str(list) + '\n')

        if numwhite <= fly_num and numblack > fly_num and stepflag != 0:
            stepflag = 2#白飞

        if numblack <= fly_num and numwhite > fly_num and stepflag != 0:
            stepflag = 3#黑飞

        if numblack <= fly_num and numwhite <=fly_num and stepflag != 0:
            stepflag = 4#飞


        numblacktext = font.render(str(numblack), 1, (253, 177, 6))
        screen.blit(numblacktext, (720, 160))
        numwhitetext = font.render(str(numwhite), 1, (253, 177, 6))
        screen.blit(numwhitetext, (720, 260))

        global latestX, latestY
        if latestX != -1 and latestY != -1:
            recent = font.render("N", 1, (253, 177, 6))
            screen.blit(recent, (chessX[latestX] - 30, chessY[latestY] - 30))

        if waitingForElse:
            titleText = font.render("Waiting For Else to Act", 1, (253, 177, 6))
            screen.blit(titleText, (450, 350))

        pygame.display.update()
    except:
        errorMessage()


def findWinner():
    global numblack,numwhite,lose_num
    if numblack < lose_num:
        return 2
    if numwhite < lose_num:
        return 1

    return 0


def mainScene():
    try:
        global waitingForConnect
        global waitingForPlayer
        if waitingForConnect:
            return
        if waitingForPlayer == False:
            global mainBackground
            global startButton
            screen.fill((255, 255, 255))
            screen.blit(mainBackground, (0, 0))

            titleText = font.render("藏族“久”棋", 1, (253, 177, 6))
            screen.blit(titleText, (250, 200))
            screen.blit(startButton, (350, 350))
            pygame.display.update()
        else:
            screen.fill((255, 255, 255))
            screen.blit(mainBackground, (0, 0))
            titleText = font.render("Waiting For Else Player...", 1, (253, 177, 6))
            screen.blit(titleText, (250, 200))
            pygame.display.update()

            # 阻塞，发送消息，直到回应游戏开始
            data = "1"
            data = data.encode('utf-8')
            global client
            client.sendall(data)

            waitingForConnect = True
            # 接收服务端的反馈数据
            while True:
                msg = client.recv(1024).decode(encoding='utf8')
                print(msg)
                if msg == "0":
                    print('game Start:', msg)
                    break
                else:
                    print('game Start:', msg)
                    global blackPlayer, waitingForElse
                    blackPlayer = False
                    waitingForElse = True
                    global mynumber
                    mynumber = 1
                    break
            # 切换场景
            waitingForPlayer = False
            print('start')
            global currentScene
            currentScene = "playerScene"

            if not blackPlayer:
                # 第一次消息
                thread = threading.Thread(target=firstMessage)
                thread.start()
    except:
        errorMessage()


def createScene():
    global currentScene
    if currentScene == "mainMenu":
        mainScene()
    elif currentScene == "playerScene":
        playerScene()
    elif currentScene == "win":
        winScene()
    elif currentScene == "lose":
        loseScene()


def winScene():
    screen.fill((255, 255, 255))
    screen.blit(mainBackground, (0, 0))
    titleText = font.render("You WIN!!!!!", 1, (253, 177, 6))
    screen.blit(titleText, (250, 200))
    pygame.display.update()
    time.sleep(1)
    # 切换场景
    f1.close()


def loseScene():
    screen.fill((255, 255, 255))
    screen.blit(mainBackground, (0, 0))
    titleText = font.render("You LOSE......", 1, (253, 177, 6))
    screen.blit(titleText, (250, 200))
    pygame.display.update()
    time.sleep(1)
    # 切换场景
    f1.close()


def restartGame():
    global numblack, numwhite, stepflag
    numwhite = numblack = stepflag = 0
    for i in range(14):
        for j in range(14):
            board[i, j] = 0
    global waitingForElse
    waitingForElse = False
    global currentScene
    currentScene = "playerScene"
    if mynumber == 1:
        waitingForElse = True
        thread = threading.Thread(target=firstMessage)
        thread.start()


# 判断在哪个下标的棋盘格子
def boardID(x, y):
    # 可点击半径为5
    radius = 7
    indexX = -1
    indexY = -1

    global chessX, chessY
    minDistX = 9999
    minDistY = 9999

    for i in range(14):
        if np.abs(chessX[i] - x) < minDistX and np.abs(chessX[i] - x) < radius:
            minDistX = np.abs(chessX[i] - x)
            indexX = i
        if np.abs(chessY[i] - y) < minDistY and np.abs(chessY[i] - y) < radius:
            minDistY = np.abs(chessY[i] - y)
            indexY = i

    return indexX, indexY


# 点击事件
def buttonEvent(x, y):
    global numblack, numwhite
    global MES

    try:
        global waitingForElse

        if (currentScene == "mainMenu" and x >= 350
                and x <= startButton.get_width() + 350
                and y >= 350 and y <= startButton.get_height() + 350):
            # start game
            global waitingForPlayer
            waitingForPlayer = True
        # 在下棋界面
        elif currentScene == "playerScene" and not waitingForElse:
            if stepflag == 0:
                i, j = boardID(x, y)
                if i != -1 and j != -1 and board[i, j] == 0:
                    # new qizi

                    if blackPlayer:
                        if numblack != 0 or [i, j] == [6, 7] or [i, j] == [7, 6]:
                            waitingForElse = True
                            msg = str(i) + " " + str(j)

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 1

                    else:
                        if numwhite != 0 or [i, j] == [6, 7] or [i, j] == [7, 6]:
                            waitingForElse = True
                            msg = str(i) + " " + str(j)

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 2
            elif stepflag == 1:
                print("走子")
                i, j = boardID(x, y)

                flag = 0
                if MES != '':
                    flag = 2
                for ii in range(14):
                    for jj in range(14):
                        if board[ii][jj] == 3 or board[ii][jj] == 4:
                            flag = 1
                            I = ii
                            J = jj

                if blackPlayer:
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 3
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1,J])
                        if I + 2 < 14 and board[I + 1][J] == 2 and board[I + 2][J] == 0:
                            choice.append([I + 2,J])
                            if I + 4 < 14 and board[I + 3][J] == 2 and board[I + 4][J] == 0 :
                                choice.append([I + 4,J])
                                if I + 6 < 14 and board[I + 5][J] == 2 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 2 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 2 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 2 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1,J])
                        if I - 2 > -1 and board[I - 1][J] == 2 and board[I - 2][J] == 0:
                            choice.append([I - 2,J])
                            if I - 4 > -1 and board[I - 3][J] == 2 and board[I - 4][J] == 0 :
                                choice.append([I - 4,J])
                                if I - 6 > -1 and board[I - 5][J] == 2 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 2 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 2 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 2 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I,J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 2 and board[I][J + 2] == 0:
                            choice.append([I,J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 2 and board[I][J + 4] == 0 :
                                choice.append([I,J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 2 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 2 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 2 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 2 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I,J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 2 and board[I][J - 2] == 0:
                            choice.append([I,J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 2 and board[I][J - 4] == 0 :
                                choice.append([I,J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 2 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 2 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 2 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 2 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] != 2 and ((i == I) or (j == J)) and [i,j] in choice:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if i == I:
                                for t in range(min(j, J),max(j, J)):
                                    if board[i, t] == 2:
                                        board[i, t] = 0
                            if j == J:
                                for t in range(min(i, I),max(i, I)):
                                    if board[t, j] == 2:
                                        board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 1
                            board[I, J] = 0

                            if (board[i-1,j-1] == 1 and board[i-1,j] == 1 and board[i,j-1] == 1) or (board[i-1,j+1] == 1 and board[i-1,j] == 1 and board[i,j+1] == 1) or (board[i+1,j-1] == 1 and board[i+1,j] == 1 and board[i,j-1] == 1) or (board[i+1,j+1] == 1 and board[i+1,j] == 1 and board[i,j+1] == 1):

                            # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:# 加判断条件  不吃

                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

                else:#白棋
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 4
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 1 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 1 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 1 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 1 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 1 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 1 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 1 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 1 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 1 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 1 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 1 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 1 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 1 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 1 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 1 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 1 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 1 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 1 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 1 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 1 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 1 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 1 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 1 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 1 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] == 0 and ((i == I) or (j == J)) and [i, j] in choice:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if i == I:
                                for t in range(min(j, J), max(j, J)):
                                    if board[i, t] == 1:
                                        board[i, t] = 0
                            if j == J:
                                for t in range(min(i, I), max(i, I)):
                                    if board[t, j] == 1:
                                        board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 2
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 2 and board[i - 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i - 1, j + 1] == 2 and board[i - 1, j] == 2 and board[i, j + 1] == 2) or (
                                    board[i + 1, j - 1] == 2 and board[i + 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i + 1, j + 1] == 2 and board[i + 1, j] == 2 and board[i, j + 1] == 2):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃
                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()
            elif stepflag == 2:
                print("白飞")
                i, j = boardID(x, y)

                flag = 0
                if MES != '':
                    flag = 2
                for ii in range(14):
                    for jj in range(14):
                        if board[ii][jj] == 3 or board[ii][jj] == 4:
                            flag = 1
                            I = ii
                            J = jj

                if blackPlayer:
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 3
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 2 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 2 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 2 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 2 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 2 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 2 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 2 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 2 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 2 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 2 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 2 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 2 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 2 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 2 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 2 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 2 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 2 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 2 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 2 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 2 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 2 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 2 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 2 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 2 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] != 2 and ((i == I) or (j == J)) and [i, j] in choice:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if i == I:
                                for t in range(min(j, J), max(j, J)):
                                    if board[i, t] == 2:
                                        board[i, t] = 0
                            if j == J:
                                for t in range(min(i, I), max(i, I)):
                                    if board[t, j] == 2:
                                        board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 1
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 1 and board[i - 1, j] == 1 and board[i, j - 1] == 1) or (
                                    board[i - 1, j + 1] == 1 and board[i - 1, j] == 1 and board[i, j + 1] == 1) or (
                                    board[i + 1, j - 1] == 1 and board[i + 1, j] == 1 and board[i, j - 1] == 1) or (
                                    board[i + 1, j + 1] == 1 and board[i + 1, j] == 1 and board[i, j + 1] == 1):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃

                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

                else:  # 白棋
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 4
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 1 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 1 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 1 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 1 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 1 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 1 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 1 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 1 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 1 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 1 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 1 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 1 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 1 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 1 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 1 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 1 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 1 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 1 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 1 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 1 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 1 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 1 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 1 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 1 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] == 0:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if [i,j] in choice:
                                if i == I:
                                    for t in range(min(j, J), max(j, J)):
                                        if board[i, t] == 1:
                                            board[i, t] = 0
                                if j == J:
                                    for t in range(min(i, I), max(i, I)):
                                        if board[t, j] == 1:
                                            board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 2
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 2 and board[i - 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i - 1, j + 1] == 2 and board[i - 1, j] == 2 and board[i, j + 1] == 2) or (
                                    board[i + 1, j - 1] == 2 and board[i + 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i + 1, j + 1] == 2 and board[i + 1, j] == 2 and board[i, j + 1] == 2):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃
                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()
            elif stepflag == 3:
                print("黑飞")
                i, j = boardID(x, y)

                flag = 0
                if MES != '':
                    flag = 2
                for ii in range(14):
                    for jj in range(14):
                        if board[ii][jj] == 3 or board[ii][jj] == 4:
                            flag = 1
                            I = ii
                            J = jj

                if blackPlayer:
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 3
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 2 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 2 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 2 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 2 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 2 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 2 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 2 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 2 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 2 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 2 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 2 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 2 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 2 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 2 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 2 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 2 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 2 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 2 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 2 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 2 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 2 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 2 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 2 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 2 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] != 2:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if [i,j] in choice:
                                if i == I:
                                    for t in range(min(j, J), max(j, J)):
                                        if board[i, t] == 2:
                                            board[i, t] = 0
                                if j == J:
                                    for t in range(min(i, I), max(i, I)):
                                        if board[t, j] == 2:
                                            board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 1
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 1 and board[i - 1, j] == 1 and board[i, j - 1] == 1) or (
                                    board[i - 1, j + 1] == 1 and board[i - 1, j] == 1 and board[i, j + 1] == 1) or (
                                    board[i + 1, j - 1] == 1 and board[i + 1, j] == 1 and board[i, j - 1] == 1) or (
                                    board[i + 1, j + 1] == 1 and board[i + 1, j] == 1 and board[i, j + 1] == 1):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃

                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0


                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

                else:  # 白棋
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 4
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 1 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 1 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 1 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 1 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 1 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 1 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 1 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 1 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 1 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 1 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 1 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 1 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 1 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 1 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 1 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 1 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 1 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 1 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 1 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 1 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 1 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 1 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 1 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 1 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] == 0 and ((i == I) or (j == J)) and [i, j] in choice:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if i == I:
                                for t in range(min(j, J), max(j, J)):
                                    if board[i, t] == 1:
                                        board[i, t] = 0
                            if j == J:
                                for t in range(min(i, I), max(i, I)):
                                    if board[t, j] == 1:
                                        board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 2
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 2 and board[i - 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i - 1, j + 1] == 2 and board[i - 1, j] == 2 and board[i, j + 1] == 2) or (
                                    board[i + 1, j - 1] == 2 and board[i + 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i + 1, j + 1] == 2 and board[i + 1, j] == 2 and board[i, j + 1] == 2):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃
                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()
            elif stepflag == 4:
                print("黑白飞")
                i, j = boardID(x, y)

                flag = 0
                if MES != '':
                    flag = 2
                for ii in range(14):
                    for jj in range(14):
                        if board[ii][jj] == 3 or board[ii][jj] == 4:
                            flag = 1
                            I = ii
                            J = jj

                if blackPlayer:
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 3
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 2 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 2 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 2 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 2 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 2 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 2 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 2 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 2 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 2 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 2 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 2 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 2 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 2 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 2 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 2 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 2 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 2 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 2 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 2 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 2 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 2 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 2 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 2 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 2 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] != 2 :
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if [i,j] in choice:
                                if i == I:
                                    for t in range(min(j, J), max(j, J)):
                                        if board[i, t] == 2:
                                            board[i, t] = 0
                                if j == J:
                                    for t in range(min(i, I), max(i, I)):
                                        if board[t, j] == 2:
                                            board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 1
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 1 and board[i - 1, j] == 1 and board[i, j - 1] == 1) or (
                                    board[i - 1, j + 1] == 1 and board[i - 1, j] == 1 and board[i, j + 1] == 1) or (
                                    board[i + 1, j - 1] == 1 and board[i + 1, j] == 1 and board[i, j - 1] == 1) or (
                                    board[i + 1, j + 1] == 1 and board[i + 1, j] == 1 and board[i, j + 1] == 1):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃

                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0


                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

                else:  # 白棋
                    if flag == 0:
                        if i != -1 and j != -1 and board[i, j] == 2:
                            msg = str(i) + " " + str(j)

                            # thread = threading.Thread(target=sendMessage, args=(msg,))
                            # thread.start()

                            latestX = i
                            latestY = j
                            board[i, j] = 4
                    elif flag == 1:
                        choice = []
                        if I + 1 < 14 and board[I + 1][J] == 0:
                            choice.append([I + 1, J])
                        if I + 2 < 14 and board[I + 1][J] == 1 and board[I + 2][J] == 0:
                            choice.append([I + 2, J])
                            if I + 4 < 14 and board[I + 3][J] == 1 and board[I + 4][J] == 0:
                                choice.append([I + 4, J])
                                if I + 6 < 14 and board[I + 5][J] == 1 and board[I + 6][J] == 0:
                                    choice.append([I + 6, J])
                                    if I + 8 < 14 and board[I + 7][J] == 1 and board[I + 8][J] == 0:
                                        choice.append([I + 8, J])
                                        if I + 10 < 14 and board[I + 9][J] == 1 and board[I + 10][J] == 0:
                                            choice.append([I + 10, J])
                                            if I + 12 < 14 and board[I + 11][J] == 1 and board[I + 12][J] == 0:
                                                choice.append([I + 12, J])

                        if I - 1 > -1 and board[I - 1][J] == 0:
                            choice.append([I - 1, J])
                        if I - 2 > -1 and board[I - 1][J] == 1 and board[I - 2][J] == 0:
                            choice.append([I - 2, J])
                            if I - 4 > -1 and board[I - 3][J] == 1 and board[I - 4][J] == 0:
                                choice.append([I - 4, J])
                                if I - 6 > -1 and board[I - 5][J] == 1 and board[I - 6][J] == 0:
                                    choice.append([I - 6, J])
                                    if I - 8 > -1 and board[I - 7][J] == 1 and board[I - 8][J] == 0:
                                        choice.append([I - 8, J])
                                        if I - 10 > -1 and board[I - 9][J] == 1 and board[I - 10][J] == 0:
                                            choice.append([I - 10, J])
                                            if I - 12 > -1 and board[I - 11][J] == 1 and board[I - 12][J] == 0:
                                                choice.append([I - 12, J])

                        if J + 1 < 14 and board[I][J + 1] == 0:
                            choice.append([I, J + 1])
                        if J + 2 < 14 and board[I][J + 1] == 1 and board[I][J + 2] == 0:
                            choice.append([I, J + 2])
                            if J + 4 < 14 and board[I][J + 3] == 1 and board[I][J + 4] == 0:
                                choice.append([I, J + 4])
                                if J + 6 < 14 and board[I][J + 5] == 1 and board[I][J + 6] == 0:
                                    choice.append([I, J + 6])
                                    if J + 8 < 14 and board[I][J + 7] == 1 and board[I][J + 8] == 0:
                                        choice.append([I, J + 8])
                                        if J + 10 < 14 and board[I][J + 9] == 1 and board[I][J + 10] == 0:
                                            choice.append([I, J + 10])
                                            if J + 12 < 14 and board[I][J + 11] == 1 and board[I][J + 12] == 0:
                                                choice.append([I, J + 12])

                        if J - 1 > -1 and board[I][J - 1] == 0:
                            choice.append([I, J - 1])
                        if J - 2 > -1 and board[I][J - 1] == 1 and board[I][J - 2] == 0:
                            choice.append([I, J - 2])
                            if J - 4 > -1 and board[I][J - 3] == 1 and board[I][J - 4] == 0:
                                choice.append([I, J - 4])
                                if J - 6 > -1 and board[I][J - 5] == 1 and board[I][J - 6] == 0:
                                    choice.append([I, J - 6])
                                    if J - 8 > -1 and board[I][J - 7] == 1 and board[I][J - 8] == 0:
                                        choice.append([I, J - 8])
                                        if J - 10 > -1 and board[I][J - 9] == 1 and board[I][J - 10] == 0:
                                            choice.append([I, J - 10])
                                            if J - 12 > -1 and board[I][J - 11] == 1 and board[I][J - 12] == 0:
                                                choice.append([I, J - 12])

                        if i != -1 and j != -1 and board[i, j] == 0:
                            msg = str(i) + " " + str(j) + " " + str(I) + " " + str(J)

                            if [i,j] in choice:
                                if i == I:
                                    for t in range(min(j, J), max(j, J)):
                                        if board[i, t] == 1:
                                            board[i, t] = 0
                                if j == J:
                                    for t in range(min(i, I), max(i, I)):
                                        if board[t, j] == 1:
                                            board[t, J] = 0

                            latestX = i
                            latestY = j
                            board[i, j] = 2
                            board[I, J] = 0

                            if (board[i - 1, j - 1] == 2 and board[i - 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i - 1, j + 1] == 2 and board[i - 1, j] == 2 and board[i, j + 1] == 2) or (
                                    board[i + 1, j - 1] == 2 and board[i + 1, j] == 2 and board[i, j - 1] == 2) or (
                                    board[i + 1, j + 1] == 2 and board[i + 1, j] == 2 and board[i, j + 1] == 2):

                                # 如果形成四方，不发送信息，flag置为2，选择吃子
                                flag = 2
                                MES = msg
                            else:  # 加判断条件  不吃
                                thread = threading.Thread(target=sendMessage, args=(msg,))
                                thread.start()


                    else:
                        if i != -1 and j != -1 and board[i, j] == 1:
                            msg = MES + " " + str(i) + " " + str(j)
                            MES = ''
                            board[i, j] = 0

                            thread = threading.Thread(target=sendMessage, args=(msg,))
                            thread.start()

    except:
        errorMessage()


# 主函数
if __name__ == "__main__":

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    errorMessage()
                # 用户点击
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 获得鼠标位置
                    x, y = pygame.mouse.get_pos()
                    buttonEvent(x, y)

            result = findWinner()
            if result != 0 and stepflag != 0:
                if (result == 1 and blackPlayer) or (result == 2 and not blackPlayer):

                    currentScene = "win"
                else:
                    currentScene = "lose"

            createScene()
    except:
        errorMessage()