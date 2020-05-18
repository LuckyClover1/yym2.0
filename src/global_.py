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

workFlag = False

window_hwnd_arr = []
config_file_arr = []
configs = []
configs_dsc = []
log = None

queue_ = queue.Queue
