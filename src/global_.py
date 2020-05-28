import sys
import os
import threading
import queue

param = threading.local()

local = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"
capture_img_path = local + 'resources\\capture\\'
resources = local + 'resources\\'
config_path = local + 'config\\'

threads = []

threeFlag  = False
#挑战场次
challengeNum = 9999
#悬赏封印标识
rewardFlag = False
#线程工作标识
workFlag = False
#窗口集
window_hwnd_arr = []
#模块文件名称集
config_file_arr = []
#选择模块配置文件
configs = []
#选择模块配置中文描述
configs_dsc = []
log = None

queue_ = queue.Queue
