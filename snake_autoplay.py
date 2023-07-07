import numpy as np
import cv2 as cv
from pynput import keyboard
from pynput.keyboard import Key
import math as ma
import time
import random as ra


releas, press = None, None


def on_release(key):
    global releas
    try:
        releas = key.char
    except AttributeError:
        pass
    if key:
        return False


def get_key(key):
    try:
        return key.char
    except AttributeError:
        return ""



def on_press(key):
    global press
    try:
        press = key.char
    except AttributeError:
        pass


def key_data(q1, q2):
    while 1:
        pres, relea = "a", "z"
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            # if press == "ф" or press == "ц" or press == "ы" or press == "в":
            #q1.value = bytes(press, encoding = 'utf-8')
            # print(pres, "press")


def nothing(x):
    pass


def move(arr, val):
    ste = -1
    arr.append(val)
    arr = arr[ste:] + arr[:ste]
    # arr[1]=val
    return arr


def move2(arr, val):
    del arr[0]
    arr.append(val)
    return arr


def crt_apl(bad_z, n):
    while 1:
        b = True
        apl_p = [ra.randint(0, n-1), ra.randint(0, n-1)]
        for i in bad_z:
            if apl_p == i:
                b = False
        if b is True:
            return apl_p
            break


def rand_st(pos, n, path, lo, t):
    time.sleep(t)
    press = ra.choice(
        [["ф", "lef"],
         ["в", "rig"],
         ["ц", "up"],
         ["ы", "dow"]])  # randint()
    # print(press[1])
    return check(press[0], pos, n, path, lo)


def che_in(a, path, ch, pos, p1, p2, m):
    for i in path:
        if i[0] == pos[0]+p1*m and i[1] == pos[1]+p2*m:
            ch = False
    if ch == True:
        pos[a] += m
    return pos, ch


def check(press, pos, n, path, lo, rev=False):
    a1, a2 = 0, 1
    if rev == True:
        a1, a2 = 1, 0
    ch = True
    if len(path) == 1:
        if press in "фa" and pos[a1] != 0:
            pos[a1] -= 1
        elif press in "вd" and pos[a1] != n-1:
            pos[a1] += 1
        elif press in "цw" and pos[a2] != 0:
            pos[a2] -= 1
        elif press in "ыs" and pos[a2] != n-1:
            pos[a2] += 1
    else:
        if press in "фa" and pos[a1] != 0:
            pos, ch = che_in(a1, path, ch, pos, lo[0], 0, -1)
        elif press in "вd" and pos[a1] != n-1:
            pos, ch = che_in(a1, path, ch, pos, lo[2], 0, 1)
        elif press in "цw" and pos[a2] != 0:
            pos, ch = che_in(a2, path, ch, pos, 0, lo[1], -1)
        elif press in "ыs" and pos[a2] != n-1:
            pos, ch = che_in(a2, path, ch, pos, 0, lo[3], 1)

        if pos == path[-1]:
            ch = False
    return pos, ch


apl_col = (0, 255, 0, 255)
my_col = (255, 0, 0, 255)
bod_col = (255, 0, 255, 255)
not_fill = (50, 50, 50, 255)
sh_col = (0, 0, 255, 100)
c_s = 48
ot = 3
n = 9
ver = n*(c_s+ot)+ot
cv.namedWindow("Tracking", cv.WINDOW_NORMAL)
cv.createTrackbar("len", "Tracking", 0, 25, nothing)
cv.createTrackbar("use", "Tracking", 0, 1, nothing)
path = [0, [n//2, n//2]]
m, c = -1, -1
pos = [n//2, n//2]
look = [[pos[0], pos[1]-1], [pos[0]+1, pos[1]], [pos[0], pos[1]+1]]
look2 = [0, 1, 1, 1]
apl_p = crt_apl(path, n)

a = np.array([["." for y in range(n)]for x in range(n)])
a[pos[0]][pos[1]] = "#"
mo = True

# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.join()
# print(press)
# pos, mo = check(press, pos, n, path[1:], look2)
# listener.start()

while 1:
    pos = [pos[0] % n, pos[1] % n]
    if pos == apl_p:
        # print(path)
        path = [path[0]]+move(path[1:], path[0])  # path[-1])
        # print(path)
        apl_p = crt_apl(path[1:], n)
    else:
        pass
        # print(path)

    a[apl_p[0]][apl_p[1]] = "@"

    # while 1:
    for _ in range(1):
        #old = a.copy()
        img = np.zeros((ver, ver, 4), dtype="uint8")
        for y in range(n):
            for x in range(n):
                xy1 = ((x+1)*c_s+ot*(x+1), (y+1)*c_s+ot*(y+1))
                xy2 = (x*c_s+ot*(x+1), y*c_s+ot*(y+1))
                if a[x][y] == "#":
                    cv.rectangle(img, xy1, xy2, my_col, -1)
                elif a[x][y] == "0":
                    cv.rectangle(img, xy1, xy2, bod_col, -1)
                elif a[x][y] == "@":
                    cv.rectangle(img, xy1, xy2, apl_col, -1)
                elif a[x][y] == 4:
                    cv.rectangle(img, xy1, xy2, sh_col, -1)
                else:
                    cv.rectangle(img, xy1, xy2, not_fill, 0)
        cv.imshow("img", img)
        # print(a)
        a = np.array([["." for y in range(n)]for x in range(n)])
        if cv.waitKey(1) & 0xFF == ord('2'):
            break

        use = cv.getTrackbarPos("use", "Tracking")
        if bool(use):
            t = cv.getTrackbarPos("len", "Tracking")
            if t+2 > len(path):
                path.append(path[0])
            elif t+2 < len(path):
                del path[-1]
            pass

    pos, mo = rand_st(pos,n,path[1:],look2,0.00)

    # with keyboard.Events() as events:
    #     event = events.get(0.2)
    #     # for event in events:
    #     if type(event) == keyboard.Events.Press:
    #         # event.key == keyboard.Key.esc
    #         # on_press(event.key)
    #         pos, mo = check(event.key.char, pos, n, path[1:], look2)

    # for _ in range(1):
    #     with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #         listener.join()
    #         # print(press)
    #         pos, mo = check(press, pos, n, path[1:], look2)

    if mo == True:
        path = move2(path, pos)

    if path[0] != 0:
        dif = (pos[0]-path[-2][0], pos[1]-path[-2][1])
        if dif[0] > 0:
            look = [[pos[0], pos[1]-1], [pos[0]+1, pos[1]],
                    [pos[0], pos[1]+1]]  # print("rig")
            look2 = [0, 1, 1, 1]
        elif dif[0] < 0:
            look = [[pos[0], pos[1]+1], [pos[0]-1, pos[1]],
                    [pos[0], pos[1]-1]]  # print("lef")
            look2 = [1, 1, 0, 1]
        elif dif[1] > 0:
            look = [[pos[0]+1, pos[1]], [pos[0], pos[1]+1],
                    [pos[0]-1, pos[1]]]  # print("down")
            look2 = [1, 0, 1, 1]
        elif dif[1] < 0:
            look = [[pos[0]-1, pos[1]], [pos[0], pos[1]-1],
                    [pos[0]+1, pos[1]]]  # print("up")
            look2 = [1, 1, 1, 0]
            pass

    pos = [pos[0] % n, pos[1] % n]
    a[pos[0]][pos[1]] = "#"
    for i in path[1:-1]:
        if path[0] != 0:
            a[i[0]][i[1]] = "0"
