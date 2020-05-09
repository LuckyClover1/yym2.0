import sys
import os
import threading
import queue

param = threading.local()

local = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"
test_img_path = local + 'test\\'
resources = local + 'resources\\'
config_path = local + 'config\\'

threads = []

workFlag = False

window_hwnd_arr = []
config_file_arr = []
configs = []

log = None

queue_ = queue.Queue
