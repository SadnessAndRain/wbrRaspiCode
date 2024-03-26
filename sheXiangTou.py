import cv2  # 导入OpenCV库，用于图像处理
import socket  # 导入socket库，用于网络通信
import numpy as np  # 导入NumPy库，用于数值计算
import time  # 导入time库，用于控制时间相关的功能

# 设置IP地址和端口号
ip = "192.168.137.1"
port = 8080

# 创建一个socket对象，AF_INET表示IPv4，SOCK_STREAM表示使用TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 使用OpenCV捕获视频，0代表计算机的默认摄像头
cap = cv2.VideoCapture(0)
cap.set(3,640)               #cap.set 摄像头参数设置
cap.set(4,480)               #3代表图像高度，4代表图像宽度，5代表图像帧率
cap.set(5,30)                #图像高为600，宽度为480，帧率为30

# 尝试连接到服务器
try:
    s.connect((ip, port))
except socket.error as e:
    print("Failed connecting...")  # 如果连接失败，打印错误信息

# 定义一个函数用于发送图片
def send_pic():
    ret, frame = cap.read()  # 从摄像头读取一帧图像
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]  # 设置JPEG图像的质量
    while ret:  # 如果读取图像成功
        time.sleep(0.01)  # 稍微暂停一下，以减少CPU占用率
        result, imgencode = cv2.imencode('.JPG', frame, encode_param)  # 将图像编码为JPEG格式
        data = np.array(imgencode)  # 将编码后的图像转换为NumPy数组
        stringdata = data.tostring()  # 将NumPy数组转换为字符串
        send = str.encode('size=' + str(len(stringdata)).ljust(16))  # 准备发送图像大小信息
        print(send)  # 打印发送的信息
        s.send(send)  # 发送图像大小信息
        rx = s.recv(16)  # 接收服务器的响应
        if rx == b'ack!':  # 如果服务器响应"ack!"
            print('step 2 : recv length ack!')  # 打印接收到确认信息
            s.send(stringdata)  # 发送图像数据
            if s.recv(16) == b'finsh!':  # 如果服务器响应"finsh!"
                print("step 3 : recv finsh ack!")  # 打印接收到完成信息

        ret, frame = cap.read()  # 继续读取下一帧图像

    s.close()  # 关闭socket连接

# 如果这个脚本是作为主程序运行，而不是被导入到其他Python脚本中
if __name__ == "__main__":
    send_pic()  # 调用send_pic函数

