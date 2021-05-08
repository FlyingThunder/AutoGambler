import pyscreenshot as ImageGrab
import pydirectinput as pyautogui
import time


class AutoGambler:
    def Main(self, *args):
        #print(args)
        intervals = args[0]
        weaponPos = args[1]
        gamblePos = args[2]
        wipePos = args[3]
        colors = args[4]
        q = args[5]
        #print(colors)
        keepgoing = True
        x = 0
        counter = int(intervals)
        while x < int(intervals) and keepgoing == True:
            print("\n")
            print("tries left: " + str(counter))
            counter -= 1
            #print("keepgoing: " + str(keepgoing))
            self.gamble(weaponPos, gamblePos, wipePos)
            #print("gamble succeeded")

            Color = self.checkPix()
            print("detected color: " + str(Color))
            if Color == False:
                keepgoing = False
            #print("checkPix suceeded")
            x+=1
            #print("step: " + str(x))

            if x == int(intervals):
                break

        if x >= int(intervals):
            print("abandoning mainloop - out of retries \n")
            q.put(False)

        elif keepgoing == False:
            print("abandoning mainloop - rare fix detected \n")
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

        im = ImageGrab.grab(bbox=(1645, 920, 1910, 1020), childprocess=False)  # X1,Y1,X2,Y2
        im.save("box.png")
        pix = im.load()
        #print(pix[1, 75])
        for x in range(69, 79):
            if pix[1,x] == (255, 255, 255):
                #print("White")
                return "White"
            if pix[1,x] == (119, 187, 34):
                #print("Green")
                return "Green"
            if pix[1,x] == (255, 255, 0):
                #print("Yellow")
                return "Yellow"
            if pix[1,x] == (0, 255, 255):
                #print("Cyan")
                return "Cyan"
            if pix[1,x] == (255, 0, 0):
                #print("Red")
                return "Red"
            if pix[1,x] == (255, 102, 238):
                #print("Pink")
                return "Pink"

        print("Rare fix detected")
        return False