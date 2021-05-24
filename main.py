import pyscreenshot as ImageGrab
import pydirectinput as pyautogui
import time
import os
import sys
from multiprocessing import Process, freeze_support, Queue
from Autogambler import AutoGambler




def main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input, color_input):
    foo = AutoGambler()
    p1 = Process(target=foo.Main, args=(intervals_input, weaponPos_input, gamblePos_input, wipePos_input, color_input, q))
    p1.start()
    p1.join()
    if q.get() == False:
        x = input("Keep going? (Enter amount of retries, default 10)") or 10
        print(x)
        intervals_input = x
        main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input, color_input)

if __name__ == "__main__":
    freeze_support()
    q = Queue()
    print("The game has to be run in Windowed mode, 1920x1080, on the main screen for this to work.")
    intervals_input = input("Repeat how often? (X for infinite, default 10)") or 10
    weaponPos_input = input("What square is your weapon on? (e.g. 5th from left, 3rd from top => '5-3')")
    gamblePos_input = input("What square is your gamble on?")
    wipePos_input = input("What square is your wipe on?")
    color_input = input("What rarity do you want to stop on? e.g. 'legendary,pierce,super rare' (default: legendary - will always stop on legendary)") or "legendary"



    main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input, color_input)