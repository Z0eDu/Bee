#!/usr/bin/env python

'''Demonstrate Python wrapper of C apriltag library by running on camera frames.'''
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import cv2
import apriltag
import math
import serial
import time
import glob


def main():

    '''Main function.'''

    parser = ArgumentParser(
        description='test apriltag Python bindings')
    

    apriltag.add_arguments(parser)

    options = parser.parse_args()


    window = 'Camera'
    cv2.namedWindow(window)

    # set up a reasonable search path for the apriltag DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    
    detector = apriltag.Detector(options,
                                 searchpath=apriltag._get_demo_searchpath())

    start_append=False
    motion={}
    pre_detection=[]
    time.sleep(1)
    pre_tag=None
    for k in range(20):
        
        rgb = cv2.imread('/home/pi/beecam/var/asd/image%02d.jpg'%k)
   
        
        if rgb is None:
            print('warning: error opening {}, skipping'.format(filename))
            break
        
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        detections, dimg = detector.detect(gray, return_image=True)

        num_detections = len(detections)
        print('Detected {} tags.\n'.format(num_detections))
        
        
        
        overlay = rgb // 2 + dimg[:, :, None] // 2
        if len(detections):
            for i, detection in enumerate(detections):
                print('Detection {} of {}:'.format(i+1, num_detections))
                H = detection.homography
                #assume bee only travel one direction a time
                #if the tag first time appears, start append to the list until the tag dispears
                if detection[1] not in pre_detection:
                    start_append=True
                if start_append:
                    if detection[1] in motion.keys():
                        motion[detection[1]].append(detection.center[1])
                    else:
                        motion[detection[1]]=[]
                        motion[detection[1]].append(detection.center[1])
                centerX = detection.center[0]
                centerY = detection.center[1]
                pre_detection.append(detection[1])
                
                print('centerX,centerY',centerX,centerY)
        else:
            if pre_detection
            pre_detection=[]

        print('loaded: /home/pi/beecam/var/asd/image%02d.jpg'%k)
        cv2.imshow(window, overlay)
        
        
        while cv2.waitKey(5) not in range(128): pass


if __name__ == '__main__':
    main()
