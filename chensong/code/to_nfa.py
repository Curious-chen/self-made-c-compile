"""
    将正规式转化为等价的nfa

"""

import pandas as pd
import string
import re
from chensong.code.model import draw

# 算符优先表
operator_table = pd.DataFrame(columns=['.', '|', '(', ')', '*', '#'], index=['.', '|', '(', ')', '*', '#'],
                              data=[[1, 1, -1, 1, -1, 1], [-1, 1, -1, 1, -1, 1], [-1, -1, -1, 0, -1, 2],
                                    [1, 1, 2, 1, 1, 1], [1, 1, 2, 1, 1, 1], [-1, -1, -1, 2, -1, 0]])


class NFA:
    def __init__(self, regular):
        # 接受正规式
        self.regular = regular
        self.node_i = 0
        # 表示经过字符varch,从from到to状态
        self.nfa_dict = {'from': [], 'to': [], 'varch': [], 'start': [], 'end': []}
        # 弧的队列
        self.arc_queue = {}

    # 检查正规式是否合法
    def verify(self):
        pass

    # 识别a的正规式
    def create_NFA_a(self, a):
        # 获得节点编号
        self.nfa_dict['from'].append(self.node_i)
        # 获得第二节点编号
        self.node_i += 1
        self.nfa_dict['to'].append(self.node_i)
        # 添加边
        self.nfa_dict['varch'].append(a)
        self.node_i += 1

    def create_NFA_or(self, s, t):
        # 空弧1
        self.nfa_dict['from'].append(self.node_i)
        self.nfa_dict['to'].append(s)
        self.nfa_dict['varch'].append('ε')
        # 空弧2
        self.nfa_dict['from'].append(self.node_i)
        self.nfa_dict['to'].append(t)
        self.nfa_dict['varch'].append('ε')
        self.node_i += 1
        # 空弧3
        self.nfa_dict['from'].append(self.arc_queue[s])
        self.nfa_dict['to'].append(self.node_i)
        self.nfa_dict['varch'].append('ε')
        # 空弧4
        self.nfa_dict['from'].append(self.arc_queue[t])
        self.nfa_dict['to'].append(self.node_i)
        self.nfa_dict['varch'].append('ε')
        self.node_i += 1

    def create_NFA_connect(self, s, t):
        end_s = self.arc_queue[s]
        for i in range(len(self.nfa_dict['from'])):
            if self.nfa_dict['from'][i] == t:
                self.nfa_dict['from'][i] = end_s
        # NFA的弧入队列
        end_t = self.arc_queue[t]
        # 构建 a.b的弧
        self.arc_queue[s] = end_t
        self.arc_queue.pop(t)

    def create_NFA_closure(self, s):
        end_s = self.arc_queue[s]
        # 引一条空弧 从ends->s
        self.nfa_dict['from'].append(end_s)
        self.nfa_dict['to'].append(s)
        self.nfa_dict['varch'].append('ε')

        # 引一条空弧 从new_s -> s
        self.nfa_dict['from'].append(self.node_i)
        self.nfa_dict['to'].append(s)
        self.nfa_dict['varch'].append('ε')
        self.node_i += 1

        # 引一条空弧 从end_s -> new_ens_s
        self.nfa_dict['from'].append(end_s)
        self.nfa_dict['to'].append(self.node_i)
        self.nfa_dict['varch'].append('ε')
        self.node_i += 1
        # 引一条空弧从 从new_s -> new_ens_s
        self.nfa_dict['from'].append(self.node_i - 2)
        self.nfa_dict['to'].append(self.node_i - 1)
        self.nfa_dict['varch'].append('ε')

    # 添加连接符。
    def add_point(self):
        reu = re.compile(r'[a-zA-Z0-9]+')
        new_char, i = '', 0
        while i < len(self.regular) - 1:
            a, b = self.regular[i], self.regular[i + 1]
            # [a.b]
            if reu.match(a) and reu.match(b):
                new_char += a + '.'
            # [a.(]
            elif reu.match(a) and b == '(':
                new_char += a + '.'
            # [*.a],[).a]
            elif (a in ['*', ')']) and reu.match(b):
                new_char += a + '.'
            # [*.(],[).(]
            elif (a in ['*', ')']) and (b == '('):
                new_char += a + '.'
            else:
                new_char += a
            i += 1
        new_char += self.regular[-1]
        return new_char

    def to_nfa(self):
        # 匹配数字或字母
        reu = re.compile(r'[a-zA-Z0-9]+')
        # ‘#’入符号栈
        char_stack = ['#']
        # 状态栈
        state_stack = []
        # 将输入串中的连接用'.'代替
        new_char = self.add_point()
        # 添加终结标识符'#'
        new_char += '#'
        i = 0
        while (new_char[i] != '#') or (char_stack[-1] != '#'):
            if reu.match(new_char[i]):  # 是操作数
                # 构建正规式a的NFA
                self.create_NFA_a(new_char[i])
                # # NFA的弧入队列
                self.arc_queue[self.node_i - 2] = self.node_i - 1
                # 起始节点入状态栈
                state_stack.append(self.node_i - 2)
            else:
                compare_i = operator_table.loc[char_stack[-1], new_char[i]]
                # < 将符号加入符号栈
                if compare_i == -1:
                    char_stack.append(new_char[i])
                # = 弹出符号栈元素
                elif compare_i == 0:
                    char_stack.pop()
                # > 进行规约
                elif compare_i == 1:
                    char_stack_top = char_stack.pop()
                    if char_stack_top == '|':
                        s = state_stack.pop()
                        t = state_stack.pop()
                        # 构造识别正规式s|t的NFA
                        self.create_NFA_or(s, t)
                        # NFA的弧入队列
                        self.arc_queue[self.node_i - 2] = self.node_i - 1
                        # 起始节点入状态栈
                        state_stack.append(self.node_i - 2)
                        continue
                    elif char_stack_top == '.':
                        s = state_stack.pop()
                        t = state_stack.pop()
                        # 构造识别正规式s.t的NFA
                        self.create_NFA_connect(t, s)
                        # NFA的弧入队列已在构造NFA中完成
                        # 起始结点入状态栈
                        state_stack.append(t)
                        continue
                    elif char_stack_top == '*':
                        s = state_stack.pop()
                        # 构造识别正规式s*的NFA
                        self.create_NFA_closure(s)
                        # 构建闭包块所对应的弧
                        self.arc_queue[self.node_i - 2] = self.node_i - 1
                        state_stack.append(self.node_i - 2)
                        continue
                    else:
                        return -1
                else:
                    return -1
            # 若能规约，则不将当前操作符出栈
            i += 1
        # 把状态栈顶的元素出栈
        # 整个正规式的起点
        start = state_stack.pop()
        end = self.arc_queue[start]
        self.nfa_dict['start'].append(start)
        self.nfa_dict['end'].append(end)
        # draw(self.nfa_dict['start'], self.nfa_dict['end'])
        # output_table()
        return self.nfa_dict


if __name__ == '__main__':
    print(string.ascii_letters)
    s_regular = '(a|b)*'

    to_nfa = NFA(s_regular)
    print(to_nfa.to_nfa())
    draw(to_nfa.nfa_dict, './graphviz/nfa')
