import copy
from Semantic.DAG_Node import *
from Semantic.Sentence import *
from collections import defaultdict
import operator


class Optimizathon_:
    def __init__(self):
        self.sen_list, self.basic_block, self.fun_block_list = [], [], []
        self.nodes, self.gen_list, self.Act_var = [], [], []
        self.n, self.count = 0, 0

        pass

    def read_file(self):
        path = 'gen_.txt'
        with open(path, 'r', encoding='UTF-8')as f:
            lines = f.readlines()
            lines = lines[1:]
            for i in lines:
                i = i.split(':')
                strs_ = i[1].strip()[1:-1].split(',')
                self.sen_list.append([tmp.strip() for tmp in strs_])
        # for j in self.sen_list:
        #     print(j)

    def fun_block(self):
        split_list = []
        for index, key in enumerate(self.sen_list):
            if len(key[0]) > 1 and key[1] == '_' and key[2] == '_' and key[3] == '_':  # 表示函数名
                split_list.append(index)
        begin = 0
        list_ = []
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
        NODE = defaultdict(set)
        tmp = defaultdict(set)
        entry.append(0)
        begin = 0
        for index, key in enumerate(fun_):
            # if key[0] == 'j' and self.sen_list[index - 1][0] in ['j<', 'j>', 'j=']:
            if key[0] in ['j', 'break', 'con'] and fun_[index + 1][0] not in ['j', 'j==', 'j>', 'j<']:
                entry.append(int(key[-1]) - lens)  # 跳转入口
                entry.append(index + 1)
                NODE[begin].add(index + 1)
                NODE[begin].add(int(key[-1]) - lens)
                begin = index + 1
        entry.append(len(fun_))
        entry = list(set(entry))
        entry.sort()  # 将入口从小到大排序
        print('entry:{}'.format(entry))
        dic = {}
        for index in range(0, len(entry) - 1):
            t = 'B' + str(index)
            dic[entry[index]] = t
        # print(dic)
        for key in NODE.keys():
            for i in list(NODE[key]):
                if i != len(fun_):
                    tmp[dic[key]].add(dic[i])  # 流图
        return entry, tmp

    def split_fun(self, fun_, lens):  # 划分基本块
        entry, liu_list = self.find_entry(fun_, lens)
        dic, pos = {}, 0
        if len(entry) == 1:
            self.basic_block = copy.deepcopy(fun_)  # 因为入口为0，无需再分割
        else:
            begin = entry[0]  # 程序开始入口
            for index in entry[1:]:
                tmp = []
                for key in fun_[begin:index]:
                    tmp.append(key)
                self.basic_block.append(tmp)
                dic['B' + str(pos)] = tmp
                pos += 1
                begin = index
        print(dic)
        print(liu_list)
        for p in self.basic_block:
            print('basic_block:{}'.format(p))
        self.Act_var.clear()
        AAA = self.Active_variable(liu_list, dic)
        self.DAG(AAA)

    def Active_variable(self, liu_list, dic):
        all, tmp_use, tmp_def = [], [], []
        ttt = defaultdict(list)
        for key in dic.keys():
            tmp_use.clear()
            tmp_def.clear()
            for per_key in dic[key]:
                if per_key[0] == '=' and per_key[-1] not in tmp_use:
                    if not self.is_number(per_key[1]) and 'T' not in per_key[1] and per_key[1] not in tmp_def:
                        tmp_use.append(per_key[1])
                    if not self.is_number(per_key[-1]) and 'T' not in per_key[-1] and per_key[-1] not in tmp_use:
                        tmp_def.append(per_key[-1])
                elif per_key[0] in ['+', '-', '*', '/']:  # 赋值
                    if not self.is_number(per_key[1]) and 'T' not in per_key[1] and per_key[1] not in tmp_def:
                        tmp_use.append(per_key[1])
                    if not self.is_number(per_key[2]) and 'T' not in per_key[2] and per_key[2] not in tmp_def:
                        tmp_use.append(per_key[2])
                    if 'T' not in per_key[-1] and per_key[-1] not in tmp_use:
                        tmp_def.append(per_key[-1])
            if [copy.deepcopy(tmp_use), copy.deepcopy(tmp_def)] not in self.Act_var: self.Act_var.append(
                [copy.deepcopy(tmp_use), copy.deepcopy(tmp_def)])  # 计算use 和 def
            ttt[key].extend([copy.deepcopy(set(tmp_use)), copy.deepcopy(set(tmp_def))])
        AAA = copy.deepcopy(ttt)
        for A in AAA.keys():
            AAA[A] = [[], []]
        flag = True
        flag_A = copy.deepcopy(AAA)
        print(ttt)
        print(flag_A)
        while flag:
            for key in list(ttt.keys())[::-1]:
                if key in list(liu_list.keys()):
                    later_node = liu_list[key]
                else:
                    later_node = []
                for per in later_node:
                    print(AAA[key][1], AAA[per][0])
                    AAA[key][1] = set(AAA[key][1]) | set(AAA[per][0])  # out
                AAA[key][0] = set(AAA[key][1]) - set(ttt[key][1]) | set(ttt[key][0])
            flag = self.nonChange(flag_A, AAA)
            flag_A = copy.deepcopy(AAA)
            print('AAA:{}'.format(AAA))
        return AAA

    def nonChange(self, tmp_act, tmp_act_T1):
        flag = False
        for key in tmp_act.keys():
            if operator.eq(tmp_act[key], tmp_act_T1[key]):
                continue
            else:
                flag = True
                break
        return flag

    def DAG(self, AAA):
        operation = ['+', '-', '*', '/', '=', '>', '<', '==', '>=', '<=']
        for index__, __block in enumerate(self.basic_block):  # 对每个基本块进行优化
            list__ = list(AAA.keys())
            self.n, self.count = 0, 0
            self.nodes.clear()
            for _block in __block:
                flag_ = True
                if _block[0] in operation:
                    if _block[0] == '=':  # 一元运算符
                        id = self.get_node(_block[1])
                        self.add_node(id, _block[-1])
                        self.delt_(id, _block[-1])
                    else:
                        if _block[1].isdigit() and _block[2].isdigit():  # 合并已知量
                            id = self.get_node(str(eval(_block[1] + _block[0] + _block[2])))
                            self.add_node(id, _block[-1])
                            self.delt_(id, _block[-1])
                        else:
                            if _block[1].isdigit() and self.find_id(_block[2]):
                                for index, node in enumerate(self.nodes):
                                    # if flag_:
                                    for _node in node.value:
                                        if _block[2] in _node:
                                            id = self.get_node(
                                                str(eval(_block[1] + _block[0] + self.nodes[index].val)))
                                            self.add_node(id, _block[-1])
                                            self.delt_(id, _block[-1])
                                            # flag_ = False
                                            break
                            elif _block[2].isdigit() and self.find_id(_block[1]):
                                for index, node in enumerate(self.nodes):
                                    # if flag_:
                                    for _node in node.value:
                                        if _block[1] in _node:
                                            id = self.get_node(
                                                str(eval(self.nodes[index].val + _block[0] + _block[2])))
                                            self.add_node(id, _block[-1])
                                            self.delt_(id, _block[-1])
                                            # flag_ = False
                                            break
                            else:
                                id_1 = self.get_node(_block[1])
                                id_2 = self.get_node(_block[2])
                                id = self.get_node(_block[0], id_1, id_2)
                                self.add_node(id, _block[-1])
                                self.delt_(id, _block[-1])
            for i in self.nodes:
                print('id:{} val:{} value:{} left:{} right:{}'.format(i.id, i.val, i.value, i.leftchild, i.rightchild))
            self.delt_tmp_and_nonuse(index__, list__, AAA)
            for i in self.nodes:
                print('id:{} val:{} value:{} left:{} right:{}'.format(i.id, i.val, i.value, i.leftchild, i.rightchild))
            self.gen_()
        for i in self.gen_list:
            print("{:<3s}: ( {:<4s} {:<4s} {:<4s} {:<4s} )".format(str(i.id), str(i.op), str(i.n1), str(i.n2),
                                                                   str(i.res)))

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
            node.value = copy.deepcopy(list_)
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
                self._delt_(node)
                self.n -= 1
                pass
            else:
                tmp_list.append(node)
        self.nodes = copy.deepcopy(tmp_list)
        # self.n = len(self.nodes)

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
                    return in_[0], False

    def is_number(self, num):  # 判断是不是已知量
        try:
            float(num)
            return True
        except ValueError:
            pass
        return False

    def add_node(self, id, sym):
        if 'T' in sym:
            self.nodes[id].add_value([sym])
        else:
            self.nodes[id].add_value([sym, self.n])
            self.n += 1

    def find_id(self, val):
        for index, node in enumerate(self.nodes):
            for va in node.value:
                if val in va:
                    return True
        return False


if __name__ == '__main__':
    O = Optimizathon_()
    O.read_file()
    O.fun_block()
    # O.split_fun()
    # O.DAG()
