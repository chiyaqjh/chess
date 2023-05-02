import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import socket
from datetime import datetime

class TALK:

    def __init__(self,id):
        SERVER = '10.151.24.239'  # 请替换为您的服务器IP地址
        PORT = 6688
        ADDR = (SERVER, PORT)
        FORMAT = 'utf-8'
        ipv4s = socket.gethostbyname_ex(socket.gethostname())[2]
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)

        def receive():
            while True:
                try:
                    msg = client.recv(1024).decode(FORMAT)
                    text_area.configure(state='normal')
                    text_area.insert(tk.END, msg + "\n")
                    text_area.configure(state='disabled')
                    text_area.see(tk.END)
                except:
                    print("An error occurred!")
                    client.close()
                    break

        def on_send():


            # 获取当前日期和时间
            current_datetime = datetime.now()
            print(current_datetime)
            print(type(current_datetime))


            msg = "用户名:"+id+"  ip:10.151.71.228"+ "  \n于"+str(current_datetime)+'\n说:'+ message_entry.get()
            if msg:
                message_entry.delete(0, tk.END)
                client.send(msg.encode(FORMAT))

        def on_close():
            window.destroy()
            client.close()

        window = tk.Tk()
        window.title("Chat Room")
        window.geometry("300x750+1355+130")
        window.protocol("WM_DELETE_WINDOW", on_close)

        text_area = scrolledtext.ScrolledText(window, state='disabled', wrap='word', font=("Arial", 10))
        text_area.pack(padx=5, pady=4, fill=tk.BOTH, expand=True)

        message_entry = tk.Entry(window, font=("Arial", 12))
        message_entry.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        message_entry.bind('<Return>', lambda event: on_send())

        send_button = tk.Button(window, text="Send", font=("Arial", 12), command=on_send)
        send_button.pack(fill=tk.X, padx=5, pady=5)

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        window.mainloop()


if __name__ == '__main__':
    TALK('大眼睛')