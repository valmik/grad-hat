#!/usr/bin/env python

# Referenced code from hzeller rpi-rgb-led-matrix python examples: https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
# Referenced code from alexlib split_image_4_quarters.py: https://gist.github.com/alexlib/ef7df7bfdb3dba1698f4

import sys
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

def crop(im,height,width):
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            # print (i,j)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def main():
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

    imgwidth, imgheight = image.size
    height = imgheight/2
    width = imgwidth/2
    startnum = 0

    for k, piece in enumerate(crop(image, height, width), startnum):

        img = Image.new('L', (width, height), 255)
        img.paste(piece)

        img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

        matrix.SetImage(img.convert('RGB'))
        time.sleep(1)

    try:
        print("Press CTRL-C to stop")
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        sys.exit(0)




if __name__ == '__main__':
    main()


