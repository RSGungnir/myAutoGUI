'''
公用的基础函数和类
'''

import random
import pyautogui as pag
import time
import configparser

# 下列参数仅适用于网易MuMu模拟器
# 后续可能添加对雷电模拟器的支持
config = configparser.ConfigParser()
config.read('config.ini')

DISPLAY_WIDTH = int(config['MuMu']['display_width'])    # 游戏画面宽度
DISPLAY_HEIGHT = int(config['MuMu']['display_height'])  # 游戏画面高度
WINDOW_TITLE_PATH = str(config['MuMu']['title_pic'])    # 窗口标题图片
TITLE_HEIGHT = int(config['MuMu']['title_height'])      # 标题栏高度
WINDOW_POSITION = (0, 0)                                # 窗口位置
DISPLAY_LOCATION = (0, 0, 0, 0)                         # 游戏画面位置和大小

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


def initial():
    global WINDOW_POSITION
    global DISPLAY_LOCATION
    global TITLE_HEIGHT
    global WINDOW_TITLE_PATH
    global DISPLAY_HEIGHT
    global DISPLAY_WIDTH
    # pyautogui参数设置
    pag.FAILSAFE = True  # 鼠标移至左上退出模式
    pag.PAUSE = 0.2      # 脚本执行最小间隔时间
    # 获取窗口位置
    while True:
        WINDOW_POSITION = pag.locateOnScreen(WINDOW_TITLE_PATH)
        if WINDOW_POSITION:
            WINDOW_POSITION = (WINDOW_POSITION.left, WINDOW_POSITION.top)
            break
        else:
            pag.alert(text='未找到窗口,请确保窗口非最小化且未被遮挡', title='警告', button='重试')
    # 计算画面位置
    DISPLAY_LOCATION = (WINDOW_POSITION[0], WINDOW_POSITION[1]+TITLE_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    print('WINDOW_POSITION: ', WINDOW_POSITION, '\nDISPLAY_LOCATION: ', DISPLAY_LOCATION)
