#**Discontinued - use Meteor/Lizardess gamblebot**


#**What is this?**
This is a gamble bot made by me to automate applying fixes to weapons or armors in Airrivals.

I made this because fucklabwhoring and fuck equipmentwhoring.

This programm has two modes: Rarity, and Fixes - you can either specify a rarity (e.g. red/pierce, blue/prob, yellow/weight for armor, or purple/cyan aka super rare/legendary for weapons)

The Rarity mode is a pixelbot, which only checks the color of the message in the system log. It is very safe to use as there isnt really a room for errors.

The Fix mode uses OCR. OCR basically means a blackbox where you put an image in, and get a text out. Its magic.
This means that **_IF YOU DONT FOLLOW MY GUIDELINES, OR ARE SUPER UNLUCKY, A FIX MIGHT NOT GET PROPERLY DETECTED_**

If this happens, rest assured that i do not give a fuck.
# How do i use this?

First of, this programm only works in windowed or borderless window mode, not in fullscreen.

Second, you can only use 1920x1080, and 2560x1440 as your game resolution. Anything else will not work at all.

Third, the "System message" dialogue box (the one where the fixes, skill usage etc appear) has to be made to minimum size, and dragged into the top right corner so that it snaps there. If it does not snap and is even slightly off it will not work.

Lastly, the programm has to be ran in admin mode. Else the win32 API cannot perform mouse clicks. Also, it only works in windows, obviously.

So, just follow the instructions i left you in the programm itself. For reference on what to enter you can also check the config.txt out - you will not need this file for the programm, unless you tell it to do so (if it asks you if you have a config)

I recommend using the fixes mode even if it uses OCR just because its obviously way more efficient, and i was too lazy to properly document the different rarities yet, and its so awesome???

For the fixes, the input isnt case sensitive, and if you want suffixes you have to include the "of".


If you want to cancel it while running, press "q".


# IMPORTANT

Now, what is actually the most important part if you use the OCR mode: You have to position the system message dialogue so that it is on top of a dark, even surface.

What does this mean? First snap it in the corner like i said above. Then *rotate your camera* so that what i wrote above is true.

Why is this important? As you know, the fixes in the system box arent nice and easy to read black-on-white - they have colours, and the background depends on where you are in town.

In order to stil be able to read what the fuck this game is writing, i had to implement another step in front of the OCR: Tresholding the detected image, so it is black and white. 
This means that the programm takes the image, and for every pixel it checks the brightness. If its above a certain level, it will make the pixel black. If its below, itll end up white.
The result is an easy (for the programm) to scan image.


# FINAL NOTE
Nerf reduce damage
