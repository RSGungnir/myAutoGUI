'''
命运-冠位指定 FGO
游戏脚本，负责将Elf.Worker传入的ins_info(str)转换成相应的instructions(list(str))
instructions必须是基础操作的组合，不可嵌套
'''

import json

with open(r'FGO.json', 'r') as f:
    parameter_set = json.load(f)


def trans(ins_info):
    if ins_info.endswith(')'):
        instructions = exec(f'{ins_info}')
    else:
        instructions = exec(f'{ins_info}()')
    return instructions


def tap(x, y):
    return f'tap(Point({x}, {y}))'


def check(x1, y1, x2, y2, pic):
    return f'waitFor(isPicInArea(Point({x1}, {y1}), Point({x2}, {y2}), {pic}))'


def daily():
    global parameter_set
    ins = []
    # 开始
    ins.append(check(0,0,0,0,None))
    # 点进迦勒底之门
    ins.append(tap(0, 0))
    # 点进种火场
    # 开始刷本，执行3次
    # 结束
    return ins
