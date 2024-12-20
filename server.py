import socket
import struct
import cv2
import numpy as np

# 配置接收端地址和端口
host = "127.0.0.1"
port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

client_list = []

max_packet_size = 1200

try:
    while True:
        # 接收数据
        packet, addr = sock.recvfrom(65535)

        if addr not in client_list:
            client_list.append(addr)
            
        # 解析帧头
        header = packet[:7]
        frame_id, fragment_id, is_last = struct.unpack("IHB", header)
        fragment_data = packet[7:]
        frame_size = len(fragment_data)

        for i in client_list:
            print("send")
            for j in range(0, frame_size, max_packet_size):
                fragment = fragment_data[j:j + max_packet_size]
                header = struct.pack("IHBQ", frame_id, fragment_id, is_last, client_list.index(addr))
                sock.sendto(header + fragment, i)

except Exception as e:
    print(e)    
finally:
    sock.close()
    cv2.destroyAllWindows()
