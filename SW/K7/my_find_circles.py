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
# Changes: function "my_number" gets number corresponding to ring color
#          "main" gets a pixel of every ring and adds the corresponding numbers

import csi
import time

csi0 = csi.CSI()
csi0.reset()
csi0.pixformat(csi.RGB565)  # grayscale is faster
csi0.framesize(csi.QQVGA)
csi0.vflip(True)  # Flips the image vertically
csi0.hmirror(True)  # Mirrors the image horizontally
csi0.snapshot(time=2000)

clock = time.clock()

# get number corresponding to r, g, b
def my_number(r_brightness, g_brightness, b_brightness):
    # threshold forFalse/ True
    r_threshold = 80
    g_threshold = 60
    b_threshold = 100
    # initialize color channels
    r_status = False
    g_status = False
    b_status = False
    number = -99  # illegal number
    # compare r, g, bto threshold
    if r_brightness > r_threshold:
        r_status = True
    if g_brightness > g_threshold:
        g_status = True
    if b_brightness > b_threshold:
        b_status = True
    # find colorand number
    if (not r_status) and (not g_status) and (not b_status):
        # print("black ring")
        number = -2
    elif r_status and (not g_status) and (not b_status):
        # print("red ring")
        number = -1
    elif r_status and g_status and (not b_status):
        # print("yellow ring")
        number = 0
    elif (not r_status) and g_status and (not b_status):
        # print("green ring")
        number = 1
    elif (not r_status) and g_status and b_status:
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
    img = csi0.snapshot().lens_corr(1.8)

    # Circle objects have fourvalues: x, y, r(radius), and magnitude. The
    # magnitude is the strength of the detection of the circle. Higheris
    # better...

    # `threshold` controls how many circles are found. Increase its value
    # to decrease the numberof circles detected...

    # `x_margin`, `y_margin`, and `r_margin` control the merging of similar
    # circles in the x, y, and r(radius) directions.

    # r_min, r_max, and r_step control what radiuses of circles are tested.
    # Shrinking the numberof tested circle radiuses yields a big performance boost.

    for c in img.find_circles(
        threshold=6000,
        x_margin=10,
        y_margin=10,
        r_margin=10,
        r_min=30,
        r_max=60,
        r_step=2,
    ):
        img.draw_circle(c, color=(255, 0, 0))
        # Centre x coordinate, in pixels. Integer. Index [0]
        # Centre y coordinate, in pixels. Integer. Index [1]
        # Radius, in pixels. Integer. Index [2]
        # Magnitude of the circle in Hough-space. Index [3]
        print("min =", c[1] - c[2])
        print("max =", c[1] + c[2])
        print(c)
        ring_half = c[2]/10
        distance = [0, int(3*ring_half), int(5*ring_half), int(7*ring_half), int(9*ring_half)]
        my_sum = 0
        for i in range(5):
            y_coord = c[1] + distance[i]
            print("y_coord =", y_coord)
            r_brightness, g_brightness, b_brightness = img.get_pixel([c[0], y_coord])
            # print(r_brightness, g_brightness, b_brightness)
            my_sum += my_number(r_brightness, g_brightness, b_brightness)
        print("my_sum =", my_sum)

    print("FPS %f" % clock.fps())
