import time
from src.ui import *
from src.img import *
from src.tklog import Log


class Module(object):
    def __init__(self):
        self.module_name = None
        self.action = None
        self.describe = None
        self.template = None
        self.next_action = None
        self.time_ = None
        self.team_num = 0

    def set_start_module(self, start_module_name):
        global_.param.start_module_name = start_module_name

    def set_module_name(self, module_name):
        self.module_name = module_name

    def set_action(self, action):
        self.action = action

    def set_describe(self, describe):
        self.describe = describe

    def set_template(self, template):
        self.template = template

    def set_next_action(self, next_action):
        self.next_action = next_action

    def set_time_(self, time_):
        self.time_ = time_

    def set_team_num(self, team_num):
        self.team_num = team_num

    def check(self):
        Log.debug("------->【", self.describe, "】开始匹配...")
        window_capture()
        point = match_template(self.template)

        while point[0] == 0 and point[1] == 0 and global_.workFlag:  # 检验是否匹配上,没有匹配上时继续
            Log.debug("------->【", self.describe, "】匹配中...")
            time.sleep(0.5)#防止过快匹配校验
            window_capture()
            point = match_template(self.template)
        #匹配上时进行点击
        while point[0] > 0 and point[1] > 0 and global_.workFlag:  # 匹配上后进行点击，当界面未跳转时继续点击
            Log.debug("------->【", self.describe, "】匹配成功，进行点击...")
            print(point)
            time.sleep(0.5)
            #move_click(point)
            window_capture()
            point = match_template(self.template)

        Log.debug("------->【", self.describe, "】完成，进行下一步...")
        return self.next_action

    def team(self):
        if self.team_num == 2:
            point = (0, 0)
            while point and point[0] == 0 and point[1] == 0:
                time.sleep(0.5)
                # Log.debug('matching ', self.template)
                window_capture()
                point = match_template(self.template)
        else:
            point = (1, 1)
            while point and point[0] > 0 and point[1] > 0:
                time.sleep(0.5)
                # Log.debug('matching ', self.template, point)
                window_capture()
                point = match_template(self.template)
        return self.end

    def sleep(self):
        Log.debug("=======》任务完成！线程等待中...")
        time.sleep(self.time_)
        return self.next_action
