from Semantic.Symbol_table import *
from collections import namedtuple


class Semantic_:
    def __init__(self):
        self.lev = 0
        self.error_list, self.token_list = [], []
        self.syn_table = SYMBOL()
        self.Token = namedtuple('Token', 'val typ cur_line cur_col id')

    def read_token_file(self, all_word):
        for index, pre_line in enumerate(all_word):
            self.token_list.append(self.Token(pre_line[0], str(pre_line[1]), pre_line[2], pre_line[3], index))
        self.token_list.append(self.Token('#', '#', '#', '#', len(all_word)))

    def Traver(self):
        index = 0
        lev_stake = []
        sts_stake = []
        while index < len(self.token_list) - 2:
            if self.token_list[index].val == '{':
                lev_stake.append('{')  # 作用域
                self.lev += 1
            if self.token_list[index].val == '}':
                lev_stake.pop()  # 匹配到一个{}则作用域减一
                sts_stake.pop()
                # self.lev -= 1
                '''---------------------常量定义---------------------'''
            if self.token_list[index].val == 'const':  # 代表常量
                type = self.token_list[index].val
                index += 1
                if self.token_list[index].val in ['int', 'char', 'float', 'double',
                                                  'void']:
                    type += (' ' + self.token_list[index].val)  # 变量类型
                    while self.token_list[index].val != ';':
                        if self.token_list[index].val == '=':  # const int a = 123;
                            message = self.syn_table.addVariableToTable(self.token_list[index - 1],
                                                                        type, str(self.token_list[index + 1].val),
                                                                        self.lev,
                                                                        False)
                            if message.ErrorType != None:
                                self.error_list.append(message)
                        index += 1
                else:  # const a = 123;
                    while self.token_list[index].val != ';':
                        if self.token_list[index].val == '=':  # const int a = 123;
                            message = self.syn_table.addVariableToTable(self.token_list[index - 1],
                                                                        type, str(self.token_list[index + 1].val),
                                                                        self.lev,
                                                                        False)
                            if message.ErrorType != None:
                                self.error_list.append(message)
                        index += 1
            '''---------------------调用函数判断参数个数是否匹配---------------------'''
            if self.token_list[index].typ == '700' and self.token_list[index + 1].val == '(' and self.token_list[
                index].val not in ['for', 'while', 'if', 'switch']:  # 调用函数参数个数是否匹配
                message = self.syn_table.checkFunction(self.token_list, self.token_list[index].id)
                if message.ErrorType != None:
                    self.error_list.append(message)
            '''---------------------添加函数名和变量名---------------------'''
            if self.token_list[index].val in ['int', 'char', 'float', 'double', 'void']:
                if self.token_list[index + 2].val == '(':  # 表示函数名
                    sts_stake.append(self.token_list[index + 1].val)  # 函数名
                    message = self.syn_table.addFunction(self.token_list[index + 1], self.token_list[index].val)
                    if message.ErrorType != None:  # 已定义的函数错误
                        self.error_list.append(message)
                    index += 2
                    while self.token_list[index].val != ')':
                        if self.token_list[index].val in ['int', 'char', 'float', 'double']:
                            index += 1  # 指针后移
                            message = self.syn_table.addVariableToTable(self.token_list[index],
                                                                        self.token_list[index - 1].val, 'undefine',
                                                                        self.lev,
                                                                        True)  # 表示函数的形参

                            if message.ErrorType != None:
                                self.error_list.append(message)
                        else:
                            index += 1
                else:  # 表示变量名
                    if self.token_list[index].val in ['int', 'char', 'float', 'double']:
                        type_ = self.token_list[index].val  # 变量名类型
                        while self.token_list[index].val != ';':
                            index += 1
                            if self.token_list[index].typ == '700' and self.token_list[index + 1].val != '=':
                                message = self.syn_table.addVariableToTable(self.token_list[index],
                                                                            type_, 'undefine', self.lev, False)
                                if message.ErrorType != None:
                                    self.error_list.append(message)
                            elif self.token_list[index].typ == '700' and self.token_list[index + 1].val != '==':  # 更新赋值
                                message = self.syn_table.addVariableToTable(self.token_list[index],
                                                                            type_, str(self.token_list[index + 2].val),
                                                                            self.lev, False)
                                if message.ErrorType != None:
                                    self.error_list.append(message)
                    else:
                        index += 1  # 目的是为了进不了if判断则指针后移，继续进行匹配
            '''---------------------判断条件语句内的变量是否引用前定义---------------------'''
            if self.token_list[index].val in ['if', 'switch', 'while', 'for']:  # 判断if、switch、while条件变量是否存在未定义情况
                sts_stake.append(self.token_list[index].val)
                tmp = self.token_list[index].val
                index += 1
                while self.token_list[index].val != ')':
                    if self.token_list[index].typ == '700':  # 如果是标识符
                        message = self.syn_table.checkDoDefineInFunction(self.token_list[index])  # 检查变量是否定义
                        index += 1
                        if message.ErrorType != None:
                            self.error_list.append(message)
                    else:
                        index += 1
            '''---------------------对赋值表达式进行的变量定义、函数调用返回值、参数个数 赋值是否为同类型---------------------'''
            if self.token_list[index].val == '=':  # a = b + c 判断 变量是否定义、是否是同类型变量
                list_ = []
                list_.append(self.token_list[index - 1])
                print(self.token_list[index - 1].typ, self.token_list[index - 1].val)
                if self.token_list[index - 1].typ in ['400', '800']:
                    ErrorType = '赋值错误'
                    Location = {'line': self.token_list[index - 1].cur_line + 1,
                                'col': self.token_list[index - 1].cur_col}
                    ErrorMessage = "变量 '{token}' 赋值错误".format(token=self.token_list[index - 1].val)
                    self.error_list.append(Message(ErrorType, Location, ErrorMessage))
                else:
                    message = self.syn_table.checkDoDefineInFunction(self.token_list[index - 1])
                if message.ErrorType != None:
                    self.error_list.append(message)
                while self.token_list[index].val != ';':  # 一个赋值表达式
                    if self.token_list[index + 2].val == '(' and self.token_list[index + 1].val not in ['+','-','*','/']:  # 表示函数调用参数匹配与否
                        message = self.syn_table.checkFunction(self.token_list,
                                                               self.token_list[index + 1].id)  # 参数个数是否一致
                        list_.append(self.token_list[index + 1])
                        while self.token_list[index + 1].val != ')': index += 1  # 指针移动到函数的)末尾
                        if message.ErrorType != None:
                            self.error_list.append(message)
                    else:  # 变量是否定义
                        if self.token_list[index].typ == '700':
                            message = message = self.syn_table.checkDoDefineInFunction(self.token_list[index])
                            list_.append(self.token_list[index])
                            if message.ErrorType != None:
                                self.error_list.append(message)
                        # if self.token_list[index + 1].val.isdigit():
                        #     list_.append(self.token_list[index + 1])
                    index += 1
                if len(list_) != 0:
                    message = self.syn_table.checkExpType(list_, self.token_list)  # 变量类型不匹配
                    if message.ErrorType != None:
                        self.error_list.append(message)
            if self.token_list[index].val in ['else']: sts_stake.append(self.token_list[index].val)
            '''---------------------对return break continue 在函数中使用是否恰当----------------------'''
            if self.token_list[index].val in ['break', 'continue', 'return']:
                tmp = sts_stake[-1]  # 取出当前作用域中的for switch
                if self.token_list[index].val in ['break', 'continue'] and tmp in ['if', 'else'] and len(
                        sts_stake) >= 2 and sts_stake[-2] in ['for', 'while']:
                    pass
                elif self.token_list[index].val == 'break' and tmp not in ['switch', 'for', 'while']:  # 表示break 位置出错
                    ErrorType = '关键字使用错误'
                    Location = {'line': self.token_list[index].cur_line + 1,
                                'col': self.token_list[index].cur_col}
                    ErrorMessage = "关键字 '{token}' 使用错误".format(token=self.token_list[index].val)
                    message = Message(ErrorType, Location, ErrorMessage)
                    if message.ErrorType != None:
                        self.error_list.append(message)
                elif self.token_list[index].val == 'continue' and tmp not in ['while', 'for']:  # continue 关键字作用范围
                    ErrorType = '关键字使用错误'
                    Location = {'line': self.token_list[index].cur_line + 1,
                                'col': self.token_list[index].cur_col}
                    ErrorMessage = "关键字 '{token}' 使用错误".format(token=self.token_list[index].val)
                    message = Message(ErrorType, Location, ErrorMessage)
                    if message.ErrorType != None:
                        self.error_list.append(message)
                else:
                    index += 1  # 将当前指针后移指向表达式的最开始
                    message = self.syn_table.checkReturn(self.token_list, index)
                    if message.ErrorType != None:
                        self.error_list.append(message)
            index += 1  # 匹配完成则指针后移进行新的一轮匹配

    def access(self, token_list):
        self.read_token_file(token_list)
        self.Traver()
        self.syn_table.showTheInfo()
        for i in self.syn_table.symbolTableInfo:
            print(i)
        for j in self.error_list:
            print(j)


if __name__ == '__main__':
    S = Semantic_()
    S.Traver()
    S.syn_table.showTheInfo()
    for i in S.syn_table.symbolTableInfo:
        print(i)
    for j in S.error_list:
        print(j)
