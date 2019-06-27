'''
包含了所有的基础函数和类
通过Listener读取用户的命令，通过Worker在模拟器上执行操作
模拟器和各游戏的相关参数储存于config.ini配置文件中
具体脚本位于script文件夹中，暂定为json文件
'''
# TODO: 完善注释

import random
import pyautogui as pag
import time
import configparser
import json

# 下列参数仅适用于网易MuMu模拟器
# 下一个可能添加支持的模拟器为雷电模拟器
# 后续可能添加对其他主流模拟器的支持
config = configparser.ConfigParser()
config.read('config.ini')
DISPLAY_WIDTH = int(config['MuMu']['display_width'])    # 游戏画面宽度
DISPLAY_HEIGHT = int(config['MuMu']['display_height'])  # 游戏画面高度
WINDOW_TITLE_PATH = str(config['MuMu']['title_pic'])    # 窗口标题图片
TITLE_HEIGHT = int(config['MuMu']['title_height'])      # 标题栏高度

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def revise(self):
        global DISPLAY_LOCATION
        self.x += DISPLAY_LOCATION.left + self.gauss()
        self.y += DISPLAY_LOCATION.top + self.gauss()
    
    def gauss(self):
        result = round(random.gauss(0, 2))
        if -15 < result < 15:
            return result
        else:
            return self.gauss()
    
    def __str__(self):
        return f'{self.x}, {self.y}'


def offset(func):  # 对函数参数中的所有Point对象进行偏移
    def wrapper(*args, **kwargs):
        for p in [*args, *kwargs.values()]:
            if isinstance(p, Point):
                p.revise()
        return func(*args, **kwargs)
    return wrapper


@offset
def tap(point):
    pag.click(point.x, point.y)


@offset
def hold(point, time):
    pag.mouseDown(point.x, point.y)
    time.sleep(time)
    pag.mousUp()


@offset
def drag(point_start, point_end):
    pag.mouseDown(point_start.x, point_start.y)
    pag.dragTo(point_end.x, point_end.y, duration=0.4)


@offset
def isPicInArea(point_topleft, point_bottomright, path_picture):
    area = (point_topleft.x, point_topleft.y, point_bottomright.x-point_topleft.x, point_bottomright.y-point_topleft.y)
    shot = pag.screenshot(region=area)
    return bool(pag.locate(path_picture, shot))


class Worker:
    def __init__(self, game):
        self.game = game
    
    def told(self, instructions):
        for ins in instructions:
            self.execute(ins)
    
    def execute(self, ins):
        print(ins)


class Listener:
    def __init__(self, game):
        self.game = game
        with open(f'.\scripts\{game}.json', 'r') as f:
            self.instruction_set = json.load(f)
        self.worker = Worker(game)
        self.running = True
    
    def listen(self):
        while self.running:
            cmd = input('输入指令：\n').lower().split()
            if len(cmd) == 1:
                exp = f'self.{cmd[0]}()'
            else:
                exp = f'self.{cmd[0]}("{cmd[-1]}")'
            try:
                eval(exp)
            except AttributeError:
                print(f'{cmd[0]}方法未定义')
            except TypeError:
                print(f'{cmd[0]}成员不可用')
    
    def run(self, par):
        try:
            instructions = self.instruction_set[par]
            self.tell(instructions)
        except KeyError:
            print(f'"{par}"为未知参数')
            # TODO: 猜测正确的参数
    
    def tell(self, info):
        self.worker.told(info)
    
    def quit(self, *args):
        self.running = False
        # TODO: 对需要保存的数据进行序列化
    
    def help(self):
        print('help: show this')
        print('quit: save and exit')
        # TODO: 完善帮助信息


def initial(simulator):
    global WINDOW_POSITION    # 窗口位置
    global DISPLAY_LOCATION   # 游戏画面位置和大小
    global TITLE_HEIGHT       # 标题栏高度
    global WINDOW_TITLE_PATH  # 窗口标题图片
    global DISPLAY_HEIGHT     # 游戏画面高度
    global DISPLAY_WIDTH      # 游戏画面宽度
    pag.FAILSAFE = True       # 鼠标移至左上角退出
    pag.PAUSE = 0.2           # 脚本执行最小间隔时间
    config = configparser.ConfigParser()
    config.read('config.ini')
    DISPLAY_WIDTH = int(config[simulator]['display_width'])
    DISPLAY_HEIGHT = int(config[simulator]['display_height'])
    WINDOW_TITLE_PATH = str(config[simulator]['title_pic'])
    TITLE_HEIGHT = int(config[simulator]['title_height'])
    while True:
        WINDOW_POSITION = pag.locateOnScreen(WINDOW_TITLE_PATH)
        if WINDOW_POSITION:
            WINDOW_POSITION = (WINDOW_POSITION.left, WINDOW_POSITION.top)
            break
        else:
            pag.alert(text='未找到窗口,请确保窗口非最小化且未被遮挡', title='警告', button='重试')
    DISPLAY_LOCATION = (WINDOW_POSITION[0], WINDOW_POSITION[1]+TITLE_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    print('WINDOW_POSITION: ', WINDOW_POSITION, '\nDISPLAY_LOCATION: ', DISPLAY_LOCATION)


if __name__ == '__main__':
    SIMULATOR = input('模拟器：\n') or 'MuMu'
    initial(SIMULATOR)
    GAME = input('游戏：\n') or 'FGO'
    elf = Listener(GAME)
    elf.listen()
