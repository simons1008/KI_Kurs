# Dataset Capture Script - By: marti - Fri Nov 6 2026

# Use this script to control how your OpenMV Cam captures images for your
# dataset. You should apply the same image pre-processing steps you expect
# to run on images that you will feed to your model during run-time.

import csi
import time

csi0 = csi.CSI()
csi0.reset()
csi0.pixformat(csi.GRAYSCALE)  # Modify as you like.
csi0.framesize(csi.QVGA)  # Modify as you like.
csi0.window((240, 240))
csi0.vflip(True)
csi0.hmirror(True)
csi0.snapshot(time=2000)

clock = time.clock()

while True:
    clock.tick()
    img = csi0.snapshot()
    # print("\x1b[64OMV")  # trigger Dataset Editor
    # time.sleep(1)
    print(clock.fps())
