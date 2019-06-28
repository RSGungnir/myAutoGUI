'''
命运-冠位指定 FGO
游戏脚本，负责将Elf.Worker传入的ins_info(str)转换成相应的instructions(list(str))
instructions必须是基础操作的组合，不可嵌套
'''

import json

with open(r'FGO.json', 'r') as f:
    parameter_set = json.load(f)


def trans(ins_info):
    instructions = exec(f'{ins_info}()')
    return instructions


def daily():
    ins = ''
    # 开始
    # 点进迦勒底之门
    # 点进种火场
    # 开始刷本，执行3次
    # 结束
    pass


def tap(p):
    x, y = p
    return f'tap(Point({x}, {y}))'
