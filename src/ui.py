import win32api
import win32con
import win32gui
import win32ui
import os
import sys
import time
import threading
current_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_path)[0]
sys.path.append(root_path)
from src import global_
from src.tklog import Log

window_width = 850

lock = threading.RLock()


def get_react():
    return get_react_(global_.param.hwnd)


def get_react_(hwnd):
    lock.acquire()
    try:
        rate = 1
        # 获取句柄窗口的大小信息
        print("获取句柄窗口的大小信息")
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        print(left, top, right, bot)
        top = int(top * rate)
        left = int(left * rate)
        right = int(right * rate)
        bot = int(bot * rate)

        return left, top, right, bot
    finally:
        lock.release()


def window_capture():
    lock.acquire()
    try:
        react = get_react()
        left = react[0]
        top = react[1]
        right = react[2]
        bot = react[3]
        width = right - left
        height = bot - top
        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hWndDC = win32gui.GetWindowDC(0)

        # 创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        # 创建内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap(hWndDC)
        # 为bitmap开辟存储空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        # 将截图保存到saveBitMap中
        saveDC.SelectObject(saveBitMap)
        # 保存bitmap到内存设备描述表
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, global_.param.test_img)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(0, hWndDC)
        return react
    finally:
        lock.release()

def move_click(point):
    lock.acquire()
    try:
        # global_.queue_.put(point)
        make_long = win32api.MAKELONG(point[0], point[1])
        hwnd = global_.param.hwnd
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, make_long)  # 模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, make_long)  # 模拟鼠标弹起
    finally:
        lock.release()


def queue_click():
    while global_.workFlag:
        point = global_.queue_.get()
        make_long = win32api.MAKELONG(point[0], point[1])
        hwnd = global_.param.hwnd
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, make_long)  # 模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, make_long)  # 模拟鼠标弹起
        time.sleep(0.2)


def drag(s_point, e_point):
    pos = win32api.GetCursorPos()
    win32api.SetCursorPos(s_point)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.SetCursorPos(e_point)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.SetCursorPos(pos)


def reset_windows_size():
    lock.acquire()
    try:
        left, top, right, bot = get_react()
        # win32gui.GetWindow(global_.param.hwnd)
        # 仅设置了宽度，长度yys会自适应
        win32gui.SetWindowPos(global_.param.hwnd, win32con.HWND_NOTOPMOST, left, top, 800, 1, win32con.SWP_SHOWWINDOW)
        Log.debug("设置窗口大小")
    finally:
        lock.release()

#激活窗口，并置顶
def active_window(hwnd):
    lock.acquire()
    try:
        left, top, right, bot = get_react_(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, left, top, right-left, bot-top, win32con.SWP_SHOWWINDOW)
    finally:
        lock.release()

#遍历所有窗口
def list_windows():
    win32gui.EnumWindows(win_enum_handler, None)

#获取阴阳师窗口，放入全局中
def win_enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        text = win32gui.GetWindowText(hwnd)
        if text == '阴阳师-网易游戏':
            global_.window_hwnd_arr.append(hwnd)


if __name__ == '__main__':
    # global_.param.thread_name = "test_ui"
    # global_.param.test_img = global_.test_img_path + "test-test_ui" + ".bmp"
    # global_.param.hwnd = 329572
    # window_capture()
    # global_.param.test_img = global_.test_img_path + "test-test_ui2" + ".bmp"
    # global_.param.hwnd = 394932
    # window_capture()
    global_.param.hwnd = 329572
    reset_windows_size()
