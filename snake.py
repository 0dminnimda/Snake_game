import numpy as np
import cv2 as cv
from pynput import keyboard
from pynput.keyboard import Key
#from multiprocessing import Process, Value, Array
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
import math as ma
import time
import random as ra

def on_release(key):
    global releas
    try:
        releas = key.char
    except AttributeError:pass
    if key:
        return False

def on_press(key):
    global press
    try:
        press = key.char
    except AttributeError:pass

def key_data(q1,q2):
    while 1:
        pres, relea = "a", "z"
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
            #if press == "ф" or press == "ц" or press == "ы" or press == "в":
            #q1.value = bytes(press, encoding = 'utf-8')
            print(pres,"press")

def nothing(x):
    pass

def move(arr,val):
    steps = -1
    if len(arr)!= 1:
        arr = arr[steps:] + arr[:steps]
    arr[0]=val
    return arr

def crt_apl(bad_z,n):
    b = True
    while 1:
        apl_p = (ra.randint(0,n-1),ra.randint(0,n-1))
        for i in bad_z:
            if apl_p == i:
                b = False
        if b == True:
            return apl_p
            break

apl_col = (0,255,0)
my_col = (255,0,255)
fill_col = (255,0,255)
not_fill = (50,50,50)
c_s = 45
ot = 10
n = 11
ver = n*(c_s+ot)+ot
#cv.namedWindow("Tracking", cv.WINDOW_NORMAL)
#cv.createTrackbar("speed", "Tracking", 0, 10, nothing)
path = [(n//2,n//2)]
m,c = -1,-1
posx,posy = n//2,n//2
apl_e = False
apl_p = (ra.randint(0,n-1),ra.randint(0,n-1))

#for _ in range(1):
while 1:
    posx,posy = posx%n,posy%n
    img = np.zeros((ver,ver, 3), dtype = "uint8")
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    if press == "ф":
        posx -= 1
    elif press == "в":
        posx += 1
    elif press == "ц":
        posy -= 1
    elif press == "ы":
        posy += 1

    path = move(path,(posx%n,posy%n))

    if (posx,posy) == apl_p:
        path.append(path[-1])
        apl_e = True

    if apl_e == True:
        apl_p = crt_apl(path,n)
        apl_e = False

    print(apl_p,(posx,posy),len(path))
    a = [[0 for y in range(n)]for x in range(n)]
    a = np.array(a)
    a[posx][posy]=-2
    for i in path:
        a[i[0]][i[1]]=-1
    a[apl_p[0]][apl_p[1]]=-3
    #a[:1]=-1
    #print(a)
    for x in range(n):
        for y in range(n):
            x1=(x+1)*c_s+ot*(x+1)
            y1=(y+1)*c_s+ot*(y+1)
            x2=x*c_s+ot*(x+1)
            y2=y*c_s+ot*(y+1)
            if a[x][y] == -1:
                cv.rectangle(img,(x1,y1),(x2,y2),fill_col,-1)
            elif a[x][y] == -2:
                cv.rectangle(img,(x1,y1),(x2,y2),my_col,-1)
            elif a[x][y] == -3:
                cv.rectangle(img,(x1,y1),(x2,y2),apl_col,-1)
            else:
                cv.rectangle(img,(x1,y1),(x2,y2),not_fill,a[x][y])
    cv.imshow("img", img)
    if cv.waitKey(1) & 0xFF == ord('2'):
        break
    #t = cv.getTrackbarPos("speed", "Tracking")
    #pr.terminate()

#if __name__ == '__main__':
#main_f()