import pyscreenshot as ImageGrab
import pydirectinput as pyautogui
import time
import os
import sys
from multiprocessing import Process, freeze_support, Queue

class AutoGambler:
    def Main(self, *args):
        #print(args)
        intervals = args[0]
        weaponPos = args[1]
        gamblePos = args[2]
        wipePos = args[3]
        colors = args[4]
        q = args[5]
        sys.stdin = os.fdopen(args[6])
        #print(colors)
        keepgoing = True
        x = 0
        print("intervals: " + str(intervals))
        print("keepgoing: " + str(keepgoing))
        while x < int(intervals) and keepgoing == True:
            self.gamble(weaponPos, gamblePos, wipePos)
            #print("gamble succeeded")

            keepgoing = self.checkPix()
            #print("checkPix suceeded")
            x+=1
            print(x)

            if x == int(intervals):
                break

        if x >= int(intervals):
            print("abandoning mainloop - out of retries")
            q.put(False)

        elif keepgoing == False:
            print("abandoning mainloop - rare fix detected")
            q.put(False)

    def doubleclickBox(self, horz,vert):
        #608 | 683 "0/0"
        #640 | 715 erste box
        #930 | 875 letzte box
        #32 abstand
        xcoord = 608+32*horz
        ycoord = 683+32*vert
        time.sleep(0.01)
        pyautogui.doubleClick(x=xcoord, y=ycoord)

    def accept(self):
        #1270 | 690
        time.sleep(0.01)
        pyautogui.click(1270,690)

    def gamble(self, weaponPos, gamblePos, wipePos):
        #print(weaponPos)
        #print(weaponPos.split("-"))
        xweaponPos = int(weaponPos.split("-")[0])
        ygamblePos = int(weaponPos.split("-")[1])
        xgamblePos = int(gamblePos.split("-")[0])
        yweaponPos = int(gamblePos.split("-")[1])
        xwipePos = int(wipePos.split("-")[0])
        ywipePos = int(wipePos.split("-")[1])
        self.doubleclickBox(xweaponPos,ygamblePos)
        self.doubleclickBox(xwipePos,ywipePos)
        self.accept()
        self.accept()
        self.doubleclickBox(xweaponPos,ygamblePos)
        self.doubleclickBox(xgamblePos,yweaponPos)
        self.accept()
        self.accept()

    def checkPix(self):

        im = ImageGrab.grab(bbox=(1645, 920, 1910, 1020))  # X1,Y1,X2,Y2
        im.save("box.png")
        pix = im.load()
        print(pix[6, 75])
        if pix[1,75] == (255, 255, 255):
            print("White")
            return True
        if pix[1,75] == (119, 187, 34):
            print("Green")
            return True
        if pix[1,75] == (255, 255, 0):
            print("Yellow")
            return True
        if pix[1,75] == (0, 255, 255):
            print("Cyan")
            return False
        else:
            print("Rare fix detected")
            return False

def main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input):
    foo = AutoGambler()
    fn = sys.stdin.fileno()
    p1 = Process(target=foo.Main, args=(intervals_input, weaponPos_input, gamblePos_input, wipePos_input, "cyan", q, fn))
    p1.start()
    p1.join()
    if q.get() == False:
        print("test")
        x = input("Rare gamble detected. Keep going? (Enter amount of retries, default 10)") or 10
        intervals_input = x
        main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input)

if __name__ == "__main__":
    intervals_input = input("Repeat how often? (X for infinite, default 10)") or 10
    weaponPos_input = input("What square is your weapon on? (e.g. 5th from left, 3rd from top => '5-3')")
    gamblePos_input = input("What square is your gamble on?")
    wipePos_input = input("What square is your wipe on?")

    freeze_support()
    q = Queue()
    main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input)