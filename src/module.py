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
        self.true = None
        self.false = None
        self.callback = None
        self.remarks = None

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

    def set_true(self, true):
        self.true = true

    def set_false(self, false):
        self.false = false

    def set_callback(self, callback):
        self.callback = callback

    def set_remarks(self, remarks):
        self.remarks = remarks

    #御魂方法
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
        while point[0] > 0 and point[1] > 0 and global_.workFlag:
            Log.debug("------->【", self.describe, "】匹配成功，进行点击...")
            time.sleep(0.5)
            move_click(point)
            window_capture()
            point = match_template(self.template)

        Log.debug("------->【", self.describe, "】完成，进行下一步...")
        return self.next_action

    #探索检测方法
    def check2(self):
        Log.debug("------->【", self.describe, "】开始匹配...")
        window_capture()
        point = None
        if self.template.find("team.bmp") > 0:
            point = match_template2(self.template)
        else:
            point = match_template(self.template)
        if point[0] == 0 and point[1] == 0 and global_.workFlag:  # 沒匹配上
            time.sleep(0.5)
            if self.callback is not None: #当有回调时，说明是准备/战斗事件，3次检测未进入战斗状态->检测是否离队
                i = 0
                while i < 2:
                    Log.debug("------->【", self.describe, "】", str(2+i), "次开始匹配...")
                    window_capture()
                    point = match_template(self.template)
                    if point[0] == 0 and point[1] == 0 and global_.workFlag:
                        time.sleep(0.5)
                    else:
                        while point[0] > 0 and point[1] > 0 and global_.workFlag:
                            Log.debug("------->【", self.describe, "】匹配成功，进行点击...")
                            time.sleep(0.5)
                            move_click(point)
                            window_capture()
                            point = match_template(self.template)
                            Log.debug("------->【", self.describe, "】完成，进行下一步...")
                            return self.true
                    i = i + 1
                return self.callback
            return self.false
        else:
            if self.template.find("team.bmp") > 0: #当离队时，无需点击，
                Log.debug("------->【", self.describe, "】完成，进行下一步...")
                return self.true
            if self.template.find("out.bmp") > 0: #检测到退出按钮后,由于点击退出后界面不跳转，退出按钮还存在，只需要点击2次就行
                i = 0
                while i < 2 and global_.workFlag :
                    Log.debug("------->【", self.describe, "】匹配成功，", str(i), "次进行点击...")
                    time.sleep(0.5)
                    move_click(point)
                    window_capture()
                    point = match_template(self.template)
                    i = i + 1
                Log.debug("------->【", self.describe, "】完成，进行下一步...")
                return self.true
            while point[0] > 0 and point[1] > 0 and global_.workFlag:
                Log.debug("------->【", self.describe, "】匹配成功，进行点击...")
                time.sleep(0.5)
                move_click(point)
                window_capture()
                point = match_template(self.template)

            Log.debug("------->【", self.describe, "】完成，进行下一步...")
            return self.true


    def sleep(self):
        Log.debug("=======》任务完成！线程等待中...")
        time.sleep(self.time_)
        return self.next_action


