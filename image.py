#!/usr/bin/env python

# Referenced code from hzeller rpi-rgb-led-matrix python examples: https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
# Referenced code from alexlib split_image_4_quarters.py: https://gist.github.com/alexlib/ef7df7bfdb3dba1698f4

import sys
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)

