import cv2
import time
import socket
import struct
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread


other_list = {}

class my_canvas(tk.Canvas):
    def __init__(self):
        super().__init__()
        self.current_frame_id = None
        self.frame_buffer = {}

    def get(self, frame_id, fragment_id, is_last, fragment_data):
        if frame_id != self.current_frame_id:
            self.frame_buffer = {}
            self.current_frame_id = frame_id

        self.frame_buffer[fragment_id] = fragment_data

        if is_last:
            # 按序号合并数据
            frame_data = b"".join(self.frame_buffer[i] for i in sorted(self.frame_buffer.keys()))
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.image = imgtk  # 防止被垃圾回收

def recive():
    while 1:
        data, addr = sock.recvfrom(65535)

        header = data[:struct.calcsize("IHBQ")]
        frame_id, fragment_id, is_last, other_id = struct.unpack("IHBQ", header)
        fragment_data = data[struct.calcsize("IHBQ"):]

        if other_id not in other_list:
            other_list[other_id] = my_canvas()
            other_list[other_id].config(bg="skyblue")
            other_list[other_id].place(x=220*((len(other_list.keys()))%3), y=150*((len(other_list.keys())+1)//3), width=220, height=150)

        other_list[other_id].get(frame_id, fragment_id, is_last, fragment_data)
        print(other_list[other_id].winfo_x(), other_list[other_id].winfo_y())
        #win.after(100, recive)

def update_canvas():
    # take camera
    while 1:
        ret, frame = cap.read()
        if not ret:
            #win.after(100, update_canvas)
            continue

        frame = cv2.resize(frame, (220, 150))

        _, buffer = cv2.imencode('.jpg', frame)

        # bgr to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # change to pil img
        img = Image.fromarray(frame)

        # change to tk img
        imgtk = ImageTk.PhotoImage(image=img)

        # update to canvas
        local_video.create_image(0, 0, anchor=tk.NW, image=imgtk)
        local_video.image = imgtk  # 防止被垃圾回收

        max_packet_size = 1200  # UDP单个数据包最大值
        frame_data = buffer.tobytes()
        frame_size = len(frame_data)

        for i in range(0, frame_size, max_packet_size):
            fragment = frame_data[i:i + max_packet_size]
            # 帧头：帧ID（4字节） + 分片序号（2字节） + 是否是最后一个片段（1字节）
            header = struct.pack("IHB", 1, i // max_packet_size, i + max_packet_size >= frame_size)
            sock.sendto(header + fragment, (host, port))

        # do this func every 100 ms
        #win.after(100, update_canvas)

host = "127.0.0.1"
port = 5000

local_port = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", local_port))

cap = cv2.VideoCapture(0)

win = tk.Tk()
win.title = "meeting room"
win.geometry("1200x700")
win.resizable(False, False)

local_video = tk.Canvas()
local_video.config(bg="black")
local_video.place(x=0, y=0, width=220, height=150)

camera_lock = tk.Button(text="camera")
camera_lock.config(bg="skyblue")
camera_lock.place(x=100, y=600, width=100, height=50)

mic_lock = tk.Button(text="mic")
mic_lock.config(bg="skyblue")
mic_lock.place(x=200, y=600, width=100, height=50)

leave_button = tk.Button(text="leave")
leave_button.config(bg="skyblue")
leave_button.place(x=300, y=600, width=100, height=50)

text_label = tk.Label()
text_label.config(bg="skyblue")
text_label.place(x=800, y=0, width=400, height=700)

thread_1 = Thread(target=update_canvas)
thread_2 = Thread(target=recive)
thread_1.start()
thread_2.start()

# 清暫存
def on_closing():
    sock.close()
    cap.release()
    win.destroy()

win.protocol("WM_DELETE_WINDOW", on_closing)

win.mainloop()