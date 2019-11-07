import numpy as np
import cv2 as cv
from pynput import keyboard
from pynput.keyboard import Key
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
    if len(arr)!= 1 and arr[0] != arr[1]:
        arr = arr[steps:] + arr[:steps]
    arr[0]=val
    return arr

def move2(arr,val):
    del arr[0]
    arr.append(val)
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

def rand_st(pos,n,path,lo,t):
    time.sleep(t)
    press = ra.choice(["ф","в","ц","ы"])#randint()
    return check(press,pos,n,path,lo)

def check(press,pos,n,path,lo):
    ch=True
    if len(path) == 1:
        if press == "ф" and pos[0] != 0:
            pos[0] -= 1
        elif press == "в" and pos[0] != n-1:
            pos[0] += 1
        elif press == "ц" and pos[1] != 0:
            pos[1] -= 1
        elif press == "ы" and pos[1] != n-1:
            pos[1] += 1
    else:
        if press == "ф" and pos[0] != 0:
            for i in path:
                if i[0] == pos[0]-lo[0] and i[1] == pos[1]:
                    ch = False
            if ch == True:
                pos[0] -= 1
        elif press == "в" and pos[0] != n-1:
            for i in path:
                if i[0] == pos[0]+lo[2] and i[1] == pos[1]:
                    ch = False
            if ch == True:
                pos[0] += 1
        elif press == "ц" and pos[1] != 0:
            for i in path:
                if i[0] == pos[0] and i[1] == pos[1]-lo[1]:
                    ch = False
            if ch == True:
                pos[1] -= 1
        elif press == "ы" and pos[1] != n-1:
            for i in path:
                if i[0] == pos[0] and i[1] == pos[1]+lo[3]:
                    ch = False
            if ch == True:
                pos[1] += 1
        if pos == path[-1]:
            ch = False
    return pos, ch

apl_col = (0,255,0,255)
my_col = (255,0,0,255)
bod_col = (255,0,255,255)
not_fill = (50,50,50,255)
sh_col = (0,0,255,100)
c_s = 48
ot = 3
n = 9
ver = n*(c_s+ot)+ot
cv.namedWindow("Tracking", cv.WINDOW_NORMAL)
cv.createTrackbar("len", "Tracking", 0, 25, nothing)
#path = [0 for i in range(2)]
path = [0,[n//2,n//2]]
m,c = -1,-1
pos = [n//2,n//2]
look = [[pos[0],pos[1]-1],[pos[0]+1,pos[1]],[pos[0],pos[1]+1]]
look2 = [0,1,1,1]
apl_e = False
apl_p = crt_apl(path,n)

a = np.array([[0 for y in range(n)]for x in range(n)])
for i in range(0):#len(look)):
    a[look[i][0]][look[i][1]]=4
a[pos[0]][pos[1]]=1

while 1:
    for _ in range(1):
        old = a.copy()
        img = np.zeros((ver,ver, 4), dtype = "uint8")
        for x in range(n):
            for y in range(n):
                x1=(x+1)*c_s+ot*(x+1)
                y1=(y+1)*c_s+ot*(y+1)
                x2=x*c_s+ot*(x+1)
                y2=y*c_s+ot*(y+1)
                if a[x][y] == 1:
                    cv.rectangle(img,(x1,y1),(x2,y2),my_col,-1)
                elif a[x][y] == 2:
                    cv.rectangle(img,(x1,y1),(x2,y2),bod_col,-1)
                elif a[x][y] == -1:
                    cv.rectangle(img,(x1,y1),(x2,y2),apl_col,-1)
                elif a[x][y] == 4:
                    cv.rectangle(img,(x1,y1),(x2,y2),sh_col,-1)
                else:
                    cv.rectangle(img,(x1,y1),(x2,y2),not_fill,a[x][y])
        cv.imshow("img", img)
        a = np.array([[0 for y in range(n)]for x in range(n)])
        if cv.waitKey(1) & 0xFF == ord('2'):
            break

        
        t = cv.getTrackbarPos("len", "Tracking")
        if t+2 > len(path):
            path.append(path[0])
        elif t+2 < len(path):
            del path[-1]
        pass

    pos, mo = rand_st(pos,n,path[1:],look2,0.05)

    for _ in range(0):
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        pos, mo = check(press,pos,n,path[1:],look2)

    if mo == True:
        path = move2(path,pos)

    if path[0]!=0:
        dif = (pos[0]-path[-2][0],pos[1]-path[-2][1])
        if dif[0] > 0:
            look = [[pos[0],pos[1]-1],[pos[0]+1,pos[1]],[pos[0],pos[1]+1]]#print("rig")
            look2 = [0,1,1,1]
        elif dif[0] < 0:
            look = [[pos[0],pos[1]+1],[pos[0]-1,pos[1]],[pos[0],pos[1]-1]]#print("lef")
            look2 = [1,1,0,1]
        elif dif[1] > 0:
            look = [[pos[0]+1,pos[1]],[pos[0],pos[1]+1],[pos[0]-1,pos[1]]]#print("down")
            look2 = [1,0,1,1]
        elif dif[1] < 0:
            look = [[pos[0]-1,pos[1]],[pos[0],pos[1]-1],[pos[0]+1,pos[1]]]#print("up")
            look2 = [1,1,1,0]
            pass

    for i in range(0):#len(look)):
        if -1<look[i][0]<n and -1<look[i][1]<n:
            a[look[i][0]][look[i][1]]=4

    pos = [pos[0]%n,pos[1]%n]
    a[pos[0]][pos[1]]=1
    for i in path[1:-1]:
        if path[0]!=0:
            a[i[0]][i[1]]=2

while 0:
    a = np.array([[0 for y in range(n)]for x in range(n)])

    if path[1]!=0:
        dif = (posx-path[1][0],posy-path[1][1])
        pr = True

    for _ in range(1):
        img = np.zeros((ver,ver, 4), dtype = "uint8")
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        if press == "ф" and posx != 0:
            posx -= 1
        elif press == "в" and posx != n-1:
            posx += 1
        elif press == "ц" and posy != 0:
            posy -= 1
        elif press == "ы" and posy != n-1:
            posy += 1

    if pr == True:
        #dif = (posx-path[1][0],posy-path[1][1])
        if dif[0] > 0:
            look = [[posx,posy-1],[posx+1,posy],[posx,posy+1]]
            print("rig")
        elif dif[0] < 0:
            look = [[posx,posy+1],[posx-1,posy],[posx,posy-1]]
            print("lef")
        elif dif[1] > 0:
            look = [[posx+1,posy],[posx,posy+1],[posx-1,posy]]
            print("down")
        elif dif[1] < 0:
            look = [[posx-1,posy],[posx,posy-1],[posx+1,posy]]
            print("up")
            pr = False

    for i in range(len(look)):
        if -1<look[i][0]<n and  -1<look[i][1]<n:
            a[look[i][0]][look[i][1]]=-4

    #if path[1]!=0:
       # a[dir_f[0]][dir_f[1]]=-4
    #posx,posy = rand_st(posx,posy,n)

    posx,posy = posx%n,posy%n
    path = move(path,(posx,posy))

    if (posx,posy) == apl_p:
        path.append(path[-1])
        apl_e = True

    if apl_e == True:
        apl_p = crt_apl(path,n)
        apl_e = False

    print(apl_p,(posx,posy),len(path))
    a[posx][posy]=-2
    for i in path[1:-1]:
        a[i[0]][i[1]]=-1
    a[apl_p[0]][apl_p[1]]=-3

    for x in range(n):
        for y in range(n):
            x1=(x+1)*c_s+ot*(x+1)
            y1=(y+1)*c_s+ot*(y+1)
            x2=x*c_s+ot*(x+1)
            y2=y*c_s+ot*(y+1)
            if a[x][y] == -1:
                cv.rectangle(img,(x1,y1),(x2,y2),bod_col,-1)
            elif a[x][y] == -2:
                cv.rectangle(img,(x1,y1),(x2,y2),my_col,-1)
            elif a[x][y] == -3:
                cv.rectangle(img,(x1,y1),(x2,y2),apl_col,-1)
            elif a[x][y] == -4:
                cv.rectangle(img,(x1,y1),(x2,y2),sh_col,-1)
            else:
                cv.rectangle(img,(x1,y1),(x2,y2),not_fill,a[x][y])

    cv.imshow("img", img)
    if cv.waitKey(1) & 0xFF == ord('2'):
        break
    #t = cv.getTrackbarPos("speed", "Tracking")