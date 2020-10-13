"""
    模型工厂
"""
import graphviz
import os


# 语法分析器
def is_terminal(word: str):
    # 单引号标注的为结符或运算符
    # 全大写的单词为文本形式的终结符
    if word.islower():
        return False
    return True


def to_dot(tree):
    # 广度遍历
    input_tree = [tree]
    dy = str()
    lc = str()
    while True:
        if len(input_tree) == 0:
            break
        node = input_tree.pop(0)
        dy += '{}[label="{}"];'.format(node.name, node.value)
        lc += ''.join(['{}->{};'.format(node.name, _.name) for _ in node.next_nodes])
        input_tree.extend(node.next_nodes)
    return dy + lc


def draw(fa_dict, save_path='./graphviz/DFA'):
    start = fa_dict['start']
    end = fa_dict['end']
    dot = graphviz.Digraph()
    # from和to的并集
    union = set(fa_dict['from']) | set(fa_dict['to'])
    # 先创建结点
    for i in union:
        if i in start:
            dot.node(str(i), color="yellow")
        if i in end:
            dot.node(str(i), shape="doublecircle")
        else:
            dot.node(str(i))
    # 连接结点
    for i in range(len(fa_dict['from'])):
        dot.edge(str(fa_dict['from'][i]), str(fa_dict['to'][i]), label=fa_dict['varch'][i])
    dot.render(save_path, view=False, cleanup=True, format='png')


def add_tree_node(node, candidate: list):
    name = node.name
    old_num = len(node.next_nodes)
    for i, word in enumerate(candidate):
        node.next_nodes.append(TreeNode('{}_{}'.format(name, old_num + i), word))
    return node.next_nodes


"""
    数据结构 用来存放每个非终结符的First,Fllow集
    created by Curious
    2020/04/02 18:21
"""


class Sponser:
    def __init__(self, candidate_list):
        # 候选式列表
        self.candidate_list = candidate_list
        # first相关集
        self.first_relation = dict()
        # first集,必须记住其对应的候选式
        self.first = dict()
        # follow集
        self.follow = []
        # synch集，即同步集
        self.synch = ['#']


class TreeNode:
    def __init__(self, n, v):
        self.name = n  # 节点名称，需要每个节点不同
        self.value = v  # 显示值
        self.next_nodes = list()  # 子节点
        self.chain = -1
        self.TC = -1
        self.FC = -1
        self.place = -1
        self.token = None
        # self.place = [0, 0]
        # self.TC = 0
        # self.FC = 0


def default_open(path):
    # 打开语法树图片
    path = path if os.path.isabs(path) else os.path.join(os.path.abspath('.'), path)
    if os.path.exists(path):
        # 相对路径不能打开
        os.startfile(path, 'open')

