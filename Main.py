import subprocess
import sympy

from DataGen import DataGen

def execute_java(java_input):
    cmd = r'"C:\Program Files\Java\jdk1.8.0_321\bin\java.exe" "-javaagent:D:\JetBrains\IntelliJ IDEA 2021.2.4\lib\idea_rt.jar=64476:D:\JetBrains\IntelliJ IDEA 2021.2.4\bin" -Dfile.encoding=UTF-8 -classpath "C:\Program Files\Java\jdk1.8.0_321\jre\lib\charsets.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\deploy.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\access-bridge-64.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\cldrdata.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\dnsns.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\jaccess.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\jfxrt.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\localedata.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\nashorn.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\sunec.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\sunjce_provider.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\sunmscapi.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\sunpkcs11.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\ext\zipfs.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\javaws.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\jce.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\jfr.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\jfxswt.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\jsse.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\management-agent.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\plugin.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\resources.jar;C:\Program Files\Java\jdk1.8.0_321\jre\lib\rt.jar;D:\FILE\javaProject\OO\homework\homework_2022_20373821_hw_2\out\production\untitled;D:\FILE\javaProject\OO\officalTools\homework_2-master\面向对象表达式系列第二次官方包\official_2.jar" MainClass'

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding='gb2312')

    stdout, stderr = proc.communicate(java_input)
    my_out = stdout.split("\n")[1]
    return my_out


def makeInput():
    dataGen = DataGen()
    dataGen.newExpr()
    tmp = str(len(dataGen.fun_java)) + "\n"
    for j in range(0, len(dataGen.fun_java)):
        tmp += dataGen.list_fun[dataGen.fun_java[j][0] - 1][dataGen.fun_java[j][1] - 1] + "\n"
    java_input = tmp + dataGen.std_java
    return java_input, dataGen.std_py

def judge():
    java_input, py_input = makeInput()

    f = java_input
    g = py_input
    f_ans = sympy.trigsimp(f)
    g_ans = sympy.trigsimp(g)
    difference = sympy.simplify(sympy.trigsimp(str(f).strip() + "-(" + g + ")"))

    if difference == 0:
        print("\033[32mAccept!\033[0m")  # 输出颜色为绿色
    else:
        print("\033[31mWrong Answer!\033[0m")  # 输出颜色为红色
        print("java输入：\n" + java_input)
        print("python输入：\n" + py_input)
        print("java执行结果：\n" + f)
        print("三角函数处理后的java结果：\n" + str(f_ans))
        print("三角函数处理后的python结果：\n" + str(g_ans))
        print("差值：\n" + str(difference))

def main():
        judge()
        # java_input, py_input = makeInput()
        # print(py_input)


if __name__ == "__main__":
    main()
