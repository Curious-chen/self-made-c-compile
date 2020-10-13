import copy


class anayword:
    def __init__(self):
        self.list_ = ['(', ')', '[', ']', '{', '}', ';', ' ', '+', '-', '*', '/', ',', '\n']  # 用于数字后跟的各种运算符、界符作为结束条件
        self.opt_list = ['+', '-', '*', '%', '&', '|', '!', '=']  # 对于判断运算符作为判断条件
        self.opt_other_list = ['.', '~', '(', ')', '[', ']', ':']  # 单目运算符列表
        self.split_list = [',', ';', '\'', '{', '}', ':', '\\', '、', '"', '#']  # 界符列表
        self.opt_all = ['<', '>', '/', '+', '-', '*', '%', '&', '|', '!', '=', '.', '~', '(', ')', '[', ']']

    def err_find(self, str, index, row, col, word):
        while index < len(str) and str[index] not in [' ', '\n', '\t', '+', '-', '*', '/', '%', '<', '>', '&', '^', ',',
                                                      '!', '=', ';']:  # 提取错误单词
            word.append(str[index])
            index += 1
            col += 1
        return word, index, row, col

    def alphabat(self, str, index, state, row, col):  # 判断字母
        word = []
        while index < len(str) and str[index] == ' ':
            index += 1
            col += 1
        while index < len(str) and state != 2:
            if state == 0:
                if str[index].isalpha() or str[index] == '_':  # 单词开始为字母或者下划线
                    word.append(str[index])
                    state = 1
            elif state == 1:
                if str[index].isdigit() or str[index].isalpha() or str[index] == '_':
                    word.append(str[index])
                    state = 1
                else:
                    index -= 1
                    col -= 1
                    state = 2
            index += 1
            col += 1
        return index, word, state, row, col

    def digit(self, str, index, state, row, col):  # 数字
        word = []
        pre_state = 0
        while index < len(str) and str[index] == ' ':  # 删去空格
            index += 1
            col += 1
        while index < len(
                str) and state != 9 and state != 10 and state != 11 and state != 12 and state != 15 and state != 18 and state != 19:
            if state == 0:
                if str[index].isdigit() and str[index] != '0':
                    word.append(str[index])
                    state = 3
                elif str[index] == '0':
                    word.append(str[index])
                    state = 13
            elif state == 3:
                if str[index].isdigit():  # 判断是数字
                    word.append(str[index])
                    state = 3
                elif str[index] == '.':
                    word.append(str[index])
                    state = 4
                elif str[index] == 'E' or str[index] == 'e':
                    word.append(str[index])
                    state = 6
                elif str[index] in self.list_:  # 判断为整数
                    index -= 1
                    col -= 1
                    state = 9
                else:  # TODO 如何判断整数错误并得到完整的错误字符串
                    index -= 1
                    col -= 1
                    pre_state = 3
                    state = 11
            elif state == 4:
                if str[index].isdigit():
                    word.append(str[index])
                    state = 5
                else:  # TODO 如何判断整数错误并得到完整的错误字符串
                    index -= 1
                    col -= 1
                    pre_state = 4
                    state = 11
            elif state == 5:
                if str[index].isdigit():
                    word.append(str[index])
                    state = 5
                elif str[index] == 'e' or str[index] == 'E':
                    word.append(str[index])
                    state = 6
                elif str[index] in self.list_:  # 得到小数
                    index -= 1
                    col -= 1
                    state = 10
                else:  # TODO 如何判断整数错误并得到完整的错误字符串
                    index -= 1
                    col -= 1
                    pre_state = 5
                    state = 11
            elif state == 6:
                if str[index] == '+' or str[index] == '-':
                    word.append(str[index])
                    state = 7
                elif str[index].isdigit():
                    word.append(str[index])
                    state = 8
                else:  # TODO 如何判断整数错误并得到完整的错误字符串
                    index -= 1
                    col -= 1
                    pre_state = 6
                    state = 11
            elif state == 7:
                if str[index].isdigit():
                    word.append(str[index])
                    state = 8
                else:  # TODO 如何判断整数错误并得到完整的错误字符串
                    index -= 1
                    col -= 1
                    pre_state = 7
                    state = 11
            elif state == 8:
                if str[index].isdigit():
                    word.append(str[index])
                    state = 8
                elif str[index] in self.list_:
                    index -= 1
                    col -= 1
                    state = 12
                else:  # TODO 如何判断整数错误并得到完整的错误字符串
                    index -= 1
                    col -= 1
                    pre_state = 8
                    state = 11
            elif state == 13:
                if '0' <= str[index] <= '7':
                    word.append(str[index])
                    state = 14
                elif str[index] == 'x' or str[index] == 'X':
                    word.append(str[index])
                    state = 16
                elif str[index] == '.':
                    word.append(str[index])
                    state = 4
                elif str[index] in self.list_:
                    index -= 1
                    col -= 1
                    state = 19
                else:
                    index -= 1
                    col -= 1
                    pre_state = 13
                    state = 11
            elif state == 14:
                if '0' <= str[index] <= '7':
                    word.append(str[index])
                    state = 14
                else:
                    index -= 1
                    col -= 1
                    state = 15  # 八进制
            elif state == 16:
                if str[index].isdigit() or 'a' <= str[index] <= 'f' or 'A' <= str[index] <= 'F':
                    word.append(str[index])
                    state = 17
                else:
                    index -= 1
                    col -= 1
                    pre_state = 16
                    state = 11
            elif state == 17:
                if str[index].isdigit() or str[index].isalpha():
                    word.append(str[index])
                    state = 17
                else:
                    index -= 1
                    col -= 1
                    state = 18  # 十六进制
            index += 1
            col += 1
        return index, word, state, row, col

    def opt_grea(self, str, index, state, row, col):  # >> << >>= << = < >
        word = []
        while index < len(
                str) and state != 24 and state != 25 and state != 26 and state != 27 and state != 28 and state != 29:
            if state == 0:
                if str[index] == '>':
                    word.append(str[index])
                    state = 20
                elif str[index] == '<':
                    word.append(str[index])
                    state = 21
            elif state == 20:
                if str[index] == '>':
                    word.append(str[index])
                    state = 22
                elif str[index] == '=':
                    word.append(str[index])
                    state = 24
                else:
                    index -= 1
                    col -= 1
                    state = 25
            elif state == 22:
                if str[index] == '=':
                    word.append(str[index])
                    state = 24
                else:
                    index -= 1
                    col -= 1
                    state = 27
            elif state == 21:
                if str[index] == '<':
                    word.append(str[index])
                    state = 23
                elif str[index] == '>' or str[index] == '=':
                    word.append(str[index])
                    state = 26
                else:
                    index -= 1
                    col -= 1
                    state = 29
            elif state == 23:
                if str[index] == '=':
                    word.append(str[index])
                    state = 24
                else:
                    index -= 1
                    col -= 1
                    state = 28
            index += 1
            col += 1
        return index, word, state, row, col

    def opt_eql(self, str, index, state, row, col):  # 各种运算符
        word = []
        while index < len(
                str) and state != 45 and state != 46 and state != 47 and state != 48 and state != 49 and state != 50 and state != 51 and state != 52:
            if state == 0:
                if str[index] == '+':
                    word.append(str[index])
                    state = 38
                elif str[index] == '-':
                    word.append(str[index])
                    state = 39
                elif str[index] == '*':
                    word.append(str[index])
                    state = 40
                elif str[index] == '=' or str[index] == '%':
                    word.append(str[index])
                    state = 41
                elif str[index] == '&':
                    word.append(str[index])
                    state = 42
                elif str[index] == '|':
                    word.append(str[index])
                    state = 43
                elif str[index] == '!':
                    word.append(str[index])
                    state = 44
            elif state == 38:
                if str[index] in ['+', '=']:
                    word.append(str[index])
                    state = 45
                else:
                    index -= 1
                    col -= 1
                    state = 52
            elif state == 39:
                if str[index] in ['-', '=', '>']:
                    word.append(str[index])
                    state = 46
                else:
                    index -= 1
                    col -= 1
                    state = 52
            elif state == 40:
                if str[index] in ['*', '=']:
                    word.append(str[index])
                    state = 47
                else:
                    index -= 1
                    col -= 1
                    state = 52
            elif state == 41:
                if str[index] in ['=']:
                    word.append(str[index])
                    state = 48
                else:
                    index -= 1
                    col -= 1
                    state = 52
            elif state == 42:
                if str[index] in ['&', '=']:
                    word.append(str[index])
                    state = 49
                else:
                    index -= 1
                    col -= 1
                    state = 52
            elif state == 43:
                if str[index] in ['|', '=']:
                    word.append(str[index])
                    state = 50
                else:
                    index -= 1
                    col -= 1
                    state = 52
            elif state == 44:
                if str[index] in ['!', '=']:
                    word.append(str[index])
                    state = 51
                else:
                    index -= 1
                    col -= 1
                    state = 52
            index += 1
            col += 1
        return index, word, state, row, col

    def opt_note(self, str, index, state, row, col):  # 注释
        word = []
        while index < len(str) and state != 33 and state != 35 and state != 36 and state != 37:
            if state == 0:
                if str[index] == '/':
                    word.append(str[index])
                    state = 30
            elif state == 30:
                if str[index] == '*':
                    word.append(str[index])
                    state = 31
                elif str[index] == '/':
                    word.append(str[index])
                    state = 34
                elif str[index] == '=':
                    word.append(str[index])
                    state = 36
                else:
                    index -= 1
                    col -= 1
                    state = 37
            elif state == 31:
                if str[index] == '*':
                    word.append(str[index])
                    state = 32
                else:
                    word.append(str[index])
                    if str[index] == '\n':
                        row += 1
                        col = 0
            elif state == 32:
                if str[index] == '/':  # 多行注释直接跳过
                    word.clear()
                    state = 33
                else:  # 判断不以 */结束却进入了*等待/出现的多行注释状态，期间如果遇到换行就进行行数++操作并将列数清零
                    if str[index] == '\n':
                        row += 1
                        col = 0
            elif state == 34:
                if str[index] == '\n':
                    row += 1
                    col = 0
                    word.clear()
                    state = 35
                else:
                    word.append(str[index])
            index += 1
            col += 1
        return index, word, state, row, col

    def opt_other(self, str, index, state, row, col):  # 各种单目运算符
        word = []
        while index < len(str) and state != 53:
            if str[index] in self.opt_other_list:
                word.append(str[index])
                state = 53
            index += 1
            col += 1
        return index, word, state, row, col

    def split_(self, str, index, state, row, col):  # 界符
        word = []
        while index < len(str) and str[index] == ' ':
            index += 1
            col += 1
        while index < len(
                str) and state != 55 and state != 56 and state != 57 and state != 60 and state != 61 and state != 67 and state != 68:
            if state == 0:
                if str[index] == '"':  # 处理字符串
                    word.append(str[index])
                    state = 54
                elif str[index] == '\'':  # 处理字符
                    word.append((str[index]))
                    state = 58
                elif str[index] == '#':
                    word.append(str[index])
                    state = 63
                elif str[index] in self.split_list:
                    word.append(str[index])
                    state = 56
            elif state == 54:
                if str[index] == '"':  # 表示字符串结束
                    word.append(str[index])
                    state = 55
                elif str[index] == '\n':  # 代表异常终止
                    state = 57  # 出错状态
                else:
                    word.append(str[index])
                    state = 54
            elif state == 58:
                word.append(str[index])
                state = 59
            elif state == 59:
                if str[index] == '\'':  # 表示字符串结束
                    word.append(str[index])
                    state = 60
                else:  # 代表异常终止
                    index -= 1
                    col -= 1
                    state = 61  # 出错状态
            elif state == 63:
                if str[index].isalpha():
                    word.append((str[index]))
                    state = 63
                elif str[index] == '<':
                    word.append((str[index]))
                    state = 64
                else:
                    index -= 1
                    col -= 1
                    state = 68  # 出错
            elif state == 64:
                if str[index].isalpha():
                    word.append((str[index]))
                    state = 64
                elif str[index] == '.':
                    word.append((str[index]))
                    state = 65
                else:
                    index -= 1
                    col -= 1
                    state = 68  # 出错
            elif state == 65:
                if str[index].isalpha():
                    word.append((str[index]))
                    state = 66
                else:
                    index -= 1
                    col -= 1
                    state = 68  # 出错
            elif state == 66:
                if str[index] == '>':
                    word.append((str[index]))
                    state = 67
                else:
                    index -= 1
                    col -= 1
                    state = 68  # 出错
            index += 1
            col += 1
        return index, word, state, row, col

    def opt(self, str, index, state, row, col):
        word = []
        while index < len(str) and str[index] == ' ':
            index += 1
            col += 1
        if str[index] == '<' or str[index] == '>':
            index, word, state, row, col = self.opt_grea(str, index, state, row, col)
        elif str[index] in self.opt_list:
            index, word, state, row, col = self.opt_eql(str, index, state, row, col)
        elif str[index] == '/':
            index, word, state, row, col = self.opt_note(str, index, state, row, col)
        elif str[index] in self.opt_other_list:
            index, word, state, row, col = self.opt_other(str, index, state, row, col)
        return index, word, state, row, col

    def other(self, str, index, state, row, col):
        word = []
        while index < len(str) and str[index] == ' ':
            index += 1
            col += 1
        while index < len(str) and state != 62:
            word.append(str[index])
            index += 1
            col += 1
            state = 62  # 表示无法识别的字符

        return index, word, state, row, col

    def read_file(self, s):
        all_word = []
        row, col = 0, 0
        # with open(path, 'r', encoding='UTF-8') as f:
        #     strs = f.readlines()
        #     print(strs)
        #     s = ''.join(strs)
        index = 0
        while index < len(s):
            state = 0
            if s[index] == '\n' or s[index] == '\t' or s[index] == ' ':
                if s[index] == '\n':  # 表示遇到换行就进行 行列的重置
                    row += 1
                    col = 0
                else:
                    col += 1
                index += 1
                word.clear()  # 目的是删除上一次的结果
            elif s[index].isalpha():
                index, word, state, row, col = self.alphabat(s, index, state, row, col)
            elif s[index].isdigit():
                index, word, state, row, col = self.digit(s, index, state, row, col)
            elif s[index] in self.split_list:
                index, word, state, row, col = self.split_(s, index, state, row, col)
            elif s[index] in self.opt_all:
                index, word, state, row, col = self.opt(s, index, state, row, col)
            else:
                index, word, state, row, col = self.other(s, index, state, row, col)
            if len(word) != 0:
                if state == 11 or state == 61 or state == 68:
                    word, index, row, col = self.err_find(s, index, row, col, word)
                    all_word.append([''.join(word), state, row, col])
                else:
                    all_word.append([''.join(word), state, row, col])
            if state == 57:  # 表示单字符遇到符号不匹配行尾是进行手动换行
                row += 1
                col = 0
        return all_word

    def token(self, all_word):
        token_word = dict()
        token_code = []
        with open('Lexical/code.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for pre_ in lines:
                pre_ = pre_.replace('\n', '').split(' ')
                token_word[pre_[0]] = pre_[1]
        words = list(token_word.keys())
        for word in all_word:
            if word[1] == 2:  # 字母 1
                if word[0] in words:
                    token_code.append([word[0], token_word[word[0]], word[2], word[3]])
                else:
                    token_code.append([word[0], 700, word[2], word[3]])
            if word[1] == 9 or word[1] == 15 or word[1] == 18 or word[1] == 19:  # 整数数字
                token_code.append([word[0], 400, word[2], word[3]])
            if word[1] == 10 or word[1] == 12:  # 小数 2
                token_code.append([word[0], 800, word[2], word[3]])
            if 24 <= word[1] <= 53:  # 运算符 4
                if word[0] in words:
                    token_code.append([word[0], token_word[word[0]], word[2], word[3]])
            if word[1] == 55:  # 字符串
                token_code.append([word[0], 600, word[2], word[3]])
            if word[1] == 56:  # 分界符3
                if word[0] in words:
                    token_code.append([word[0], token_word[word[0]], word[2], word[3]])
            if word[1] == 60:  # 字符
                token_code.append([word[0], 500, word[2], word[3]])
            if word[1] == 11 or word[1] == 57 or word[1] == 61 or word[1] == 62 or word[1] == 68:  # 错误信息
                token_code.append([word[0], word[1], word[2], word[3]])
            if word[1] == 67:  # 头文件
                pass
        print(token_code)
        return token_code


if __name__ == '__main__':
    index, state = 0, 0
    T = anayword()
    all_ = T.read_file('1.txt')
    T.token(all_)
