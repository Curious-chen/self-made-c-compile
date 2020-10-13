from Analysis.Pre_anaylysis import *
from Analysis.erroe_list import *
from Analysis.TreeNode import *
from Semantic.Symbol_table import *
import pydotplus as pdp
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
import graphviz
from collections import namedtuple

dot = graphviz


class Predict_:
    def __init__(self):
        self.tooken_word, self.tooken_row, self.tooken_code, self.token_list, self.err_list = [], [], [], [], []
        self.A, self.E, self.tree = None, None, None
        self.Token = namedtuple('Token', 'val typ cur_line id')
        self.syn_table = SYMBOL()

    def read_token_file(self, path):
        with open(path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            all_word = lines[2:]
            for index, pre_line in enumerate(all_word):
                pre_line = pre_line.strip().split('\t')
                self.tooken_word.append(pre_line[1])
                self.tooken_row.append(pre_line[0])
                self.tooken_code.append(pre_line[2])
                self.token_list.append(self.Token(pre_line[1], pre_line[2], pre_line[0], index))
            self.token_list.append(self.Token('#', '#', '#', len(all_word)))
            self.tooken_word.append('#')
            self.tooken_row.append('#')
            self.tooken_code.append('#')

    def search_(self, word):
        flag = ''
        pos = -1
        if word == '|=': word = 'OR='
        if word == '||': word = 'OROR'
        if word == '|': word = 'OR'
        if word == '->': word = 'ARROW'
        for index, pre in enumerate(self.tooken_word):
            if pre == word:
                pos = index
                if self.tooken_code[index] == '700':
                    flag = 'IDENTIFIER'  # 表示为标识符
                    break
                elif self.tooken_code[index] == '600':
                    flag = 'STRING_LITERAL'
                    break
                elif self.tooken_code[index] == '500':
                    flag = 'CONSTANT'
                    break
                elif self.tooken_code[index] == '400':
                    flag = 'CONSTANT'
                    break
                elif self.tooken_code[index] == '800':
                    flag = 'CONSTANT'
                    break
                elif self.tooken_code[index] in ['11', '57', '61', '62']:  # 表示词法分析出错单词
                    flag = 'CONSTANT'
                    break
        if len(flag) == 0:  # 未找到
            flag = word
        return flag, pos

    def predict_syna(self, tooken, table):
        stack = ['#', 'Translation_unit']
        index = 0
        self.tree = Node('Translation_unit', 'start')
        anal_seq = [Node('-1', '#'), self.tree]
        brackets_count1, brackets_count2, brackets_count3 = 0, 0, 0  # 记录括号个数是否匹配
        sign, f = True, True
        while len(stack) != 0:
            new_stack = copy.deepcopy(stack)  # 用于记录前一个状态站
            stack_top = stack.pop()  # 弹出栈顶元素
            tree_node = anal_seq.pop()
            print('stack:{} token:{}'.format(stack_top, tooken[index]))
            word, pos = self.search_(tooken[index])
            word = word.upper()
            if stack_top in self.A.vt:  # 如果为终结符
                if stack_top == word and stack_top != '#':  # 表明匹配成功
                    sign = True
                    brackets_count1, brackets_count2, brackets_count3 = self.E.count_(stack_top, brackets_count1,
                                                                                      brackets_count2, brackets_count3)
                    print(' '.join(new_stack), ''.join(tooken[index:]), '匹配: {}'.format(tooken[index]))
                    if tooken[index][0:1] == '"':
                        wo = tooken[index].replace('"', '')
                        tree_node.vaule = wo
                    else:
                        tree_node.vaule = tooken[index]
                    index += 1
                    new_stack.pop()
                else:
                    pass  # 栈顶为终结符 并且不等于当前串则表示当前确实这个符号，记录错误信息，并讲此终结符弹栈
                    if stack_top != '#':
                        _, pos_ = self.search_(stack_top)
                        info = '第 {} 行 {}符号缺失'.format(str(int(self.tooken_row[pos_]) + 1), stack_top)
                        if info not in self.err_list: self.err_list.append(info)
                        print("不匹配的终结符:{}、{}".format(stack_top, tooken[index]))
            if stack_top == '#':
                if stack_top == word:
                    print(' '.join(new_stack), ''.join(tooken[index:]), '接受')
                    new_stack.pop()
                    return
                else:
                    print(' '.join(new_stack), ''.join(tooken[index:]), '失败')
            if stack_top in self.A.list_:  # 如果为非终结符
                key_row, first_col = self.A.find_index(table, stack_top, word)
                print(' '.join(new_stack), ''.join(tooken[index:]), table[key_row][first_col])
                if table[key_row][first_col] == 0:  # 表示此处不存在表达式,忽略掉此处的符号
                    print(' '.join(new_stack), ''.join(tooken[index:]), table[key_row][first_col])
                    if sign:
                        info = '第 {} 行 {}附近存在错误'.format(str(int(self.tooken_row[index]) + 1), tooken[index])
                        if info not in self.err_list: self.err_list.append(info)
                        sign = False
                    if word not in self.A.follow[stack_top]:
                        if index < len(tooken) - 1:
                            index += 1  # tooken指针后移进行后续的匹配
                            stack.append(stack_top)  # 保持栈顶元素不变
                            anal_seq.append(tree_node)
                        else:
                            pass
                elif table[key_row][first_col] == 'synch':  # 弹出栈顶元素非终结符A，试图继续分析后面的语法
                    if sign:
                        info = '第 {} 行 {}附近存在错误'.format(str(int(self.tooken_row[index]) + 1), tooken[index])
                        if info not in self.err_list: self.err_list.append(info)
                        sign = False
                    if word in self.A.follow[stack_top]:
                        pass
                    print(' '.join(new_stack), ''.join(tooken[index:]), table[key_row][first_col])
                    new_stack.pop()
                    pass
                else:
                    strs = table[key_row][first_col].split('->')[1].split(' ')  # 字符串逆序
                    strs.reverse()
                    lists = list()
                    lists.clear()
                    for pre in strs:
                        if pre != 'ε':
                            stack.append(pre)
                            lists.append(pre)
                    anal_seq.extend(self.add_Tree_node(tree_node, lists))
                    # message = self.Symbol_(table[key_row][first_col], word, self.token_list[index])
                    # print('----------------------{}'.format(message))
                    new_stack.pop()

    def add_Tree_node(self, node, item):
        name = node.name
        next_node = list()
        for i, word in enumerate(item):
            next_node.append(Node('{}_{}'.format(name, i), word))
        node.next_node = next_node
        return next_node

    def get_tree(self, tree):
        input_tree = [tree]
        dy = str()
        lc = str()
        while True:
            if len(input_tree) == 0:
                break
            node = input_tree.pop()
            dy += '{}[label="{}"];'.format(node.name, node.vaule)
            lc += ''.join(['{}->{};'.format(node.name, _.name) for _ in node.next_node])
            input_tree.extend(node.next_node)
        print(dy + '\n' + lc)
        graph = pdp.graph_from_dot_data('digraph demo1{{{:}}}'.format(dy + lc))
        graph.write_pdf('test1.pdf')

    def Symbol_(self, s, word, token):
        def addFunc(token):
            self.syn_table.addFunction(self.token_list[token.id + 1], token.val)

        def addVar(token, doseParameter=False):
            self.syn_table.addVariableToTable(self.token_list, self.token_list[token.id + 1], token.val, doseParameter)

        def checkVar(token):
            return self.syn_table.checkDoDefineInFunction(token)

        def checkFun(token):
            index = self.token_list[token.id + 1].id
            if self.token_list[token.id + 1].val == '=':  # a = Demo(a,b)
                index += 1
            else:
                index -= 1
            return self.syn_table.checkFunction(self.token_list, index)

        if s == 'External_declaration->Declaration_specifiers Declarator External_declaration_1':  # 函数定义
            addFunc(token)
        if s == 'Parameter_declaration->Declaration_specifiers Parameter_declaration\'':  # 参数声明
            addVar(self.token_list[token.id], True)
        if s == 'Compound_statement_1->Declaration_list Compound_statement_2' or s == 'Declaration_list\'->Declaration Declaration_list\'':  # 变量定义
            addVar(token)
        # if s == 'Expression->Assignment_expression Expression\'':
        if s == 'Expression_statement->Expression ;':
            return checkVar(token)
        message = Message(None, None, None)
        return message

    def Acess_(self):
        self.A = Analysis_()
        pre_table = self.A.main()
        self.E = ERROR()
        self.read_token_file('new1.txt')
        self.predict_syna(self.tooken_word, pre_table)
        self.get_tree(self.tree)
        return self.A.list_


if __name__ == '__main__':
    P = Predict_()
    P.Acess_()
    P.syn_table.showTheInfo()
    for i in P.syn_table.symbolTableInfo:
        print(i)
    pass
