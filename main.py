from multiprocessing import Process, freeze_support, Queue
from Autogambler import AutoGambler
import configparser



def main(q, intervals_input, weaponPos_input, gamblePos_input, wipePos_input, mode_input, color_input, resolution, windowmode, delay_input):
    foo = AutoGambler()
    p1 = Process(target=foo.Main, args=(intervals_input, weaponPos_input, gamblePos_input, wipePos_input, mode_input, color_input, q, resolution, windowmode, delay_input))
    p1.start()
    p1.join()
    if q.get() == False:
        x = input("Keep going? (Enter amount of retries, default 10)") or 10
        print(x)
        intervals_input = x
        main(q, intervals_input, weaponPos_input, gamblePos_input, wipePos_input, mode_input, color_input, resolution, windowmode, delay_input)

if __name__ == "__main__":
    freeze_support()
    q = Queue()
    print("""The game has to be run on the main screen for this to work. Both the game and this programm should be ran in Admin mode \n
    !!! The system message box has to be snapped just in the upper right corner, in minimum size !!!""")
    print("\nMade by FlyingThunder @ 28.05.2021\n")
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
            color_input = configParser.get('gamble-config', 'fixes')
        except:
            print("Could not load config. Refer to example config, maybe a value is missing.")
    else:
        delay_input = input("\nHow many ms should the macro wait between each step? (Default 0 - only needed if you are latino or pinoy and play with 200ms)\n") or "0"
        resolution = input("\nWhat resolution are you playing on? (Currently supported: 1920x1080 and 2560x1440)").lower()
        windowmode = input("\nAre you playing on windowed or borderless? !! FULLSCREEN WILL NOT WORK !!").lower()
        weaponPos_input = input("\nWhat square is your weapon on? (e.g. 5th from left, 3rd from top => '5-3')")
        gamblePos_input = input("\nWhat square is your gamble on?")
        wipePos_input = input("\nWhat square is your wipe on?")
        mode_input = input("\nFilter for [r]arity, or a specific [f]ix?").lower()
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

#testtesttest#testtesttest
    # testtesttest
    # testtesttest
    # testtesttest
    # testtesttest
    # testtesttest
    # testtesttest

    main(q, intervals_input, weaponPos_input, gamblePos_input,wipePos_input, mode_input, color_input, resolution, windowmode, delay_input)