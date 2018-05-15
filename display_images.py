#!/usr/bin/env python

# image.py is the test script. This is the running script

# Referenced code from hzeller rpi-rgb-led-matrix python examples: https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
# Referenced code from alexlib split_image_4_quarters.py: https://gist.github.com/alexlib/ef7df7bfdb3dba1698f4
# Referenced DTing's answer at: https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


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

def display_image_to_matrix(image, matrix):
    imgwidth, imgheight = image.size
    height = imgheight/2
    width = imgwidth/2
    startnum = 0

    long_img = Image.new('RGB', (width*4, height))
    x_offset = 0;
    for k, piece in enumerate(crop(image, height, width), startnum):
        long_img.paste(piece, (x_offset, 0))
        x_offset += piece.size[0]

    long_img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    matrix.SetImage(long_img.convert('RGB'))


def main():

    if len(sys.argv) < 2:
        sys.exit("require an image argument")
    else:
        image_set = sys.argv[1]

    sets = {"broccoli_test": ["broccoli.png", "broccoli_black.png"],
        "snorunt": 8,
        "fireworks": 23,
        "uc_broccoli": ["uc.png", "uc.png", "uc.png", "broccoli.png", "broccoli.png", "broccoli.png"]}

    image_path = "images/"

    if isinstance(sets[image_set], (int, long)):
        slides = []
        for i in range(sets[image_set]):
            slides.append(str(i) + ".gif")
    else:
        slides = sets[image_set]

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 32
    options.chain_length = 4
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    try:
        print("Press CTRL-C to stop")
        index = 0
        while True:
            if index == len(slides):
                index = 0
            print index
            image_file = image_path + image_set + '/' + slides[index]
            image = Image.open(image_file)
            display_image_to_matrix(image, matrix)
            index = index + 1
            time.sleep(0.1)

    except KeyboardInterrupt:
        sys.exit(0)



if __name__ == '__main__':
    main()





