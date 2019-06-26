'''
命运-冠位指定 Fate/Grand Order
'''

from General import *
import pyautogui as pag

RUN = 1

class Operator:
    def __init__(self):
        self.instructions = {'daily':''}
        print('operator done')
    
    def operate(self, cmd):
        cmd = cmd.split()
        if len(cmd) == 1:
            exp = r'self.{fun}()'.format(fun=cmd[0])
        else:
            exp = r'self.{fun}({par})'.format(fun=cmd[0], par=cmd[1])
        try:
            eval(exp)
        except AttributeError:
            print(cmd[0],'not defined')
    
    def run(self, par):
        try:
            instruction = self.instruction[par]
            
        except KeyError:
            print('no "{}" option'.format(par))
    
    def quit(self, *args):
        global RUN
        RUN = 0


def main():
    op = Operator()
    initial()
    print('initial done')
    while RUN:
        op.operate(input())


if __name__ == '__main__':
    main()
