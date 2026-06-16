# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Find Circles Example
#
# This example shows off how to find circles in the image using the Hough
# Transform. https://en.wikipedia.org/wiki/Circle_Hough_Transform
#
# Note that the find_circles() method will only find circles which are completely
# inside of the image. Circles which go outside of the image/roi are ignored...
#
# Changed: Add pixel extraction and corresponding number processing

import sensor
import time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time=2000)
clock = time.clock()


# get number corresponding to r, g, b
def my_number(r_brightness, g_brightness, b_brightness):
    # threshold for False/ True
    r_threshold = 80
    g_threshold = 60
    b_threshold = 100
    # initialize color channels
    r = False
    g = False
    b = False
    number = -99  # illegal number
    # compare r, g, b to threshold
    if r_brightness > r_threshold:
        r = True
    if g_brightness > g_threshold:
        g = True
    if b_brightness > b_threshold:
        b = True
    # find color and number
    if (not r) and (not g) and (not b):
        # print("black ring")
        number = -2
    elif r and (not g) and (not b):
        # print("red ring")
        number = -1
    elif r and g and (not b):
        # print("yellow ring")
        number = 0
    elif (not r) and g and (not b):
        # print("green ring")
        number = 1
    elif (not r) and g and b:
        # print("cyan ring")
        number = 2
    else:
        print("unknown color")
    print(number)
    # return
    return number


# Loop
while True:
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)

    # Circle objects have four values: x, y, r (radius), and magnitude. The
    # magnitude is the strength of the detection of the circle. Higher is
    # better...

    # `threshold` controls how many circles are found. Increase its value
    # to decrease the number of circles detected...

    # `x_margin`, `y_margin`, and `r_margin` control the merging of similar
    # circles in the x, y, and r (radius) directions.

    # r_min, r_max, and r_step control what radiuses of circles are tested.
    # Shrinking the number of tested circle radiuses yields a big performance boost.

    for c in img.find_circles(
        threshold=5000,
        x_margin=10,
        y_margin=10,
        r_margin=10,
        r_min=2,
        r_max=60,
        r_step=2,
    ):
        img.draw_circle(c.x(), c.y(), c.r(), color=(255, 0, 0))
        print(c)
        # print("min =", c.y() - c.r())
        # print("max =", c.y() + c.r())
        ring_width = c.r()/10
        distance = [0, int(3*ring_width), int(5*ring_width), int(7*ring_width), int(9*ring_width)]
        my_sum = 0
        for i in range(5):
            y_coord = c.y() + distance[i]
            print("y_coord =", y_coord)
            r, g, b = img.get_pixel(c.x(), y_coord)
            print(r, g, b)
            my_sum += my_number(r, g, b)
        print("my_sum =", my_sum)

    print("FPS %f" % clock.fps())
