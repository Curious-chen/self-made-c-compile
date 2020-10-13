import itertools
from chensong.code.model import draw
from chensong.code.to_nfa import NFA
from chensong.code.config import save_dfa, save_min_dfa, save_nfa


# 根据value得到key
def get_key(v, node_dict):
    for key, values in node_dict.items():
        if v == values:
            return key
    return -1


def get_in_key(v, node_dict):
    for key, values in node_dict.items():
        if v in values:
            return key
    return -1


class DFA:
    def __init__(self, nfa_dict):
        self.nfa_dict = nfa_dict
        self.closure_list = []
        # 确定定化的nfa ->DFA
        self.dfa_dict = {'from': [], 'to': [], 'varch': [], 'start': [], 'end': []}
        # 简化dfa
        self.mini_dfa = {'from': [], 'to': [], 'varch': [], 'start': [], 'end': []}
        # 划分部分
        self.divide_part = {}
        # 划分id
        self.divide_id = 0

    def get_index(self, v):
        from_list = self.nfa_dict['from'].copy()
        result = []
        # 找到所有以v为值的index
        while v in from_list:
            from_index = from_list.index(v)
            result.append(from_index)
            from_list[from_index] = -1
        return result

    # 得到列表的ε-closure集
    def get_closure(self, index_list: list):
        # 结果列表，存编号
        result = [self.nfa_dict['from'][index_list[0]]]
        # 下标栈，存下标
        stack_temp = index_list.copy()
        while len(stack_temp):
            temp = stack_temp.pop()
            if self.nfa_dict['varch'][temp] == 'ε':
                # 入结果列表
                result.append(self.nfa_dict['to'][temp])
                # 结果的下标列表入栈
                stack_temp += self.get_index(self.nfa_dict['to'][temp])
        result = list(set(result))
        result.sort()
        return result

    # 得到弧转换
    def get_transform(self, start, varch):
        for i in range(len(self.nfa_dict['from'])):
            if self.nfa_dict['from'][i] == start and self.nfa_dict['varch'][i] == varch:
                return self.nfa_dict['to'][i]
        return -1

    def add_s_e(self, start, end, closure):
        # 开始节点和结束节点
        if start in closure and closure not in self.dfa_dict['start']:
            self.dfa_dict['start'].append(closure)
        if end in closure and closure not in self.dfa_dict['end']:
            self.dfa_dict['end'].append(closure)

    def to_dfa(self):

        # 非空弧结点
        node_list = list(set(self.nfa_dict['varch']))
        node_list.sort()
        if 'ε' in node_list:
            node_list.remove('ε')
        start = self.nfa_dict['start'][0]
        end = self.nfa_dict['end'][0]
        # 开始结点的closure加入到closure数组中
        closure_start = self.get_closure(self.get_index(start))
        self.closure_list.append(closure_start)
        # 初始化状态集栈
        closure_stack = [closure_start]
        self.add_s_e(start, end, closure_start)
        while len(closure_stack):
            closure = closure_stack.pop(0)
            for node in node_list:
                closure_temp = []
                for i in closure:
                    # 得到该结点的弧转换 不管是nfa还是dfa,任意两个节点间(弧数《=1)最多只有一条相等的弧
                    transform = self.get_transform(i, node)
                    if transform == end:
                        closure_temp.append([transform])
                    elif transform != -1:
                        closure_temp.append(self.get_closure(self.get_index(transform)))
                    # if transform != -1:
                    #     # 从from中找到值为v的所有位置
                    #     result = self.get_index(transform)
                    #     if result:
                    #         closure_temp.append(self.get_closure(result))
                closure_temp = list(set([x for l in closure_temp for x in l]))
                closure_temp.sort()
                if not closure_temp:
                    continue
                self.dfa_dict['from'].append(closure)
                self.dfa_dict['to'].append(closure_temp)
                self.dfa_dict['varch'].append(node)
                self.add_s_e(start, end, closure_temp)
                # 确定起始结点和终止结点
                if closure_temp not in self.closure_list:
                    closure_stack.append(closure_temp)
                    self.closure_list.append(closure_temp)
        # 为dfa的状态集编号
        node_dict = {}
        # DFA编号
        node_i = 1
        for i in itertools.chain(self.dfa_dict['from'], self.dfa_dict['to']):
            if i not in list(node_dict.values()):
                node_dict[node_i] = i
                node_i += 1
        # 替换数组为状态
        for i in range(len(self.dfa_dict['from'])):
            self.dfa_dict['from'][i] = get_key(self.dfa_dict['from'][i], node_dict)
            self.dfa_dict['to'][i] = get_key(self.dfa_dict['to'][i], node_dict)
        for i in range(len(self.dfa_dict['start'])):
            self.dfa_dict['start'][i] = get_key(self.dfa_dict['start'][i], node_dict)
        for i in range(len(self.dfa_dict['end'])):
            self.dfa_dict['end'][i] = get_key(self.dfa_dict['end'][i], node_dict)
        # # 输出表格和状态转换图
        # # output_table()
        return self.dfa_dict

    # 得到所有的状态
    def get_all_states(self):
        result = []
        for i in itertools.chain(self.dfa_dict['from'], self.dfa_dict['to']):
            if i not in result:
                result.append(i)
        return result

    def init_divide(self):
        all_states = self.get_all_states()
        # 非终态集
        self.divide_part[self.divide_id] = list(set(all_states) - set(self.dfa_dict['end']))
        self.divide_id += 1
        # 终态集
        self.divide_part[self.divide_id] = self.dfa_dict['end']
        self.divide_id += 1
        print('初始化:', self.divide_part)

    # 得到所有的终结符
    def get_all_varches(self):
        result = []
        for i in self.dfa_dict['varch']:
            if i not in result:
                result.append(i)
        return result

    def get_min_key(self):
        result = list(self.divide_part.keys())
        result.sort()
        return result[0]

    def divide(self, d_part: list, varch):
        result = []
        for s in d_part:
            # 状态s是否能接受该终结符
            append_flag = 0
            for i in range(len(self.dfa_dict['from'])):
                if self.dfa_dict['from'][i] == s and self.dfa_dict['varch'][i] == varch:
                    # to状态在当前分割的状态集中的哪一个
                    result.append(get_in_key(self.dfa_dict['to'][i], self.divide_part))
                    append_flag = 1
                    break
            if append_flag != 1:
                result.append(-1)
        return result

    # 划分结果
    def divide_result(self, result_i: list, index_i):
        # 将当前分割前的状态弹出
        temp_list = self.divide_part.pop(index_i)
        lenth = len(set(result_i))
        if lenth > 1:
            # 按当前分割集编号来划分
            result = {}
            for i in range(len(result_i)):
                if result_i[i] not in result.keys():
                    result[result_i[i]] = [temp_list[i]]
                else:
                    result[result_i[i]].append(temp_list[i])
            for key, value in result.items():
                self.divide_part[self.divide_id] = value
                self.divide_id += 1
            return 1
        # 不能被分割
        else:
            self.divide_part[index_i] = temp_list
            return 0

    def get_next_i(self, i):
        divide_part_i = list(self.divide_part.keys())
        divide_part_i.sort()
        if i in divide_part_i:
            return i
        elif i - 1 in divide_part_i:
            return i
        elif i - 2 in divide_part_i:
            index_i = divide_part_i.index(i - 2)
            if index_i + 1 < len(divide_part_i):
                return divide_part_i[index_i + 1]
            else:
                return i
        else:
            return i

    # 重新对DFA进行编号
    def reset_index(self):
        i = 0
        new_divide = {}
        for key, value in self.divide_part.items():
            new_divide[i] = value
            i += 1
        self.divide_part = new_divide

    # 填mini_dfa
    def fill_mini_dfa(self):
        for i in self.dfa_dict['from']:
            self.mini_dfa['from'].append(get_in_key(i, self.divide_part))
        for i in self.dfa_dict['to']:
            self.mini_dfa['to'].append(get_in_key(i, self.divide_part))
        for i in self.dfa_dict['start']:
            self.mini_dfa['start'].append(get_in_key(i, self.divide_part))
        for i in self.dfa_dict['end']:
            self.mini_dfa['end'].append(get_in_key(i, self.divide_part))

        self.mini_dfa['varch'] = self.dfa_dict['varch'].copy()
        self.mini_dfa['start'] = list(set(self.mini_dfa['start']))
        self.mini_dfa['end'] = list(set(self.mini_dfa['end']))

    # 删除重复的弧
    def del_dup_arc(self):
        result = []
        i = 0
        while i < len(self.mini_dfa['from']):
            temp = [self.mini_dfa['from'][i], self.mini_dfa['to'][i], self.mini_dfa['varch'][i]]
            if temp in result:
                self.mini_dfa['from'].pop(i)
                self.mini_dfa['to'].pop(i)
                self.mini_dfa['varch'].pop(i)
            else:
                result.append(temp)
                i += 1

    def to_min_nfa(self):
        # 初始化 划分终态集和非终态集
        self.init_divide()
        # 得到所有的终结符
        all_varches = self.get_all_varches()
        # 循环两轮
        for k in range(1):
            # print("\n-------------第%d轮:--------------" % (k + 1))
            if k == 1:
                print(1)
                raise Exception('不可能有第二轮')
            # 开始划分
            pre_id = -1
            i = self.get_min_key()
            while pre_id != self.divide_id:
                while i < self.divide_id:
                    print("正在划分:", end='')
                    print("{} : {}".format(i, self.divide_part[i]))
                    for varch in all_varches:
                        result = self.divide(self.divide_part[i], varch)
                        divide_success = self.divide_result(result, i)
                        print("%s:结果" % varch, end='<>')
                        print(self.divide_part)
                        # 已经改变了当前分割集
                        if divide_success:
                            break
                    i = self.get_next_i(i + 1)
                pre_id = self.divide_id
        # 重新对分组进行编号
        self.reset_index()
        # 填写mini_DFA
        self.fill_mini_dfa()
        # 删除重复的弧
        self.del_dup_arc()
        return self.mini_dfa


if __name__ == '__main__':
    nfa_dict = {
        'from': ['i', '1', '1', '1', '2', '2', '3', '4', '5', '6', '6', '6'],
        'to': ['1', '1', '1', '2', '3', '4', '5', '5', '6', '6', '6', 'f'],
        'varch': ['ε', 'a', 'b', 'ε', 'a', 'b', 'a', 'b', 'ε', 'a', 'b', 'ε'],
        'start': ['i'],
        'end': ['f']

    }

    nfa = NFA('ab')
    nfa_dict = nfa.to_nfa()
    # draw(nfa_dict, save_nfa)
    dfa = DFA(nfa_dict)
    dfa.to_dfa()
    # draw(dfa.dfa_dict, save_dfa)
    dfa.to_min_nfa()
    # draw(dfa.mini_dfa, save_min_dfa)
