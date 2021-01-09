import os
import errno
import time
import queue
from collections import OrderedDict
from threading import Thread

import torch
from torchvision.transforms import Compose, CenterCrop, ToPILImage, ToTensor, Normalize
import torch.nn as nn
import pygame
import cv2 as cv
import numpy as np
from model import ConvColumn

from AppScreen import AppScreen

class NoSuchScreen(Exception):
    pass

class GestureDetectorThread(Thread):
    SWIPE_LEFT = 'Swiping Left'
    SWIPE_RIGHT = 'Swiping Right'
    SWIPE_UP = 'Swiping Up'
    SWIPE_DOWN = 'Swiping Down'
    THUMB_OK = 'Thumb Up'
    THUMB_NOT = 'Thumb Down'

    NO_GESTURE = 'No gesture'
    OTHER_GESTURE = 'Doing other things'

    def __init__(self, fps=12, width=176, height=100, use_gpu=True, model_data="model_best.pth.tar"):
        Thread.__init__(self)
        self.isRunning = True

        self._capture = cv.VideoCapture(0)
        self._target_frame_size = (width, height)
        self._sleeping_time = 1/fps

        self._event_queue = queue.Queue()
        self._frame_queue = queue.Queue(maxsize=18)
        self._predict_queue = queue.Queue(maxsize=3)

        self._model = ConvColumn(8)
        if use_gpu:
            self._model.cuda()

        if os.path.isfile(model_data):
            last_checkpoint = torch.load(model_data, map_location='cpu')

            new_state_dict = OrderedDict()
            for k, v in last_checkpoint.items():
                if k == 'state_dict':
                    del last_checkpoint['state_dict']
                    for j, val in v.items():
                        name = j[7:] # we need name without 'module.' prefix
                        new_state_dict[name] = val
                    last_checkpoint['state_dict'] = new_state_dict
                    break

            self._model.load_state_dict(last_checkpoint['state_dict'])
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), model_data)

        self._transform = Compose([
            ToPILImage(),
            CenterCrop(84),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
        ])
        self._device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")

        self._gestures = {0: GestureDetectorThread.SWIPE_LEFT,
                          1: GestureDetectorThread.SWIPE_RIGHT,
                          2: GestureDetectorThread.SWIPE_DOWN,
                          3: GestureDetectorThread.SWIPE_UP,
                          4: GestureDetectorThread.THUMB_OK,
                          5: GestureDetectorThread.THUMB_NOT,
                          6: GestureDetectorThread.NO_GESTURE,
                          7: GestureDetectorThread.OTHER_GESTURE,
                          GestureDetectorThread.SWIPE_LEFT: 0,
                          GestureDetectorThread.SWIPE_RIGHT: 1,
                          GestureDetectorThread.SWIPE_DOWN: 2,
                          GestureDetectorThread.SWIPE_UP: 3,
                          GestureDetectorThread.THUMB_OK: 4, 
                          GestureDetectorThread.THUMB_NOT: 5,
                          GestureDetectorThread.NO_GESTURE: 6,
                          GestureDetectorThread.OTHER_GESTURE: 7}

        self.TRESHOLD = 0.7

    def run(self):
        while self.isRunning:
            start_time = time.time()
            _, frame = self._capture.read()
            frame = cv.resize(frame, self._target_frame_size)

            try:
                self._frame_queue.put_nowait(frame)
            except queue.Full:
                _ = self._frame_queue.get()
                self._frame_queue.put_nowait(frame)

                frames = [torch.unsqueeze(self._transform(img), 0) for img in list(self._frame_queue.queue)]
                
                data = torch.cat(frames)
                data = data.permute(1, 0, 2, 3)
                data = data[None, :, :, :, :]
                data = data.to(self._device)
 

                self._model.eval()
                nn_output = self._model(data)
                nn_output = torch.nn.functional.softmax(nn_output, dim=1)
                pred, class_index = nn_output.max(1)
                pred = pred.item()
                class_index = class_index.item()

                g = self._gestures[class_index]
                if pred > self.TRESHOLD and g != GestureDetectorThread.OTHER_GESTURE and g != GestureDetectorThread.NO_GESTURE:

                    try:
                        self._predict_queue.put_nowait((pred, g))
                    except queue.Full:
                        self._predict_queue.get()
                        self._predict_queue.put_nowait((pred, g))

                        predictions = sorted(list(self._predict_queue.queue))
                        print(predictions)

                        g = predictions[-1][1]
                        self._event_queue.put(g)

                        # Clear queues
                        while not self._frame_queue.empty():
                            self._frame_queue.get_nowait()
                        while not self._predict_queue.empty():
                            self._predict_queue.get_nowait()

                else:
                    while not self._predict_queue.empty():
                        self._predict_queue.get_nowait()


            time_diff = time.time() - start_time
            try:
                time.sleep(self._sleeping_time - time_diff)
            except:
                pass

        self._capture.release()
    
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
                        self.imitate_down_to_up_swipe_gesture()
                    elif event.key == pygame.K_UP:
                        self.imitate_up_to_down_swipe_gesture()
                    elif event.key == pygame.K_LEFT:
                        self.imitate_right_to_left_swipe_gesture()
                    elif event.key == pygame.K_RIGHT:
                        self.imitate_left_to_right_swipe_gesture()
                    elif event.key == pygame.K_PAGEUP:
                        self.imitate_thumb_up_gesture()
                    elif event.key == pygame.K_PAGEDOWN:
                        self.imitate_thumb_down_gesture()

            self._update()
            pygame.display.update()

        for s in self._screens.items():
            s[1].on_destroy()
        
        self._gesture_detector.stop_detector()
        self._gesture_detector.join()

        pygame.quit()

    def imitate_thumb_up_gesture(self):
        self._current_app_screen.on_thumb_up()

    def imitate_thumb_down_gesture(self):
        self._current_app_screen.on_thumb_down()

    def imitate_left_to_right_swipe_gesture(self):
        self._current_app_screen.on_left_to_right_swipe()

    def imitate_right_to_left_swipe_gesture(self):
        self._current_app_screen.on_right_to_left_swipe()

    def imitate_up_to_down_swipe_gesture(self):
        self._current_app_screen.on_up_to_down_swipe()

    def imitate_down_to_up_swipe_gesture(self):
        self._current_app_screen.on_down_to_up_swipe()

    def _update(self) -> None:

        # Check gestures
        gesture = self._gesture_detector.get_event()
        if gesture == None:
            pass
        else:
            print('Event: ' + gesture)
            if gesture == GestureDetectorThread.SWIPE_DOWN:
                self._current_app_screen.on_down_to_up_swipe()
            elif gesture == GestureDetectorThread.SWIPE_UP:
                self._current_app_screen.on_up_to_down_swipe()
            elif gesture == GestureDetectorThread.SWIPE_LEFT:
                self._current_app_screen.on_right_to_left_swipe()
            elif gesture == GestureDetectorThread.SWIPE_RIGHT:
                self._current_app_screen.on_left_to_right_swipe()
            elif gesture == GestureDetectorThread.THUMB_OK:
                self._current_app_screen.on_thumb_up()
            elif gesture == GestureDetectorThread.THUMB_NOT:
                self._current_app_screen.on_thumb_down()
            else:
                print("Gesture not recognized")

        # Update current app screen
        if self._current_app_screen:
            self._current_app_screen.draw(self._surface)
