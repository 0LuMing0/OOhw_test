import random

class DataGen:
    __maxLevel = 1
    __minTerm = 1
    __maxTerm = 3
    __minFactor = 1
    __maxFactor = 3
    __maxPow = 7
    __allowWhite = 0
    __preZero = 0
    std_py = ""
    std_java = ""
    fun_java = []  # 随机出了哪些函数，记录一下，java输入时要用到
    fun_record = []  # 函数名不能重复，也记录一下

    list_fun1 = ["f(x)=x", "f(y)=sin(y)", "f(z)=z*z", "f(y)=y*y"]
    list_fun2 = ["g(x,y)=x+y", "g(y,z)=sin(y)*cos(z)", "g(x,z)=x*z+x-z", "g(z,y)=y*y-z+2"]
    list_fun3 = ["h(x,y,z)=x+y-z", "h(x,z,y)=sin(x)+y+cos(z)", "h(x,z,y)=x+y*(z-1)", "h(x,y,z)=y*y*x*(4-z)"]
    list_fun = [list_fun1, list_fun2, list_fun3]

    # 用于替换函数参数的变量，即若函数为f(y)=sin(y)，则从list_var中随机一个当作y填入函数
    __list_var = ["1", "2", "x", "x**2", "x**3", "x**0"]

    def __init__(self):
        self.fun_record = []
        self.fun_java = []

    # 生成空白字符
    def __generate_blank(self):
        output = ""
        if self.__allowWhite:
            cnt = random.randint(0, 2)
            for i in range(0, cnt):
                if random.randint(0, 1):
                    output += "\t"
                else:
                    output += " "
        return output

    def __generate_num(self):
        output = ""
        if random.randint(0, 1):
            if random.randint(0, 1):
                output += "-"
            else:
                output += "+"

        output += str(random.randint(0, 10000))

        self.std_py += output
        self.std_java += output

    def __generate_pow(self):
        output = "x"
        exp = random.randint(0, self.__maxPow)
        output += self.__generate_blank() + "**" + self.__generate_blank()
        if random.randint(0, 1):
            output += "+"
        output += str(exp)

        self.std_py += output
        self.std_java += output

    def __generate_num_or_pow(self):
        if random.randint(0, 1) == 0:
            self.__generate_num()
        else:
            self.__generate_pow()

    def __generate_triangle(self):
        if random.randint(0, 1) == 0:
            self.std_java += "sin("
            self.std_py += "sin("
            self.__generate_num_or_pow()
            self.std_java += ")"
            self.std_py += ")"
        else:
            self.std_java += "cos("
            self.std_py += "cos("
            self.__generate_num_or_pow()
            self.std_java += ")"
            self.std_py += ")"

    def __generate_sum(self):
        list_sum = ["1", "i", "i+2", "sin(i)", "cos(i)", "i*i", "(i-1)*i", "sin(x)", "(x+1)**2"]
        self.std_java += "sum(i,"
        down = random.randint(-5, 5)  # 下界
        up = down + random.randint(-1, 3)  # 上界
        self.std_java += str(down) + "," + str(up) + ","
        num = random.randint(0, len(list_sum) - 1)
        self.std_java += list_sum[num] + ")"

        if down > up:  # 如果下界大于上界一定要输出0
            self.std_py += "0"
        else:
            self.std_py += "("  # 加括号保持优先级
            for i in range(down, up + 1):
                # 将i替换掉，但注意不能把sin中的i替换了，这里的第二个replace就是替换回sin
                self.std_py += list_sum[num].replace("i", str(i)).replace("s" + str(i) + "n", "sin")
                if i < up:
                    self.std_py += "+"
            self.std_py += ")"

    def __generate_function(self):
        p = random.randint(1, len(self.list_fun1))  # 类型（每个函数列表中的第几个）
        num = random.randint(1, 3)  # 参数个数/函数名
        self.fun_record.append(num)  # 记录用过的函数名
        self.fun_java.append((num, p))  # 记录随机出的函数
        self.std_java += self.list_fun[num - 1][p - 1].split("=")[0][0:2]
        # 假如函数为 g(x,y)=x+y ，按等于符号split，第0项是g(x,y)，取 g(

        arr = []  # 记录实际表达式中的参数列表
        for i in range(0, num):
            arr.append(self.__list_var[random.randint(0, len(self.__list_var) - 1)])  # 从参数列表随机
            self.std_java += arr[i]
            if i < num - 1:
                self.std_java += ","
        self.std_java += ")"

        s = self.list_fun[num - 1][p - 1].split("=")[1]
        # 假如函数为 g(x,y)=x+y ，按等于符号split，第1项是x+y
        for i in range(0, num):
            # 分别将x,y替换为arr中的实际参数
            s = s.replace(self.list_fun[num - 1][p - 1].split("=")[0][2 + i * 2], arr[i])
        self.std_py += "(" + s + ")"  # 加括号维持优先级

    # 生成项
    def __generate_term(self, leftLeval, factorNum):
        if random.randint(0, 1):
            if random.randint(0, 1):
                self.std_py += "-"
                self.std_java += "-"
            else:
                self.std_py += "+"
                self.std_java += "+"
        for i in range(0, factorNum):
            if i >= 1:
                self.std_py += "*"
                self.std_java += "*"
                self.std_java += self.__generate_blank()
                self.std_py += self.__generate_blank()
            if random.randint(0, 5) == 1 & leftLeval > 0:
                self.std_py += "("
                self.std_java += "("
                self.__generate_expression(leftLeval - 1,
                                           random.randint(self.__minTerm, self.__maxTerm))
                self.std_py += ")"
                self.std_java += ")"
            elif random.randint(0, 4) == 1:
                self.__generate_triangle()
            elif random.randint(0, 3) == 1:
                self.__generate_sum()
            elif random.randint(0, 2) == 1 & len(self.fun_record) == 0:
                self.__generate_function()
            elif random.randint(0, 1):
                self.__generate_num()
            else:
                self.__generate_pow()

        # 生成表达式

    def __generate_expression(self, leftLeval, termNum):
        for i in range(0, termNum):
            if i >= 1:
                if random.randint(0, 1):
                    self.std_py += "-"
                    self.std_java += "-"
                else:
                    self.std_py += "+"
                    self.std_java += "+"
            self.std_java += self.__generate_blank()
            self.std_py += self.__generate_blank()
            self.__generate_term(leftLeval,
                                 random.randint(self.__minFactor, self.__maxFactor))

    def newExpr(self):
        self.fun_java = []  # 随机出了哪些函数，记录一下，java输入时要用到
        self.fun_record = []  # 函数名不能重复，也记录一下
        self.__generate_expression(self.__maxLevel, self.__maxTerm)
