from collections import defaultdict


def remove_recall(list_grammer):
    result = {}  # 保存整个文法的结果
    judge = []
    for i in range(len(list_grammer)):
        item_left, item_right = list_grammer[i].split('->')  # 左右部分开
        item_left = item_left.strip()
        judge.append(item_left)
    for i in range(len(list_grammer)):
        item_left, item_right = list_grammer[i].split('->')  # 左右部分开
        item_left = item_left.strip()
        item_right = item_right.split('|')  # 右部根据|再分
        dicts = defaultdict(list)
        for Yi in item_right:
            Yi = Yi.strip().split(' ')
            dicts[Yi[0]].append(' '.join(Yi))  # 根据候选式的首字符分组放进字典
        norm_list = []  # 保存有回溯的候选式
        unorm_list = []  # 保存没有回溯的候选式
        flag = False  # 存在回溯的标志

        result_tmp = {}  # 保存每个产生式的结果

        ss = ''
        for k, v in dicts.items():
            if len(v) > 1:  # 存在回溯
                flag = True
                # 找到公共左因子ss
                zipped = zip(*v)  # 传入zip(*[abc,abd]) 将列表的元素作为参数传递给zip >>> (a,a),(b,b),(c,d)
                for i in zipped:
                    if len(set(i)) == 1:  # 是公共左因子的部分就拼接
                        ss += i[0]
                    else:
                        break
                # 去掉有回溯的候选式的公共左因子
                for i in range(len(v)):
                    dicts[k][i] = dicts[k][i].replace(ss, '')
                    if dicts[k][i] == '':  # 候选式刚好等于公共左因子
                        dicts[k][i] = 'ε'
                norm_list.extend(dicts[k])
            else:  # 不存在回溯的候选式
                unorm_list.extend(dicts[k])

        # 存在回溯的处理
        if flag:
            # 有回溯的候选式的合并
            new_item_left = item_left + '\''
            if new_item_left in judge:
                new_item_left += '\''
            result_tmp[new_item_left] = new_item_left + '->'
            for i in range(len(norm_list)):
                if i == len(norm_list) - 1:
                    result_tmp[new_item_left] = result_tmp[new_item_left] + norm_list[i]
                else:
                    result_tmp[new_item_left] = result_tmp[new_item_left] + norm_list[i] + '|'

            # 没有回溯的候选式的合并
            nonrecall = ''
            for i in range(len(unorm_list)):
                if i == len(unorm_list) - 1:
                    nonrecall = nonrecall + ' ' + unorm_list[i]
                else:
                    nonrecall = nonrecall + ' ' + unorm_list[i] + '|'
            if nonrecall != '':
                result_tmp[item_left] = item_left + '->' + ss.strip() + ' ' + new_item_left.strip() + '|' + nonrecall
            else:
                result_tmp[item_left] = item_left + '->' + ss.strip() + ' ' + new_item_left.strip()

        # 不存在回溯的处理
        else:
            # for Yi in item_right:
            result_tmp[item_left] = list_grammer[i]
        result.update(result_tmp)
    result_new = []
    for k, v in result.items():
        result_new.append(v)
    return result_new


def remove_recursion(list_grammer):
    grammer_dit = dict()  # 存储消除左递归后产生的新构建的表达式
    for per_grammer in list_grammer:
        item_left, item_right = per_grammer.split('->')
        item_left = item_left.strip()  # 去除空格、回车
        item_right = item_right.strip().split('|')
        norm_list = []  # 存放不是递归的表达式
        unorm_list = []  # 存放去除递归后剩下的部分
        new_item = ''
        flag = False
        for per in item_right:
            if per.split(' ')[0] == item_left:
                flag = True  # 存在递归
        if flag:  # 处理递归
            for per_item in item_right:
                per_item = per_item.split(' ')
                if per_item[0] == item_left:  # E->E+T|T -> E'->+TE'
                    unorm_list.append(' '.join(per_item[1:]).strip() + ' ' + item_left + '\'')
                else:
                    grammer_dit[item_left] = ' '.join(per_item) + ' ' + item_left + '\''  # E->E+T|T -> E->TE'
                    norm_list.append(grammer_dit[item_left])
            grammer_dit[item_left + '\''] = item_left + '\'' + '->'
            for index, per in enumerate(unorm_list):  # 合并
                if index == len(unorm_list) - 1:  # 最后一个表达式
                    grammer_dit[item_left + '\''] = grammer_dit[item_left + '\''] + ' ' + per
                else:
                    grammer_dit[item_left + '\''] = grammer_dit[item_left + '\''] + ' ' + per + '|'
            if item_left + '\'' in grammer_dit:
                grammer_dit[item_left + '\''] = grammer_dit[item_left + '\''] + '|ε'

            for index, per in enumerate(norm_list):  # 合并
                if index == len(norm_list) - 1:  # 最后一个表达式
                    new_item = new_item + ' ' + per
                else:
                    new_item = new_item + ' ' + per + '|'
            grammer_dit[item_left] = item_left + '->' + ' ' + new_item
        else:  # 表达式不存在递归
            grammer_dit[item_left] = per_grammer
    result = []
    for k, v in grammer_dit.items():
        result.append(v)
    return result


if __name__ == '__main__':
    with open('grammer.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        t = (remove_recall(remove_recursion(lines)))
    # f = remove_recursion([
    #     'Declaration_specifiers -> Storage_class_specifier|Storage_class_specifier Declaration_specifiers|Type_specifier|Type_specifier Declaration_specifiers|Type_qualifier|Type_qualifier Declaration_specifiers'])
    # t = remove_recall(f)
    for i in t:
        print(i)
