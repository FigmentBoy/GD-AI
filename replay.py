import gd
import win32gui
import win32api
import win32con
import json
import math

mem = gd.memory.get_memory()
win = win32gui.FindWindow(None, 'Geometry Dash')

def click():
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def unclick():
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))


print('Playing replay!')
with open('replay.json', 'r') as file:
    l = [bool(l) for l in json.loads(file.read())]
    mem.player_kill()
    while mem.is_dead() or mem.percent > 0:
        pass
    while not mem.is_dead() and mem.percent < 100:
        cx = mem.get_x_pos()
        if l[math.floor(cx)]:
            click()
        else:
            unclick()
    unclick()