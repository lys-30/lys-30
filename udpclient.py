import socket
import os
import tqdm

def send_file(file_name, server_address, server_port):
    # 创建UDP套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # 构建文件夹路径
    folder_path = os.path.join(desktop_path, "1")

    # 创建文件夹（如果不存在）
    os.makedirs(folder_path, exist_ok=True)

    # 构建文件路径
    file_path = os.path.join(folder_path, file_name)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 '{file_name}' 不存在，请确保输入正确的文件名。")
        udp_socket.close()
        return

    # 读取文件内容
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 发送文件大小
    udp_socket.sendto(str(file_size).encode(), (server_address, server_port))

    # 接收服务器的确认
    ack, _ = udp_socket.recvfrom(1024)
    if ack.decode() != 'ACK':
        print("未收到服务器的确认，退出")
        udp_socket.close()
        return

    # 发送文件数据
    progress = tqdm.tqdm(range(0, len(file_data), 1024), f"Sending {file_name}", unit="B", unit_scale=True)
    for i in progress:
        udp_socket.sendto(file_data[i:i+1024], (server_address, server_port))

    # 关闭套接字
    udp_socket.close()

    print(f"{file_name} 发送完成")

if __name__ == "__main__":
    file_name = input("请输入要发送文件的文件名: ")
    target_ip = input("请输入目标IP地址: ")
    target_port = int(input("请输入目标端口号: "))

    send_file(file_name, target_ip, target_port)
