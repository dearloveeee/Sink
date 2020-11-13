# -*- coding: utf-8 -*-
# @Time : 2020/7/8 21:09
# @Author : DH
# @Site :
# @File : car_control.py
# @Software: PyCharm
import time
import math
import msvcrt
import socket
import threading
from location import trilateration
from gps_transform import gps_transform
INF = float('inf')


class ControlShow:
    @staticmethod
    def show_msg():
        '''
        下行控制
        '''
        '''
        小车方向电机控制
        '''
        print('小车方向电机控制')
        print('前：$1,0,0,0,0,0,0,0,0#')
        print('后：$2,0,0,0,0,0,0,0,0#')
        print('左：$3,0,0,0,0,0,0,0,0#')
        print('右：$4,0,0,0,0,0,0,0,0#')
        print('左转：$0,1,0,0,0,0,0,0,0#')
        print('右转：$0,2,0,0,0,0,0,0,0#')
        print('停：$0,0,0,0,0,0,0,0,0#')
        '''
        摄像头电机方向控制
        '''
        print('摄像头电机方向控制')
        print('前：$0,0,0,0,3,0,0,0,0#')
        print('后：$0,0,0,0,4,0,0,0,0#')
        print('左：$0,0,0,0,6,0,0,0,0#')
        print('右：$0,0,0,0,7,0,0,0,0#')
        print('停：$0,0,0,0,8,0,0,0,0#')
        '''
        超声波电机控制
        '''
        print('超声波电机控制')
        print('左：$0,0,0,0,1,0,0,0,0#')
        print('中：$0,0,0,0,0,0,0,0,1#')
        print('右：$0,0,0,0,2,0,0,0,0#')
        '''
        灯控制
        '''
        print('灯控制')
        print('开：$0,0,0,0,0,0,1,0,0#')
        print('关：$0,0,0,0,0,0,8,0,0#')
        print('红：$0,0,0,0,0,0,2,0,0#')
        print('绿：$0,0,0,0,0,0,3,0,0#')
        print('蓝：$0,0,0,0,0,0,4,0,0#')

        '''
        其他功能
        '''
        print('其他功能')
        print('灭火：$0,0,0,0,0,0,0,1,0#')
        print('鸣笛：$0,0,1,0,0,0,0,0,0#')
        print('加速：$0,0,0,1,0,0,0,0,0#')
        print('减速：$0,0,0,2,0,0,0,0,0#')

        '''
        转动角度控制
        '''
        # print("舵机转动到180度：$4WD,PTZ180#")

        '''
        上行显示
        '''
        '''
        小车超声波传感器采集的信息发给上位机显示
        打包格式如:
            超声波 电压  灰度  巡线  红外避障 寻光
        $4WD,CSB120,PV8.3,GS214,LF1011,HW11,GM11#
        '''

    @staticmethod
    def show_key():
        print('小车方向控制')
        print('前：w，后：x，左：a，右：d，左转：z，右转：c，停：s')
        print('摄像头方向控制')
        print('上：i，下：m，左：j，右：l，停：k')
        print('超声波方向控制')
        print('左：r，中：t，右：y')
        print('灯开关控制')
        print('开：v，关：b')
        print('其他功能')
        print('鸣笛：f，灭火：g')


class ControlKeyboard:
    def __init__(self, keyboard_input):
        self.KEYBOARD_INPUT = keyboard_input

    def get_control(self):
        """

        :return:
        """
        msg = []
        # 小车方向
        if self.KEYBOARD_INPUT == 'w':  # 前
            msg.append('$1,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'x':  # 后
            msg.append('$2,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'a':  # 左
            msg.append('$3,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'd':  # 右
            msg.append('$4,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'z':  # 左转
            msg.append('$0,1,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'c':  # 右转
            msg.append('$0,2,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 's':  # 停
            msg.append('$0,0,0,0,0,0,0,0,0#')

        # 摄像头方向
        elif self.KEYBOARD_INPUT == 'i':  # 上
            msg.append('$0,0,0,0,3,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'm':  # 下
            msg.append('$0,0,0,0,4,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'j':  # 左
            msg.append('$0,0,0,0,6,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'l':  # 右
            msg.append('$0,0,0,0,7,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'k':  # 停
            msg.append('$0,0,0,0,8,0,0,0,0#')

        # 超声波控制
        elif self.KEYBOARD_INPUT == 'r':  # 左
            msg.append('$0,0,0,0,1,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 't':  # 中
            msg.append('$0,0,0,0,0,0,0,0,1#')
        elif self.KEYBOARD_INPUT == 'y':  # 右
            msg.append('$0,0,0,0,2,0,0,0,0#')

        # 灯开关控制
        elif self.KEYBOARD_INPUT == 'v':  # 开
            msg.append('$0,0,0,0,0,0,1,0,0#')
        elif self.KEYBOARD_INPUT == 'b':  # 关
            msg.append('$0,0,0,0,0,0,8,0,0#')

        # 其他功能
        elif self.KEYBOARD_INPUT == 'f':  # 鸣笛
            msg.append('$0,0,1,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'g':  # 灭火
            msg.append('$0,0,0,0,0,0,0,1,0#')

        return msg


class Car:
    def __init__(self, car_number):
        self.car_number = car_number
        self.connected = False
        self.socket = None
        self.position = []
        self.acc = []
        self.angle = []

    # 把每个小车作为一个线程单独接收。
    def receive(self):
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print("收到来自小车 {0} 的消息：{1}".format(self.car_number, message))
                m1, m2, m3 = message.split('#')  # 三种数据之间用#号分隔，分别是加速度、角度、GPS信息
                m1 = m1.split(',')  # 每种数据本身用，号分隔
                m2 = m2.split(',')
                m3 = m3.split(',')
                lock.acquire()
                for item in m1:
                    self.acc.append(round(float(item), 3))
                for item in m2:
                    self.angle.append(round(float(item), 3))
                lon = float(m3[0] + '.' + m3[1])
                lat = float(m3[2] + '.' + m3[3])
                self.position = gps_transform([lon, lat])
                lock.release()
        except:
            pass
        finally:
            self.connected = False
            print("小车 {0} 的tcp连接已断开！".format(self.car_number))

    def send(self, message):
        self.socket.send(message.encode('utf-8'))


class UWB:
    def __init__(self, uwb_number, position):
        self.distance = 0
        self.uwb_number = uwb_number
        self.position = position
        self.connected = False
        self.socket = None

    def receive(self):
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print("收到来自UWB {0} 的消息：{1}".format(self.uwb_number, data.decode('utf-8')))
                lock.acquire()
                self.distance = round(float(data.decode('utf-8')), 2)
                lock.release()
        except:
            pass
        finally:
            self.connected = False
            print("UWB {0} 的tcp连接已断开！".format(self.uwb_number))

    def send(self, cmd):
        # cmd = 'start','stop',...
        self.socket.send(cmd.encode('utf-8'))


total_car_number = 5
ip2CarNumber = {
    '192.168.31.99': 1,
    # '169.254.62.154': 2,
    '192.168.50.1': 3,
    '192.168.43.51': 4,
}
ip2UWB = {
    '127.0.0.1': 1,
    '169.254.62.154': 2,
    '192.168.31.222': 3,
}
car_list = {}
for i in range(1, total_car_number + 1):
    car_list[i] = Car(i)
uwb_list = {}
for i in range(1, 4):
    uwb_list[i] = UWB(i, [0, 0])

lock = threading.Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.31.66'
port = 8888
# host = socket.gethostname()
# port = 6666
server.bind((host, port))
server.listen(total_car_number + 3)


# 计算每一个小车与目标的距离
def calculate_distance(target_pos):
    distances = [INF] * (total_car_number + 1)
    for num, car in car_list.items():
        if car.connected:
            distance = math.sqrt((car.position[0] - target_pos[0]) ** 2 +
                                 (car.position[1] - target_pos[1]) ** 2)
            distances[num] = distance
    return distances


# 返回距离最近的三个小车
def find_3_cars(target_pos):
    distances = calculate_distance(target_pos)
    sorted_dists = sorted(distances)
    cars = []
    cars.append(car_list[distances.index(sorted_dists[0])])
    cars.append(car_list[distances.index(sorted_dists[1])])
    cars.append(car_list[distances.index(sorted_dists[2])])
    return cars

# 多线程监听小车和UWB的连接请求
def bind_socket():
    print("等待连接中...")
    while True:
        try:
            client, addr = server.accept()
            if client:
                lock.acquire()
                global car_list
                if ip2UWB.get(addr[0], None):
                    # 如果是UWBip地址，则需要建立单独的线程来控制uwb；
                    uwb_number = ip2UWB[addr[0]]
                    uwb = uwb_list[uwb_number]
                    # 如果对应uwb没有活跃的连接线程，则创建线程；否则，忽视。
                    if not uwb.connected:
                        uwb.socket = client
                        uwb.connected = True
                        thread = threading.Thread(target=uwb.receive)
                        thread.start()
                    print("UWB {0} 已连接！".format(uwb_number))
                elif ip2CarNumber.get(addr[0], None):
                    # 如果为小车地址；
                    car_number = ip2CarNumber[addr[0]]
                    car = car_list[car_number]
                    # 如果对应小车没有活跃的连接线程，则创建线程；否则，忽视。
                    if not car.connected:
                        car.socket = client
                        car.connected = True
                        thread = threading.Thread(target=car.receive)
                        thread.start()
                    print("小车 {0} 已连接！".format(car_number))
                else:
                    pass
                lock.release()
        except:
            print("服务器取消监听了！！！")
            break


def main():
    p0 = gps_transform([103.92388, 30.74216])
    p1 = gps_transform([103.93755, 30.75348])
    area_x = [p0[0], p1[0]]
    area_y = [p0[1], p1[1]]
    target_detected = False
    target_position = None
    while True:
        try:
            lock.acquire()
            if uwb_list[0].distance != 0 and uwb_list[1].distance != 0 and uwb_list[2].distance != 0:
                target_position = trilateration(uwb_list[0].position, uwb_list[1].position, uwb_list[2].position,
                                                uwb_list[0].distance, uwb_list[1].distance, uwb_list[2].distance)
                uwb_list[0].distance = 0
                uwb_list[1].distance = 0
                uwb_list[2].distance = 0
                target_detected = True
            lock.release()
            if target_detected:
                target_detected = False
                # 如果检测到目标位置，首先选择最近的三个小车
                selected_cars = find_3_cars(target_position)
                # 计算每个小车的转向和移动距离

            keyboard_input = msvcrt.getch().decode('utf-8')
            if keyboard_input == "\x1b":
                print("服务器关闭！")
                break
            data = ControlKeyboard(keyboard_input).get_control()
            active_cars = [1 if car.connected else 0 for car in car_list.values()]
            number = input("发送给第几个小车？目前连接的小车有:\r\n{0}\r\n".format(active_cars))
            print("发送给小车 {0}:{1}".format(number, str(data)))
            for d in data:
                car_list[int(number)].send(d)
                time.sleep(0.2)
        finally:
            pass


if __name__ == '__main__':
    ControlShow.show_key()
    listen_thread = threading.Thread(target=bind_socket)
    listen_thread.setDaemon(True)
    listen_thread.start()
    main()

