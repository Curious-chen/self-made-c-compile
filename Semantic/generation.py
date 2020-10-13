# from Semantic.Semantic_analysis import *
from Semantic.Sentence import *
from collections import namedtuple
import copy


class Genration_:
    '''
    参数说明
    self.token_list:存储token信息
    self.sen_list:存储四元式信息
    self.FC:存储if..的假出口
    self.or_TC_list:用于存储or的真出口，便于回填
    self.jump_list: 存储if-else中if为真执行完成后四元式('j,'_','_',0)
    self.out_list；结果输出列表
    self.count:记录if嵌套层次
    self.flag:记录是否存在if-else if级联
    '''

    def __init__(self):
        # self.S = Semantic_()
        self.Token = namedtuple('Token', 'val typ cur_line id')
        self.token_list, self.sen_list, self.FC, self.lev_stake, self.or_TC_list, self.jump_list, self.out_list, self.break_list, self.contnue_list = [], [], [], [], [], [], [], [], []
        self.NQT, self.n, self.TC, self.lev, self.index, self.count = 0, 0, 0, 0, 0, 0
        self.flag = True
        pass

    def read_token_file(self, all_word):
        for index, pre_line in enumerate(all_word):
            self.token_list.append(self.Token(pre_line[0], str(pre_line[1]), pre_line[3], index))

    def Executing(self, token):
        self.FC.append([-1, -1])
        self.jump_list.append([-1, -1])
        self.break_list.append([-1, -1])
        self.contnue_list.append([-1, -1])
        while self.index < len(token) - 2:
            if self.token_list[self.index].val == '{':
                self.lev_stake.append('{')  # 作用域
                self.lev += 1
            if self.token_list[self.index].val == '}':
                self.lev_stake.pop()  # 匹配到一个{}则作用域减一
            self.func(token)
            self.fun_call(token)
            self.call_fun(token)
            self.assign(token)
            if self.token_list[self.index].val == 'if':
                self.index += 1
                self.ifs(token)
            if self.token_list[self.index].val == 'while':
                self.index += 1
                self.whiles(token)
            if self.token_list[self.index].val == 'for':
                self.index += 1
                self.fors(token)
            if self.token_list[self.index].val == 'do':
                self.index += 1
                self.do_whiles(token)
            self.index += 1
            pass

    def func(self, token):
        if token[self.index].val in ['void', 'int', 'char', 'float', 'double'] and token[
            self.index + 1].typ == '700' and token[
            self.index + 2].val == '(':  # 函数定义生成四元式
            tmp = token[self.index + 1].val
            self.index += 2
            if token[self.index].val == '(':
                while token[self.index].val != ')':
                    self.index += 1
            if token[self.index].val == ')': self.index += 1
            if token[self.index].val == '{':
                self.lev_stake.append('{')
                self.lev += 1
                self.index += 1
                self.sen_list.append(Sentence_(self.NQT, tmp, '_', '_', '_'))
                self.NQT += 1
        if token[self.index].val == 'return':  # 表示return的值
            self.index += 1
            bterm = []
            while token[self.index].val != ';':
                bterm.append(token[self.index])  # 记录表达式
                self.index += 1
            tn = self.Reverse_Polish(bterm)
            self.sen_list.append(Sentence_(self.NQT, 'ret', '_', '_', tn))
            self.NQT += 1

    def call_fun(self, token):
        if token[self.index].typ == '700' and token[self.index + 1].val == '(':  # Demo(a,b)
            call_name = token[self.index].val
            self.index += 2
            bterm = []
            while token[self.index].val != ';':  # 遍历形式参数
                if token[self.index].val == ',':
                    bterm.append(token[self.index].val)
                else:
                    bterm.append(token[self.index])
                self.index += 1
            bterm = bterm[0:len(bterm) - 1]
            bterm1, list_, t = [], [], 0
            for index, pre in enumerate(bterm):
                if pre != ',':
                    bterm1.append(pre)
                else:
                    t = index
                    list_.append(copy.deepcopy(bterm1))
                    bterm1.clear()
                if index == len(bterm) - 1:
                    list_.append(bterm[t + 1:])
            for pre_bterm in list_:
                tn = self.Reverse_Polish(pre_bterm)
                self.sen_list.append(Sentence_(self.NQT, 'para', tn, '_', '_'))
                self.NQT += 1
            self.sen_list.append(Sentence_(self.NQT, 'call', call_name, '_', '_'))
            self.NQT += 1

    def fun_call(self, token):
        if token[self.index].typ == '700' and token[self.index + 1].val == '=' and token[
            self.index + 2].typ == '700' and token[self.index + 3].val == '(':  # a = DEMO()
            var = token[self.index].val
            fun_name = token[self.index + 2].val
            self.index += 3
            list_ = []
            while token[self.index].val != ';':  # 表达式结束
                if token[self.index].val not in ['(', ')', ',']:
                    list_.append(token[self.index].val)
                self.index += 1
            strs = ' '.join(list_)
            self.sen_list.append(Sentence_(self.NQT, fun_name, strs, '_', var))
            self.NQT += 1

    def assign(self, token):
        if token[self.index].typ == '700' and token[self.index + 1].val in ['=', '+=', '-=', '/=', '*=', '%=', '++',
                                                                            '--']:  # a = 2*3+5
            if token[self.index + 1].val in ['=', '+=', '-=', '/=', '*=', '%=']:
                bterm = []
                s = token[self.index].val
                op = token[self.index + 1].val
                self.index += 2  # 将指针指向表达式开始的第一个位置
                while token[self.index].val != ';':  # 表达式结束
                    if token[self.index].val == '++':
                        bterm.append(token[self.index].val)
                    else:
                        bterm.append(token[self.index])
                    self.index += 1
                if (len(bterm) == 1):
                    self.sen_list.append(Sentence_(self.NQT, op, bterm[0].val, '_', s))
                    self.NQT += 1
                else:
                    if '++' in bterm:
                        _op = bterm[-1]  # 记录运算符++\--
                        bterm = bterm[0:len(bterm) - 1]  # 去掉++
                        tn = self.Reverse_Polish(bterm)
                        tn1 = 'T' + str(self.n)
                        self.n += 1
                        self.sen_list.append(Sentence_(self.NQT, op, tn, '_', s))
                        self.NQT += 1
                        self.sen_list.append(Sentence_(self.NQT, op, tn, '1', tn1))
                        self.NQT += 1
                        self.sen_list.append(Sentence_(self.NQT, '=', tn1, '_', s))
                        self.NQT += 1
                    else:
                        tn = self.Reverse_Polish(bterm)
                        self.sen_list.append(Sentence_(self.NQT, op, tn, '_', s))
                        self.NQT += 1
            else:
                s = token[self.index].val
                op = token[self.index + 1].val
                self.index += 2  # 将指针指向表达式开始的第一个位置
                tn = 'T' + str(self.n)
                self.n += 1
                self.sen_list.append(Sentence_(self.NQT, op[0:1], s, '1', tn))
                self.NQT += 1
                self.sen_list.append(Sentence_(self.NQT, '=', tn, '_', s))
                self.NQT += 1

    def break_(self, token):
        if token[self.index].val == 'break':
            fc = [self.NQT, self.lev]
            self.break_list.append(fc)  # 存储假出口回填
            self.sen_list.append(Sentence_(self.NQT, 'break', '_', '_', '0'))  # if语句执行完成后应跳出if语句不再执行else后的语句,待回填
            self.NQT += 1
        if token[self.index].val == 'continue':
            fc = [self.NQT, self.lev]
            self.contnue_list.append(fc)  # 存储假出口回填
            self.sen_list.append(Sentence_(self.NQT, 'con', '_', '_', '0'))  # if语句执行完成后应跳出if语句不再执行else后的语句,待回填
            self.NQT += 1

    def if_(self, token):
        self.count += 1
        self.Logic(token)
        self.backpatch(self.NQT, self.TC)  # 回填if的真出口
        while len(self.or_TC_list) != 0:
            t = self.or_TC_list.pop()
            self.backpatch(self.NQT, t)  # 回填if的真出口
        if token[self.index].val == ')': self.index += 1
        self.next_(token)

    def ifs(self, token):
        flag, flag1 = True, True
        self.if_(token)
        # if token[self.index].val == '}': self.index += 1
        if token[self.index].val == 'else' and token[self.index + 1].val == 'if': flag = False
        if token[self.index + 1].val == 'else':
            self.index += 1
            fc = [self.NQT, self.lev]
            self.jump_list.append(fc)  # 存储假出口回填
            self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', '0'))  # if语句执行完成后应跳出if语句不再执行else后的语句,待回填
            self.NQT += 1
            new_tmp = self.NQT
            while self.FC[len(self.FC) - 1][1] == self.lev - 1:  # 寻找if的加出口位置
                fc1 = self.FC.pop()
                if len(fc1) == 3:
                    self.backpatch(self.NQT, fc1[0])
                else:
                    self.backpatch(new_tmp, fc1[0])
                new_tmp = fc1[0] - 1
            self.lev -= 1  # 为了回填嵌套if语句上一层if的出口
            self.next_(token)
            if not flag:  # 回填 if 嵌套 if的假出口
                while self.FC[len(self.FC) - 1][1] == self.lev + 1:  # 寻找else语句的出口 lev+1的原因是填级联上一层的假出口
                    fc1 = self.FC.pop()
                    self.backpatch(self.NQT, fc1[0])
                self.lev -= 1
            else:  # 回填最外层if存在else的情况
                while self.FC[len(self.FC) - 1][1] == self.lev:  # 寻找else语句的出口
                    fc1 = self.FC.pop()
                    self.backpatch(self.NQT, fc1[0])
                self.lev -= 1
            while self.jump_list[len(self.jump_list) - 1][1] == self.lev + 1:
                fc2 = self.jump_list.pop()
                self.backpatch(self.NQT, fc2[0])
                # self.lev -= 1
            self.count -= 1

        else:
            self.count -= 1
            if not flag:  # 回填if-else_if级联最外层if的假出口
                self.backpatch_()
            elif flag:  # #回填if且无级联和else的假出口
                self.backpatch_()
            while self.jump_list[len(self.jump_list) - 1][1] == self.lev:
                fc2 = self.jump_list.pop()
                self.backpatch(self.NQT, fc2[0])
                self.lev -= 1

    def whiles(self, token):
        in_ = self.NQT  # 记录入口
        self.Logic(token)  # while条件生成四元式
        if token[self.index].val == ')': self.index += 1
        self.backpatch(self.NQT, self.TC)
        while len(self.or_TC_list) != 0:
            t = self.or_TC_list.pop()
            self.backpatch(self.NQT, t)  # 回填if的真出口
        self.next_(token)
        self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', in_))
        self.NQT += 1
        self.backpatch_()
        self.backpatch_while(in_)

    def fors_init(self, token):
        bterm = []
        if token[self.index].val == '(': self.index += 1
        while token[self.index].val != '{':
            if token[self.index].val == ';':
                bterm.append(token[self.index].val)
            else:
                bterm.append(token[self.index])
            self.index += 1
        bterm = bterm[0:len(bterm) - 1]
        bterm1, list_, t = [], [], 0
        for index, pre in enumerate(bterm):
            if pre != ';':
                bterm1.append(pre)
            else:
                t = index
                list_.append(copy.deepcopy(bterm1))
                bterm1.clear()
            if index == len(bterm) - 1:
                list_.append(bterm[t + 1:])
        return list_

    def fors(self, token):
        flag, in_ = 0, 0  # 循环入口
        list_ = self.fors_init(token)
        for pre_bterm in list_:
            index = 0
            if pre_bterm[index].typ == '700' and pre_bterm[index + 1].val in ['=', '>', '<', '<=', '>=', '++', '--']:
                if pre_bterm[index + 1].val in ['>', '<', '<=', '>=']: flag = self.NQT  # 循环判断入口
                idf = pre_bterm[index].val
                op = pre_bterm[index + 1].val
                index += 2
                bterm, bt = [], ''
                if op not in ['++', '--']:
                    while index < len(pre_bterm):
                        bterm.append(pre_bterm[index])
                        index += 1
                    bt = self.Reverse_Polish(bterm)
                else:
                    bt = 'T' + str(self.n)
                    self.n += 1
                if op in ['>', '<', '<=', '>=']:  # 表示判断条件
                    self.TC = self.NQT  # 记录真出口的下标位置
                    self.sen_list.append(Sentence_(self.NQT, 'j' + op, idf, bt, '0'))  # 真出口待回填
                    self.NQT += 1
                    self.FC.append([self.NQT, self.lev])
                    self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', '0'))  # 假出口待回填
                    self.NQT += 1
                    in_ = self.NQT  # 循环入口
                elif op in ['++', '--']:
                    # tn = 'T' + str(self.n)
                    # self.n += 1
                    self.sen_list.append(Sentence_(self.NQT, op[0:1], idf, '1', bt))
                    self.NQT += 1
                    self.sen_list.append(Sentence_(self.NQT, '=', bt, '_', idf))
                    self.NQT += 1
                else:
                    self.sen_list.append(Sentence_(self.NQT, op, bt, '_', idf))
                    self.NQT += 1
        self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', flag))  # 循环
        self.NQT += 1
        self.backpatch(self.NQT, self.TC)  # 回填真出口进行for语句内部
        if token[self.index].val == ')': self.index += 1
        self.next_(token)
        self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', in_))  # 循环条件+1
        self.NQT += 1
        self.backpatch_()
        self.backpatch_while(in_)

    def do_whiles(self, token):
        flag = self.NQT  # do的入口
        self.next_(token)
        while token[self.index].val != '(':
            self.index += 1
        self.Logic(token)
        if token[self.index].val == ')': self.index += 1
        self.backpatch(flag, self.TC)
        # self.backpatch(self.NQT, self.TC)
        while len(self.or_TC_list) != 0:
            t = self.or_TC_list.pop()
            self.backpatch(flag, t)  # 回填if的真出口
        self.lev += 1
        self.backpatch_()
        self.lev -= 1
        self.backpatch_while(flag)

    def Reverse_Polish(self, bterm):  # 计算逆波兰式
        s = ''
        if len(bterm) == 0:
            return '_'
        if len(bterm) == 1:
            return bterm[0].val
        i = 0
        stack1, stack2 = [], []  # stack1存储操作失 stack2存储运算符
        stack1.append('#')  # 防止栈空
        while (i < len(bterm)):
            ch = bterm[i]
            i += 1
            if (ch.typ in ['400', '700', '800'] and ch.val not in ['+', '-', '*', '/', '%', '||', '&&']):
                stack2.append(ch.val)
                # top2 += 1
            else:
                if ch.val == '(':
                    stack1.append('(')
                elif ch.val == ')':
                    while stack1[len(stack1) - 1] != '(':
                        stack2.append(stack1[len(stack1) - 1])
                        stack1.pop()
                    stack1.pop()  # 删除多余的括号
                else:  # 判断优先级 * / + -
                    if stack1[len(stack1) - 1] == '(':
                        stack1.append(ch.val)
                    else:
                        t = stack1[len(stack1) - 1]
                        if self.Priority(t) > self.Priority(ch.val):
                            stack2.append(stack1.pop())
                        stack1.append(ch.val)
        while len(stack1) > 1:
            tmp = stack1.pop()
            stack2.append(tmp)
        for i_ in stack2:
            print(i_, end=' ')
        stack = []  # 存储结果
        top = 0
        for index in range(0, len(stack2)):
            if stack2[index] not in ['+', '-', '*', '/', '%', '||', '&&']:
                stack.append(stack2[index])
                top += 1
            else:
                s = 'T' + str(self.n)
                self.sen_list.append(Sentence_(self.NQT, stack2[index], stack[top - 2], stack[top - 1], s))
                top -= 2
                stack = stack[0:top]
                stack.append(s)
                top += 1
                self.n += 1
                self.NQT += 1
        return s
        pass

    def Priority(self, t):
        if t == '*':
            return 4
        if t == '/':
            return 4
        if t == '%':
            return 4
        if t == '+':
            return 3
        if t == '-':
            return 3
        if t == '&&':
            return 2
        if t == '||':
            return 1
        return 0

    def Logic(self, token):
        self.Logic_1(token)
        if token[self.index].val == '||':
            self.or_TC_list.append(self.TC)
            self.Logic(token)

    def Logic_1(self, token):
        self.Logic_2(token)
        if token[self.index].val == '&&':
            fc = self.FC.pop()
            fc.append('&&')
            self.FC.append(fc)
            self.backpatch(self.NQT, self.TC)
            self.TC = self.NQT
            self.Logic_1(token)

    def Logic_2(self, token):
        self.index += 1
        if token[self.index].val == '!':  # ！的优先级最高
            self.Logic(token)
        else:
            if token[self.index].val == '(':  # 匹配表达式
                self.Logic(token)
                if token[self.index].val == ')':
                    self.index += 1
            else:
                bterm = []
                while token[self.index].val not in ['>', '>=', '<', '<=', '==', '!=', '&&', '||', '!'] and token[
                    self.index].val != ')':
                    bterm.append(token[self.index])
                    self.index += 1
                tn = self.Reverse_Polish(bterm)
                if token[self.index].val in ['>', '>=', '<', '<=', '==', '!=']:  # 判断是关系运算还是布尔运算
                    op = token[self.index].val
                    self.index += 1
                    bterm1 = []
                    while token[self.index].val not in ['>', '>=', '<', '<=', '==', '!=', '||', '&&', '!'] and token[
                        self.index].val != ')':
                        bterm1.append(token[self.index])
                        self.index += 1
                    tn1 = self.Reverse_Polish(bterm1)
                    self.TC = self.NQT
                    self.sen_list.append(Sentence_(self.NQT, 'j' + op, tn, tn1, '0'))  # 待回填
                    self.NQT += 1
                    self.FC.append([self.NQT, self.lev])
                    self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', '0'))  # 待回填
                    self.NQT += 1
                else:
                    self.TC = self.NQT  # 记录真出口位置
                    self.sen_list.append(Sentence_(self.NQT, 'jnz', tn, '_', '0'))  # 待回填
                    self.NQT += 1
                    self.FC.append([self.NQT, self.lev])
                    self.sen_list.append(Sentence_(self.NQT, 'j', '_', '_', '0'))  # 待回填
                    self.NQT += 1

    def all_stas(self, token):
        if token[self.index].val in ['if', 'for', 'while', 'do']:
            self.com_sta(token)
        if token[self.index].typ == '700' and token[self.index].val not in ['if', 'for', 'while', 'do']:
            self.fun_call(token)
            self.assign(token)  # 赋值语句
        # if token[self.index].typ == '700' and token[self.index + 1].val == '=' and token[
        #     self.index + 2].typ == '700' and token[self.index + 3].val == '(':  # a = DEMO()
        if token[self.index].typ == '700' and token[self.index + 1].val == '(':  # Demo(a,b)
            self.call_fun(token)
        if token[self.index].val == 'break' or token[self.index].val == 'continue':
            self.break_(token)
        if token[self.index].val == '{':
            self.lev_stake.append('{')
            self.lev += 1
        if token[self.index].val == '}':
            self.lev_stake.pop()
        self.index += 1

    def com_sta(self, token):
        if token[self.index].val == 'if':
            self.index += 1
            self.ifs(token)
        elif token[self.index].val == 'while':
            self.index += 1
            self.whiles(token)
        elif token[self.index].val == 'for':
            self.index += 1
            self.fors(token)
        elif token[self.index].val == 'do':
            self.index += 1
            self.do_whiles(token)

    def backpatch(self, out, nxt):
        self.sen_list[nxt].setRes(out)

    def backpatch_(self):
        new_tmp = self.NQT
        while self.FC[len(self.FC) - 1][1] == self.lev - 1:  # 寻找if的加出口位置
            fc1 = self.FC.pop()
            if len(fc1) == 3:
                self.backpatch(self.sen_list[new_tmp + 1].res, fc1[0])
            else:
                self.backpatch(new_tmp, fc1[0])
            new_tmp = fc1[0] - 1
        self.lev -= 1  # 为了回填嵌套if语句上一层if的出口

    def backpatch_while(self, in_):
        if len(self.break_list) > 1:
            while self.break_list[len(self.break_list) - 1][1] == self.lev + 2:  # 寻找if的加出口位置
                fc1 = self.break_list.pop()
                self.backpatch(self.NQT, fc1[0])
        if len(self.contnue_list) > 1:
            while self.contnue_list[len(self.contnue_list) - 1][1] == self.lev + 2:  # 寻找if的加出口位置
                fc1 = self.contnue_list.pop()
                self.backpatch(in_, fc1[0])

    def next_(self, token):
        while token[self.index].val != '}':
            self.all_stas(token)  # 生成while体内的四元式

    def out_gen(self):
        for i in self.sen_list:
            self.out_list.append(
                "       {:<4s}: ( {:<4s}, {:<4s}, {:<4s}, {:<4s} )".format(str(i.id), str(i.op), str(i.n1), str(i.n2),
                                                                           str(i.res)))

    def Acess_gen(self, all_word):
        self.read_token_file(all_word)
        self.Executing(self.token_list)
        self.out_gen()
        print(self.sen_list)


if __name__ == '__main__':
    G = Genration_()
    G.Executing(G.token_list)
    print()
    for i in G.sen_list:
        print("{:<3s}: ( {:<3s} {:<3s} {:<3s} {:<3s} )".format(str(i.id), str(i.op), str(i.n1), str(i.n2), str(i.res)))
    pass
