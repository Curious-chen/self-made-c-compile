class ERROR:
    def __init__(self):
        pass

    def count_(self, item, count1, count2, count3):
        if item == '{':
            count1 += 1
        if item == '}':
            count1 -= 1
        if item == '(':
            count2 += 1
        if item == ')':
            count2 -= 1
        if item == '[':
            count3 += 1
        if item == ']':
            count3 -= 1
        return count1, count2, count3

    def judge_brackets(self, brackets_count1, brackets_count2, brackets_count3):
        if brackets_count1 > 0:
            return "缺少的符号: {"
        elif brackets_count1 < 0:
            return "缺少的符号: {"
        if brackets_count2 > 0:
            return "缺少的符号: {"
        elif brackets_count2 < 0:
            return "缺少的符号: {"
        if brackets_count3 > 0:
            return "缺少的符号: {"
        elif brackets_count3 < 0:
            return "缺少的符号: {"
