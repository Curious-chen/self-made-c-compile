from collections import namedtuple, defaultdict

Message = namedtuple('Message', 'ErrorType Location ErrorMessage')
Global = namedtuple('Global', 'name type value addr lev')
Var = namedtuple('Var', 'name type value addr lev')
Func = namedtuple('Func', 'name type NumOfParameters size')


class SecTable:
    def __init__(self):
        self.variableDict = defaultdict(list)
        self.variableType = namedtuple('variable', 'name type value addr lev')
        self.totalSize = 0  # 整体变量占的空间方便汇编代码填写地址

    def addPavariable(self, token, type, value, lev):
        pass

    def addVariable(self, token, type, value, size, lev):
        message = self.checkHasDefine(token, lev)
        if message != Message(None, None, None):
            return message
        tmp = self.variableType(token.val, type, value, self.totalSize, lev)  # 使用临时变量存储
        self.totalSize += size
        self.variableDict[token.val].append(tmp)  # 用于查找是否重复
        return message

    def checkHasDefine(self, token, lev):  # 重复定义语义错误
        if token.val in list(self.variableDict.keys()):
            # for pre in self.variableDict[token.val]:  # 找到该函数下相同的变量
            #     print(self.variableDict[token.val])
            #     if pre.lev == lev and pre.name == token.val:  # 表明重复定义报错
            ErrorType = '重复定义'
            Location = {'line':token.cur_line + 1, 'col': token.cur_col}
            ErrorMessage = "变量 '{token}' 重复定义".format(token=token.val)
            return Message(ErrorType, Location, ErrorMessage)
        return Message(None, None, None)

    def checkDoDefine(self, token, glob_var):  # 检查是变量使用时是否定义
        if token.val not in list(self.variableDict.keys()) and token.val not in list(glob_var.keys()):
            ErrorType = '未声明的变量: '
            Location = {'line':token.cur_line + 1, 'col': token.cur_col}
            ErrorMessage = "变量 '{token}' 未声明".format(token=token.val)
            return Message(ErrorType, Location, ErrorMessage)
        return Message(None, None, None)

    def checkSameType(self, list_, globalVar, fun_list):  # 判断表达式的类型是否相同
        # print('-------{}'.format(list_))
        type_, type__, temp = '', '', None
        if list_[0].val in list(self.variableDict.keys()):  # 得到表达式被赋值的标识符类型
            temp_list = self.variableDict[list_[0].val]  # 局部变量中寻找
            for pre in temp_list[::-1]:
                if pre.name == list_[0].val:
                    type_ = pre.type
            # type_ = self.variableDict[list_[0].val][0].type
        elif list_[0].val in list(globalVar.keys()):  # 全局变量中寻找
            type_ = globalVar[list_[0].val].type
        for ind in range(0, len(list_)):
            type__ = ''  # 初始化
            if list_[ind].val in list(self.variableDict.keys()):
                temp_list = self.variableDict[list_[ind].val]
                for pre in temp_list[::-1]:
                    if pre.name == list_[ind].val:
                        type__ = pre.type
                        temp = list_[ind]
                # type__ = self.variableDict[list_[ind].val][0].type
            elif list_[ind].val in list(globalVar.keys()):
                type__ = globalVar[list_[ind].val].type
                temp = list_[ind]
            else:  # 函数返回类型
                for i in fun_list:
                    if list_[ind].val == i.functionName:
                        type__ = i.returnType
                        temp = list_[ind]
            # print('type:{},type_:{}'.format(type_, type__))
            if type_ != type__:
                ErrorType = '参数类型不同'
                Location = {'line':temp.cur_line + 1, 'col': temp.cur_col}
                ErrorMessage = "参数 '{token}' 返回值类型不同".format(token=temp.val)
                return Message(ErrorType, Location, ErrorMessage)
        return Message(None, None, None)

    def checkreturen(self, fun_name, fun_list, token_list, globalvar, id):  # 判断函数返回值类型是否与函数一致
        temp_token = token_list[id]
        temp_fun = None
        type_, type__ = '', ''
        for i in fun_list:
            if fun_name == i.functionName:  # 找到函数类型
                temp_fun = i
                type__ = i.returnType
        while temp_token.val != ';':
            if temp_token.typ in ['700', '400', '500']:  # 表示标识符
                if temp_token.typ == '400':
                    type_ = 'int'
                elif type_ == '500':
                    type_ = 'char'
                else:
                    message = self.checkDoDefine(temp_token, globalvar)  # 判断是否定义过
                    if message.ErrorType != None: return message
                    type_ = self.variableDict[temp_token.val][0].type  # 得到表达式的类型
                # temp_fun = temp_token
                # print('fun:{},var:{}'.format(type__, type_))
                if type_ != type__:  # 如果函数类型与返回值类型不匹配则报错
                    ErrorType = '返回值类型不同'

                    Location = {'line':temp_token.cur_line + 1, 'col': temp_token.cur_col}
                    ErrorMessage = "函数 '{token}' 返回值类型不同".format(token=fun_name)
                    return Message(ErrorType, Location, ErrorMessage)
            temp_token = token_list[temp_token.id + 1]
        return Message(None, None, None)
        pass


class Function(SecTable):
    def __init__(self, name, returnType):
        super().__init__()
        self.functionName = name  # 函数体名
        self.numOfParameters = 0  # 参数个数
        self.parametersDict = {}  # 参数字典，用于查询是否重复定义
        self.typeOfParametersList = []  # 参数类型列表
        self.returnType = returnType  # 返回值类型

    def addPavariable(self, token, type, value, lev):
        message = self.checkHasDefine(token, lev)
        if message != Message(None, None, None):
            return message
        tmp = self.variableType(token.val, type, value, -2, -1)
        for key in list(self.variableDict.keys()):
            t = self.variableDict[key]
            # print(t)
            self.variableDict[key].append(self.variableType(t[0].name, t[0].type, t[0].value, t[0].addr - 2, -1))
            self.variableDict[key] = self.variableDict[key][1:]
        self.variableDict[token.val].append(tmp)
        self.parametersDict[token.val] = tmp
        self.numOfParameters += 1
        # print('{}******************************'.format(self.numOfParameters))
        return message


class SYMBOL:
    def __init__(self):
        self.symbolTableInfo, self.var_list = None, None
        self.globalvar = {}
        self.functionList = []  # 函数体列表
        self.allList = []  # 保存函数
        self.globalNameList = []  # Function  name 集合方便查找重复定义情况
        self.functionNameList = []
        self.symDict = {}  # {name:secTable}    #用于生成目标代码时查找
        self.P = SecTable()
        self.type_dic = {'int': 4, 'char': 1, 'float': 4, 'double': 8, 'const': 0}

    def checkHasDefineFun(self, token):  # 定义的时候检查是否已经定义
        if token.val in self.globalNameList:
            ErrorType = '重复定义'
            Location = {'line':token.cur_line + 1, 'col': token.cur_col}
            ErrorMessage = "函数 '{token}' 重复定义".format(token=token.val)
            return Message(ErrorType, Location, ErrorMessage)
        if token.val in self.globalvar:
            ErrorType = '函数名错误'
            Location = {'line':token.cur_line + 1, 'col': token.cur_col}
            ErrorMessage = "函数 '{token}' 与变量冲突".format(token=token.val)
            return Message(ErrorType, Location, ErrorMessage)
        return Message(None, None, None)

    def addglobalvar(self, token, type, value, size, lev):  # 全局变量
        if token.val in self.globalvar:  # 重复定义
            ErrorType = '重复定义'
            Location = {'line': token.cur_line + 1, 'col': token.cur_col}
            ErrorMessage = "变量 '{token}' 重复定义".format(token=token.val)
            return Message(ErrorType, Location, ErrorMessage)
        else:
            tmp = self.P.variableType(token.val, type, value, self.P.totalSize, lev)  # 使用临时变量存储
            self.P.totalSize += size
            self.globalvar[token.val] = tmp  # 用于查找是否重复
        return Message(None, None, None)

    def addFunction(self, token, returnType):
        message = self.checkHasDefineFun(token)
        function = Function(token.val, returnType)
        self.functionList.append(function)
        self.allList.append(function)
        self.globalNameList.append(token.val)
        self.functionNameList.append(token.val)
        self.symDict[token.val] = function
        return message

    def addVariableToTable(self, token, varType, value, lev, doseParameter=False):
        if len(self.allList) == 0:
            if 'const' in varType and len(varType) > 5:
                varType = varType.split(' ')[1].strip()
            message = self.addglobalvar(token, varType, value, self.type_dic[varType], lev)
            # message = self.addglobalvar(token, varType, value, len(token.val), lev)
        else:
            tmp = self.allList[-1]
            if doseParameter:  # 表示是函数参数列表
                message = tmp.addPavariable(token, varType, value, lev)
            else:
                message = tmp.addVariable(token, varType, value, self.type_dic[varType], lev)
                # message = tmp.addVariable(token, varType, value, len(token.val), lev)
        return message

    def checkDoDefineInFunction(self, token):  # 检查是否重定义
        function = self.functionList[-1]
        message = function.checkDoDefine(token, self.globalvar)
        return message

    def checkExpType(self, list_, token_list):  # 检查表达式类型是否相同
        function = self.functionList[-1]
        message = function.checkSameType(list_, self.globalvar, self.functionList)
        return message

    def checkReturn(self, token_list, id):  # self, fun_name, fun_list, token_list, globalvar, id
        tmp = self.functionList[-1]  # 取出当前函数名
        message = tmp.checkreturen(tmp.functionName, self.allList, token_list, self.globalvar, id)
        return message

    def checkFunction(self, RES_TOKEN, id):  # 调用函数时候检查函数是否定义
        if RES_TOKEN[id].val not in self.globalNameList:
            ErrorType = '未定义的函数'
            Location = {'line': RES_TOKEN[id].cur_line + 1, 'col': RES_TOKEN[id].cur_col}
            ErrorMessage = "函数 '{token}' 未定义".format(token=RES_TOKEN[id].val)
            return Message(ErrorType, Location, ErrorMessage)
        else:
            temp_token = RES_TOKEN[id]
            para_num = 0
            while temp_token.val != ")":
                if temp_token.val == "(":
                    para_num = -1
                if temp_token.val != ',':
                    para_num += 1
                temp_token = RES_TOKEN[temp_token.id + 1]
            # print(self.functionNameList, RES_TOKEN[id].val)
            i = self.functionNameList.index(RES_TOKEN[id].val)
            fun = self.functionList[i]
            if (fun.numOfParameters != para_num):
                ErrorType = '函数参数缺失'
                Location = {'line': RES_TOKEN[id].cur_line + 1, 'col': RES_TOKEN[id].cur_col}
                ErrorMessage = "函数 '{token}' 参数过多或过少".format(token=RES_TOKEN[id].val)
                return Message(ErrorType, Location, ErrorMessage)
            return Message(None, None, None)

    def showTheInfo(self):  # 打印符号表的信息
        symbolTableInfoStr = []
        var_list = []
        for key in self.globalvar.keys():
            demo = "    GlobalVarName: {:<5s} Type: {:<5s} Value: {:<8s} Addr:{:<3d} lev: {:<3d}".format(
                self.globalvar[key].name, self.globalvar[key].type, str(self.globalvar[key].value),
                self.globalvar[key].addr, self.globalvar[key].lev
            )
            var_list.append(Global(self.globalvar[key].name, self.globalvar[key].type, str(self.globalvar[key].value),
                                   self.globalvar[key].addr, self.globalvar[key].lev))
            symbolTableInfoStr.append(demo)
        for fun in self.functionList:
            demo = "    FuncName: {:<5s} ReturnType: {:<5s} NumOfParameters:{:<3d} Size: {:<3d}".format(
                fun.functionName, fun.returnType, fun.numOfParameters, fun.totalSize
            )
            var_list.append(Func(fun.functionName, fun.returnType, fun.numOfParameters, fun.totalSize))
            symbolTableInfoStr.append(demo)
            for _, tmp in fun.variableDict.items():
                for __, v in enumerate(tmp):
                    demo = "    VariableName: {:<5s} Type: {:<5s} Value: {:<8s} Addr: {:<3d} lev: {:<3d}".format(v.name,
                                                                                                                 v.type,
                                                                                                                 v.value,
                                                                                                                 v.addr,
                                                                                                                 v.lev)
                    var_list.append(Var(v.name, v.type, v.value, v.addr, v.lev))
                    symbolTableInfoStr.append(demo)
        self.symbolTableInfo = symbolTableInfoStr
        self.var_list = var_list
