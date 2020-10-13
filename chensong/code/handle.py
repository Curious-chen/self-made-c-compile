"""
    手动构造词法分析器
    2020/03/10
"""

"""
    具体要求:
        组织源程序的输入
        按规则拼单词，并转换为二元式形式
        删除注释行、空格及无用符号
        行计数、列计数
        列表打印源程序
        发现并定义语法错误
"""
from chensong.code.seedCode import sc_boundary, sc_Keyword, sc_operator, sc_other

from chensong.code.model import is_terminal, Sponser, TreeNode
from collections import namedtuple
import os, re

nextWord_space = [' ', '\n', '\t', '+', '-', '*', '/', '%', '<', '>', '&', '^', ',', '!', '=', ';', ')', '(']


# 词法分析器
class LexicalAnalysis:
    def __init__(self, file_path=None):
        # 读取代码
        self.content = str()
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        # 初始化行列
        self.l, self.c = 1, 0
        self.content = re.sub('#[\s\S]*?\n', '', self.content)
        self.content = re.sub('//[\s\S]*?\n', '', self.content)

        # 分析结果集
        self.result_lex = list()
        # 错误集，错误直接停止
        self.result_error = list()
        # token
        self._Token = namedtuple('Token', 'cur_line cur_col val s_code id typ')
        self._token_list = []

    def get_token_list(self):
        if not self._token_list and self.result_lex:
            for i, v in enumerate(self.result_lex):
                self._token_list.append(self._Token(*v[:4], i, v[-1]))
        return self._token_list

    def analysis(self, content=None):
        self.content = content if content else self.content
        self.content += '\n'
        self.content = re.sub('#[\s\S]*?\n', '', self.content)
        self.content = re.sub('//[\s\S]*?\n', '', self.content)
        ind = 0
        c_len = len(self.content)
        while ind < c_len:
            cha = self.content[ind]
            # 字母或下划线->关键字标识符
            if 'a' <= cha <= 'z' or 'A' <= cha <= 'Z' or cha == '_':
                ind = self.kwAndid(ind)
            # 数字
            elif '0' <= cha <= '9':
                ind = self.isNum(ind)
            # 单引号->字母
            elif cha == r"'":
                ind = self.ischar(ind)
            # 双引号 -> 字符串
            elif cha == r'"':
                ind = self.isString(ind)
            elif cha in [' ', '\t', '\n']:
                if cha == '\n':
                    self.l += 1
                    self.c = 0
                else:
                    self.c += 1
                ind += 1
            else:
                ind = self.isOther(ind)
            if isinstance(int, tuple):
                return False
        return True

    def error_deal(self, start, info=str()):
        # 错误处理，直接跳到下一个单词开始
        end = start
        for ch in self.content[start:]:
            if ch in nextWord_space:
                break
            end += 1
        # 错误点坐标(行号，列号)，错误内容，附加信息，表明什么地方错了
        self.result_error.append(((self.l, self.c), self.content[start:end], info))
        # 改变列坐标
        self.c += (end - start)
        return end

    def lex_add(self, args):
        try:
            word, seed_code, info = args
        except Exception as e:
            print(type(args))
            print(e)
        self.result_lex.append((self.l, self.c, word, seed_code, info))

    # 如果是注释
    def isNotes(self, start):
        ind = start
        while ind < len(self.content):
            ch2 = self.content[ind:ind + 2]  # 避免越界错误
            if ch2 == '*/':
                self.result_lex.pop()
                return ind + 2
            ind += 1
        return -1

    def isOther(self, start):
        cha1 = self.content[start]
        cha2 = self.content[start:start + 2]
        cha3 = self.content[start:start + 3]

        if cha3 in sc_operator:
            self.lex_add((cha3, sc_operator[cha3], cha3.upper()))
            return start + 3
        elif cha2 in sc_operator:
            self.lex_add((cha2, sc_operator[cha2], cha2.upper()))
            return start + 2
        elif cha2 in sc_boundary:
            # if 是 c的注释，需要跳过执行，直到遇到"/*"
            self.lex_add((cha2, sc_boundary[cha2], cha2.upper()))
            if cha2 == '/*':
                return self.isNotes(start + 2)
            return start + 2
        elif cha1 in sc_operator:
            self.lex_add((cha1, sc_operator[cha1], cha1.upper()))
        elif cha1 in sc_boundary:
            self.lex_add((cha1, sc_boundary[cha1], cha1.upper()))
        elif cha1 in sc_other:
            self.lex_add((cha1, sc_other[cha1], cha1.upper()))
        else:
            self.lex_add((cha1, 0, '未定义'))
        return start + 1

    def ischar(self, start):
        end = start + 1

        for ch in self.content[start + 1:]:
            if ch == r"'" or ch in nextWord_space:
                break
            end += 1
        if (end - start) <= 2:
            self.lex_add((self.content[start:end + 1], sc_other['字符'], 'CHARACTER'))
        else:
            return self.error_deal(start, "只能有一个字符")
        self.c += (end - start + 1)
        return end + 1

    def isString(self, start):
        end = start + 1
        while end < len(self.content):
            cha = self.content[end]
            if cha == '"':
                break
            end += 1
        if end >= len(self.content):
            return -1
        self.lex_add((self.content[start:end + 1], sc_other['字符串'], 'STRING_LITERAL'))
        return end + 1

    def kwAndid(self, start):
        end = start + 1

        for cha in self.content[start + 1:]:
            # 字母或下划线
            if not ('a' <= cha <= 'z' or 'A' <= cha <= 'Z' or cha == '_' or '0' <= cha <= '9'):
                break
            end += 1

        # 判断是否为关键字
        kw = self.content[start:end]
        try:
            # 添加识别的关键字或标识符
            if kw.lower() in sc_Keyword:
                self.lex_add((kw, sc_Keyword[kw.lower()], kw.upper()))
            else:
                self.lex_add((kw, sc_other['标识符'], 'IDENTIFIER'))
        except Exception as e:
            print(e)

        # 改变列
        self.c += (end - start)
        return end

    # 八进制
    def isOctol(self, Rstart, start):
        is_next_line = False
        end = start + 1
        for cha in self.content[start + 1:]:
            if '0' <= cha <= '7':
                pass
            elif cha in nextWord_space:
                break
            else:
                return self.error_deal(Rstart, "八进制数常量构词错误")
            end += 1
        # 添加识别的单词
        kw = self.content[Rstart:end]
        self.lex_add((kw, sc_other['整数'], 'INTERGER'))

        # 改变列坐标
        self.c += (end - start)
        return end

    # 十六进制
    def isHexadecimal(self, Rstart, start):
        is_next_line = False
        end = start + 1
        for cha in self.content[start + 1:]:
            if ('0' <= cha <= '9') or ('a' <= cha <= 'f') or ('A' <= cha <= 'F'):
                pass
            elif cha in nextWord_space:
                break
            else:
                return self.error_deal(Rstart, "十六进制数常量构词错误")
            end += 1

        # 添加识别的单词
        kw = self.content[Rstart:end]
        self.lex_add((kw, sc_other['整数'], 'INTERGER'))

        # 改变行坐标
        self.c += (end - start)
        return end

    def isScientificCount(self, Rstart, start):
        end = start + 1
        # 考虑+-的科学计数法
        end = end + 1 if self.content[end] in ['+', '-'] else end
        for cha in self.content[end:]:
            if '0' <= cha <= '9':
                pass
            elif cha in nextWord_space:
                break
            else:
                return self.error_deal(Rstart, "科学计数法数常量构词错误")
            end += 1
        # 添加识别的单词
        kw = self.content[Rstart:end]
        self.lex_add((kw, sc_other['浮点数'], 'FLOATOR'))

        # 改变列坐标
        self.c += (end - start)
        return end

    # 是浮点数？
    def isFloat(self, Rstart, start):
        end = start + 1
        for cha in self.content[start + 1:]:
            if '0' <= cha <= '9':
                pass
            elif cha in ['E', 'e']:
                return self.isScientificCount(Rstart, end)
            elif cha in nextWord_space:
                break
            else:
                return self.error_deal(Rstart, "实数常量构词错误")
            end += 1

        # 添加识别的单词
        kw = self.content[Rstart:end]
        self.lex_add((kw, sc_other['浮点数'], 'FLOATOR'))

        # 改变列坐标
        self.c += (end - start)
        return end

    # 整数？
    def isInteger(self, Rstart, start):
        end = start + 1
        for cha in self.content[start + 1:]:
            if '0' <= cha <= '9':
                pass
            elif cha == '.':
                return self.isFloat(Rstart, end)
            elif cha in ['E', 'e']:
                return self.isScientificCount(Rstart, end)
            elif cha in nextWord_space:
                break
            else:
                return self.error_deal(Rstart, "数字常量构词错误")
            end += 1

        # 添加识别的单词
        kw = self.content[Rstart:end]
        self.lex_add((kw, sc_other['整数'], 'INTERGER'))

        # 改变列坐标
        self.c += (end - start)
        return end

    def isNum(self, start):
        end = start + 1
        num = self.content[start]
        cha = num
        if cha == '0':
            cha = self.content[end]
            if '0' <= cha <= '7':
                return self.isOctol(start, end)
            elif cha in ['x', 'X']:
                return self.isHexadecimal(start, end)
            elif cha == '.':
                return self.isFloat(start, end)
            elif cha in nextWord_space:
                pass
            else:
                # 发生错误
                return self.error_deal(start, "数字常量构词错误")
        elif '1' <= cha <= '9':
            cha = self.content[end]
            if '0' <= cha <= '9':
                return self.isInteger(start, end)
            elif cha == '.':
                return self.isFloat(start, end)
            elif cha in ['E', 'e']:
                return self.isScientificCount(start, end)
            elif cha in nextWord_space:
                pass
            else:
                return self.error_deal(start, "数字常量构词错误")

        # 添加识别的单词
        kw = self.content[start:end]
        self.lex_add((kw, sc_other['整数'], 'INTERGER'))

        # 改变列坐标
        self.c += (end - start)
        return end


"""
    语法分析器
    created by Curious
    2020/04/02
"""

from chensong.code.model import to_dot, add_tree_node


class SyntaxAnalysis:
    def __init__(self, file_path=''):
        # 以字典形式存放
        self.g_dict = dict()
        gammar = str()
        # file_path 文法规则路径
        if os.path.exists(file_path):
            self.read_to_dict(file_path)
        else:
            raise Exception("文法路径错误")

    # 将文本形式的转换为字符形式
    def read_to_dict(self, file_path):
        # 单引号标注的为结符或运算符
        # 全大写的单词为文本形式的终结符
        # 否则均为非终结符
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            grammar = f.read()
        # 将文法中的注释清除
        grammar = re.sub("[^']#.*", '', grammar)
        # 将每个文法分割出来
        g_list = re.findall(r"([\s\S]*?):([\s\S]*?)[^'];", grammar)

        # print('------------------------------转化后的文法--------------------------------------')
        for g in g_list:
            # 非终结符
            non_terminal = g[0].strip()
            # 候选式
            candidate_list = [i.strip() for i in re.split(r"[^'|]\|", g[1])]  # 避免 ‘|’
            # 拆分每个候选式,将每个word单独列出
            # candidate_list = [tuple(candidate.split(' ')) for candidate in candidate_list]
            # 去除边界符和运算符间的‘’ eg: '|' -> |
            candidate_list = [tuple([_[1:-1] if _[0] == "'" else _ for _ in re.split(r" ", candidate)]) for candidate in
                              candidate_list]
            # 组装成字典
            if non_terminal in self.g_dict:
                self.g_dict[non_terminal].candidate_list.extend(candidate_list)
            else:
                self.g_dict[non_terminal] = Sponser(candidate_list)
            # print("{:30s} -> {:}".format(non_terminal, candidate_list))
        # print('-----------------------------------------------------------------------------')

    # 判断其是否为终结符

    # 获得First集
    def get_first(self):
        # A->aT or A->EMPTY
        for non_t, sponser in self.g_dict.items():
            # 获得候选式
            candidate_list = sponser.candidate_list
            # print('cal:', candidate_list)
            for candidate in candidate_list:
                # 获得每个候选式的首单词
                word = candidate[0]
                if is_terminal(word) or word == 'EMPTY':
                    sponser.first[word] = candidate
                else:
                    sponser.first_relation[candidate] = None

        # A->X1X2X3a
        for non_t, sponser in self.g_dict.items():
            # 获得候选关系表
            first_relation = sponser.first_relation
            ks = [c for c in first_relation.keys()]
            for candidate in ks:
                # 计数，截断
                count = 0
                # 是否停止查找
                flag = True
                for word in candidate:
                    count += 1
                    # 非结符，找其候选式是否存在EMPTY
                    if not is_terminal(word):
                        for can in self.g_dict[word].candidate_list:
                            if can[0] == 'EMPTY':
                                flag = False
                                break
                    else:
                        flag = False
                    if flag:
                        break
                first_relation[candidate] = count

        # 依靠FIRST关系表,将其关系表中的word的FIRST集中元素加入其中
        for non_t, sponser in self.g_dict.items():
            first_relation = sponser.first_relation
            # 对每个候选式递归地求first
            for candidate, count in first_relation.items():
                canc = list(candidate[:count])
                for word in canc:
                    if not is_terminal(word):
                        # 对应非终结符的FIRST集
                        first = self.g_dict[word].first
                        # 终结符 ->产生式
                        first: dict
                        for k in first:
                            if k == "EMPTY":
                                continue
                            if k not in sponser.first:
                                sponser.first[k] = candidate
                        # 将对应非终结符的first关系链表加入此产生式对应的关系表中
                        for k, v in self.g_dict[word].first_relation.items():
                            for w in k[:v]:
                                if w not in canc:
                                    canc: list
                                    canc.append(w)
                    else:
                        sponser.first[word] = candidate

    # 获得Follow集
    def get_follow(self, t_unit='translation_unit'):

        # 将# 加入到开始符号的follow集中
        if t_unit in self.g_dict:
            self.g_dict[t_unit].follow.append('#')
        else:
            raise Exception("求follow出错，未定义开始符号")
        while True:
            # 获得当前follow集，以此判断follow集经过定义是否增大
            test_follow = {k: [i for i in v.follow] for k, v in self.g_dict.items()}
            # 经过定义后的follow集
            self._get_follow()
            # 去除follow集中重复的元素
            for k, v in self.g_dict.items():
                self.g_dict[k].follow = list(set(v.follow))

            current_follow = {k: [i for i in v.follow] for k, v in self.g_dict.items()}
            # 如果follow集未增大，即循环结束
            # if test_follow != current_follow:
            #     break
            #
            # print("-----------------------------求follow不相等-------------------------------------------")
            flag = True
            for k, v in self.g_dict.items():
                if set(v.follow) != set(test_follow[k]):
                    flag = False
                    # print("{:30s} -> {:}".format(k, v.candidate_list))
                    # print("{:}   != {:}".format(test_follow[k], v.follow))
                    break
            if flag:
                print('全部follow集没有改变')
                break

    def _get_follow(self):
        # 遍历所有非终结符的产生式
        for k, v in self.g_dict.items():
            for candidate in v.candidate_list:
                # 若候选式中仅有一个单词，一定是非终结符
                if len(candidate) == 1:
                    if not is_terminal(candidate[0]):
                        self.g_dict[candidate[0]].follow.extend(v.follow)
                else:
                    # 得到候选式的逆序
                    temp = candidate[::-1]
                    if not is_terminal(temp[0]):
                        # 定义flag,避免 S ->ABD B-->EMPTY D!-->EMPTY
                        flag = True
                        # S - > ABD 即folow(D) +=follow(S)
                        self.g_dict[temp[0]].follow.extend(v.follow)
                        temp1 = temp[0]
                        for i in temp[1:]:
                            # 当前i是终结符，则跳过
                            if is_terminal(i):
                                temp1 = i
                                flag = False
                            else:
                                # S-> ABD 即folow(A) += first(BD/EMPTY)
                                # folow(B) +=First(D/EMPTY)
                                # folow(A) ++FIRST(B/EMPTY)
                                if not is_terminal(temp1):
                                    # 过滤掉FIRST中的EMPTY
                                    self.g_dict[i].follow.extend(
                                        filter(lambda x: x != 'EMPTY', self.g_dict[temp1].first.keys()))
                                    # S->ABD D-->EMPTY folow(B)+=follow(S)
                                    if flag and ('EMPTY' in self.g_dict[temp1].first):
                                        self.g_dict[i].follow.extend(v.follow)
                                    else:
                                        # 避免 S ->ABD B-->EMPTY D!-->EMPTY
                                        flag = False
                                # S->AaB follow(A) += a
                                else:
                                    # 去除单引号
                                    if temp1[0] == "'":
                                        self.g_dict[i].follow.append(temp1[1])
                                    else:
                                        self.g_dict[i].follow.append(temp1)
                                temp1 = i
                    # S->ABa
                    else:
                        temp1 = temp[0]
                        for i in temp[1:]:
                            # 是终结符，跳过
                            if is_terminal(i):
                                temp1 = i
                            else:
                                # S->ABa follow(B) += a
                                if is_terminal(temp1):
                                    # 去除单引号
                                    if temp1[0] == "'":
                                        self.g_dict[i].follow.append(temp1[1])
                                    else:
                                        self.g_dict[i].follow.append(temp1)
                                else:
                                    # S->ABa follow(A) += first(B/EMPTY)
                                    self.g_dict[i].follow.extend(
                                        filter(lambda x: x != 'EMPTY', self.g_dict[temp1].first.keys()))
                                temp1 = i

    # 获得同步集
    def get_synch(self):
        # 将first集和follow集加入同步集中
        # 同时考虑将
        for k, v in self.g_dict.items():
            v: Sponser
            v.synch.extend(set(list(v.first.keys())) | set(v.follow))

    # def _pop(self, input_seq):
    #     num = self.current_index
    #     self.current_index += 1
    #     return input_seq[num]

    def analysis(self, input_seq: list, t_unit, sema_analysis=False):
        """

        :param input_seq: [(1,0,const,120,CONST)]
        :param t_unit:str
        ":param token : cur_line cur_col val typ id VAL
        :return:
        """
        # 建立分析树开始节点
        start = TreeNode('0', t_unit)
        # 初始化分析栈
        anal_seq = [TreeNode('-1', '#'), start]
        # 将‘#’加入输入串
        input_seq.append(['#'])
        # 弹出栈顶原数到a
        input_node = input_seq.pop(0)
        a = input_node[-1]
        # 标志是否发生错误
        error = list()
        if sema_analysis:
            # 同时进行语义分析
            semantic_analysis = SemanticAnalysis()
        self.br = False
        while True:
            # 弹出分析栈底元素到x
            tree_node = anal_seq.pop()
            x = tree_node.value
            if x == '#':
                break
            if is_terminal(x):
                # 分析结束
                if x == a:
                    # 匹配上终结符,修改，eg:'INT'->100
                    tree_node.value = input_node[2]
                    if sema_analysis:
                        # 匹配上终结符,进行语义分析
                        semantic_analysis.analysis_terminal(input_node)
                    # 匹配上终结符,取出下一个输入符号
                    input_node = input_seq.pop(0)
                    a = input_node[-1]
                else:
                    # # 添加错误
                    # 当前输入符号与栈顶终结符不匹配,即该符号应该是x
                    if input_node[-1] == '#':
                        continue
                    error.append(tuple([len(error), input_node.cur_line, input_node.cur_col, input_node.val, x, True]))
                    # 回复
                    # if self.br:
                    #     input_node = input_seq.pop(0)
                    #     a = input_node[-1]
                    # self.br = False
                    # 保留 x
                    # anal_seq.append(tree_node)
                    # input_node = input_seq.pop(0)
                    # a = input_node[-1]
            else:
                if sema_analysis:
                    # 语义分析非终结符，
                    semantic_analysis.analysis_non_terminal(x, len(anal_seq) - 1)
                # 查分析表
                if a in self.g_dict[x].first:
                    # 反序压入栈中
                    anal_seq.extend(add_tree_node(tree_node, self.g_dict[x].first[a])[::-1])
                elif 'EMPTY' in self.g_dict[x].first:
                    # 匹配空
                    if a in self.g_dict[x].follow:
                        add_tree_node(tree_node, ['Σ'])
                    else:
                        # print(a, self.g_dict[x].follow)
                        # 发生错误检查,跳到能匹配的位置
                        if input_node[-1] == '#':
                            continue
                        error.append(
                            tuple([len(error), input_node.cur_line, input_node.cur_col, input_node.val, a, False]))
                        input_node = self.error_deal(input_node, x, tree_node, anal_seq, input_seq)
                        a = input_node[-1]
                else:
                    error.append(tuple([len(error), input_node.cur_line, input_node.cur_col, input_node.val, a, False]))
                    input_node = self.error_deal(input_node, x, tree_node, anal_seq, input_seq)
                    a = input_node[-1]
        fu_table = {}
        if sema_analysis:
            fu_table = {'fun': semantic_analysis.fun_table, 'con': semantic_analysis.constant_table,
                        'var': semantic_analysis.variable_table}
            for i in semantic_analysis.error:
                print(i)
            error.extend([tuple(i) for i in semantic_analysis.error])

        # 将错误转换
        error = sorted(list(set(error)), key=lambda x: x[0])
        error_info_list = []
        for err in error:
            i, c, l, v, x, zq = err
            if zq:
                error_info_list.append('第{:^3d}行第{:^3d}列 符号{:^7}前缺失符号{:^7}'.format(int(c) + 1, int(l), v, x))
            else:
                error_info_list.append('第{:^3d}行第{:^3d}列 符号{:^7}附近存在错误'.format(int(c) + 1, int(l), v))
        return start, fu_table, self._fi(error_info_list)

    def _fi(self, error_list):
        tmp = []
        for v in error_list:
            if v not in tmp:
                tmp.append(v)
        return tmp

    def _hf(self, input_node):
        input_node = list(self.hf_input_node)
        return input_node

    def error_deal(self, input_node, x, tree_node, anal_seq: list, input_seq: list):
        # anal_seq 分析栈
        # input_seq 输入符号栈
        info = '非终结符{} 遇到{}'.format(x, input_node[-1])
        sponser = self.g_dict[x]
        a = input_node[-1]
        # 输入符号在同步集里,忽略F(弹出F)
        tb = ['{','}','IDENTIFIER']
        if (a in sponser.follow) or (a == '#') or (a in tb):
            # 对当前需匹配的输入字符不做改变,即弹出当前非终结符
            print(f'synch :{info} 弹出{x}')
            return input_node
        # 找到一个可重新开始的输入符号
        # 恐慌模式，忽略输入符号a
        else:
            print(f'恐慌 :{info} 忽略：{input_node[-1]}')
            anal_seq.append(tree_node)
            input_node = input_seq.pop(0)
            return input_node
        # 直接弹出对应值
        # self.br = True
        # while True:
        #     t = anal_seq.pop()
        #     if is_terminal(t.value):
        #         anal_seq.append(t)
        #         return input_node[-1]


# 定义语义分析类
"""
    在函数外的定义,
    external_declaration : 0
    declaration_specifiers : 1
    declartor: 2
    external_declaration_1 :3              
    
    declaration:4                          # 声明类型  (声明 赋值)列表                
    declaration_1:5                        # (声明 赋值)列表 a, b =5 
    init_declarator:6                      # 声明 赋值 b=5
    init_declarator_1:7                    # = initializer
    initializer:8                          # 初始化赋值 5
    compound_statement:9                   # 复合阶段 {}
"""


class SemanticAnalysis:
    def __init__(self):
        # 常量表 常名：（类型、值）
        self.constant_table = dict()
        # 变量表 变量名：[(作用域路径、类型、值)]
        self.variable_table = dict()
        # 函数表 函数名:【返回值类型,参数个数,(作用域路径,参数1类型,值）(作用域路径,参数2类型,值)、、、】
        self.fun_table = dict()
        # 符号作用域([非终结符类型,非终结符位置)]，第一个external_declaration的位置为1,-1后结束此非终结符的递归
        self.symbol_action = [(0, 0)]
        # 作用域划分(域数，当前域编号)
        self.scope_of_action = [0, 0]
        # 数据缓冲区[是否缓冲数据,缓冲的数据]
        self.buffer = [0, dict()]
        # 可见回溯点
        self.declaration_symbol = ['external_declaration', 'declaration', 'statement_list', 'iteration_statement',
                                   'init_declarator',
                                   'compound_statement', 'declaration', 'declaration_specifiers',
                                   'declarator', 'initializer']
        # 语义检查[('检查类型','检查类型','检查类型'...]
        self.semantic_check = []
        # 语义错误
        self.error = list()

    # 逐一分析语义分析器传来的符号
    def analysis_non_terminal(self, symbol: str, index):
        sa_s, sa_i = self.symbol_action[-1]
        # 表明当前符号已经递归分析完成
        if sa_i > index:
            # 停止读取
            self.buffer[0] = 0
            # 弹出定义的检测阶段
            if sa_s in ['statement_list', 'iteration_statement', 'initializer']:
                self.symbol_pop(index, 1)
            # 将所有已结束符号符号弹出
            sa_s = self.symbol_pop(index, 0)
            # 当且仅当external_declaration，declaration完成时，将缓冲区的数据加入符号表
            if sa_s in self.declaration_symbol[:2]:
                print(sa_s, self.scope_of_action[1], self.buffer[1])
                self._add(0)
                # 清空缓冲区
                self.buffer[1] = dict()
                # 区域退回到0
                if sa_s == 'external_declaration':
                    self.scope_of_action[1] = 0
            else:
                pass

        # 符号为定义的终结符时，添加其在分析栈弹出的位置
        if symbol in self.declaration_symbol:
            self.symbol_action.append((symbol, index))
            # 开始缓冲当前非终结符
            if symbol in self.declaration_symbol[-4:]:
                self.buffer[0] = 1
            # 修改作用域:全局定义若有符合语句，说明其为函数，即后面的需要修改定义域
            if symbol == 'compound_statement':
                print('sssss:', self.symbol_action)
            if symbol == 'compound_statement' and self.symbol_action[-2][0] == 'external_declaration':
                # 函数，则将函数定义添加到符号表中
                print(symbol, self.scope_of_action[1], self.buffer[1])
                # 改变作用域
                self.scope_of_action[1] = self.scope_of_action[0] + 1
                self.scope_of_action[0] += 1
                # 添加函数
                self._add(1)
                # 清空缓冲区
                self.buffer[1] = dict()
            if symbol in ['statement_list', 'iteration_statement', 'initializer']:
                self.semantic_check.append((symbol, index))
                print(">>>start:", symbol, index)

    def symbol_pop(self, index, select):
        op_list = self.semantic_check if select else self.symbol_action
        sa_ss, _ = op_list.pop()
        print("<<<stop:", sa_ss, _)
        count = len(op_list)
        for sa_s, sa_i in op_list[::-1]:
            if sa_i > index:
                count -= 1
                sa_ss = sa_s
                print("<<<stop:", sa_ss, sa_i)
            else:
                if select:
                    self.semantic_check = op_list[:count]
                else:
                    self.symbol_action = op_list[:count]
                break
        return sa_ss

    def analysis_terminal(self, symbol):
        """

        :param symbol:[c,l,原始符号，种别码，字母大写后的符号]
        :return:
        """
        # 将当前匹配的终结符加如缓冲区
        state, data = self.buffer
        if state:
            # 去掉边界符
            if symbol[2] not in nextWord_space:
                # 获得当前递归的非终结符
                sa_s = self.symbol_action[-1][0]
                if sa_s in data:
                    data[sa_s].append(symbol)
                else:
                    data[sa_s] = [symbol]
        flag = False
        # 对当前终结符进行语义检查
        for check_type in set([_[0] for _ in self.semantic_check]):
            s = symbol[2]
            print('test:', s)
            if check_type in ['statement_list', 'initializer']:
                # 未定义便使用
                if symbol[-1] == 'IDENTIFIER' and not self.is_used(s):
                    error = list(symbol)
                    error.append('{:^5s}未定义便使用'.format(s))
                    self.error.append(error)
            elif check_type == 'iteration_statement':
                flag = True
        if symbol[-1] in ['BREAK', 'CONTINUE'] and not flag:
            error = list(symbol)
            error.append('{:^5s}必须在循环语句里嵌套使用'.format(symbol[2]))
            self.error.append(error)

    # 标识符是否被使用过
    def is_used(self, s):
        # 查符号表，看是否定义
        if s in self.constant_table:
            return '常量名'
        if s in self.variable_table:
            return '变量名'
        if s in self.fun_table:
            return '函数名'
        return 0

    def _add(self, type):
        """
        :param type: 当前定义类型,即函数（1）和其他(0)
        :return:
        """
        print(self.buffer)
        data = self.buffer[1]
        if not data:
            return 0
        declaration_specifiers = data['declaration_specifiers']
        if 'declarator' not in data:
            if 'MAIN' not in self.fun_table:
                self.fun_table['MAIN'] = []
            else:
                raise Exception("main函数只能定义一个")
            return 0
        # 获得声明段
        declarator = data['declarator']
        # 获得初始化段
        initializer = data['initializer'] if 'initializer' in data else []
        # 获得声明类型
        declaration_type = declaration_specifiers[0][-1]
        if type == 1:
            fun_name = declarator[0][2]

            used_name_type = self.is_used(fun_name)
            if used_name_type:
                error = list(declarator[0])
                error.append('{:^5s}与定义的{:}重复'.format(fun_name, used_name_type))
                self.error.append(error)
            else:
                value = [declaration_type, len(declaration_specifiers[1:])]
                value.extend(
                    [(self.scope_of_action[1], t[-1], n[2]) for t, n in
                     zip(declaration_specifiers[1:], declarator[1:])])
                self.fun_table[fun_name] = value
        else:
            count = len(declarator) - len(initializer)
            init = [None for _ in range(count)]
            init.extend(initializer)
            if declaration_type != 'CONST':
                for k, v in zip(declarator, init):
                    valve = (self.scope_of_action[1], declaration_type, v)
                    used_name_type = self.is_used(k[2])
                    if used_name_type:
                        if used_name_type == '变量名':
                            # 标识不重复
                            flag = True
                            # 看同名变量表中是否存在形同路径
                            for lj in self.variable_table[k[2]]:
                                lj = lj[0]
                                if self.scope_of_action[1] == lj:
                                    flag = False
                                    break
                            if flag:
                                self.variable_table[k[2]].append(valve)
                            else:
                                error = list(k)
                                error.append('{:^5s}与已定义的{:}重复'.format(k[2], used_name_type))
                                self.error.append(error)
                    else:
                        self.variable_table[k[2]] = [valve]
                        # 检查初始值是否符合定义
                        if v and declaration_type not in v[-1]:
                            error = list(k)
                            error.append('初始化值类型{:^7s}与定义类型{:^7s}不符'.format(v[-1], declaration_type))
                            self.error.append(error)
            else:
                for k, v in zip(declarator, initializer):
                    if v:
                        valve = [v[-1], v]
                        used_name_type = self.is_used(k[2])
                        if used_name_type:
                            error = list(k)
                            error.append('{:^5s}与定义的{:}重复'.format(k[2], used_name_type))
                            self.error.append(error)
                        else:
                            self.constant_table[k[2]] = valve
                    else:
                        self.constant_table[k[2]] = valve
        return 0


if __name__ == '__main__':
    # t = LexicalAnalysis('../data/test.c')
    # t.analysis()
    # print(t.get_token_list())
    t = SyntaxAnalysis('../data/c_ll.txt')
    print("-------------------first---------------------\n")
    t.get_first()
    t.get_follow()
    t.get_synch()
    print("-------------------------------------------------\n\n\n")
    # print("-------------------------------相交集------------------------")
    # for k, v in t.g_dict.items():
    #     first = set(v.first.keys())
    #     follow = set(v.follow)
    #     if 'EMPTY' in first:
    #         if first & follow:
    #             print("{:30s} -> firstL{:}".format(k, first))
    #             print("{:30s} -> follow{:}".format('', follow))
    #             print("{:30s} -> 相交： {:}".format('', first & follow))

    # a, c, m = t.analysis()
