import pyscreenshot
import pydirectinput as pyautogui
import time
import pytesseract
import cv2

class AutoGambler:
    def Main(self, *args):
        with open("debug.txt", "w") as x:
            x.write(str(args))
        intervals = args[0]
        weaponPos = args[1]
        gamblePos = args[2]
        wipePos = args[3]
        mode = args[4]
        stopcolors = []
        for x in args[5].lower().split(","):
            x = x[:-1] if x.endswith(" ") else x
            x = x[1:] if x.startswith(" ") else x
            stopcolors.append(x)

        q = args[6]
        resolution = args[7]
        windowmode = args[8]
        self.delay = int(args[9])/1000

        print(stopcolors)

        self.display_vars = {} #internal config vars for varying resolution and modi
        self.display_vars['beginning_inventory_x'] = 608
        self.display_vars['beginning_inventory_y'] = 683
        self.display_vars['square_distance'] = 32
        self.display_vars['accept_button_x'] = 1270
        self.display_vars['accept_button_y'] = 690
        self.display_vars['sysmessage_box_x_min'] = 1645
        self.display_vars['sysmessage_box_x_max'] = 1910
        self.display_vars['sysmessage_box_y_min'] = 120
        self.display_vars['sysmessage_box_y_max'] = 135


        #maths to get the correct pixels based on resolution

        if windowmode == "windowed":
            pass
        elif windowmode == "borderless":
            x_add = 1
            y_substract = 31

            for z in self.display_vars:
                if "sysmessage_box_x" in z:
                    self.display_vars[z] = self.display_vars[z] + x_add
                elif "sysmessage_box_y" in z:
                    self.display_vars[z] = self.display_vars[z] - y_substract


        if resolution == "1920x1080":
            #pixel_factor = 1
            pass
        elif resolution == "2560x1440":
            pixel_factor = 1.333
            for z in self.display_vars:
                self.display_vars[z] = round(self.display_vars[z]*pixel_factor)
                print(z)

        if mode == "r":
            stopcolors.append("legendary")
            print(f"Watching for {stopcolors} fixes")
        elif mode == "f":
            print(f"Watching for {stopcolors}")
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

            if mode == "r":
                Color = self.checkPix()
                print("detected color: " + str(Color))
                if Color in stopcolors:
                    keepgoing = False
                    print(f"{str(Color)} is found in {stopcolors}")
                elif Color == False:
                    print("color could not be detected. waiting 5 seconds and then checking again...")
                    time.sleep(5)
                    Color = self.checkPix()
                    if Color == False:
                        print("color could still not be detected.")
                        q.put(False)
                    elif Color in stopcolors:
                        keepgoing = False
                        break
                    else:
                        print("oopsie")
                        keepgoing = True
                        continue

            elif mode == "f":
                fix = self.checkFixOCR()
                print("detected fix: " + str(fix))
                if fix in stopcolors:
                    keepgoing = False
                else:
                    print(f"{fix} is not found in {stopcolors}")

            x += 1
            if x == int(intervals):
                break

        if x >= int(intervals):
            print("abandoning mainloop - out of retries \n")
            q.put(False)

        elif keepgoing == False:
            print(f"abandoning mainloop - fix matches {stopcolors} \n")
            q.put(False)




    def doubleclickBox(self, horz,vert):
        #in windowmode 1920x1080:
        #608 | 683 "0/0"
        #640 | 715 erste box
        #930 | 875 letzte box
        #32 abstand

        time.sleep(self.delay)
        xcoord = self.display_vars['beginning_inventory_x']+self.display_vars['square_distance']*horz
        ycoord = self.display_vars['beginning_inventory_y']+self.display_vars['square_distance']*vert
        time.sleep(0.01)
        pyautogui.doubleClick(x=xcoord, y=ycoord)

    def accept(self):
        #1270 | 690

        time.sleep(self.delay)
        time.sleep(0.01)
        pyautogui.click(self.display_vars['accept_button_x'],self.display_vars['accept_button_y'])

    def gamble(self, weaponPos, gamblePos, wipePos):
        #print(weaponPos)
        #print(weaponPos.split("-"))
        xweaponPos = int(weaponPos.split("-")[0])
        ygamblePos = int(weaponPos.split("-")[1])
        xgamblePos = int(gamblePos.split("-")[0])
        yweaponPos = int(gamblePos.split("-")[1])
        xwipePos = int(wipePos.split("-")[0])
        ywipePos = int(wipePos.split("-")[1])

        time.sleep(self.delay)
        self.doubleclickBox(xweaponPos,ygamblePos)
        time.sleep(self.delay)
        self.doubleclickBox(xwipePos,ywipePos)
        time.sleep(self.delay)
        self.accept()
        time.sleep(self.delay)
        self.accept()
        time.sleep(self.delay)
        self.doubleclickBox(xweaponPos,ygamblePos)
        time.sleep(self.delay)
        self.doubleclickBox(xgamblePos,yweaponPos)
        time.sleep(self.delay)
        self.accept()
        time.sleep(self.delay)
        self.accept()

    def checkFixOCR(self):
        #+1 ,-31 wenn borderless statt windowed


        time.sleep(self.delay)
        im = pyscreenshot.grab(bbox=(self.display_vars['sysmessage_box_x_min'], self.display_vars['sysmessage_box_y_min'],
                                     self.display_vars['sysmessage_box_x_max'], self.display_vars['sysmessage_box_y_max']), childprocess=False)  # X1,Y1,X2,Y2
        im.save("box.png")

        img = cv2.imread("box.png", 0)
        ret, thresh1 = cv2.threshold(img, 48, 255, cv2.THRESH_BINARY)
        cv2.imwrite("box2.png", thresh1)

        pytesseract.pytesseract.tesseract_cmd = r'TesseractOCR\tesseract.exe'
        fix = (pytesseract.image_to_string('box2.png')).lower()
        print(fix)
        if "(" in fix:
            return fix.split("(")[0]
        elif "Suffix)" in fix:
            return fix.split("Suffix)")[0][:-1]
        else:
            return "OCR krangled the fix :( \n" + fix

    def checkPix(self):

        time.sleep(self.delay)
        im = pyscreenshot.grab(bbox=(self.display_vars['sysmessage_box_x_min'], self.display_vars['sysmessage_box_y_min'],
                                     self.display_vars['sysmessage_box_x_max'], self.display_vars['sysmessage_box_y_max']), childprocess=False)  # X1,Y1,X2,Y2
        im.save("box.png")

        img = cv2.imread("box.png", 0)
        ret, thresh1 = cv2.threshold(img, 48, 255, cv2.THRESH_BINARY)
        cv2.imwrite("box2.png", thresh1)

        pytesseract.pytesseract.tesseract_cmd = r'TesseractOCR\tesseract.exe'
        fix = (pytesseract.image_to_string('box2.png')).lower()
        print(fix)

        pix = im.load()
        #print(pix[1, 75])
        for x in range(3, 13):
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

        print(f"unknown color detected")# - debug:{str(list(pix[1,x] for x in range(3, 13)))}")


        return False