# Edge Impulse - OpenMV Image Classification Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
import csi
import time
import ml

csi0 = csi.CSI()
csi0.reset()
csi0.pixformat(csi.GRAYSCALE)
csi0.framesize(csi.QVGA)
csi0.window((240, 240))
csi0.vflip(True)
csi0.hmirror(True)
csi0.snapshot(time=2000)

# Load the model from internal Flash by setting MODEL_FROM_ROMFS to true. This allows running larger
# models directly from internal Flash without the need to copy from SD Card to internal RAM
# More info: https://docs.openmv.io/v5.0.0/openmvcam/tutorial/ml/ml-module/romfs.html
MODEL_FROM_ROMFS = False

if MODEL_FROM_ROMFS:
    model = ml.Model("/rom/ei-model.tflite")
    labels = model.labels
else:
    model = ml.Model('ei-float32-model.lite', load_to_fb=True)
    labels = [line.rstrip('\n') for line in open("ei-model.txt")]

print(model)

clock = time.clock()
while True:
    clock.tick()
    img = csi0.snapshot()

    # This combines the labels and confidence values into a list of tuples
    # and then sorts that list by the confidence values.
    scores = sorted(
        zip(labels, model.predict([img])[0].flatten().tolist()),
        key=lambda x: x[1],
        reverse=True
    )

    print(clock.fps(), "fps\t", "%s = %f\t" % (scores[0][0], scores[0][1]))
