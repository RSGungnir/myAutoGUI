'''
命运-冠位指定 Fate/Grand Order
'''

from General import *
import pyautogui as pag
import json

GAME = 'FGO'
SCRIPT_PATH = r'.\scripts\FGO.json'
RUN = 1
initial()

class Orderer:
    def __init__(self):
        global GAME
        global SCRIPT_PATH
        with open(SCRIPT_PATH, 'r') as f:
            self.instruction_set = json.load(f)
        self.executor = Executor(GAME)
    
    def order(self, cmd):
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
            instructions = self.instruction_set[par]
            self.executor.reader(instructions)
        except KeyError:
            print('no "{}" option'.format(par))
            # TODO: Guess what the actual command is and give suggestion.
    
    def quit(self, *args):
        global RUN
        RUN = 0


def main():
    op = Operator()
    while RUN:
        op.operate(input())


if __name__ == '__main__':
    main()
