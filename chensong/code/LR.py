from chensong.code.model import is_terminal, TreeNode, default_open
from chensong.code.table import Semantic_
from chensong.code.config import *
from collections import namedtuple

ADDR = {
    'CHAR': 1,
    'INT': 4
}

TVALUE = 0


def newtemp():
    global TVALUE
    t = TVALUE
    TVALUE += 1
    return 'T{:}'.format(t)


NODENUM = 0


def get_tree_node(word):
    global NODENUM
    name = '{}'.format(NODENUM)
    NODENUM += 1
    return TreeNode(name, word)


def get_VAL(s_code, val):
    s_code = int(s_code)
    if 100 < s_code < 200:
        return str(val).upper()
    if s_code == 700:
        return 'IDENTIFIER'
    if s_code == 500:
        return 'CHARACTER'
    if s_code == 600:
        return 'STRING_LITERAL'
    if s_code == 800:
        return 'FLOATOR'
    if s_code == 400:
        return 'INTERGER'
    return str(val)


def get_lex(path=save_token_list):
    Token = namedtuple('Token', 'cur_line cur_col val typ id VAL')
    token_list = []
    with open(path, 'r', encoding='UTF-8') as f:
        all_word = f.readlines()
        for index, pre_line in enumerate(all_word):
            pre_line = pre_line.strip().split(' ')
            VAL = get_VAL(pre_line[1], pre_line[0])
            token_list.append(Token(pre_line[2], pre_line[3], pre_line[0], str(pre_line[1]), index, VAL))
    return token_list


class SLR:
    def __init__(self, grams: dict, dot='.', t_unit='s'):
        # 默认的dot,以及开始符号
        self.dot = dot
        self.t_unit = t_unit
        # 终结符号集
        self.quaternion_list = []

        self.v_t = []
        # 非终结符号集
        self.v_n = []
        # 所有符号集
        self.v_s = []
        #
        self.v_t_2_int = {}
        self.v_n_2_int = {}
        # 带有follow集
        self.grams_s = grams
        self.grams_s['s_'] = grams[self.t_unit]
        # 不带follow集
        # self.grams = {k: v.candidate_list for k, v in grams.items()}
        # 添加产生式 s_ -> s; s 即开始符号
        self.grams = [('s_', t_unit)]
        # 直接构造产生式列表
        for k, v in grams.items():
            c_l = v.candidate_list
            for css in c_l:
                tmp = [k]
                tmp.extend(css)
                self.grams.append(tuple(tmp))
        print('gamms:', self.grams)

        # 添加产生式 s_ -> s;

        self.dot_grams = dict()

        self.ACTION = []
        self.GOTO = []
        # 标志是否为布尔值运算
        self.br = True

    # 分割非终结符和终结符
    def get_v(self):
        for n_css in self.grams:
            k, v = n_css[0], n_css[1:]
            self.v_n.append(k)
            self.v_s.append(k)
            for w in v:
                if is_terminal(w):
                    self.v_t.append(w)
                else:
                    self.v_n.append(w)
                self.v_s.append(w)
        self.v_s = sorted(set(self.v_s))
        self.v_t = sorted(set(self.v_t))
        # 分析时遇到 # 表示接受
        self.v_t.append('#')
        self.v_n = sorted(set(self.v_n))
        # 映射
        self.v_t_2_int = {v: i for i, v in enumerate(self.v_t)}
        self.v_n_2_int = {v: i for i, v in enumerate(self.v_n)}
        # print('所有符号:', self.v_s)
        # print('终结符  :', self.v_t)
        # print('非终结符:', self.v_n)

    def dot_gram(self):
        for n_css in self.grams:
            k, css = n_css[0], n_css[1:]
            for ind in range(len(css) + 1):
                dot_it = list(css)
                dot_it.insert(ind, self.dot)
                if k in self.dot_grams:
                    self.dot_grams[k].append(dot_it)
                else:
                    self.dot_grams[k] = [dot_it]
        # print('-------------------------------------dot_grams------------------------------')
        # for k, k_dot_l in self.dot_grams.items():
        #     print(k, k_dot_l)

    def get_VN_gram(self, v):
        # 返回非终结符产生的A->.aBb形式
        res = []
        for gram in self.dot_grams[v]:
            if gram[0] == self.dot:
                r = [v]
                r.extend(gram)
                res.append(r)
        return res

    def get_CLOSURE(self, tmp):
        # 生成闭包
        CLOSURE = []
        for it in tmp:
            # I的任何项目都属于CLOSURE(I)
            if it not in CLOSURE:
                CLOSURE.append(it)
            # 分离出点后的字母
            ind = it.index(self.dot) + 1
            if ind == len(it):
                continue
            v = it[ind]
            # 若v 属于非终结符
            if not is_terminal(v):
                # 获得 A->.r r:任意字符串
                res = self.get_VN_gram(v)
                for re in res:
                    if re not in CLOSURE:
                        CLOSURE.append(re)
                        tmp.append(re)

        return CLOSURE

    def go(self, item, v):
        # 生成并返回下一个item
        tmp = []
        for it in item:
            # 找到下一字符为V的项目
            ind = it.index(self.dot) + 1
            if ind == len(it):
                continue
            # 向后移动一个点
            if it[ind] == v:
                new_it = list(it)
                # 后插，加一
                new_it.insert(ind + 1, self.dot)
                # 删除前面的dot
                new_it.remove(self.dot)
                tmp.append(new_it)
        # 对下一项目集求闭包
        if len(tmp) != 0:
            new_item = self.get_CLOSURE(tmp)
            return new_item

    def go_next_word(self, item):
        next_words = []
        for it in item:
            ind = it.index(self.dot) + 1
            if ind == len(it):
                continue
            next_words.append(it[ind])
        return next_words

    def is_inItems(self, new_item, items):
        # 判断item是否已经存在, 存在返回位置，不存在返回-1
        if new_item == None:
            return -1
        # 去掉item列表的顺序
        new_set = set([tuple(_) for _ in new_item])
        num = 0
        for item in items:
            old_set = set([tuple(_) for _ in item])
            if old_set == new_set:
                return num
            num = num + 1

        return -1

    # 获得扩展后的文法，即获得每条文法的项目集
    def get_items(self):
        # 构建item的集合

        # 构建扩展的文法，即加dot
        self.dot_gram()
        # 初始化,生成I0
        items = [self.get_CLOSURE([['s_', self.dot, self.t_unit]])]
        # print('I_0::', items)
        for item in items:
            next_words = self.go_next_word(item)
            for v in next_words:
                new_item = self.go(item, v)
                # print('I_', new_item)
                # 判断状态不为空，且不存在于原状态中
                if new_item != None:
                    if self.is_inItems(new_item, items) == -1:
                        # print("添加了%s" % str(new_item))
                        items.append(new_item)
        print('--------------------------items--------------------------------------')
        for i, v in enumerate(items):
            print('I{:>03d}: {:}'.format(i, v))
        return items

    # ---------------构造LR(0)表代码--------------#
    def init_lr_table(self, items):
        action_len = len(self.v_t)
        goto_len = len(self.v_n)

        for h in range(len(items)):
            self.ACTION.append([])
            self.GOTO.append([])
            for w1 in range(action_len):
                self.ACTION[h].append('')
            for w2 in range(goto_len):
                self.GOTO[h].append('')

    def lr_is_legal(self, items):
        # 判别lr是否合法
        has_protocol = 0  # 是否存在规约项目
        has_shift = 0  # 是否存在移进项目

        for item in items:
            for it in item:
                ind = it.index(self.dot) + 1
                if ind == len(it):
                    if has_protocol != 0 or has_shift != 0:
                        return False
                    has_protocol = 1
                else:
                    if is_terminal(it[ind]):
                        has_shift = 1
        return True

    # 找到对应产生式的编号
    def find_gram(self, it):

        itt = list(it)
        itt.remove(self.dot)
        n_css = tuple(itt)
        try:
            ind = self.grams.index(n_css)
            return ind
        except ValueError:
            return -1

    """
        假定项目集规范族C={I0,I1,…,In}。令每一个项目集Ik的下标k作为分析器的状态。分析表的ACTION子表和GOTO子表可按如下方法构造
        令那个包含项目S’→•S的集合Ik的下标k为分析器的初态。
        若项目A→α•aβ属于Ik且GO(Ik , a)= Ij,a为终结符，置ACTION[k,a]为“把(j,a)移进栈”，简记为“sj”。
        若项目A→α•属于Ik，对任何终结符a(或结束符#)，置ACTION[k,a]为“用产生式A→α进行归约”，简记为“rj”（假定产生式A→α是文法G’的第j个产生式）。
        若项目S’→S•属于Ik，则置ACTION[k,#]为“接受”，简记为“acc”。
        若GO(Ik , A)= Ij，A为非终结符，则置GOTO[k,A]=j。
        分析表中凡不能用规则1至4填入信息的空白格均填上“err”。

    """

    def simple_deal(self):
        pass

    def get_lr_table(self, items):
        # 构建lr分析表
        self.init_lr_table(items)
        # hf = self.lr_is_legal(items)
        # if not hf:
        #     print("不合法")
        #     # exit()
        for i, item in enumerate(items):
            yi_set = set()
            fo_set_list = list()
            ind_to_not_t = list()
            for it in item:
                ind = it.index(self.dot) + 1
                # 即dot是否在产生式末尾
                if ind == len(it):  # 判断是否写入ACTION
                    # if it == ['s_', t_unit, dot]:
                    #     self.ACTION[i][-1] = "acc"
                    inde = self.find_gram(it)
                    if inde != -1:
                        for k in range(len(self.ACTION[i])):
                            # 进行规约 r k v[inde]
                            if self.ACTION[i][k]:
                                print('簇:{:>05d} 遇到 {:18s} 保留前者:{}'.format(i, self.v_t[k], self.ACTION[i][k]))
                                # print('发生冲突族:{:>06d} info:移进:规约 {:}'.format(i,it))
                                # if self.ACTION[i][k][0] == 's':
                                #     if not yi_set:
                                #         yi_set, fo_set_list, ind_to_not_t = self._is_solvable(item)
                                # flag = self.conflict_check(self.v_t[k], yi_set, fo_set_list)
                                # if flag == -2:
                                #     print(i, self.v_t[k])
                                #     print('保留移进:', self.ACTION[i][k])
                                # else:
                                #     raise Exception('rdfgdr')
                                # 若移进-规约冲突 归约-归约冲突
                            else:
                                self.ACTION[i][k] = ['r', inde]

                else:
                    next_item = self.go(item, it[ind])
                    # print("go(%s, %s)-->%s" % (str(item), y[0], str(next_item)))
                    inde = self.is_inItems(next_item, items)
                    y = it[ind]
                    if inde != -1:  # 判断是否写入GOTO
                        if is_terminal(y):
                            # 表示没有发生冲突,
                            flag = -2
                            j = self.v_t.index(y)

                            # 发生冲突
                            if self.ACTION[i][j]:
                                print('发生冲突族:{:>06d} info:移进'.format(i))
                                # 没有判断此项目族是否可解决
                            #     if not yi_set:
                            #         yi_set, fo_set_list, ind_to_not_t = self._is_solvable(item)
                            #     flag = self.conflict_check(y, yi_set, fo_set_list)
                            # if flag == -2:
                            #     if yi_set:
                            #         print('解决冲突族:{:>06d} info:移进'.format(i))
                            #         print('解决冲突族:{:>06d} info:移进'.format(i))
                            # if self.v_t[j] in ['(']:
                            #     flag = 1

                            self.ACTION[i][j] = ['s', inde]
                            # else:
                            #     raise Exception('sdfd')
                        else:
                            # 非终结符的坐标
                            j = self.v_n.index(y)
                            self.GOTO[i][j] = inde
                    else:
                        raise Exception("go不来")
        self.print_lt_table()

    def _is_solvable(self, item):
        # 获得移进符号集，以及规约项目的follow集
        yi_set = set()
        fo_set_list = []  # follow集列表
        # 映射
        ind_to_not_t = []
        # 对应列表的非终结符
        for old_it in item:
            # 是规约项目
            if old_it[-1] == self.dot:
                # 获得非终结符
                non_t = old_it[0]
                # 添加follow集
                sp = self.grams_s[non_t]
                old_it_follow = set(sp.follow)
                fo_set_list.append(old_it_follow)
            else:
                ind = old_it.index(self.dot) + 1
                # 加入到移进符号集
                yi_set.add(old_it[ind])
        # 表示可解决
        flag = True
        for i, a in enumerate(fo_set_list[:-1]):
            if not (a & yi_set):
                raise Exception("冲突无法解决")
            for b in fo_set_list[i + 1:]:
                if not (a & b):
                    flag = False
                    raise Exception("冲突无法解决")
        if flag:
            return yi_set, fo_set_list, ind_to_not_t

    def conflict_check(self, current_a, yi_set, fo_set_list):
        if current_a in yi_set:
            return -2
        else:
            return -3
            # for ind, v in fo_set_list:
            #     if current_a in v:
            #         return ind

    def print_lt_table(self):
        v_t_mat = '{:^30s}' * (len(self.v_t))
        v_n_mat = '{:^30s}' * (len(self.v_n))
        print('{:4s} '.format('') + v_t_mat.format(*tuple(self.v_t)) + v_n_mat.format(*tuple(self.v_n)))
        num = 0
        for a, g in zip(self.ACTION, self.GOTO):
            print('I{:>03d} '.format(num) + v_t_mat.format(*tuple([str(_) for _ in a])),
                  v_n_mat.format(*tuple([str(_) for _ in g])))
            num += 1

    def analysis(self, input_seq: list, in_code=False):
        # 初始化四元式
        self.quaternion_list = []
        # 初始化符号栈，将状态0和#号入栈
        input_seq.append(('#'))
        symbol_stack = [TreeNode(-1, '#')]
        status_stack = [0]
        location = 0
        now_step = 0
        while True:
            now_state = status_stack[-1]
            input_node = input_seq[location]
            input_ch = input_node[-1]

            print("----now_step:{:<4d}".format(now_step))
            now_step += 1
            print('status_stack:', status_stack)
            print('symbol_stack:', [i.value for i in symbol_stack])
            print('----info:', end='')
            find = self.ACTION[now_state][self.v_t_2_int[input_ch]]
            if find:
                op = find[0]
                # 移进
                if op == 's':
                    print('移进\n')
                    # 当前输入符号进入符号栈
                    t = get_tree_node(input_node[2])
                    t.token = input_node  # 加入完整描述
                    symbol_stack.append(t)
                    # 将action表中的状态移入状态栈
                    status_stack.append(find[-1])
                    location += 1
                else:  # op == 'r': ('r',1)
                    print('规约')
                    # 获得该规约的产生式
                    n_css = self.grams[find[1]]
                    # 显示
                    print('产生式:{:}\n'.format(tuple(n_css)))
                    # 非终结符
                    non_t = n_css[0]
                    # 获得非终结符树节点
                    non_t_node = get_tree_node(non_t)
                    # 接受，返回生成的树
                    if non_t == 's_':
                        return 1, symbol_stack[-1]
                    # 规约式右端长度
                    r_num = len(n_css) - 1
                    # 两个栈顶的r个元素同时出栈
                    for i in range(r_num):
                        # 将父节点和子节点间连起来
                        non_t_node.next_nodes.insert(0, symbol_stack.pop())
                        status_stack.pop()

                    # 获得规约链表
                    node_list = [non_t_node]
                    node_list.extend(non_t_node.next_nodes)
                    if now_step == 146:
                        print(9999)
                    # 中间代码生成
                    if in_code:
                        self.semantic_translation(n_css, node_list)
                    # A->B 根据S_m-r 和 A 查goto表
                    s = self.GOTO[status_stack[-1]][self.v_n_2_int[non_t]]
                    # 将状态s进入状态栈
                    status_stack.append(s)
                    # A进符号栈
                    symbol_stack.append(non_t_node)
            else:
                return 0, input_node

    def semantic_translation(self, css, node_list: list, **kwargs):
        k_ = '_'
        css = tuple(css)
        if (css[0] in ['assignment_expression']) and (len(css) == 4):
            ae, ce, op, ae1 = node_list
            ae.place = ae1.place
            # 更新变量的值
            ae.token = ce.token
            # 移除产生的布尔表达式
            self.l_remove([ce, ae1])
            if isinstance(ae1.place, list):
                id_name, prl = ae1.place
                self.gencode(id_name, prl, k_, ce.place)
            else:
                # 生成目标代码
                self.gencode(op.op, ae1.place, k_, ce.place)

        elif css[0] == 'jump_statement':
            jum, _, e, _ = node_list
            self.l_remove([e])
            if isinstance(e.place, list):
                idv, rpl = e.place
                t = newtemp()
                self.gencode(idv, rpl, k_, t)
                self.gencode('ret', k_, k_, t)
            else:
                self.gencode('ret', k_, k_, e.place)
        elif css[0] == 'declaration':
            decl, ty, ini, _ = node_list
            # 插入符号表
            for token, value in ini.token_list:
                print(token, value, ty.type)

        elif css[0] == 'const_definition':
            _, decl, ty, ini, _ = node_list
            # 插入符号表
            for token, value in ini.token_list:
                print(token, value, ty.type)

        elif css[0] == 'type_specifier':
            ty_spe, ty_type = node_list
            ty_spe.type = ty_type.value

        elif css[0] == 'initializer':
            if len(node_list) == 4:
                ini, ae, _, ini2 = node_list
                ini.token_list = [(ae.token, ae.place)]
                ini.token_list.extend(ini2.token_list)
            else:
                ini, ae = node_list
                ini.token_list = [(ae.token, ae.place)]
            self.l_remove([ae])

        elif css[0] in ['unary_operator', 'assignment_operator', 'rop_operator']:
            # 将操作符向上传递
            ao, op = node_list
            ao.op = op.value

        elif (css[0] in ['additive_expression', 'multiplicative_expression']) and (len(css) == 4):
            e, e1, ad_op, t = node_list
            # ex_str = '{:}{:}{:}'.format(e1.place[1], op, t.place[1])
            # 发现表达式不是布尔运算
            self.l_remove([e1, t])
            e.place = newtemp()
            self.gencode(ad_op.value, e1.place, t.place, e.place)

        elif (css[0] == 'unary_expression') and (len(css) == 3):
            ue, u_op, be = node_list
            # ex_str = '{:}{:}'.format(u_op.op, be.place[1])
            ue.place = newtemp()
            self.gencode('@{:}'.format(u_op.op), be.place, k_, ue.place)

        elif css[0] == 'basic_expression':
            if len(css) == 2:
                be, v = node_list
                # 实际的值
                be.place = v.value
                if v.token.VAL == 'IDENTIFIER':
                    be.token = v.token
                if self.br:
                    # 生成两条四元式，并将TC,FC指向中间代码的序号
                    be.TC = self.NXQ()
                    be.FC = self.NXQ() + 1
                    self.gencode('jnz', v.value, k_, 0)
                    self.gencode('j', k_, k_, 0)

            else:
                be, _, e, _ = node_list
                be.place = e.place
                # 将真假出口的值直接赋值到左边
                be.TC = e.TC
                be.FC = e.FC
        elif (css[0] in ['relational_expression']) and (len(css) == 4):
            s, a1, op, a2 = node_list
            # # 传递place
            # s.place = [a1.place, a2.place]
            # 发现表达式不是布尔运算
            self.l_remove([a1, a2])
            s.TC = self.NXQ()
            s.FC = self.NXQ() + 1
            self.gencode('j{:}'.format(op.op), a1.place, a2.place, 0)
            self.gencode('j', k_, k_, 0)

        elif css == ('logical_and', 'logical_and_expression', '&&'):
            bt_and, bt, a_nd = node_list
            # 填写place
            bt_and.place = []
            # 回填真出口
            self.backpath(bt.TC, self.NXQ())
            bt_and.FC = bt.FC
        elif css == ('logical_or', 'logical_or_expression', '||'):
            be_or, be, o_r = node_list
            # 填写place
            be_or.place = []
            # 回填真出口
            self.backpath(be.FC, self.NXQ())
            be_or.TC = be.TC
        elif css == ('logical_and_expression', 'logical_and', 'relational_expression'):
            a, b, c = node_list
            # 填写place
            a.place = []
            a.TC = c.TC
            a.FC = self.merge(b.FC, c.FC)
        elif css == ('logical_or_expression', 'logical_or', 'logical_and_expression'):
            a, b, c = node_list
            # 填写place
            a.place = []
            a.FC = c.FC
            a.TC = self.merge(b.TC, c.TC)

        elif css[0] == 'selection_statement':
            s, c, s1 = node_list
            # 修改前面的
            s.chain = self.merge(c.chain, s1.chain)
            self.backpath(s.chain, self.NXQ())
        elif css[0] == 'selection_statement_if':
            s_f, _, _, e, _ = node_list
            self.backpath(e.TC, self.NXQ())
            s_f.chain = e.FC
        elif css[0] == 'selection_statement_if_else':
            s_f_e, s_f, s, _ = node_list
            q = self.NXQ()
            # s结束，生成一条无条件跳转语句
            self.gencode('j', k_, k_, 0)

            self.backpath(s_f.chain, self.NXQ())
            s_f_e.chain = self.merge(s.chain, q)

        elif css[0] in ['expression_statement']:
            if len(css) == 3:
                # 直接综合子节点属性
                b, e, _ = node_list
                b.place = e.place
                # 将真假出口的值直接赋值到左边
                b.TC = e.TC
                b.FC = e.FC
                b.chain = e.chain
        elif css[0] == 'do_do':
            d, _ = node_list
            d.head = self.NXQ()
        elif css[0] == 'do_do_while':
            u, d, s, _ = node_list
            u.head = d.head
            self.backpath(s.chain, self.NXQ())
        elif css[0] == 'do_statement':
            s, u, _, e, _ = node_list
            self.backpath(e.TC, u.head)
            # 直接回填
            self.backpath(e.FC, self.NXQ())
        elif css[0] == 'for_statement_e1':
            f, _, _, e_s = node_list
        elif css[0] == 'for_statement_e2':
            a, f, e_S = node_list
            a.chain = e_S.FC
            a.TC = e_S.TC
            a.inc = self.NXQ()
        elif css[0] == 'for_statement_e3':
            a, b, c, _ = node_list
            # 跳转到判断语句
            self.gencode('j', k_, k_, b.TC)
            self.backpath(b.TC, self.NXQ())
            a.chain = b.chain
            a.inc = b.inc
        elif css[0] == 'for_statement':
            f_s, b, s = node_list
            self.gencode('j', k_, k_, b.inc)
            self.backpath(b.chain, self.NXQ())
        elif css[0] == 'function_call':
            fa, id_str, _, ini, _ = node_list
            prl = ' '.join(token.val for token, value in ini.token_list)
            fa.place = [id_str.value, prl]
        elif css[0] == 'function_id':
            fun_name = node_list[2]
            self.gencode(fun_name.value, k_, k_, k_)
        #     pass
        elif len(css) == 2:
            # 直接综合子节点属性
            b, e = node_list
            b.place = e.place
            # 将真假出口的值直接赋值到左边
            b.TC = e.TC
            b.FC = e.FC
            b.chain = e.chain
            b.token = e.token
            if css[0] == 'assignment_expression':
                b.remove = e

    def l_remove(self, tree_node_list):
        tmp = []
        for i, vv in enumerate(self.quaternion_list):
            flag = True
            for v in tree_node_list:
                if v.FC == i:
                    v.FC = -1
                    flag = False
                if v.TC == i:
                    v.TC = -1
                    flag = False
            if flag:
                tmp.append(vv)
        self.quaternion_list = tmp

    def gencode(self, op, a1, a2, r):
        self.quaternion_list.append([op, a1, a2, r])

    def backpath(self, nxq, value):
        if nxq != -1:
            self.quaternion_list[nxq][-1] = value

    def merge(self, nxq1, nxq2):
        if nxq2 == -1:
            return nxq1
        # 将后面条四元式放到前前一条链的第四分量上
        self.quaternion_list[nxq1][-1] = self.quaternion_list[nxq2]
        return nxq2

    def NXQ(self):
        # 返回即将生成的四元式编号
        nxq = len(self.quaternion_list)
        return nxq

    def save_(self):
        quaternion_info = '四元式\n'

        for i, v in enumerate(self.quaternion_list):
            t = print_zzz(v)
            quaternion_info += '    ({:^4d}): ({:5},{:5},{:5},{:5})\n'.format(i, t[0], t[1], t[2], str(t[3]))

        with open(save_quaternion_info, 'w', encoding='utf-8') as f:
            f.write(quaternion_info)
        return quaternion_info

    def save_action(self, path):
        import pandas as pd
        # 显示所有列
        pd.set_option('display.max_columns', None)
        # 显示所有行
        pd.set_option('display.max_rows', None)
        # 设置value的显示长度为100，默认为50
        pd.set_option('max_colwidth', None)

        columns = list(self.v_t)
        columns.extend(self.v_n)
        data = {v: [] for v in columns}
        indexs = []
        num = 0
        for a, g in zip(self.ACTION, self.GOTO):
            indexs.append('I{:>03d}'.format(num))
            for i, v in enumerate(a):
                if isinstance(v, list):
                    data[self.v_t[i]].append(''.join([str(i) for i in v]))
                else:
                    data[self.v_t[i]].append(v)
            for i, v in enumerate(g):
                if isinstance(v, list):
                    data[self.v_n[i]].append(''.join([str(i) for i in v]))
                else:
                    data[self.v_n[i]].append(v)
            num += 1
        print(columns)
        info = str(pd.DataFrame(data, indexs))

        with open(path, 'w', encoding='utf-8') as f:
            f.write(info)
        return info


#
def print_zzz(t):
    tmp = t
    # （J,_,_,list）:list即和指向另一条中间代码
    if isinstance(t[-1], list):
        t = t[-1]
        while True:
            if not isinstance(t, list):
                tmp[-1] = t
                break
            else:
                if t == t[-1]:
                    t[-1] = '...'
                    break
            t = t[-1]
    return tmp


if __name__ == '__main__':
    from chensong.code.handle import SyntaxAnalysis

    # 文法路径
    path = '../data/yf_all.txt'
    # print('****************************FOLLOW集***********************************')
    t = SyntaxAnalysis(path)
    t.get_first()
    t.get_follow(t_unit)
    print('****************************lex***********************************')
    lex_result_token = get_lex('../cache/token_list.txt')
    # 语义分析
    s_ = Semantic_()
    s_.access()
    print(s_.syn_table.symbolTableInfo)

    print('****************************LR***********************************')
    lr = SLR(t.g_dict, dot, t_unit)
    lr.get_v()
    items = lr.get_items()
    lr.get_lr_table(items)
    tree = lr.analysis(lex_result_token, in_code=True)

    if tree:
        # 显示四元式
        print("----------------------四元式-------------------------")
        print(lr.save_())
        # # 显示语法树
        from chensong.code.model import to_dot

        data = to_dot(tree)
        # 画出语法树
        import pydotplus as pdp

        graph = pdp.graph_from_dot_data('digraph demo1{{{:}}}'.format(data))
        with open(save_syntax_tree_LR, 'wb') as f:
            f.write(graph.create_png())
        default_open(save_syntax_tree_LR)
    else:
        print('语法错误')

    from chensong.code.Aim_Code import target_Code

    ta = target_Code(lex_result_token)
    ta.data_set()
    ta.init_gen()

    """
               0   : ( =   , 3   , _   , t    )
               1   : ( Demo, _   , _   , _    )
               2   : ( +   , e   , f   , T0   )
               3   : ( ret , _   , _   , T0   )
               4   : ( main, _   , _   , _    )
               5   : ( =   , 1   , _   , a    )
               6   : ( =   , 2   , _   , b    )
               7   : ( Demo, a b , _   , cc   )
    """
