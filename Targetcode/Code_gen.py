import copy
from collections import defaultdict
from Targetcode.Demo import *


class Aim_code_:

    def __init__(self):
        self.code_ = Optimizathon_({})
        self.code_.Acess_('../Semantic/gen_.txt')
        self.aim_code_list = []
        self.op2asm = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '<': 'JL',
            '>': 'JR',
            '>=': 'JRE',
            '<=': 'JLE',
            '==': 'JNE',
            '!=': 'NEQ',

        }
        pass

    def init_(self):
        for per_fun in self.code_.block_dic:
            for key in per_fun.keys():
                for per in per_fun[key]:
                    if per[1] == '_' and per[2] == '_' and per[3] == '_':  # 表示函数定义
                        self.aim_code_list.extend([('PUSH', 'BP'), ('MOV', 'BP', ',', 'SP'), ('SUB', 'SP')])
                    elif per[0] == '+':
                        self.aim_code_list.extend(
                            [('MOV', 'AX', ',', per[1]), (self.op2asm[per[0]], 'AX', ',', per[2]),
                             ('MOV', per[3], ',', 'AX')])
                    elif per[0] == '-':
                        self.aim_code_list.extend(
                            [('MOV', 'AX', ',', per[1]), (self.op2asm[per[0]], 'AX', ',', per[2]),
                             ('MOV', per[3], ',', 'AX')])
                    elif per[0] == '*':
                        self.aim_code_list.extend(
                            [('MOV', 'AX', ',', per[1]), ('MOV', 'BX', ',', per[2]), (self.op2asm[per[0]], 'BX'),
                             ('MOV', per[3], ',', 'AX')])
                    elif per[0] == '/':
                        self.aim_code_list.extend(
                            [('MOV', 'AX', ',', per[1]), ('MOV', 'DX', ',', '0'), ('MOV', 'AX', ',', per[2]),
                             (self.op2asm[per[0]], 'BX'), ('MOV', per[3], ',', 'AX')])
                    elif per[0] == '%':
                        self.aim_code_list.extend(
                            [('MOV', 'AX', ',', per[1]), ('MOV', 'DX', ',', '0'), ('MOV', 'AX', ',', per[2]),
                             (self.op2asm[per[0]], 'BX'), ('MOV', per[3], ',', 'DX')])
                    elif per[0] == '||':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', '0'),
                             ('JNE', '_OR'), ('MOV', 'AX', ',', per[2]), ('CMP', 'AX', ',', '0'), ('JNE', '_OR'),
                             ('MOV', 'DX', ',', '0'),
                             ('_OR:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == '&&':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '0'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', '0'),
                             ('JE', '_AND'), ('MOV', 'AX', ',', per[2]), ('CMP', 'AX', ',', '0'), ('JE', '_AND'),
                             ('MOV', 'DX', ',', '1'),
                             ('_AND:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == '<':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JB', '_LT'), ('MOV', 'DX', ',', '0'), ('_LT:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == '>=':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JNB', '_GE'), ('MOV', 'DX', ',', '0'), ('_GE:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == '>':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JA', '_GT'), ('MOV', 'DX', ',', '0'), ('_GT:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == '<=':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JNA', '_LE'), ('MOV', 'DX', ',', '0'), ('_LE:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == '==':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JE', '_EQ'), ('MOV', 'DX', ',', '0'), ('_EQ:', 'MOV', 'T', ',', 'DX')])
                    elif per[0] == 'jnz':
                        self.aim_code_list.extend(
                            [('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', '0'),
                             ('JE', '_EZ'), ('JMP', 'far', 'ptr', per[-1]), ('_EZ:', 'NOP')])
                    elif per[0] == 'j':
                        self.aim_code_list.extend([('JMP', 'far', 'ptr', per[-1])])
                    elif per[0] == 'j<':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JB', '_LT'), ('JMP', 'far', 'ptr', per[-1]), ('_LT:', 'NOP')])
                    elif per[0] == 'j<':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JB', '_LT'), ('JMP', 'far', 'ptr', per[-1]), ('_LT:', 'NOP')])
                    elif per[0] == 'j>':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JA', '_GT'), ('JMP', 'far', 'ptr', per[-1]), ('_GT:', 'NOP')])
                    elif per[0] == 'j<=':
                        self.aim_code_list.extend(
                            [('MOV', 'DX', ',', '1'), ('MOV', 'AX', ',', per[1]), ('CMP', 'AX', ',', per[2]),
                             ('JNA', '_LE'), ('JMP', 'far', 'ptr', per[-1]), ('_GT:', 'NOP')])
        for i in self.aim_code_list:
            for j in i:
                print(j, end=' ')
            print()


if __name__ == '__main__':
    code = Aim_code()
    code.init_()
