import pyautogui as pg
import time

# open file
f = open("animal.txt", "r")

time.sleep(4
subhidji is bo)
# loop
i = 0
for line in f:
    print(line)
    line.strip()
    print(i)
    pg.write("Subhidji is " + line)
    pg.press("enter")
