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


class Base:
    def __init__(self):
        self.root = Tk()
        self.root.title("痒痒猫")
        self.root.geometry('500x500')
        self.frames = []

        self.frames.append(Home(self))
        self.frames.append(Setting(self))
        menu = Menu(self.root, tearoff=False)
        menu.add_command(label="首页", command=lambda: self.change('home'))
        menu.add_command(label="配置", command=lambda: self.change('setting'))
        menu.add_command(label="关于", command=lambda: copy_right())
        self.root.config(men=menu)
        frm = Frame(self.root)
        frm.place(x=0, y=0, width=500, height=500)
        self.change('home')

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
        Button(self.frame, text="停止", command=lambda: stop()).place(x=100, y=5, width=70, height=30)

        log = TkLog(master=self.frame)
        log.place(x=5, y=40, height=450)
        global_.log = log

        self.frame.place(x=5, y=5, width=495, height=495)

    def destroy(self):
        self.frame.destroy()


def start_up_():
    if start_up():
        Log.debug("程序启动完毕！")
    else:
        show_info("程序已经在运行！")


class Setting:
    def __init__(self, parent):
        self.parent = parent
        self.master = parent.root
        self.name = 'setting'
        self.frame = Frame(self.master)
        self.configs = {}
        self.window = None
        self.config = None

    def display(self):
        self.frame = Frame(self.master)

        Button(self.frame, text="刷新/加载", command=lambda: reload(self)).place(x=5, y=5, width=60, height=30)

        list_box_window = Listbox(self.frame, selectmode=SINGLE)
        if len(global_.window_hwnd_arr) > 0:
            for hwnd in global_.window_hwnd_arr:
                list_box_window.insert(hwnd, "window:" + str(hwnd))
        list_box_window.bind('<ButtonRelease-1>', self.select_window)
        list_box_window.place(x=5, y=40, width=200, height=150)

        list_box_config = Listbox(self.frame, selectmode=SINGLE)
        if len(global_.window_hwnd_arr) > 0:
            i = 0
            for config_file in global_.config_file_arr:
                list_box_config.insert(i, config_file)
                i = i + 1
        list_box_config.bind('<ButtonRelease-1>', self.select_config)
        list_box_config.place(x=250, y=40, width=200, height=150)

        Label(self.frame, text="已选择的配置文件：").place(x=5, y=200, width=120, height=30)
        show_selected_config(self.frame)
        self.frame.place(x=5, y=5, width=495, height=495)

    def destroy(self):
        self.frame.destroy()

    def select_window(self, event):
        window = event.widget.get(event.widget.curselection()[0])
        window = window.replace("window:", "")
        active_window(int(window))
        self.window = window

    def select_config(self, event):
        if self.window is None:
            show_info("请先选择窗口！")
            return
        config = event.widget.get(event.widget.curselection())
        key = str(self.window)
        self.configs.update({key: dict(window=self.window, use_json=config)})
        global_.configs = self.configs.values()
        show_selected_config(self.frame)


def show_selected_config(config_frame):
    i = 0
    for value in global_.configs:
        window_ = int(value["window"])
        text = value["window"] + " : " + value["use_json"]
        Label(config_frame, text=text, anchor=NW).place(x=5, y=240 + 30*i, width=300, height=30)
        Button(config_frame, text="检查", command=lambda window_=window_: active_window(window_)) \
            .place(x=310, y=240 + 30*i, width=40, height=30)
        i = i + 1


def create_ui():
    global_.param.thread_name = "thread-main"
    list_windows()
    list_config()
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
    # messagebox.showinfo("版权", "© 2020 Clover")
    window_capture()


def show_info(message):
    messagebox.showinfo("消息", message)


create_ui()
