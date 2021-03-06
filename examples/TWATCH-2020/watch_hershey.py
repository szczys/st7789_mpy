'''
watch_hershey.py

    Demo program for LILYGO® TTGO T-Watch-2020 that draws greetings on display
    cycling thru hershey fonts and colors.

'''

import utime
import random
import sys
from machine import Pin, SoftSPI
import axp202c
import st7789

# Load several frozen fonts from flash

import gotheng
import greeks
import italicc
import italiccs
import meteo
import romanc
import romancs
import romand
import romanp
import romans
import romant
import scriptc
import scripts


def cycle(p):
    '''
    return the next item in a list
    '''
    try:
        len(p)
    except TypeError:
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p


COLORS = cycle([0xe000, 0xece0, 0xe7e0, 0x5e0, 0x00d3, 0x7030])

FONTS = cycle([
    gotheng, greeks, italicc, italiccs, meteo, romanc, romancs,
    romand, romanp, romans, romant, scriptc, scripts])

GREETINGS = cycle([
    "bonjour", "buenas noches", "buenos dias",
    "good day", "good morning", "hey",
    "hi-ya", "hi", "how are you", "how goes it",
    "howdy-do", "howdy", "shalom", "welcome",
    "what's happening", "what's up" ])


def main():
    '''
    Draw greetings on display cycling thru hershey fonts and colors
    '''
    try:
        # Turn power on display power
        axp = axp202c.PMU()
        axp.enablePower(axp202c.AXP202_LDO2)
        axp.enablePower(axp202c.AXP202_DCDC3)

        # initialize spi port
        spi = SoftSPI(
            2,
            baudrate=32000000,
            polarity=1,
            phase=0,
            bits=8,
            firstbit=0,
            sck=Pin(18, Pin.OUT),
            mosi=Pin(19, Pin.OUT))

        # configure display
        tft = st7789.ST7789(
            spi,
            240,
            240,
            cs=Pin(5, Pin.OUT),
            dc=Pin(27, Pin.OUT),
            backlight=Pin(12, Pin.OUT),
            rotation=2)

        tft.init()
        tft.fill(st7789.BLACK)
        height = tft.height()
        width = tft.width()
        row = 0

        while True:
            row += 32
            color = next(COLORS)
            tft.fill_rect(0, row-16, width, 32, st7789.BLACK)
            tft.draw(next(FONTS), next(GREETINGS), 0, row, color)

            if row > 192:
                row = 0

            utime.sleep(0.25)

    finally:
        # shutdown spi
        if 'spi' in locals():
            spi.deinit()


main()
