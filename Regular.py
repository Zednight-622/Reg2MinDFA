# a*(abb)*b(b|a)*
from graphviz import Digraph
def Precede(r, top):  # 优先级判定 当前元素与栈顶元素
    list = [[0, 1, 1, 1],
            [-1, 0, 1, 1],
            [-1, -1, 0, 1],
            [-1, -1, -1, 0]]  # 优先级表
    Index = ['|', '·', '*','(']
    row = Index.index(r)
    col = Index.index(top)
    return list[row][col]  # 第一个参数r 与 第二个参数top 比小就返回 1 , 大就返回 -1

def Addpoint(reg):  # 添加连接运算符函数
    Reg = []
    for i in range(len(reg)):
        if reg[i] == "|"  or reg[i] == '(' :   #选择运算与左括号 后一位不会有连接运算
            Reg.append(reg[i])
        else:                                   #其余判断后一位
            if i + 1 == len(reg) or reg[i + 1] == "|" or reg[i + 1] == '*' or reg[i + 1] == ')':         #后一位如上 中间不会有连接符
                Reg.append(reg[i])
            else:
                Reg.append(reg[i])
                Reg.append('·')

    return Reg

def getChars(reg):                              # 获取字符集
    character = []
    for r in reg:
        if r != "|" and r != '*' and r != '·' and r != "(" and r != ')' and r != 'ε':
            if len(character) == 0 or r not in character:
                character.append(r)
    return character

def createRPN(Reg):             #生成逆波兰表达式
    Operator = []  # 运算符栈
    list = []  # 字符运算集
    for r in Reg:
        if r == "|" or r == '*' or r == '·':  # 运算符
            if len(Operator) == 0:
                Operator.append(r)
                continue  # 进行下一次循环
            if Operator[len(Operator) - 1] == '(':  # 栈顶为左括号
                Operator.append(r)
                continue  # 进行下一次循环
            if Precede(r, Operator[len(Operator) - 1]) == -1:  # 当前运算符比栈顶元素大
                Operator.append(r)
            else:
                list.append(Operator.pop())  # 退栈输出
                while len(Operator) != 0 and Precede(r, Operator[len(Operator) - 1]) != -1:
                    if Operator[len(Operator) - 1] != '(':
                        list.append(Operator.pop())  # 退栈输出
                    else:
                        break
                Operator.append(r)
        elif r == '(':  # 左括号
            Operator.append(r)
        elif r == ')':  # 右括号
            while Operator[len(Operator) - 1] != '(':  # 栈顶为左括号
                list.append(Operator.pop())  # 退栈输出
            Operator.pop()  # 退栈
        else:  # 运算分量
            list.append(r)
    while len(Operator) != 0:  # 表达式遍历完成，检查运算符栈，并输出
        if Operator[len(Operator) - 1] == '(':
            print('Error')
            exit()  # 错误
        else:
            list.append(Operator.pop())  # 退栈输出

    return list

def createArray(RPN):                 #通过逆波兰表达式生成节点矩阵

    NFA_stack = []   # 用来存储NFA 节点矩阵 如：'1','2','a' 第一位表示：起始,第二位表示：结束,第三位表示：连接标签
    i = 0
    for l in RPN:
        if l == '*':
            i += 1
            if len(NFA_stack) != 0:
                e = NFA_stack.pop()
                if e.__class__ == str:  # 出栈为字符，则创建三个节点进行重复运算
                    NFA_stack.append(
                        [['ε' + str(i), 'ε' + str(i + 1), 'ε'],
                         ['ε' + str(i + 1), 'ε' + str(i + 1), e],
                         ['ε' + str(i + 1), 'ε' + str(i + 2), 'ε']])
                else:  # 出栈为节点组合，将尾节点和首节点重合
                    t = e[len(e) - 1][1]
                    for e1 in e:
                        if e1[1] == t:
                            e1[1] = e[0][0]
                    e.append([e[0][0], 'ε' + str(i + 2), 'ε'])
                    NFA_stack.append(e)
        elif l == '|':
            i += 1
            if len(NFA_stack) >= 2:
                b = NFA_stack.pop()
                a = NFA_stack.pop()
                if b.__class__ == str and a.__class__ == str:  # 出栈均为字符，创建两个节点 两条路径
                    NFA_stack.append([['|' + str(i), '|' + str(i + 1), a],
                                      ['|' + str(i), '|' + str(i + 1), b]])

                elif b.__class__ != str and a.__class__ == str:  # 前为字符，后为节点组合
                    b.append([b[0][0], b[len(b) - 1][1], a])  # 将节点组合首尾建立新链接
                    NFA_stack.append(b)
                elif b.__class__ == str and a.__class__ != str:  # 前为节点组合，后为字符
                    a.append([a[0][0], a[len(a) - 1][1], b])  # 将节点组合首尾建立新链接
                    NFA_stack.append(a)
                elif b.__class__ != str and a.__class__ != str:  # 都为节点组合
                    a[0][0] = b[0][0]  # 将其中一个节点组合的首尾和另一个设置为相同节点
                    a[len(a) - 1][1] = b[len(b) - 1][1]
                    for x in a:
                        b.append(x)
                    NFA_stack.append(b)
        elif l == '·':
            i += 1
            if len(NFA_stack) != 0:
                b = NFA_stack.pop()
                a = NFA_stack.pop()
                if b.__class__ == str and a.__class__ == str:  # 都为字符，创建三个节点两条链接
                    NFA_stack.append([['·' + str(i), '·' + str(i + 1), a],
                                      ['·' + str(i + 1), '·' + str(i + 2), b]])
                elif b.__class__ != str and a.__class__ == str:  # 前为字符，则再节点组合最前添加一条链接
                    b.insert(0, ['·' + str(i + 1), b[0][0], a])
                    NFA_stack.append(b)
                elif b.__class__ == str and a.__class__ != str:  # 后为字符，则再节点组合最后添加一条链接
                    a.append([a[len(a) - 1][1], '·' + str(i + 1), b])
                    NFA_stack.append(a)
                elif b.__class__ != str and a.__class__ != str:  # 都为节点组合，将两个节点组合首尾链接
                    a.append([a[len(a) - 1][1], b[0][0], 'ε'])
                    for x in b:
                        a.append(x)
                    NFA_stack.append(a)
        else:
            i += 1
            NFA_stack.append(l)

    NFA_stack = NFA_stack[0]
    # print(NFA_stack)
    Node_stack = {}
    i = 0
    for n in NFA_stack:  # 将节点标识转换成数字
        for j in range(2):
            char = n[j]
            if len(Node_stack) == 0 or char not in Node_stack:
                i += 1
                Node_stack.update({char: str(i)})
                n[j] = str(i)
            else:
                n[j] = Node_stack.get(char)

    NFA_stack.insert(0, ['0', NFA_stack[0][0], 'ε'])  # 添加开始状态
    return NFA_stack, NFA_stack[len(NFA_stack)-1][1]

def closure(nodes,NA):       #查询某个节点的闭包
    e_closure = []
    for node in nodes:
        for N in NA:
            if N[0] == node and N[2] == 'ε':
                e_closure += closure([N[1]], NA)
                if N[1] not in e_closure:
                    e_closure.append(N[1])
    for node in nodes:
        if node not in e_closure:
            e_closure.append(node)
    e_closure.sort()
    return e_closure

def T(nodes, char, NA):         #沿char的弧能达到的状态集合
    e_closure = []
    for node in nodes:
        for N in NA:
            if N[0] == node and N[2] == char:
                if N[1] not in e_closure:
                    e_closure.append(N[1])
    e_closure.sort()
    return e_closure

def NFA2Table(NA, chars, end):
    table = []  #有字母表推导出的
    flag = []   #状态集合
    ends = []        #终结节点集合
    start0 = closure(['0'], NA)
    flag.append(start0)
    for s in start0:                            #判断初始状态中是否包含NFA的终结点
        if s == end:
            ends.append(start0)
            break
    j = 0
    for f in flag:
        table.append([])
        for char in chars:
            n = list(set(closure(T(f, char, NA), NA)))         #消除重复元素
            # if len(n) == 0:
            #     table[j].append(None)
            # else:
            if n != []:                     #得到闭包不为空
                n.sort()
                table[j].append(n)
                if end in n:
                    ends.append(n)
                if n not in flag and n != []:
                    flag.append(n)
            elif n == []:               #闭包为空
                n = ['0']
                table[j].append(n)
        j +=1
    # print(table)
    # print(flag)
    table_final = []                                            #将个状态转换为状态编号
    i = 0
    for nodes in table:
        table_final.append([])
        for node in nodes:
            if node!=['0']:
                num = flag.index(node)+1
                table_final[i].append(str(num))
            else:
                table_final[i].append(node[0])
        i+=1
    # print('DFA_ends = '),print(ends)
    end_final = []                                              #终结节点的编号
    for end in ends:
        num = flag.index(end) + 1
        if str(num) not in end_final:
            end_final.append(str(num))

    return table_final,end_final                                #返回节点标号表，终结节点的编号组,

def createNFA(NFA_Array,end):       # 生成NFA
    NFA = Digraph(comment="NFA", graph_attr={"style": 'filled', "color": 'lightgrey', "rankdir": 'LR'}, format='jpg')
    NFA.attr('node', shape='doublecircle')  # 将最终状态设置成双环
    NFA.node(end, end)
    NFA.attr('node', shape='circle')
    for l in NFA_Array:
        NFA.edge(l[0], l[1], l[2])
    NFA.render('test-output/NFA')

def createDFA(DFA_Array, ends, character):                 # 生成DFA

    DFA = Digraph(comment="DFA", graph_attr={"style": 'filled', "color": 'lightgrey', "rankdir": 'LR'}, format='jpg')
    DFA.attr('node', shape='doublecircle')
    for end in ends:
        DFA.node(end, end)
    DFA.attr('node', shape='circle')
    for i in range(len(DFA_Array)):
        for x in range(len(DFA_Array[i])):
            if DFA_Array[i][x] != '0':
                DFA.edge(str(i + 1), DFA_Array[i][x], character[x])
    DFA.render('test-output/DFA')


def createMin_DFA(min_table, index_final, character):            # 生成min_DFA

    min_DFA = Digraph(comment="min_DFA", graph_attr={"style": 'filled', "color": 'lightgrey', "rankdir": 'LR'},
                      format='jpg')
    min_DFA.attr('node', shape='doublecircle')  # 将最终状态设置成双环
    for i in range(len(index_final)):
        if index_final[i] == 2:
            min_DFA.node(str(i + 1), str(i + 1))
    min_DFA.attr('node', shape='circle')
    for i in range(len(min_table)):
        for x in range(len(min_table[i])):
            if min_table[i][x] != 0:
                min_DFA.edge(str(i + 1), str(min_table[i][x]), character[x])
    min_DFA.render('test-output/min_DFA')

def REG2MinDFA(reg):
    character = getChars(reg)       # 字符集
    Reg = Addpoint(reg)             # 添加连接运算符
    RPN = createRPN(Reg)            # 生成逆波兰表达式
    NFA_Array, end = createArray(RPN)      #NFA节点矩阵 以及终结点名
    createNFA(NFA_Array,end)
    #生成状态表
    DFA_Array, ends = NFA2Table(NFA_Array, character, end)
    createDFA(DFA_Array,ends, character)
    # 最小化DFA
    min_table = []
    index = []
    for i in range(len(DFA_Array)):         #将节点组合分为是否包含终结态，并标序号1，2
        if str(i+1) in ends:
            index.append(2)
        else:
            index.append(1)
    index_final = index.copy()              #复制为最小化后的终态序号集合

    while True:                             #将状态集合分类，并重新组合，直到序号不变完成简化
        min_table = []
        for i in range(len(DFA_Array)):
            min_table.append([])
            for j in range(len(DFA_Array[i])):
                if DFA_Array[i][j] != '0':
                    min_table[i].append(index[int(DFA_Array[i][j])-1])
                else:
                    min_table[i].append(0)
        # print('min_table = ',end=' '),print(min_table)
        i = 0
        j = 0
        index_del = []
        i_stack = []
        stack = []
        dict1 = {}
        for nodes in min_table:
            if nodes not in stack:
                stack.append(nodes)
                i+=1
                i_stack.append(i)
                dict1.update({i:nodes})
            elif nodes in stack:
                idel = min_table.index(nodes)
                i_stack.append(stack.index(nodes)+1)
                if index_final[j] == 2:
                    index_final[idel] = 2
                index_del.append(j)
            j+=1

        if i_stack == index:
            break
        else:
            index = i_stack

    #最小化DFA的节点矩阵
    min_table = []
    for i in dict1.values():
        min_table.append(i)
    #确定minDFA的终结态
    n = 0
    for i in index_del:
        index_final.pop(i-n)
        n+=1
    createMin_DFA(min_table,index_final,character)
    return min_table, index_final, character