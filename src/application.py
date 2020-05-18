# coding=utf-8
import os
import sys
from tkinter import *
import tkinter.messagebox as messagebox

current_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_path)[0]
sys.path.append(root_path)

from src.main import *
from src.tklog import TkLog
from src.tklog import Log

wins  = {}
models = {}
class Base:
    def __init__(self):
        self.root = Tk()
        self.root.title("痒痒猫")
        self.root.geometry('500x500')
        self.frames = []

        self.frames.append(Home(self))
        self.frames.append(Setting(self))
        menu = Menu(self.root, tearoff=False)
        menu.add_command(label="配置", command=lambda: self.change('setting'))
        menu.add_command(label="启动", command=lambda: self.change('home'))
        menu.add_command(label="关于", command=lambda: copy_right())
        self.root.config(men=menu)
        frm = Frame(self.root)
        frm.place(x=0, y=0, width=500, height=500)
        self.change('setting')

    def change(self, name):
        for frame in self.frames:
            if frame.name == name:
                frame.display()
            else:
                frame.destroy()

    def destroy(self):
        for f in self.frames:
            if f is not None:
                f.destroy()


class Home:
    def __init__(self, parent):
        self.parent = parent
        self.master = parent.root
        self.name = 'home'
        self.frame = Frame(self.master)

    def display(self):
        self.frame = Frame(self.master)
        Button(self.frame, text="开始", command=lambda: start_up_()).place(x=10, y=5, width=70, height=30)
        Button(self.frame, text="停止", command=lambda: stop_()).place(x=100, y=5, width=70, height=30)

        log = TkLog(master=self.frame)
        log.place(x=5, y=40, height=450)
        global_.log = log

        self.frame.place(x=5, y=5, width=495, height=495)

    def destroy(self):
        self.frame.destroy()


def start_up_():
    if start_up(): #开始方法 --main
        Log.debug("程序启动完毕！")
    else:
        show_info("程序已经在运行！")
def stop_():
    stop()
    #Log.debug("程序结束！")

class Setting:
    def __init__(self, parent):
        self.parent = parent
        self.master = parent.root
        self.name = 'setting'
        self.frame = Frame(self.master)
        self.configs = {}
        self.window = None
        self.config = None
        self.window_des = {}
        self.config_des = {}
        self.configs_des = {}

    def display(self):
        self.frame = Frame(self.master)
        # Button(self.frame, text="刷新/加载", command=lambda: reload(self)).place(x=5, y=5, width=60, height=25)
        Label(self.frame, text="----------请选择以下游戏窗口和游戏模式----------",).place(x=5, y=5, width=400, height=25)
        Label(self.frame, text="游戏窗口：").place(x=5, y=30, width=60, height=25)
        Label(self.frame, text="游戏模式：").place(x=250, y=30, width=60, height=25)


        list_box_window = Listbox(self.frame, selectmode=SINGLE)
        if len(global_.window_hwnd_arr) > 0: #窗口id
            i = 1
            for hwnd in global_.window_hwnd_arr:
                print(hwnd)
                win_des = "阴阳师窗口"+str(i)
                list_box_window.insert(hwnd, win_des)#阴阳师窗口id
                self.window_des[win_des] = hwnd
                i = i + 1
        list_box_window.bind('<ButtonRelease-1>', self.select_window)#select_window 激活窗口
        list_box_window.place(x=5, y=50, width=200, height=150)

        list_box_config = Listbox(self.frame, selectmode=SINGLE)
        if len(global_.window_hwnd_arr) > 0:
            i = 0
            for config_file in global_.config_file_arr:#加載json
                cof = config_file.split("-")
                list_box_config.insert(i, cof[1])
                self.config_des[cof[1]] = cof[0]
                i = i + 1
        list_box_config.bind('<ButtonRelease-1>', self.select_config)
        list_box_config.place(x=250, y=50, width=200, height=150)

        Label(self.frame, text="已选择的游戏模式：", font=("微软雅黑", 9), fg='blue').place(x=5, y=200, width=120, height=20)
        show_selected_config(self.frame)
        self.frame.place(x=5, y=5, width=495, height=495)

    def destroy(self):
        self.frame.destroy()

    def select_window(self, event):
        window = event.widget.get(event.widget.curselection()[0])
        # window = window.replace("window:", "")
        #window = self.window_des[window]
        active_window(int(self.window_des[window])) #激活窗口 --ui
        self.window = window

    def select_config(self, event):
        if self.window is None:
            show_info("请先选择游戏窗口！")
            return
        config_dsc = event.widget.get(event.widget.curselection())
        config = self.config_des[config_dsc]
        key = self.window_des[str(self.window)]
        self.configs.update({key: dict(window=key, use_json=config)})
        self.configs_des.update({key: dict(window=str(key) + "-" + self.window, use_json=config + "-" + config_dsc)})
        global_.configs = self.configs.values()
        global_.configs_dsc = self.configs_des.values()
        show_selected_config(self.frame)


def show_selected_config(config_frame):
    i = 0
    for value in global_.configs_dsc:
        window_ = int(value["window"].split("-")[0])
        text = value["window"].split("-")[1] + " : " + value["use_json"].split("-")[1]
        config_frame.pack
        #Label.pack_forget(config_frame)
        Label(config_frame, text=text, anchor=NW, fg='blue').place(x=5, y=220 + 30*i, width=300, height=20)
        Label(config_frame, text="御魂模式：\n【队长】组队完成一轮，默认邀请队友后，在组队界面运行程序！\n【队员】组队完成一轮，接受邀请后，运行程序！", anchor=NW, fg='red', justify='left').place(x=5, y=280 + 30*i, width=350, height=90)
        # if value["use_json"].split("-")[0].find("dui") >= 0:
        #     print(value["use_json"])
        #     Label(config_frame, text="御魂模式需要队长和队友勾选邀请打一轮！", anchor=NW, fg='red').place(x=5, y=280 + 30*i, width=300, height=30)
        # Button(config_frame, text="检查", command=lambda window_=window_: active_window(window_)) \
        #     .place(x=310, y=240 + 30*i, width=40, height=30)
        i = i + 1


def create_ui():
    print("加载初始数据")
    global_.param.thread_name = "thread-main"
    list_windows() #获取所有窗口 --ui
    list_config() #加载json文件 --file_func
    root = Base()
    # root.root.protocol("WM_DELETE_WINDOW", on_closing)
    root.root.mainloop()


def reload(self):
    global_.config_file_arr = []
    global_.window_hwnd_arr = []
    list_windows()
    list_config()
    self.parent.change("setting")
    self.configs = {}
    self.config = None
    self.window = None
    Log.debug("重新加载完成")


def copy_right():
     messagebox.showinfo("版权", "© 2020 Clover")
    # window_capture()


def show_info(message):
    messagebox.showinfo("消息", message)


create_ui()
