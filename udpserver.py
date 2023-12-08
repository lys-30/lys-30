import socket
import os
from pathlib import Path

def receive_file(server_port):
    # 创建UDP套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定服务器地址和端口
    server_address = ('127.0.0.30', server_port)
    udp_socket.bind(server_address)

    print(f"服务器正在监听端口 {server_port}...")

    # 接收文件大小
    file_size, client_address = udp_socket.recvfrom(1024)
    file_size = int(file_size.decode())

    # 发送确认
    udp_socket.sendto("ACK".encode(), client_address)

    received_data = b""
    total_received = 0

    print(f"接收来自 {client_address} 的文件...")

    # 接收文件数据
    while total_received < file_size:
        data, _ = udp_socket.recvfrom(1024)
        received_data += data
        total_received += len(data)

    # 获取桌面路径
    desktop_path = str(Path.home() / "Desktop")

    # 创建文件夹路径
    folder_path = os.path.join(desktop_path, "1")

    # 创建文件夹（如果不存在）
    os.makedirs(folder_path, exist_ok=True)

    # 保存文件到文件夹
    save_path = os.path.join(folder_path, "received_file.txt")
    with open(save_path, 'wb') as file:
        file.write(received_data)

    # 关闭套接字
    udp_socket.close()

    print(f"文件接收完成，保存到桌面文件夹 '1': {save_path}")

if __name__ == "__main__":
    server_port = 30000

    receive_file(server_port)
