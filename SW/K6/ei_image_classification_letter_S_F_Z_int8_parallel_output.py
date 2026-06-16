# Edge Impulse - OpenMV Image Classification Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
# Changed: use parallel output

import sensor
import time
import ml
import uos
import gc
from machine import LED, Pin

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.set_vflip(True)                 # Flips the image vertically
sensor.set_hmirror(True)               # Mirrors the image horizontally
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = None
labels = None

# image classification threshold
threshold = 0.5
# snapshot counter
counter = 0
# alive LED
led = LED("LED_BLUE")
# Digital Output Initialization
p0 = Pin("P0", Pin.OUT)
p1 = Pin("P1", Pin.OUT)

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = ml.Model("trained_letter_S_F_Z_int8.tflite",
                   load_to_fb=uos.stat('trained_letter_S_F_Z_int8.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained_letter_S_F_Z_int8.tflite",\
                    did you copy the .tflite and labels_letter_S_F_Z.txt\
                    file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels_letter_S_F_Z.txt")]
except Exception as e:
    raise Exception('Failed to load "labels_letter_S_F_Z.txt",\
                    did you copy the .tflite and labels_letter_S_F_Z.txt\
                    file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()
led.on()

while (True):
    clock.tick()
    counter += 1

    img = sensor.snapshot()

    predictions_list = list(zip(labels, net.predict([img])[0].flatten().tolist()))

    for i in range(len(predictions_list)):
        # print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

        if predictions_list[i][1] > threshold and (counter % 10) == 0:
            label = predictions_list[i][0]
            print(label + " " + str(counter) + " ")
            # encode label
            if label == "letter_S":
                p0.off()
                p1.off()
            elif label == "letter_F":
                p0.on()
                p1.off()
            elif label == "letter_Z":
                p0.off()
                p1.on()
            elif label == "unknown":
                p0.on()
                p1.on()
            else:
                print("label error")

    # print(clock.fps(), "fps")
