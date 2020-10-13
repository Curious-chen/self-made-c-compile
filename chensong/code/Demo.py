import copy
from DAG_Node import *
from Sentence import *
from collections import defaultdict
import pydotplus as pdp
import operator
import os


class Optimizathon_:
    def __init__(self, act_var):
        self.sen_list, self.basic_block, self.fun_block_list = [], [], []
        self.nodes, self.gen_list, self.Act_var = [], [], []
        self.n, self.count = 0, 0
        self.block_dic, self.node_dic, self.new_gen_list = [], [], []
        self.act_var = act_var
        pass

    def read_file(self, path):
        # path = 'gen_.txt'
        with open(path, 'r', encoding='UTF-8')as f:
            lines = f.readlines()
            lines = lines[1:]
            for i in lines:
                i = i.split(':')
                strs_ = i[1].strip()[1:-1].split(',')
                self.sen_list.append([tmp.strip() for tmp in strs_])
        print('sadadada----------------:',self.sen_list)
        # for j in self.sen_list:
        #     print(j)

    def fun_block(self):
        split_list = []
        for index, key in enumerate(self.sen_list):
            if len(key[0]) > 0 and key[1] == '_' and key[2] == '_' and key[3] == '_':  # 表示函数名
                split_list.append(index)
        begin = 0
        list_ = []
        if split_list[0] != 0:
            list_.extend(self.sen_list[0:split_list[0]])
            begin = split_list.pop(0)
        for index, in_ in enumerate(split_list):
            for key in self.sen_list[begin:in_]:
                list_.append(key)
            if len(list_) != 0: self.fun_block_list.append(copy.deepcopy(list_))
            list_.clear()
            begin = in_
        for key in self.sen_list[begin:]:
            list_.append(key)
        if len(list_) != 0: self.fun_block_list.append(copy.deepcopy(list_))
        lens = 0
        for per_fun_block in self.fun_block_list:
            self.basic_block.clear()
            self.split_fun(per_fun_block, lens)
            lens += len(per_fun_block)  # 下一个函数块 if 跳转偏移长度

    def find_entry(self, fun_, lens):
        entry = []  # 用于存储基本块入口
        entry.clear()
        entry.append(0)
        for index, key in enumerate(fun_):
            # if key[0] == 'j' and self.sen_list[index - 1][0] in ['j<', 'j>', 'j=']:
            # if key[0] in ['j', 'break', 'con'] and fun_[index + 1][0] in ['j', 'j==', 'j>', 'j<'] or key[0] in ['j',
            #                                                                                                     'break',
            #                                                                                                     'con']:
            if key[0] in ['j', 'break', 'con']:
                entry.append(int(key[-1]) - lens)  # 跳转入口
                entry.append(index + 1)
        # elif
        entry.append(len(fun_))
        entry = list(set(entry))
        entry.sort()  # 将入口从小到大排序
        print('entry:{}'.format(entry))
        return entry

    def split_fun(self, fun_, lens):  # 划分基本块
        entry = self.find_entry(fun_, lens)
        dic, pos = {}, 0
        NODE = defaultdict(set)
        if len(entry) == 1:
            self.basic_block = copy.deepcopy(fun_)  # 因为入口为0，无需再分割
        else:
            begin = entry[0]  # 程序开始入口
            for index in entry[1:]:
                tmp = []
                for index_, key in enumerate(fun_[begin:index]):
                    tmp.append(key)
                    if key[0] in ['j', 'break', 'con'] and fun_[begin:index][index_ - 1][0] in ['j', 'jnz', 'j==', 'j>',
                                                                                                'j<']:
                        NODE[begin].add(int(fun_[begin:index][index_ - 1][-1]) - lens)
                        NODE[begin].add(int(key[-1]))
                    elif key[0] in ['j', 'break', 'con']:
                        NODE[begin].add(int(fun_[begin:index][index_][-1]) - lens)
                    # elif key[0] not in ['+', '-', '*', '/', '='] and self.is_number(key[-1]) and index!=len(fun_):
                    elif len(fun_[begin:index]) - 1 == index_ and index != len(fun_):
                        NODE[begin].add(index - lens)
                self.basic_block.append(tmp)
                dic['B' + str(pos)] = tmp
                pos += 1
                begin = index
        # for p in self.basic_block:
        #     print('basic_block:{}'.format(p))

        dic_block = {}
        for in_ in range(0, len(entry)):
            t = 'B' + str(in_)
            dic_block[entry[in_]] = t
        tmp = defaultdict(set)
        for key_ in NODE.keys():
            for i in list(NODE[key_]):
                # if i != len(fun_):
                tmp[dic_block[key_]].add(dic_block[i])  # 流图
        # print(tmp)
        # AAA = self.act_var
        # self.DAG(fun_, AAA)
        # block, dic = self.get_new_gen(dic)
        # dic = self.back_write(tmp, dic)  # 更新分支语句的出口信息
        self.block_dic.append(dic)
        # ind_ = 0
        # for key in dic.keys():
        #     for i in dic[key]:
        #         print(ind_,i)
        #         ind_ +=1
        # print('{}:{}'.format(key, dic[key]))

    def back_write(self, tmp, dic):  # tmp为流图 dic为基本块
        for key in tmp.keys():
            lens = 0
            list_ = []
            if len(tmp[key]) == 1:  # 要么跳转语句存在 要么顺序语句
                for index, per in enumerate(dic[key]):
                    if per[0] in ['j', 'con', 'continue'] and dic[key][index - 1][0] not in ['j==', 'j>', 'j<', 'jnz']:
                        list_.extend([index, dic[key][index:]])
                        break
                if len(list_) != 0:
                    t = list(tmp[key])[0]
                    for key_ in dic.keys():
                        if key_ != t:
                            lens += len(dic[key_])
                        else:
                            break
                    dic[key][list_[0]][-1] = str(lens)
            if len(tmp[key]) == 2:  # 跳转语句
                for index, per in enumerate(dic[key]):
                    if per[0] in ['j==', 'j>', 'j<', 'j', 'jnz']:
                        list_.extend([index, dic[key][index:]])
                        break
                if len(list_) != 0:
                    pos = list_[0]
                    for index, i in enumerate(tmp[key]):
                        lens, pos = 0, pos + index
                        for key_ in dic.keys():
                            if key_ != i:
                                lens += len(dic[key_])
                            else:
                                break
                        dic[key][pos][-1] = str(lens)
        return dic

    def get_new_gen(self, dic):
        new_gen_list, block = [], []  # block获得一个函数块
        for j in self.new_gen_list:
            list_ = []
            for i in j:
                list_.append([str(i.op), str(i.n1), str(i.n2), str(i.res)])
            new_gen_list.append(copy.deepcopy(list_))
        for index_, key in enumerate(dic.keys()):
            list_1 = []
            for index, per_gen in enumerate(dic[key]):
                if per_gen[1] == '_' and per_gen[2] == '_' and per_gen[3] == '_':
                    list_1.append(index)
                elif per_gen[0] in ['j', 'jnz', 'j==', 'j>', 'j<', 'con', 'continue']:
                    list_1.append(index)
                    break
            if len(list_1) == 0:
                dic[key] = copy.deepcopy(new_gen_list[index_])
                block.extend(dic[key])
            elif len(list_1) == 1:
                tmp_list = []
                if list_1[0] == 0:  # 表明只有一个基本块并且没有跳转
                    if len(new_gen_list[index_]) == 0:
                        tmp_list.extend(dic[key][list_1[0]:])
                    else:
                        tmp_list = [dic[key][list_1[0]]]
                        tmp_list.extend(new_gen_list[index_])
                    dic[key] = copy.deepcopy(tmp_list)
                    block.extend(dic[key])
                else:
                    tmp_list.extend(new_gen_list[index_])
                    tmp_list.extend(dic[key][list_1[0]:])
                    dic[key] = copy.deepcopy(tmp_list)
                    block.extend(dic[key])
            else:
                tmp_list = []
                if list_1[0] == 0:  # 表明只有一个基本块并且没有跳转
                    tmp_list = [dic[key][list_1[0]]]
                    tmp_list.extend(new_gen_list[index_])
                tmp_list.extend(dic[key][list_1[-1]:])
                dic[key] = copy.deepcopy(tmp_list)
                block.extend(dic[key])
        # print(new_gen_list)
        return block, dic

    def DAG(self, fun_, AAA):
        operation = ['+', '-', '*', '/', '=', '>', '<', '==', '>=', '<=']
        for index__, __block in enumerate(self.basic_block):  # 对每个基本块进行优化
            list__, tmp_list = list(AAA.keys()), []
            self.n, self.count = 0, 0
            self.node_dic.append(self.nodes)
            self.nodes.clear()
            self.gen_list.clear()
            for index_, _block in enumerate(__block):
                if _block[0] in operation and index_ < len(__block) - 1:
                    if _block[0] == '=':  # 一元运算符
                        id = self.get_node(_block[1])
                        self.add_node(id, _block[-1], False)
                        self.delt_(id, _block[-1])
                    else:
                        if _block[1].isdigit() and _block[2].isdigit():  # 合并已知量
                            id = self.get_node(str(eval(_block[1] + _block[0] + _block[2])))
                            self.add_node(id, _block[-1], False)
                            self.delt_(id, _block[-1])
                        else:
                            if _block[1].isdigit() and self.find_id(_block[2]):
                                for index, node in enumerate(self.nodes):
                                    for _node in node.value:
                                        if _block[2] in _node and self.nodes[index].val not in operation:
                                            id = self.get_node(
                                                str(eval(_block[1] + _block[0] + self.nodes[index].val)))
                                            # print(__block[index_ + 1][0])
                                            if __block[index_ + 1][0] in ['+', '-', '*', '/'] and _block[-1] in __block[
                                                index_ + 1]:
                                                self.add_node(id, _block[-1], True)
                                            else:
                                                self.add_node(id, _block[-1], False)
                                            self.delt_(id, _block[-1])
                                            break
                            elif _block[2].isdigit() and self.find_id(_block[1]):
                                for index, node in enumerate(self.nodes):
                                    for _node in node.value:
                                        if _block[1] in _node and self.nodes[index].val not in operation:
                                            id = self.get_node(
                                                str(eval(self.nodes[index].val + _block[0] + _block[2])))
                                            if __block[index_ + 1][0] in ['+', '-', '*', '/'] and _block[-1] in __block[
                                                index_ + 1]:
                                                self.add_node(id, _block[-1], True)
                                            else:
                                                self.add_node(id, _block[-1], False)
                                            # self.add_node(id, _block[-1], False)
                                            self.delt_(id, _block[-1])
                                            break
                            else:
                                id_1 = self.get_node(_block[1])
                                id_2 = self.get_node(_block[2])
                                id = self.get_node(_block[0], id_1, id_2)
                                if __block[index_ + 1][0] in ['+', '-', '*', '/'] and _block[-1] in __block[
                                    index_ + 1]:
                                    self.add_node(id, _block[-1], True)
                                else:
                                    self.add_node(id, _block[-1], False)
                                # self.add_node(id, _block[-1], False)
                                self.delt_(id, _block[-1])
            self.delt_tmp_and_nonuse(index__, list__, AAA)
            # for i in self.nodes:
            #     print('-id:{} val:{} value:{} left:{} right:{}'.format(i.id, i.val, i.value, i.leftchild, i.rightchild))
            self.gen_()
            # self.get_tree()  # 画DAG图
            self.new_gen_list.append(copy.deepcopy(self.gen_list))
            # for i in self.gen_list:
            #     print("{:<3s}: ( {:<4s} {:<4s} {:<4s} {:<4s} )".format(str(i.id), str(i.op), str(i.n1), str(i.n2),
            #                                                            str(i.res)))

    def delt_(self, id, val):  # 删除重复赋值的变量
        index, val_ = 0, None
        for in_, node in enumerate(self.nodes):
            if len(node.value) != 0:
                for per_ in node.value:
                    if val in per_ and id != node.id:  # 表明之前已经赋值，现在对变量重新赋值，需删除之前赋值的变量
                        index = in_
                        val_ = per_
                        break
        if index != 0:
            self.nodes[index].value.remove(val_)
            for node in self.nodes:
                if len(node.value) != 0:
                    for per_ in node.value:
                        if len(per_) > 1 and per_[1] > val_[1]:
                            per_[1] -= 1
            self.n -= 1

    def _delt_(self, node_):
        for node in node_.value:
            for node_1 in self.nodes:
                if len(node_1.value) != 0:
                    for t in node_1.value:
                        if node[1] <= t[1]:
                            t[1] -= 1

    def delt_tmp_and_nonuse(self, index, list__, AAA):  # 删除临时变量和无用表达式
        for node in self.nodes:
            list_ = []
            if len(node.value) != 0:
                for per_ in node.value:
                    if len(per_) > 1:
                        list_.append(per_)
            node.value = list_
        if len(AAA) != 0:
            node_list, tmp_list = [], []
            for per in list(AAA[list__[index]][1]):
                for node in self.nodes:
                    for node_ in node.value:
                        if node_[0] == per:
                            node_list.append(node)
                        if node_[0] == per and node.leftchild != None:
                            node_list.append(self.nodes[node.leftchild])
                        if node_[0] == per and node.rightchild != None:
                            node_list.append(self.nodes[node.rightchild])
            for node in self.nodes:
                if node not in node_list:  # 表示无用四元式
                    for node_ in node_list:
                        if node_.leftchild == node.id or node_.rightchild == node.id:
                            tmp_list.append(node)
                    else:
                        self._delt_(node)
                        self.n -= 1
                else:
                    tmp_list.append(node)
            self.nodes = copy.deepcopy(tmp_list)
            for index_, node in enumerate(self.nodes):
                for _node in node.value:
                    if _node[0] not in list(AAA[list__[index]][1]) and self.__tmp(node, index_):  # 无关变量 删除
                        self.nodes[index_].value.remove(_node)
                        for node in self.nodes:
                            if len(node.value) != 0:
                                for per_ in node.value:
                                    if len(per_) > 1 and per_[1] > _node[1]:
                                        per_[1] -= 1
                        self.n -= 1
        else:
            node_list = []
            for index, node in enumerate(self.nodes):
                flag = True
                for node_ in self.nodes:
                    if node.id == node_.leftchild or node.id == node_.rightchild or (
                            node.leftchild != None and node.rightchild != None):
                        flag = False
                        break

                if not flag:
                    node_list.append(node)
                else:
                    self._delt_(node)
                    self.n -= 1
            self.nodes = copy.deepcopy(node_list)

    def __tmp(self, node_, index_):
        for index, node in enumerate(self.nodes):
            if (node_.leftchild == node.leftchild or node_.leftchild == node.rightchild) and (
                    node_.rightchild == node.leftchild or node_.rightchild == node.rightchild) and index != index_:
                return False
        return True

    def get_node(self, sym, BofLeftNodeID=None, CofRightNodeID=None):
        operation = ['+', '-', '*', '/', '=', '>', '<', '==', '>=', '<=']
        if sym in operation:
            for node in self.nodes:  # 查找已存在的结点中是否存在改结点
                if sym == node.val and sym in ['+', '*']:  # 不考虑运算次序
                    if (BofLeftNodeID == node.leftchild and CofRightNodeID == node.rightchild) or (
                            BofLeftNodeID == node.rightchild and CofRightNodeID == node.leftchild):
                        return node.id
                if sym == node.val:  # 其他运算符
                    if BofLeftNodeID == node.leftchild and CofRightNodeID == node.rightchild:
                        return node.id
            self.nodes.append(DAG(len(self.nodes), sym, None, BofLeftNodeID, CofRightNodeID))  # 新添加jiedian
            return len(self.nodes) - 1
        else:  # 操作数
            for node in self.nodes:
                for va in node.value:
                    if sym in va:
                        return node.id
                if sym == node.val:
                    return node.id
            self.nodes.append(DAG(len(self.nodes), sym, None, None, None))
            return len(self.nodes) - 1

    def gen_(self):
        while self.count < self.n:
            for node in self.nodes:
                if len(node.value) != 0:
                    for index, key in enumerate(node.value):
                        if key[1] == self.count and node.leftchild == None and node.rightchild == None:  # 赋值表达式
                            self.gen_list.append(Sentence_(len(self.gen_list), '=', node.val, '_', key[0]))
                            self.count += 1
                        elif index == 0 and key[1] == self.count and node.leftchild != None and node.rightchild != None:
                            op_left, flag = self.find_val(node.leftchild)
                            op_right, flag = self.find_val(node.rightchild)
                            self.gen_list.append(Sentence_(len(self.gen_list), node.val, op_left, op_right, key[0]))
                            self.count += 1
                        elif index > 0 and key[1] == self.count and node.leftchild != None and node.rightchild != None:
                            op_left, flag_left = self.find_val(node.leftchild)
                            op_right, flag_right = self.find_val(node.rightchild)
                            if flag_left and flag_right:
                                self.gen_list.append(
                                    Sentence_(len(self.gen_list), '=', node.value[index - 1][0], '_', key[0]))
                                self.count += 1
                            else:
                                self.gen_list.append(Sentence_(len(self.gen_list), node.val, op_left, op_right, key[0]))
                                self.count += 1

    def find_val(self, index):  # 寻找左右结点的值
        operation = ['+', '-', '*', '/', '=', '>', '<', '==', '>=', '<=']
        for node in self.nodes:
            if node.id == index:
                if self.is_number(node.val):  # 为数字直接返回
                    return node.val, False
                elif len(node.value) == 0:
                    return node.val, True
                elif node.val in operation:
                    min, in_ = 999, -1
                    for index, per_ in enumerate(node.value):
                        if len(per_) > 1 and per_[1] <= self.count:
                            if self.count - per_[1] > 0 and self.count - per_[1] < min:
                                min, in_ = self.count - per_[1], per_
                    return in_[0], True

    def get_tree(self):
        input_tree = [self.nodes[-1]]
        dy = str()
        lc = str()
        while True:
            if len(input_tree) == 0:
                break
            node = input_tree.pop()
            if len(node.value) != 0:
                s = ''
                for i in node.value:
                    s += i[0] + ' '
                dy += '{}[label="{}"];'.format(node.id, node.val + ' ' + s)
            else:
                dy += '{}[label="{}"];'.format(node.id, node.val)
            if node.leftchild != None:
                tmp = None
                for node_ in self.nodes:
                    if node_.id == node.leftchild:
                        tmp = node_
                        break
                lc += ''.join(['{}->{};'.format(node.id, node.leftchild)])
                input_tree.append(tmp)
            if node.rightchild != None:
                tmp = None
                for node_ in self.nodes:
                    if node_.id == node.rightchild:
                        tmp = node_
                        break
                lc += ''.join(['{}->{};'.format(node.id, node.rightchild)])
                input_tree.append(tmp)
        lc = ';'.join(list(set(lc.split(';')[0:-1])))
        lc += ';'
        print(dy + '\n' + lc)
        graph = pdp.graph_from_dot_data('digraph demo1{{{:}}}'.format(dy + lc))
        graph.write_pdf('test.pdf')

    def is_number(self, num):  # 判断是不是已知量
        try:
            float(num)
            return True
        except ValueError:
            pass
        return False

    def add_node(self, id, sym, flag):
        if 'T' in sym and not flag:
            self.nodes[id].add_value([sym])
        else:
            self.nodes[id].add_value([sym, self.n])
            self.n += 1

    def find_id(self, val):
        operation = ['+', '-', '*', '/', '=', '>', '<', '==', '>=', '<=']
        for index, node in enumerate(self.nodes):
            for va in node.value:
                if val in va and node.val not in operation:
                    return True
        return False

    def Acess_(self, all_lines):
        self.read_file(all_lines)
        self.fun_block()


if __name__ == '__main__':
    O = Optimizathon_()
    O.read_file()
    O.fun_block()

    # O.split_fun()
    # O.DAG()
