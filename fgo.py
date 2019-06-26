'''
命运-冠位指定 Fate/Grand Order
'''

from General import *
import pyautogui as pag

RUN = 1

class Operator:
    def __init__(self):
        pass
    
    def operate(self, cmd):
        cmd = cmd.split(' ')
        exp = r'self.{fun}(*{par})'.format(fun=cmd[0], par=cmd[1:])
        try:
            eval(exp)
        except AttributeError as e:
            print('AttributeError', e)
    
    def act(self, *args):
        pass
    
    def quit(self, *args):
        global RUN
        RUN = 0


def main():
    op = Operator()
    while RUN:
        op.operate(input())


if __name__ == '__main__':
    main()
