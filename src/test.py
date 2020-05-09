import win32api
import win32con
import win32gui
import win32ui

from src.tklog import Log


def list_windows():
    win32gui.EnumWindows(winEnumHandler, None)


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        text = win32gui.GetWindowText(hwnd)
        print(hwnd, text)


if __name__ == '__main__':
    list_windows()
    # win32gui.SetWindowPos(1443398, win32con.HWND_NOTOPMOST, 300, 100, 1000, 1, win32con.SWP_SHOWWINDOW)
