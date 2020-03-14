
from PIL import Image, ImageTk # 导入图像处理函数库
import tkinter as tk           # 导入GUI界面函数库
from tkinter import ttk
import Regular


def showRPN():
    Reg = Regular.Addpoint(e.get())  # 添加连接运算符
    RPN = Regular.createRPN(Reg)  # 生成逆波兰表达式
    output = '逆波兰表达式：'
    for r in RPN:
        output+=r
        output+=' '
    var.set(output)

def OpenNFA():
    global img_png
    Img = Image.open('test-output/NFA.jpg')
    Img = Image.open('test-output/NFA.jpg')
    img_png = ImageTk.PhotoImage(Img)
    label_img.configure(image=img_png)
    label_img.place(x=740, y=150, anchor='n')
def OpenDFA():
    global img_png
    Img = Image.open('test-output/DFA.jpg')
    img_png = ImageTk.PhotoImage(Img)
    label_img.configure(image=img_png)
    label_img.place(x=740, y=200, anchor='n')
def Open_min_DFA():
    global img_png
    Img = Image.open('test-output/min_DFA.jpg')
    img_png = ImageTk.PhotoImage(Img)
    label_img.configure(image=img_png)
    label_img.place(x=740, y=250, anchor='n')

def createall():
    global index_final
    global min_table
    global character
    if e.get() != '':
        min_table, index_final, character= Regular.REG2MinDFA(e.get())
        var1.set('完成对'+e.get()+'的分析')
        Label_Show2.config(fg='green')
        btn_Show1.config(state='active')
        btn_Show2.config(state='active')
        btn_Show3.config(state='active')
        btn_Show4.config(state='active')
        btn_Show6.configure(state='active')
        btn_Show7.configure(state='active')

    else:
        var1.set('输入为空，请重新输入')
        Label_Show2.config(fg='red')

def clear():
    e.delete(0,len(e.get()))
    label_img.configure(image='')
    btn_Show1.config(state='disabled')
    btn_Show2.config(state='disabled')
    btn_Show3.config(state='disabled')
    btn_Show4.config(state='disabled')
    btn_Show6.configure(state='disabled')
    btn_Show7.configure(state='disabled')
    var1.set('')
    var.set('')
    var3.set('')

def clear_test():
    var3.set('')
    e2.delete(0, len(e2.get()))

def testString():
    print(index_final)
    if e2.get() != '':
        test = e2.get()
        flag = 1
        nextnode = 0
        for c in test:
            nextnode = min_table[nextnode][character.index(c)]-1
            if nextnode == -1:
                flag = 0
                break
        if index_final[nextnode] != 2:
            flag = 0
        if flag == 1:
            var3.set('True')
            Label_Show4.configure(fg='green')
        else :
            var3.set('False')
            Label_Show4.configure(fg='red')
    else:
        var3.set('输入为空，请输入测试字符串')
        Label_Show4.configure(fg='red')


if __name__ == '__main__':
    # 创建窗口 设定大小并命名
    window = tk.Tk()
    window.title('从正则表达式到最小化DFA')
    window.geometry('1280x720')
    global img_png  # 定义全局变量 图像的
    var = tk.StringVar()  # 这时文字变量储存器
    var1 = tk.StringVar()
    var3 = tk.StringVar()
    global index_final
    global min_table
    global character
    e = tk.Entry(window,width=25)
    e.place(x=170,y=30,anchor='nw')
    e2 = tk.Entry(window,width=25)
    e2.place(x=1060,y=30,anchor='ne')

    Label_Show1 = tk.Label(window,
                            text='请输入测试字符串:',
                            font=('Arial', 12), width=15, height=2)
    Label_Show1.place(x=740,y=20,anchor='nw')

    Label_Show1 = tk.Label(window,
                            text='请输入正则表达式:',
                            font=('Arial', 12), width=15, height=2)
    Label_Show1.place(x=20,y=20,anchor='nw')

    Label_Show2 = tk.Label(window,
                            textvariable=var1,   # 使用 textvariable 替换 text, 因为这个可以变化
                            font=('Arial', 12),
                            width=30,
                            height=1,
                            fg='red')
    Label_Show2.place(x=110,y=55,anchor='nw')

    Label_Show4 = tk.Label(window,
                            textvariable=var3,   # 使用 textvariable 替换 text, 因为这个可以变化
                            font=('Arial', 12),
                            width=30,
                            height=1)
    Label_Show4.place(x=810,y=55,anchor='nw')

    # 创建文本窗口，显示当前操作状态
    Label_Show3 = tk.Label(window,
                            textvariable=var,   # 使用 textvariable 替换 text, 因为这个可以变化
                            font=('Arial', 12), width=50, height=1)
    Label_Show3.place(x=720,y=112,anchor='n')

    btn_Show = tk.Button(window,
                            text='立即生成',      # 显示在按钮上的文字
                            width=15, height=1,
                            command=createall)     # 点击按钮式执行的命令
    btn_Show.place(x=350,y=25,anchor='nw')    # 按钮位置

    btn_Show6 = tk.Button(window,
                            text='立即测试',      # 显示在按钮上的文字
                            width=15, height=1,
                            command=testString,state='disabled')     # 点击按钮式执行的命令
    btn_Show6.place(x=1100,y=25,anchor='n')    # 按钮位置

    btn_Show7 = tk.Button(window,
                            text='清空',      # 显示在按钮上的文字
                            width=15, height=1,
                            command=clear_test,state='disabled')     # 点击按钮式执行的命令
    btn_Show7.place(x=1150,y=25,anchor='nw')    # 按钮位置

    btn_Show1 = tk.Button(window,
                            text='显示逆波兰表达式',      # 显示在按钮上的文字
                            width=15, height=2,
                            command=showRPN,state='disabled')     # 点击按钮式执行的命令
    btn_Show1.place(x=20,y=100,anchor='nw')    # 按钮位置

    btn_Show5 = tk.Button(window,
                            text='清空',      # 显示在按钮上的文字
                            width=15, height=1,
                            command=clear)     # 点击按钮式执行的命令
    btn_Show5.place(x=450,y=25,anchor='nw')    # 按钮位置

    # 创建显示图像按钮
    btn_Show2 = tk.Button(window,
                            text='显示NFA图像',      # 显示在按钮上的文字
                            width=15, height=2,
                            command=OpenNFA,state='disabled')     # 点击按钮式执行的命令
    btn_Show2.place(x=20,y=150,anchor='nw')    # 按钮位置

    btn_Show3 = tk.Button(window,
                            text='显示min_DFA图像',      # 显示在按钮上的文字
                            width=15, height=2,
                            command=Open_min_DFA,state='disabled')     # 点击按钮式执行的命令
    btn_Show3.place(x=20,y=250,anchor='nw')    # 按钮位置

    btn_Show4 = tk.Button(window,
                            text='显示DFA图像',      # 显示在按钮上的文字
                            width=15, height=2,
                            command=OpenDFA,state='disabled')     # 点击按钮式执行的命令
    btn_Show4.place(x=20,y=200,anchor='nw')    # 按钮位置



    label_img = ttk.Label(window)

    # 运行整体窗口
    window.mainloop()