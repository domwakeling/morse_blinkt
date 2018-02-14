#!/usr/bin/python

import sys                # so we can access argumentsr with sys.arg
import time               # so we can access time.sleep()
import blinkt             # so we can access blinkt!
import re                 # so we can access RegExp

# constants for easy access to change
DOT_TIME = 0.05
DASH_TIME = 0.2
PAUSE_TIME = 0.2
SPACE_TIME = 0.3

morse_dict = {
    "A" : ".-",    "B" : "-...",   "C" : "-.-.",  "D" : "-..",    "E" : ".",     "F" : "..-.",
    "G" : "--.",   "H" : "....",   "I" : "..",    "J" : ".---",   "K" : "-.-",   "L" : ".-..",
    "M" : "--",    "N" : "-.",     "O" : "---",   "P" : ".--.",   "Q" : "--.-",  "R" : ".-.",
    "S" : "...",   "T" : "-",      "U" : "..-",   "V" : "...-",   "W" : ".--",   "X" : "-..-",
    "Y" : "-.--",  "Z" : "--..",   "1" : ".----", "2" : "..---",  "3" : "...--", "4" : "....-",
    "5" : ".....", "6" : "-....",  "7" : "--...", "8" : "---..",  "9" : "----.", "0" : "-----",
    " " : "|"
}

def show_pixels(state, p0, p1):
    """utility to set a continuous range of pixels to a 'grey-scale' colour; outside of that range, all off""" 
    val = 0
    p0_act = max(0, min(p0, blinkt.NUM_PIXELS - 1))
    p1_act = max(p0_act, min(blinkt.NUM_PIXELS - 1, p1)) 
    if state > 0:
        val = min(1, state) * 255
    for i in range(blinkt.NUM_PIXELS):
        if p0_act <= i <= p1_act:
            blinkt.set_pixel(i, val, val, val)
        else:
            blinkt.set_pixel(i, 0, 0, 0)
    blinkt.show()

# helper functions to abstract dot, dash and space
def show_dot():
    """Helper function to show a dot, abstracting from show_pixels()"""
    show_pixels(1, 2, 5)
    time.sleep(DOT_TIME)
    show_pixels(0, 0, 7)
    time.sleep(PAUSE_TIME)

def show_dash():
    """Helper function to show a dash, abstracting from show_pixels()"""
    show_pixels(1, 0, 7)
    time.sleep(DASH_TIME)
    show_pixels(0, 0, 7)
    time.sleep(PAUSE_TIME)

def show_space():
    """Helper function to pause between words"""
    time.sleep(SPACE_TIME)

# flashing individual characters
def show_character(chr):
    """Flash an individual character - will report if unknown character is passed"""
    blinkt.set_brightness(0.1)
    try:
        morse = morse_dict[chr]
        for m in morse:
            if m == ".":
                show_dot()
            elif m == "-":
                show_dash()
            elif m == "|":
                show_space()
            else:
                print("ERROR: Attempting to flash", m, "from morse_dict array")
    except:
        print("Unexpected character passed:", chr)

# flashing a message
def show_message(message):
    """Flash a message - carries out a regular expression to produce uppercase  alphanumeric and spaces"""
    message = re.sub('[^a-zA-z\d\s:]', '', message).upper() # only alphanumeric & spaces, upper-cased
    for chr in message:
        show_character(chr)
        time.sleep(PAUSE_TIME)

# run-time
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('No message')
    else:
        message = re.sub('[^a-zA-Z\d\s:]', '', str(sys.argv[1])).upper() #uppercase letters, numbers, spaces
        show_message(message)

    blinkt.clear()
