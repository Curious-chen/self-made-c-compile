from Targetcode.Demo import *
from Targetcode.table import *
from chensong.code.config import gen_path


class target_Code:
    init = '''
.486   ;指令集
.model flat,stdcall ;模式为flat（平坦）,函数调用方式为stdcall，代表从右到左将函数的参数
;压栈
option casemap:none ;指明大小写敏感
;inclue,includelib导入要用到的库
include     user32.inc
include     windows.inc
includelib  user32.lib
include     kernel32.inc
includelib  kernel32.lib
include     msvcrt.inc
includelib  msvcrt.lib
'''
    # ; .data存放变量
    # ; byte，缩写是db  长度是8位 (char)
    # ;word  缩写是dw，长度是16位 (shot)
    # ;dword 缩写是dd，长度是32位，(int)


    def __init__(self):
        self.code_ = Optimizathon_({})
        # self.code_.Acess_('gen_.txt')
        # self.code_.Acess_('../'+gen_path)
        self.code_.Acess_(gen_path)
        self.qua_list = self.code_.block_dic
        self.Se = Semantic_1()
        self.Se.access_table()
        self.global_var = self.Se.syn_table.globalvar
        self.fun_var = self.Se.syn_table.symDict
        self._data = ['.data', 'RETURN dword ?', "stop byte 'pause', 0", "printf byte '%d ' ,0", "scanf byte '%d',0"]
        # ;.const 里面存放常量
        self._const = ['.const']
        # ;.code是代码段。
        self._code = ['.code']
        pass

    def data_set(self):
        type_ = {'int': 'dd', 'char': 'db'}
        for i in self.global_var.keys():  # 全局变量数据段
            line = self.global_var[i].name + ' ' + type_[self.global_var[i].type] + ' ' + self.global_var[i].value
            self._const.append(line)
        for i in self.fun_var.keys():  # 局部变量
            for per in self.fun_var[i].variableDict.keys():
                var_ = self.fun_var[i].variableDict[per][0]
                if var_.lev != -1:
                    if var_.value == 'undefine':  # 表示只定义未赋值
                        line = var_.name + ' ' + type_[var_.type] + ' ' + '?'
                    else:
                        line = var_.name + ' ' + type_[var_.type] + ' ' + var_.value
                    self._data.append(line)
        for per_fun in self.qua_list:
            for key in per_fun.keys():
                for per in per_fun[key]:
                    if 'T' in per[-1]:
                        line = per[-1] + ' ' + 'dd' + ' ?'
                        if line not in self._data: self._data.append(line)
        # print(self._data)

    def init_gen(self):
        jump_ = {}
        for per_fun in self.qua_list:
            jump_list = []
            list_ = list(per_fun.keys())
            fun_name = ''
            for key in per_fun.keys():
                for per in per_fun[key]:
                    # print(per)
                    if per[1] == '_' and per[2] == '_' and per[3] == '_':
                        fun_name = per[0]
                    if per[0] in ['j', 'j>', 'j<', 'j==', 'jnz', 'continue', 'break']:  # 表示跳转语句
                        jump_list.append(int(per[-1]))  # 记录跳转位置
            jump_[fun_name] = jump_list
        fun_dic = {}
        for per_fun in self.qua_list:
            list_1 = []
            name = ''
            for key in per_fun.keys():
                for per in per_fun[key]:
                    if per[1] == '_' and per[2] == '_' and per[3] == '_':
                        name = per[0]
                    list_1.append(per)
            if name != '':
                fun_dic[name] = copy.deepcopy(list_1)
                jump_[name].append(len(fun_dic[name]))
                jump_[name] = list(set(jump_[name]))
                jump_[name].sort()  # 跳转排序
        print(fun_dic)
        for key in fun_dic.keys():
            strs = ''
            for key_1 in self.fun_var[key].variableDict.keys():
                for per in self.fun_var[key].variableDict[key_1]:
                    if per.lev == -1:
                        strs += per.name + ', '
            strs = strs[0:len(strs) - 2]
            if len(strs) == 0:
                self._code.append(key + ':')
            else:
                self._code.append(key + ' proc ' + strs)
            count = 0
            for index, per in enumerate(fun_dic[key]):
                count = index
                if len(jump_[key]) > 0 and int(jump_[key][0]) == index:
                    line = 'L' + str(jump_[key].pop(0)) + ':'
                    self._code.append(line)
                if per[0] == '+':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'ADD EAX, ' + per[2]
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '-':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'SUB EAX, ' + per[2]
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '*':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'MOV EBX, ' + per[2]
                    self._code.append(line)
                    line = 'MUL ' + 'EBX'
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '/':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'MOV EDX, 0'
                    self._code.append(line)
                    line = 'MOV EBX, ' + per[2]
                    self._code.append(line)
                    line = 'DIV EBX'
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '=':
                    flag = True
                    for i in self._const:
                        if per[-1] in i:
                            flag = False
                            break
                    if flag:
                        line = 'MOV EAX, ' + per[1]
                        self._code.append(line)
                        line = 'MOV ' + per[-1] + ', EAX'
                        self._code.append(line)
                elif per[0] == '++':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'ADD EAX, 1'
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '--':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'SUB EAX, 1'
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '+=':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'ADD EAX, ' + per[-1]
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '-=':
                    line = 'MOV EAX, ' + per[-1]
                    self._code.append(line)
                    line = 'SUB EAX, ' + per[1]
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '*=':
                    line = 'MOV EAX, ' + per[-1]
                    self._code.append(line)
                    line = 'MUL EAX, ' + per[1]
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == '/=':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'DIV EAX, ' + per[-1]
                    self._code.append(line)
                    line = 'MOV ' + per[-1] + ', EAX'
                    self._code.append(line)
                elif per[0] == 'j':
                    line = 'JMP L' + str(per[-1])
                    self._code.append(line)
                elif per[0] == 'j>':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'MOV EBX, ' + per[2]
                    self._code.append(line)
                    line = 'CMP EAX, EBX'
                    self._code.append(line)
                    line = 'JG L' + str(per[-1])
                    self._code.append(line)
                elif per[0] == 'j<':
                    line = 'MOV EAX, ' + per[1]
                    self._code.append(line)
                    line = 'MOV EBX, ' + per[2]
                    self._code.append(line)
                    line = 'CMP EAX, EBX'
                    self._code.append(line)
                    line = 'JL L' + str(per[-1])
                    self._code.append(line)
                elif per[0] == 'jnz':
                    line = 'CMP ' + per[1] + ', 0'
                    self._code.append(line)
                    line = 'JNZ L' + str(per[-1])
                    self._code.append(line)
                elif per[0] == 'ret':
                    line = 'MOV RETURN, EAX'
                    self._code.append(line)
                    self._code.append('RET')
                elif per[0] in list(fun_dic.keys()) and len(per[1]) > 0 and per[1] != '_':
                    line = 'INVOKE ' + per[0]
                    for i in per[1].strip().split(' '):
                        line += ', ' + i
                    self._code.append(line)
                    line = 'MOV EAX,RETURN'
                    self._code.append(line)
                    line = 'MOV ' + per[3] + ', EAX'
                    self._code.append(line)
            if count == len(fun_dic[key]) - 1:
                line = 'L' + str(jump_[key].pop(0)) + ':'
                self._code.append(line)
            if key != 'main':
                self._code.append(key + ' endp')
        self._code.append("invoke  crt_printf,offset printf,eax ; printf(‘%d’,a);")
        self._code.append("invoke crt_system,offset  stop ;system(‘pause’);")
        self._code.append("invoke ExitProcess,1; exit(1)")
        self._code.append('end main')

    def access_target(self):
        list_ = []
        self.data_set()
        self.init_gen()
        print(self.init)
        list_.append(self.init)
        for i in self._const:
            print(i)
            list_.append(i)
        for i in self._data:
            print(i)
            list_.append(i)
        for i in self._code:
            print(i)
            list_.append(i)
        return copy.deepcopy(list_)


if __name__ == '__main__':
    ta = target_Code()
    ta.access_target()
