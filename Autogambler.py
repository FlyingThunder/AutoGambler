import pyscreenshot
import pydirectinput as pyautogui
import time


class AutoGambler:
    def Main(self, *args):
        #print(args)
        intervals = args[0]
        weaponPos = args[1]
        gamblePos = args[2]
        wipePos = args[3]
        stopcolors = []
        for x in args[4].lower().split(","):
            stopcolors.append(x)
        stopcolors.append("legendary")
        q = args[5]
        print(f"Watching for {stopcolors} fixes")
        keepgoing = True
        x = 0

        if str(intervals).lower() == "x":
            counter = 1
        else:
            counter = int(intervals)

        while x < int(intervals) and keepgoing == True:
            print("\n")
            if str(intervals).lower() == "x":
                print("Try Nr." + str(counter))
                counter += 1
            else:
                print("tries left: " + str(counter))
                counter -= 1
            self.gamble(weaponPos, gamblePos, wipePos)

            Color = self.checkPix()
            print("detected color: " + str(Color))
            if Color in stopcolors:
                keepgoing = False
            elif Color == False:
                print("color could not be detected. waiting 5 seconds and then checking again...")
                time.sleep(5)
                Color = self.checkPix()
                if Color == False:
                    print("color could still not be detected.")
                    q.put(False)
                    break
                elif Color in stopcolors:
                    keepgoing = False
                    break
                else:
                    print("oopsie")
                    keepgoing = True
                    continue


            x+=1
            if x == int(intervals):
                break

        if x >= int(intervals):
            print("abandoning mainloop - out of retries \n")
            q.put(False)

        elif keepgoing == False:
            print(f"abandoning mainloop - fix matches {stopcolors} \n")
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

        im = pyscreenshot.grab(bbox=(1645, 920, 1910, 1020), childprocess=False)  # X1,Y1,X2,Y2
        im.save("box.png")
        pix = im.load()
        #print(pix[1, 75])
        for x in range(69, 79):
            if pix[1,x] == (255, 255, 255):
                #print("Common")
                return "common"
            if pix[1,x] == (119, 187, 34):
                #print("Uncommon")
                return "uncommon"
            if pix[1,x] == (255, 255, 0):
                #print("Weight")
                return "yellow"
            if pix[1,x] == (255, 0, 0):
                #print("Pierce")
                return "pierce"
            if pix[1,x] == (255, 102, 238):
                #print("Rare") normal rare
                return "rare"
            if pix[1,x] == (0, 255, 255):
                #print("Super Rare") super rare
                return "super rare"
            if pix[1,x] == (255, 0, 255):
                #print("Legendary") legendary
                return "legendary"
            if pix[1,x] == (0, 170, 255):
                #print("Armor prob") armor prob
                return "armor prob"

        print("unknown color detected")
        return False