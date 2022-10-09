import math
import os.path

from PIL import Image
import argparse

# arguments
parser = argparse.ArgumentParser(description="Image file to .CUBE file")
parser.add_argument('path', type=str, help="Path to input image")
parser.add_argument('name', default="", type=str, help="Optional. Name for the output CUBE file, without the extension")
args = parser.parse_args()


im = Image.open(args.path)

# Input path validation
if not os.path.exists(args.path):
    raise Exception("Specified path for image (" + args.path + ") does not exists.")
if not os.path.isfile(args.path):
    raise Exception("Specified path (" + args.path + ") is not a path to a file")
try:
    im.verify()
except:
    raise Exception("Specified path is is either: not an image, broken, or an unsupported file format")

#Output name validation
if not args.name:
    args.name = "output"


im = Image.open(args.path) # Must be opened again because of im.verify()

width = im.size[0]
height = im.size[1]
size = width * height

# CubicRoot(size)
lut_size = int(round(size ** (1.0 / 3.0)))

# Writing the file
lut_file = open(args.name + ".CUBE", "w")
lut_file.write('TITLE "Untitled" \n')
lut_file.write("LUT_3D_SIZE " + str(lut_size) + "\n")
lut_file.write("DOMAIN_MIN 0.0 0.0 0.0\n")
lut_file.write("DOMAIN_MAX 1.0 1.0 1.0\n")

for r in range(0,int(height/lut_size)):
    for c in range (0,int(width/lut_size)):
        for y in range(0, lut_size):
            for x in range(0,lut_size):
                pixel = im.getpixel((x+c*lut_size,y+r*lut_size))
                lut_file.write(str(pixel[0] / 255.0) + " " + str(pixel[1] / 255.0) + " " + str(pixel[2] / 255.0))
                if x != width - 1 or y != height - 1:
                    lut_file.write("\n")
print("File created successfully.")