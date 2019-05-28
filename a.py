import RPi.GPIO as GPIO
import time as t
import os
import subprocess
import sys
import pygame
import datetime
import cv2
import numpy as np
import json
from pygame.locals import *
from picamera import PiCamera

'''Needed to use the PI screen with the gui display'''
#piTFT environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


'''
Helper functions
'''

size = width, height = 320, 240
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size)
font = pygame.font.Font(pygame.font.get_default_font(), 12)
white = 255, 255, 255
black = 0, 0, 0
color = 127, 15, 111


ss_up_button = pygame.draw.rect(screen, white, [20, 200, 50, 30])
ss_down_button = pygame.draw.rect(screen, white, [90, 200, 50, 30])
delay_up_button = pygame.draw.rect(screen, white, [180, 200, 50, 30])
delay_down_button = pygame.draw.rect(screen, white, [250, 200, 50, 30])
top = "default.png"
