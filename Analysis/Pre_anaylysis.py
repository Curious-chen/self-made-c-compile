from collections import defaultdict
import sys
import copy
from Analysis.deal_call import *
from chensong.code.config import grammer_path

class Analysis_:
    def __init__(self):
        self.stack = []  # 存储推导式
        self.vt = ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', 'ARROW', 'SIZEOF', 'TYPEDF', 'EXTERN', 'STATIC', 'AUTO',
                   'REGISTER', 'VOID', 'CHAR', 'SHORT', 'INT', 'LONG', 'FLOAT', 'DOUBLE', 'SIGNED', 'UNSIGNED',
                   'TYPE_NAME', 'CONST', 'VOLATILE', 'OR', 'OROR', 'CASE', 'DEFAULT', 'IF', 'ELSE',
                   'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'RETURN', 'BREAK', 'SWITCH', '.', '++', '--', ',', '&',
                   '*',
                   '+',
                   '-', '~',
                   '!',
                   '/',
                   '%', '<<', '>>', '<', '>', '<=', '>=', '==', '!=', '^', '&&', '?', ':', '=', '*=', '/=', '%=', '+=',
                   '-=', '<<=', '>>=', '^=', 'OR=', ';', '{', '}', '[', ']', '(', ')', '&=', '...', '#']
        self.list_ = []
        self.nullable = []
        self.dic_list = dict()
        self.first = defaultdict(set)  # 构建元素映射到多个元素（集合）的字典
        self.follow = defaultdict(set)
        self.all_exp = defaultdict(set)
        self.test = defaultdict(set)

    def read_file(self, path):
        with open(path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            lines = remove_recursion(lines)
            lines = remove_recall(lines)
            for pre_ in lines:
                item = pre_.split('->')
                item_left = item[0].strip()
                item_right = item[1].split('|')
                if item_left not in self.list_: self.list_.append(item_left)
                for pre_word in item_right:
                    self.stack.append(item_left + '->' + pre_word.strip())
                    self.dic_list[item_left + '->' + pre_word.strip()] = len(list(self.dic_list.keys()))
        print(self.stack)

    def getVt(self):
        key_word = set()
        all_word = set()
        for per in self.stack:
            per = per.split('->')
            per_left = per[0].strip()
            per_right = per[1].strip().split(' ')
            key_word.add(per_left)
            all_word.add(per_left)
            for i in per_right:
                all_word.add(i)
        all_word.add('#')
        self.vt = list(all_word - key_word - {'ε'})
        self.vt = self.vt[1:]

    def isVn(self, item):
        flag1, flag2 = True, True
        for i in item:
            if i not in self.list_:  # 表明终结符
                flag1 = False
        for i in item:
            if i not in self.nullable:
                flag2 = False
        return flag1 and flag2

    def NULLABLE(self):
        flag = True  # 循环结束条件
        while flag:
            lenght = len(self.nullable)
            for pre_ in self.stack:  # 遍历每个产生式
                pre_ = pre_.split('->')
                pre_right = pre_[1].split(' ')
                if pre_right[0] == 'ε':
                    self.nullable.append(pre_[0])
                if self.isVn(pre_right):
                    self.nullable.append(pre_[0])
                if lenght == len(self.nullable):
                    flag = False
        print('长度:{} term:{}'.format(len(self.nullable), self.nullable))

    def isChange(self, temp_dic, dic):
        flag = True
        for X, Y in dic.items():
            if temp_dic[X] != dic[X]:
                flag = False
                break
        return flag

    def First_list(self):
        flag = True
        for pre_ in self.stack:  # 遍历每个产生式
            pre_ = pre_.split('->')
            pre_right = pre_[1].split(' ')
            self.first[pre_[0].strip()]
        temp_dic = self.first.copy()  # 记录字典是否变化
        while flag:
            for index, pre_ in enumerate(self.stack):  # 遍历每个产生式
                pre_ = pre_.split('->')
                pre_right = pre_[1].split(' ')
                count = 0
                for Yi in pre_right:
                    if Yi == 'ε' and len(pre_right) == 1:
                        self.first[pre_[0]] = self.first[pre_[0]] | {'ε'}
                        self.test[pre_[0] + '->' + pre_[1]] = self.test[pre_[0] + '->' + pre_[1]] | {'ε'}
                    elif Yi in self.vt:  # 为终结符
                        self.first[pre_[0]] = self.first[pre_[0]] | set({Yi})
                        self.test[pre_[0] + '->' + pre_[1]] = self.test[pre_[0] + '->' + pre_[1]] | set({Yi})
                        break
                    elif Yi in self.list_:
                        self.first[pre_[0]] = self.first[pre_[0]] | self.first[Yi] - {'ε'}
                        self.test[pre_[0] + '->' + pre_[1]] = self.test[pre_[0] + '->' + pre_[1]] | self.first[Yi] - {
                            'ε'}
                        if Yi not in self.nullable:
                            break
                        else:
                            count += 1
                        if count == len(pre_right):
                            self.first[pre_[0]] = self.first[pre_[0]] | {'ε'}
                            self.test[pre_[0] + '->' + pre_[1]] = self.test[pre_[0] + '->' + pre_[1]] | {'ε'}
            if not self.isChange(temp_dic, self.first):
                temp_dic = self.first.copy()
            else:
                flag = False

    def Follow_list(self):
        flag = True
        for pre_ in self.stack:  # 遍历每个产生式
            pre_ = pre_.split('->')
            pre_right = pre_[1].split(' ')
            self.follow[pre_[0].strip()]
        temp_dic = self.follow.copy()  # 记录字典是否变化
        while flag:
            for pre_ in self.stack:  # 遍历每个产生式
                pre_ = pre_.split('->')
                pre_right = pre_[1].split(' ')
                temp = self.follow[pre_[0].strip()]
                for index in range(len(pre_right) - 1, -1, -1):
                    if pre_right[index] in self.vt:
                        temp = set({pre_right[index]})
                    elif pre_right[index] in self.list_:  # 非终结符
                        self.follow[pre_right[index]] = self.follow[pre_right[index]] | temp
                        if pre_right[index] not in self.nullable:
                            temp = self.first[pre_right[index]] - {'ε'}
                        else:
                            temp = temp | self.first[pre_right[index]] - {'ε'}
            if not self.isChange(temp_dic, self.follow):
                temp_dic = self.follow.copy()
            else:
                flag = False

    def find_index(self, table, strs, per_first):
        row, col = 0, 0
        strs = strs.split('->')[0]
        for index, per in enumerate(table):  # 可能存在bug
            if strs.strip() == per[0] and index > 0:
                row = index
                break
        for index_, per_ in enumerate(table[0]):
            if per_first == per_:  # 终结符在的位置
                col = index_
        return row, col

    def predict_table(self):
        table = [[0] * (len(self.vt) + 1) for i in range(len(self.list_) + 1)]
        for index, per in enumerate(table):
            if 0 < index <= len(self.list_):
                per[0] = self.list_[index - 1]
        for index, per_ in enumerate(table[0]):
            if index > 0:
                table[0][index] = self.vt[index - 1]
        for per_key in self.test.keys():  # 得到每一个非终结符的first列表
            per_key_list = list(self.test[per_key])
            for per_first in per_key_list:  #
                if per_first != 'ε':
                    key_row, first_col = self.find_index(table, per_key, per_first)
                    table[key_row][first_col] = per_key
                else:  # 进行follow集中的元素输出
                    for per_ in list(self.follow[per_key.split('->')[0]]):  # 得到非终结符
                        key_row, first_col = self.find_index(table, per_key, per_)
                        table[key_row][first_col] = per_key.split('->')[0] + '->' + 'ε'
        for per_key in self.first.keys():  # 同步点
            per_key_list = list(self.first[per_key])
            if 'ε' not in per_key_list:  # 表示e不存在列表内
                for per_ in list(self.follow[per_key]):  # 得到非终结符
                    key_row, first_col = self.find_index(table, per_key, per_)
                    if table[key_row][first_col] == 0:
                        table[key_row][first_col] = 'synch'

        return table  # 返回预测分析表

    def getsame(self):
        '''
        函数功能：判断follow集合是否存在交集
        :return:
        '''
        print(len(self.first.items()))
        print("First与Follow集合相交的集合:")
        for pre in self.nullable:
            if len(self.first[pre] & self.follow[pre]) != 0:
                print('关键字：{}\n交集：{}\nfirst：{}\nfollow：{}'.format(pre, self.first[pre] & self.follow[pre],
                                                                  self.first[pre],
                                                                  self.follow[pre]))
        print('分析完成')

    def getfirst_(self):
        print("First与First集合相交的集合:")
        for pre in self.list_:  # 得到每个关键字
            list_ = []
            for pre_key in self.test.keys():
                pre_ = pre_key.split('->')[0]  # 得到关键字
                if pre == pre_:
                    if pre_key not in list_: list_.append(pre_key)
            for i in range(len(list_)):
                for j in range(i, len(list_)):
                    if i != j:
                        if len(self.test[list_[i]] & self.test[list_[j]]) != 0:
                            print('关键字:{}\n相交:{}\n推导式:{}、{}'.format(list_[i].split('->')[0],
                                                                    self.test[list_[i]] & self.test[list_[j]], list_[i],
                                                                    list_[j]))
        print('分析完成')

    def out_put(self, type_, item_):
        if type_ == 'dict':
            for key in item_.keys():
                print('key:{} item:{}'.format(key, item_[key]))
        elif type_ == 'list':
            for i in item_:
                print(i)

    def main(self):
        path = grammer_path
        self.read_file(path)
        # self.getVt()
        print(len(self.stack), len(self.list_), len(self.vt))
        self.NULLABLE()  # 计算可以推出为空的推导式
        self.First_list()
        self.follow['Translation_unit'].add('#')
        self.Follow_list()
        self.getsame()
        self.getfirst_()
        pre_table = self.predict_table()
        print("-------------------------------------------")
        self.out_put('dict', self.first)
        print("-------------------------------------------")
        self.out_put('dict', self.follow)
        print("-------------------------------------------")
        self.out_put('list', pre_table)
        # self.predict_(['IDENTIFIER', '+', 'IDENTIFIER', '*', 'IDENTIFIER', '-', 'IDENTIFIER', '#'], pre_table)
        # self.predict_(['i', '+', 'i', '*', 'i', '+', 'i', '#'], pre_table)
        return pre_table


if __name__ == '__main__':
    A = Analysis_()
    A.main()
