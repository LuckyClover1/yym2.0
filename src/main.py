# coding=utf-8
import os
import sys
import threading
import _thread
current_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_path)[0]
sys.path.append(root_path)

from src.module import Module
from src.file_func import *
from src.ui import *
from src.tklog import Log


class MyThread(threading.Thread):
    def __init__(self, thread_name, config, hwnd):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.config = config
        self.hwnd = hwnd

    def run(self):

        print("self.config:"+self.config)
        global_.param.thread_name = self.thread_name
        Log.debug("------->线程开始启动...")
        global_.param.hwnd = self.hwnd
        global_.param.test_img = global_.test_img_path + "test-" + self.thread_name + ".bmp"
        init_modules(self.thread_name, self.config)
        reset_windows_size()
        # queue_click()
        try:
            print("开始方法："+global_.param.start_module_name)
            execute_(global_.param.start_module_name)
        except Exception:
            Log.error()


# 根据配置启动多个线程
def create_threads():
    global_.threads = []
    # config_arr = read_json("config.json")
    config_arr = global_.configs
    thread_num = 0
    for config in config_arr:
        use_config = config["use_json"]
        global_.threads.append(MyThread("thread-" + str(thread_num.__str__()), use_config, int(config["window"])))
        thread_num = thread_num + 1
    # _thread.start_new_thread(stop(), ("Thread-key", 1, ))


def stop():
    global_.workFlag = False
    Log.debug("-------任务停止------")


# 启动线程
def start_work():
    for thread in global_.threads:
        thread.start()


# 初始化本次执行的工作配置
def init_modules(thread_name, config):
    #Log.debug("加载配置文件 ", config)
    dict_ = read_json(config)
    global_.param.modules = {}
    for module_key in dict_:
        # module
        module = Module()
        if module_key == "module_type":
            continue
        json_ = dict_[module_key]
        for key in json_:
            func = getattr(module, "set_" + key)
            func(json_[key])
        module.set_module_name(module_key)
        global_.param.modules.update({module_key: module})
        print(global_.param.modules)
    Log.debug("配置文件加载结束")


# 启动方法，点击开始按钮
def start_up():
    # if global_.workFlag:
    #     return False
    global_.workFlag = True
    create_threads()
    start_work()
    return True

# 执行工作
def execute_(module_name):
    '''
    JSON配置格式：
     "check_victory":{
        "action": "check",
        "template": "template/victory.bmp",
        "end": "victory",
     }
    工作逻辑：
    1、通过module_name(check_victory)获取执行模块的信息
    2、获取模块中action(check)，进行执行
    '''
    print("module_name:"+module_name)
    module = global_.param.modules.get(module_name)
    while global_.workFlag:
        Log.debug("------->当前事件："+module.describe)
        func = getattr(module, module.action) #getattr 从module中获取module.action函数
        next_module_name = func()
        next_module = global_.param.modules.get(next_module_name)
        Log.debug(module.describe, "------->下一个事件：", next_module.describe)
        # 睡眠操作，记录上一次的操作
        # if module.module_name.find("sleep") < 0:
        #     global_.param.last_module = module.module_name
        # if next_module_name is not None:
        #     if next_module_name.find("sleep") < 0:
        #         global_.param.last_module = next_module_name
        #     else:
        #         # sleep
        #         module = global_.param.modules.get(next_module_name)
        #         continue
        #next_module_name = global_.param.last_module
        if module.module_name.find("sleep") >= 0:
            next_module_name = global_.param.start_module_name
        module = global_.param.modules.get(next_module_name)
    Log.debug("------->程序停止<-------")
