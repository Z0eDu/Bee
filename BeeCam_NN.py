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
import file_analyze as ana
import threading
import serial

'''Needed to use the PI screen with the gui display'''
#piTFT environment variables


ser = serial.Serial ("/dev/ttyS0")    #Open named port 


'''Dictionary for bee enter/exit events'''
bee_log_dict={-1: {'entries':[], 'exits': []} }


def add_bee_event(bee_ID=-1,event_time=0,dir_out=True,log=bee_log_dict):
    if not bee_ID in log.keys():
        log[bee_ID]={'entries':[], 'exits': []} 

    if dir_out:
        log[bee_ID]['entries'].append(event_time)
    else:
        log[bee_ID]['exits'].append(event_time)

        
def get_run_count(runFile='runCount.dat'):
    '''
    Get the current run count, increment, and return
    '''
    fh=open(runFile,'r')
    s=fh.readline()
    fh.close()
    cnt=int(s)+1
    fh=open(runFile,'w')
    fh.write(str(cnt) + '\n')
    fh.close()
    return cnt

DATE_FMT_STR='%Y-%m-%d_%H-%M-%S'

def format_folder(dt):
    '''
    Create folder and return save_prefix
    '''
    usb_dir=''
    #Check if a usb key is mounted
    if not os.system('lsblk | grep usb0'):
        usb_dir = '/media/usb0/'
    else:
        print('WARNING: Did not find usb-key, writing to local dir.')
        
    pref=dt.strftime('__' + DATE_FMT_STR)
    pref = usb_dir + 'run-' + str(get_run_count()) +pref 
    os.mkdir(pref)
    os.mkdir(pref + '/var')
    return pref + '/'


GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)   #bailout button
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #beam sensor 1
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #beam sensor 2

'''
Setup Variables
'''

'''set up camera stuff'''


camera = PiCamera(resolution=(960,600), framerate=50)
camera.iso = 250
t.sleep(2)


camera.exposure_mode='off'
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

'''store local time'''
start_time=t.time()
bee_log_dict['start_time']=start_time
bee_log_dict['start_time_iso']=datetime.datetime.today().isoformat()

save_prefix=format_folder(datetime.datetime.today())


sensor1 = False     #exiting sensor
sensor2 = False     #entering sensor
current_time = 0.0
hasPollen = False
cnt = 0
num_name = ""
delay = 100         #minimum 100, maximum 6000, steps of 25
ss = 100            #100 is minimum already, maximum 1000, steps of 25
tag=[-1]


global paused
paused = False

global quit_program
quit_program = False


pics_taken = []





def GPIO27_callback(channel):
    if not GPIO.input(27):
        global quit_program
        quit_program = True
        for i in pics_taken:
            i.join()
        ser.write('end \n')
        ser.close()
        GPIO.cleanup()



GPIO.add_event_detect(27, GPIO.BOTH, callback=GPIO27_callback, bouncetime=300)

sensor1,sensor2=False,False
sensor_on_times=0
enter,exitt=False,False
start_time=t.time()
trigger_t=0
interval=10

while(not quit_program):
    
    if (not paused): 
        pre_sensor1,pre_sensor2=sensor1,sensor2
        sensor1,sensor2=not GPIO.input(5),not GPIO.input(26)

        if(not sensor1 and pre_sensor1):
            enter=True
            leave=False
            trigger_t=t.time()
            print('falling edge')
        elif (not sensor2 and pre_sensor2):
            leave=True
            enter=False
            print('falling edge')
            trigger_t=t.time()

        if (t.time()-trigger_t<interval):
            pre_num_name=num_name
            cnt = cnt + 1
            print('cnt',cnt)

            if(enter):
                num_name = str(cnt) + "_s1"
            if(leave): 
                num_name = str(cnt) + "_s2" 

            time_pre_image=t.time()
            
            
            
            camera.capture(save_prefix+"top" + num_name + ".jpg")
            
            print("Elapsed Time for capture: ", str(t.time()-time_pre_image))

            
            '''Change here to use different tag family. Currently tag36h11'''
            
            thread=threading.Thread(target=ana.analyze,args=(cnt,pre_num_name,num_name,save_prefix,bee_log_dict,start_time,tag,ser))

            pics_taken.append(thread)
            
            thread.start()
            
            
            top = save_prefix + "top" + num_name + ".jpg"
    

           
print('Bye bye!')
     
