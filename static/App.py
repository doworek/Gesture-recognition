import os
import math
import errno
import time
import queue
from collections import OrderedDict
from threading import Thread

import pygame
import cv2 as cv
import numpy as np

from AppScreen import AppScreen

class NoSuchScreen(Exception):
    pass

class GestureDetectorThread(Thread):
    OK = 'OK'
    UP_LEFT = 'Up/Left'
    DOWN_RIGHT = 'Down/Right'
    BACK = 'Back'
    WAIT = 'Wait'

    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True

        cv.namedWindow('frame')
        #show window with a mask to check if the lighting conditions are suitable
        cv.namedWindow('mask')

        self._event_queue = queue.Queue()
        self._tmp_queue = queue.Queue(maxsize=85)

        self._capture = cv.VideoCapture(0)

        self._gestures = {0: GestureDetectorThread.OK,
                          1: GestureDetectorThread.UP_LEFT,
                          2: GestureDetectorThread.DOWN_RIGHT,
                          3: GestureDetectorThread.BACK,
                          4: GestureDetectorThread.WAIT,
                          GestureDetectorThread.OK: 0,
                          GestureDetectorThread.UP_LEFT: 1,
                          GestureDetectorThread.DOWN_RIGHT: 2,
                          GestureDetectorThread.BACK: 3,
                          GestureDetectorThread.WAIT: 4}

        self._last_gesture = -1

    def run(self):
        while self.isRunning:
            try:
                _, frame = self._capture.read()
                frame=cv.flip(frame,1)
                kernel = np.ones((3,3),np.uint8)

                #define region of interest
                roi=frame[100:300, 300:500]

                cv.rectangle(frame,(300,100),(500,300),(239, 45, 243),0)
                hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
       
                # define range of skin color in HSV
                lower_skin = np.array([0,20,70], dtype=np.uint8)
                upper_skin = np.array([20,255,255], dtype=np.uint8)
                mask = cv.inRange(hsv, lower_skin, upper_skin)
                #extrapolate the hand to fill dark spots within
                mask = cv.dilate(mask,kernel,iterations = 4)
                #blur the image
                mask = cv.GaussianBlur(mask,(5,5),100) 
                #find contours
                contours, _= cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
                #find contour of max area(hand)
                cnt = max(contours, key = lambda x: cv.contourArea(x))
                #approx the contour a little
                epsilon = 0.0005*cv.arcLength(cnt,True)
                approx= cv.approxPolyDP(cnt,epsilon,True)
                #make convex hull around hand
                hull = cv.convexHull(cnt)
                #define area of hull and area of hand
                areahull = cv.contourArea(hull)
                areacnt = cv.contourArea(cnt)
                #find the percentage of area not covered by hand in convex hull
                arearatio=((areahull-areacnt)/areacnt)*100
                #find the defects in convex hull with respect to hand
                hull = cv.convexHull(approx, returnPoints=False)
                defects = cv.convexityDefects(approx, hull)
                # l = number of defects
                l=0
                #finding number of defects due to fingers
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])
                    pt= (100,180)

                    # find length of all sides of triangle
                    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    s = (a+b+c)/2
                    ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                    #distance between point and convex hull
                    d=(2*ar)/a
                    # apply cosine rule here
                    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

                    # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                    if angle <= 90 and d>30:
                        l += 1
                        cv.circle(roi, far, 3, [255, 255, 80], -1)
                    #draw lines around hand
                    cv.line(roi,start, end, [255, 255, 80], 2)
                l+=1
                #print corresponding gestures which are in their ranges
                font = cv.FONT_HERSHEY_SIMPLEX
                if l==1:
                    if areacnt<2000:
                        cv.putText(frame,'Put hand in the box',(0,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                        g = self._gestures[4]
                    else:
                        if arearatio<12:
                            cv.putText(frame,'0',(600,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                            g = self._gestures[4]
                        else:
                            cv.putText(frame,'1',(600,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                            g = self._gestures[0]
                elif l==2:
                    cv.putText(frame,'2',(600,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                    g = self._gestures[1]
                elif l==3:
                    if arearatio<27:
                        cv.putText(frame,'3',(600,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                elif l==4:
                    cv.putText(frame,'4',(600,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                    g = self._gestures[2]
                elif l==5:
                    cv.putText(frame,'5',(600,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                    g = self._gestures[3]
                elif l==6:
                    cv.putText(frame,'reposition',(0,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)
                else:
                    cv.putText(frame,'reposition',(10,50), font, 2, (0, 238, 254), 3, cv.LINE_AA)

                try:
                    self._tmp_queue.put_nowait(g)
                except:
                    q_list = list(self._tmp_queue.queue)
                    q_set = set(q_list)
                    gest = max(q_set, key = q_list.count)
                    while not self._tmp_queue.empty():
                        self._tmp_queue.get()

                if (l!=6) and (gest != self._last_gesture):
                    self._event_queue.put(gest)
                    self._last_gesture = gest

                    #Do not try to find gestures too often
                    time.sleep(0.5)
            
                #show the windows
                cv.imshow('mask', mask)
                cv.imshow('frame', frame)
            except:
                pass

        self._capture.release()
        cv.destroyAllWindows()
    
    def get_event(self) -> int:
        try:
            return self._event_queue.get(block=False)
        except:
            return None

    def stop_detector(self):
        self.isRunning = False

class App:
    def __init__(self, debug_keys_enabled=True, cursor_enabled=True):
        super().__init__()

        self._are_debug_keys_enabled = debug_keys_enabled

        pygame.init()
        self._surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.mouse.set_visible(cursor_enabled)
        self.w, self.h = pygame.display.get_surface().get_size()

        self._current_app_screen = None
        self._screens = {}
        
        self._gesture_detector = GestureDetectorThread()
        self._gesture_detector.start()

    def register_app_screen(self, screen_id: any, screen: AppScreen) -> None:
        self._screens[screen_id] = screen
        screen.on_registered_in_app(self)

    def show_screen(self, screen_id: any, *args, **kwargs) -> None:
        
        try:
            tmp_screen = self._screens[screen_id]
        except KeyError:
            raise NoSuchScreen()
        else:
            if self._current_app_screen != None:
                self._current_app_screen.on_hide()
            
            self._current_app_screen = tmp_screen
            self._current_app_screen.on_show(*args, **kwargs)

    def run(self, first_screen_id: any) -> None:
        appLoop = True

        self.show_screen(first_screen_id)

        while appLoop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    appLoop = False
                    break

                #keys for debugging
                if self._are_debug_keys_enabled and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.imitate_on_down_right()
                    elif event.key == pygame.K_UP:
                        self.imitate_on_up_left()
                    elif event.key == pygame.K_PAGEUP:
                        self.imitate_on_ok()
                    elif event.key == pygame.K_PAGEDOWN:
                        self.imitate_on_back()

            self._update()
            pygame.display.update()

        for s in self._screens.items():
            s[1].on_destroy()
        
        self._gesture_detector.stop_detector()
        self._gesture_detector.join()

        pygame.quit()

    def imitate_on_ok(self):
        self._current_app_screen.on_ok()

    def imitate_on_up_left(self):
        self._current_app_screen.on_up_left()

    def imitate_on_down_right(self):
        self._current_app_screen.on_down_right()

    def imitate_on_back(self):
        self._current_app_screen.on_back()


    def _update(self) -> None:

        # Check gestures
        gesture = self._gesture_detector.get_event()
        if gesture == None:
            pass
        else:
            print('Event: ' + gesture)
            if gesture == GestureDetectorThread.OK:
                self._current_app_screen.on_ok()
            elif gesture == GestureDetectorThread.UP_LEFT:
                self._current_app_screen.on_up_left()
            elif gesture == GestureDetectorThread.DOWN_RIGHT:
                self._current_app_screen.on_down_right()
            elif gesture == GestureDetectorThread.BACK:
                self._current_app_screen.on_back()
            elif gesture == GestureDetectorThread.WAIT:
                self._current_app_screen.on_wait()
            else:
                print("Gesture not recognized")

        # Update current app screen
        if self._current_app_screen:
            self._current_app_screen.draw(self._surface)
