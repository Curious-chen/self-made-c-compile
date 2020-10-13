from collections import defaultdict
import copy


class Opt_:
    def __init__(self):
        self.stack, self.list_, self.all_exp = [], [], []
        self.first = defaultdict(set)  # 构建元素映射到多个元素（集合）的字典
        self.last = defaultdict(set)
        self.vt = None
        # self.vt = ['+', '*', 'i', '(', ')', '#']
        pass

    def read_file(self, lines):
        # with open(path, 'r', encoding='UTF-8') as f:
        #     lines = f.readlines()
        lines = lines.split('\n')
        for pre_ in lines:
            item = pre_.split('->')
            item_left = item[0].strip()
            item_right = item[1].split('|')
            if item_left not in self.list_: self.list_.append(item_left)
            for pre_word in item_right:
                self.stack.append(item_left + '->' + pre_word.strip())
        # print(self.stack)
        self.getVt()
        # print(self.vt)

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
        # print(all_word, key_word)
        self.vt = list(all_word - key_word - {'ε'})

    def Init(self):
        F = dict()
        for vn in self.list_:
            for vt in self.vt:
                F[(vn, vt)] = 0
        return F

    def fistrVt(self):
        first_stack = []
        F = self.Init()
        for _per in self.stack:
            _per = _per.split('->')
            _per_right = _per[1].split(' ')
            # P->a...
            if _per_right[0] in self.vt:
                F[(_per[0], _per_right[0])] = 1
                first_stack.append((_per[0], _per_right[0]))
            # P->Qa...
            elif len(_per_right) > 2 and _per_right[0] in self.list_ and _per_right[1] in self.vt:
                F[(_per[0], _per_right[1])] = 1
                first_stack.append((_per[0], _per_right[1]))
        while len(first_stack) != 0:
            tmp = first_stack.pop()
            for _per in self.stack:
                _per = _per.split('->')
                _per_right = _per[1].split(' ')
                # P->Q...
                if _per_right[0] == tmp[0] and F[(_per[0], tmp[1])] == 0 and (_per[0], tmp[1]) not in first_stack:
                    F[(_per[0], tmp[1])] = 1
                    first_stack.append((_per[0], tmp[1]))
        for i in F.keys():
            if F[i] == 1:
                self.first[i[0]].add(i[1])

    def lastVt(self):
        last_stack = []
        F = self.Init()
        for _per in self.stack:
            _per = _per.split('->')
            _per_right = _per[1].split(' ')
            # P->...a
            if _per_right[-1] in self.vt:
                F[(_per[0], _per_right[-1])] = 1
                last_stack.append((_per[0], _per_right[-1]))
            # P->...aQ
            elif len(_per_right) > 2 and _per_right[-1] in self.list_ and _per_right[-2] in self.vt:
                F[(_per[0], _per_right[-2])] = 1
                last_stack.append((_per[0], _per_right[-2]))
        while len(last_stack) != 0:
            tmp = last_stack.pop()
            for _per in self.stack:
                _per = _per.split('->')
                _per_right = _per[1].split(' ')
                # P->...Q
                if _per_right[-1] == tmp[0] and F[(_per[0], tmp[1])] == 0 and (_per[0], tmp[1]) not in last_stack:
                    F[(_per[0], tmp[1])] = 1
                    last_stack.append((_per[0], tmp[1]))
        for i in F.keys():
            if F[i] == 1:
                self.last[i[0]].add(i[1])

    def find_index(self, table, str1, str2):
        row, col = 0, 0
        for index, per in enumerate(table):  # 可能存在bug
            if str1.strip() == per[0] and index > 0:
                row = index
                break
        for index_, per_ in enumerate(table[0]):
            if str2 == per_:  # 终结符在的位置
                col = index_
                break
        return row, col

    def op_table(self):
        table = [[0] * (len(self.vt) + 1) for i in range(len(self.vt) + 1)]
        for index, per in enumerate(table):
            if 0 < index <= len(self.vt):
                per[0] = self.vt[index - 1]
        for index, per_ in enumerate(table[0]):
            if index > 0:
                table[0][index] = self.vt[index - 1]
        for _per in self.stack:
            _per = _per.split('->')
            _per_right = _per[1].split(' ')
            for index in range(0, len(_per_right) - 1):
                # p -> ...ab...
                if _per_right[index] in self.vt and _per_right[index + 1] in self.vt:
                    row, col = self.find_index(table, _per_right[index], _per_right[index + 1])
                    table[row][col] = '='
                if index < len(_per_right) - 2 and _per_right[index] in self.vt and _per_right[
                    index + 1] in self.list_ and _per_right[
                    index + 2] in self.vt:
                    row, col = self.find_index(table, _per_right[index], _per_right[index + 2])
                    table[row][col] = '='
                if _per_right[index] in self.vt and _per_right[index + 1] in self.list_:
                    for i in list(self.first[_per_right[index + 1]]):
                        row, col = self.find_index(table, _per_right[index], i)
                        table[row][col] = '<'
                if _per_right[index] in self.list_ and _per_right[index + 1] in self.vt:
                    for i in list(self.last[_per_right[index]]):
                        row, col = self.find_index(table, i, _per_right[index + 1])
                        table[row][col] = '>'
        # for i in table:
        #     for j in i:
        #         print('{:<3s}'.format(str(j)), end='')
        #     print()
        return table

    def Statute(self, list_, Q):
        for _per in self.stack:
            _per = _per.split('->')
            _per_right = _per[1].split(' ')
            if Q in ['+', '-', '*', '/'] and Q in _per_right and Q in list_:
                return _per[0]
            elif ''.join(_per_right) == ''.join(list_):
                return _per[0]
        return ''

    def __annalysis__(self, table, token):
        result = []
        S = ['#']
        top, index = 0, 0
        while True:
            list_ = []
            list_.append(S)
            list_.append(token[index:])
            if S[top] in self.vt:
                j = top
            elif S[top] in self.list_:
                j = top - 1
            row, col = self.find_index(table, S[j], token[index])
            if table[row][col] == '<' or table[row][col] == '=':
                if ''.join(S[0:len(S)]) == '#E' and token[index] == '#':
                    list_.append(S)
                    list_.append(token[index:])
                    list_.append([token[index - 1], '规约'])
                    result.append(copy.deepcopy(list_))
                    # print("字符串分析成功")
                    break
                # print('{} {} 压栈'.format(S, token[index]))
                list_.append([token[index], '压栈'])
                top += 1
                S.append(token[index])
                index += 1
            elif table[row][col] == '>':
                # print('{} {} 规约'.format(S, token[index]))
                list_.append([token[index - 1], '规约'])
                while True:
                    Q = S[j]
                    if S[j - 1] in self.vt:
                        j = j - 1
                    else:
                        j = j - 2
                    row, col = self.find_index(table, S[j], Q)
                    if table[row][col] == '<':
                        break
                sta = self.Statute(S[j + 1:top + 1], Q)
                S = S[0:j + 1]
                S.append(sta)
                top = j + 1
            else:
                # print('错误')
                return result,False
            result.append(copy.deepcopy(list_))
        return result,True


if __name__ == '__main__':
    O = Opt_()
    O.read_file('opt_gram.txt')
    O.fistrVt()
    O.lastVt()
    print(O.last)
    table = O.op_table()
    O.__annalysis__(table, ['i', '+', 'i', '+', 'i', '#'])
    pass
