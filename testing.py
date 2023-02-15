import pyautogui as pg
import time

# open file
f = open("animal.txt", "r")

# time.sleep(4)
# loop
i = 0
for line in f:
    print("SAID is " + line)
    time.sleep(1)
