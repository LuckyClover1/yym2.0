import time
from src.ui import *
from src.img import *
from src.tklog import Log


class Module(object):
    def __init__(self):
        self.module_name = None
        self.action = None
        self.template = None
        self.end = None
        self.true = None
        self.false = None
        self.parent = None
        self.time_ = None
        self.team_num = 0

    def set_start_module(self, start_module_name):
        global_.param.start_module_name = start_module_name

    def set_module_name(self, module_name):
        self.module_name = module_name

    def set_action(self, action):
        self.action = action

    def set_template(self, template):
        self.template = template

    def set_end(self, end):
        self.end = end

    def set_true(self, true):
        self.true = true

    def set_false(self, false):
        self.false = false

    def set_parent(self, parent):
        self.parent = parent

    def set_time_(self, time_):
        self.time_ = time_

    def set_team_num(self, team_num):
        self.team_num = team_num

    def check(self):
        window_capture()
        point = match_template(self.template)
        time.sleep(0.3)
        if point[0] > 0 and point[1] > 0:
            return self.true
        else:
            return self.false

    def click(self):
        window_capture()
        # Log.debug("click " + self.template)
        point = match_template(self.template)
        while point[0] > 0 and point[1] > 0:  # 检验是否点击上了
            move_click(point)
            time.sleep(0.5)
            window_capture()
            point = match_template(self.template)
        return self.end

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
        time.sleep(self.time_)
        return None
