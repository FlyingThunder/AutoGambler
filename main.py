from multiprocessing import Process, freeze_support, Queue
from Autogambler import AutoGambler
import configparser
import keyboard
import sys


def main(q, intervals_input, weaponPos_input, gamblePos_input, wipePos_input, mode_input, color_input, resolution, windowmode, delay_input, queue2):
    foo = AutoGambler()
    p1 = Process(target=foo.Main, args=(intervals_input, weaponPos_input, gamblePos_input, wipePos_input, mode_input, color_input, q, resolution, windowmode, delay_input))
    p1.start()
    p2 = Process(target=keyCatcher, args=(queue2,))
    p2.start()
    if queue2.get() == False:
        print("Terminating Programm")
        p1.terminate()
        p1.join()
        p2.terminate()
        p2.join()
        sys.exit()

    if q.get() == False:
        x = input("Keep going? (Enter amount of retries, default 10)") or 10
        print(x)
        intervals_input = x
        main(q, intervals_input, weaponPos_input, gamblePos_input, wipePos_input, mode_input, color_input, resolution, windowmode, delay_input, queue2)

def keyCatcher(queue2):
    while True:
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            queue2.put(False)

if __name__ == "__main__":
    freeze_support()
    q = Queue()
    queue2 = Queue()
    print("Version 3 made by FlyingThunder @ 07.06.2021")
    print("""\nThis programm has to run in Admin mode on the main screen.\n
!!! The system message box has to be snapped just in the upper right corner, in minimum size, with a dark background (e.g. the floor/wall) !!!\n
For more info on how to use, go to \nhttps://github.com/FlyingThunder/AutoGambler/blob/master/readme.md \nor open the readme file in the AutoGambler folder\n""")
    print("Press 'q' to interrupt the programm")




    intervals_input = input("\nRepeat how often? (X for infinite, default 10)") or 10
    config_input = input("\nDo you have a set-up configuration? [y / n]").lower()
    if config_input == "y":
        try:
            configParser = configparser.ConfigParser()
            configFilePath = r'config.txt'
            configParser.read(configFilePath)

            windowmode = configParser.get('setup-config', 'windowmode')
            resolution = configParser.get('setup-config', 'resolution')
            weaponPos_input = configParser.get('setup-config', 'weaponPos')
            gamblePos_input = configParser.get('setup-config', 'gamblePos')
            wipePos_input = configParser.get('setup-config', 'wipePos')
            mode_input = configParser.get('gamble-config', 'mode')
            if mode_input == "r":
                color_input = configParser.get('gamble-config', 'rarity')
            elif mode_input == "f":
                color_input = configParser.get('gamble-config', 'fixes')
            delay_input = configParser.get('setup-config', 'delay')
        except:
            print("Could not load config. Refer to example config, maybe a value is missing.")
    else:
        delay_input = input("\nHow many ms should the macro wait between each step? (Default 0 - only needed if you are latino or pinoy and play with 200ms)") or "0"
        resolution = input("\nWhat resolution are you playing on? (Currently supported: 1920x1080 and 2560x1440)").lower() or "1920x1080"
        windowmode = input("\nAre you playing on windowed or borderless? !! FULLSCREEN WILL NOT WORK !!").lower() or "windowed"
        weaponPos_input = input("\nWhat square is your weapon on? (e.g. 5th from left, 3rd from top => '5-3')") or "1-1"
        gamblePos_input = input("\nWhat square is your gamble on?") or "2-2"
        wipePos_input = input("\nWhat square is your wipe on?") or "3-3"
        mode_input = input("\nFilter for [r]arity, or a specific [f]ix?").lower() or "r"
        if mode_input == "r":
            color_input = input("\nWhat rarity do you want to stop on? e.g. 'legendary,pierce,super rare' (default: legendary - will always stop on legendary)").lower() or "legendary"
        elif mode_input == "f":
            print("\n!!! WARNING !!! Fix detection uses OCR instead of pixel scanning which can be faulty if the background is bad.\n"
                  "To ensure maximum quality, rotate your camera so that the second bottom line of the system message dialogue is \non an even, gray surface, like the ground in the inner ring in BCU city (and not like the ground on the outer ring)"
                  "\nIt might rarely happen that it misses a fix, if so suck a fart loser lol")
            while True:
                color_input = input("\nWhat fix do you want to stop on? e.g. 'orobas,conclave,hypnos'").lower()
                if color_input == None:
                    continue
                else:
                    break
        else:
            print("invalid input")
            exit()


    main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input, mode_input, color_input, resolution, windowmode, delay_input, queue2)