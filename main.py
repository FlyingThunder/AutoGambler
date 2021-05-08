import pyscreenshot as ImageGrab
import pydirectinput as pyautogui
import time
import os
import sys
from multiprocessing import Process, freeze_support, Queue
from Autogambler import AutoGambler




def main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input):
    foo = AutoGambler()
    p1 = Process(target=foo.Main, args=(intervals_input, weaponPos_input, gamblePos_input, wipePos_input, "cyan", q))
    p1.start()
    p1.join()
    if q.get() == False:
        print("test")
        x = input("Rare gamble detected. Keep going? (Enter amount of retries, default 10)") or 10
        intervals_input = x
        main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input)

if __name__ == "__main__":
    freeze_support()
    q = Queue()
    intervals_input = input("Repeat how often? (X for infinite, default 10)") or 10
    weaponPos_input = input("What square is your weapon on? (e.g. 5th from left, 3rd from top => '5-3')")
    gamblePos_input = input("What square is your gamble on?")
    wipePos_input = input("What square is your wipe on?")



    main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input)