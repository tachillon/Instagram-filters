import os
import math
import numpy as np
import cv2
import json
import argparse

def parse_arguments():                                                                                                                                                                                                                                                
    parser = argparse.ArgumentParser(description='Apply Instagram like filters to your picture')
    parser.add_argument('--imgpath', type=str, default="./", help='path to input image')
    parser.add_argument('--filter',  type=str, default="./", help='filter to use')                                                                                                                                                                                                                  
    return parser.parse_args()  

def main():
    args = parse_arguments()
    image_path  = args.imgpath
    filterToUse = args.filter

    print()
    print('Entries summary')
    print("  > input image path: " + image_path)
    print("  > filter to use:    " + filterToUse)
    print() 

    filterList = ["Clarendon"]

    # Check entries
    if not os.path.isfile(image_path):
        print("Cannot find the input image {}".format(image_path))
        exit(-1)

    if filterToUse not in filterList:
        print("The filter you asked is not defined (yet)! :(")
        print("Filters available are the following:")
        print(filterList)
        exit(-1)

    # Load filter Look-Up Table (LUT)
    lutImage           = cv2.imread("/tmp/filters/" + filterToUse + ".jpeg")
    copyImage          = lutImage.copy()
    lutImageHeight     = lutImage.shape[0]
    lutImageWidth      = lutImage.shape[1]
    stride             = math.ceil(lutImageHeight/16)
    strideDividedByTwo = math.ceil(stride/2)
    lutDictionnary     = {}
    counter            = 0

    for y in range(0, lutImageHeight, stride):
        for x in range(0, lutImageWidth, stride):
            cv2.circle(copyImage, (y+strideDividedByTwo, x+strideDividedByTwo), 3, (0, 255, 0), -1)
            bgr = lutImage[y+strideDividedByTwo, x+strideDividedByTwo]
            lutDictionnary[counter] = (int(bgr[0]), int(bgr[1]), int(bgr[2]))
            counter = counter + 1
    with open("/tmp/lut_" + filterToUse + ".json", "w") as write_file:
        json.dump(lutDictionnary, write_file, indent=4)

    # Apply the Look-Up Table to the image
    image       = cv2.imread(image_path)
    imageHeight = image.shape[0]
    imageWidth  = image.shape[1]
    blank_image = np.zeros((imageHeight,imageWidth,3), np.uint8)

    for y in range(0, imageHeight):
        for x in range(0, imageWidth):
            b, g, r = image[y, x] 
            newB, newG, newR = lutDictionnary[b][0], lutDictionnary[g][1], lutDictionnary[r][2]
            blank_image[y, x] = [newB, newG, newR]

    cv2.imwrite("/tmp/" + filterToUse + ".jpg", blank_image)

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()