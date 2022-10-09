import argparse
import math
import os
import statistics

import numpy
import numpy as np

from PIL import Image
import re

def getDivisors(n) :
    divisors = []
    i = 1
    while i <= n :
        if (n % i==0) :
            divisors.append(i)
        i = i + 1
    return divisors

# arguments
parser = argparse.ArgumentParser(description=".CUBE file to PNG")
parser.add_argument('path', type=str, help="Path to input .CUBE file")
parser.add_argument('name', default="", type=str, help="Optional. Name for the output png file, without the extension")
args = parser.parse_args()

# Input path validation
if not os.path.exists(args.path):
    raise Exception("Specified path for .cube file (" + args.path + ") does not exists.")
if not os.path.isfile(args.path):
    raise Exception("Specified path (" + args.path + ") is not a path to a file")

#Output name validation
if not args.name:
    args.name = "output"


cube_file = open(args.path,"r")

title = None
lut_size = None
min = [None,None,None]
max = [None,None,None]

content = cube_file.read()
content = content.strip()

#Title
title_re = re.search(r'TITLE \"(.*)\"', content)
if title_re:
    title = title_re.group(1)
if not title:
    title = "Untitled"

#LUT size
lut_size_re = re.search(r'LUT_3D_SIZE (\d+)', content)
if lut_size_re:
    lut_size = int(lut_size_re.group(1))

#Min
min_re = re.search(r'DOMAIN_MIN (\d+\.\d+ \d+\.\d+ \d+\.\d+)', content)
if min_re:
    min_re = min_re.group(1)
    min = [float(x) for x in min_re.split(" ")]

#Max
max_re = re.search(r'DOMAIN_MAX (\d+\.\d+ \d+\.\d+ \d+\.\d+)', content)
if max_re:
    max_re = max_re.group(1)
    max = [float(x) for x in max_re.split(" ")]


#Data
data_re = re.findall(r'^\d+\.\d+ \d+\.\d+ \d+\.\d+', content, re.MULTILINE) #Find all matches
data = [[float(y) for y in group] for group in [x.split(" ") for x in data_re]] # Convert to list and convert from str to float
data = [tuple(le) for le in data]
data = [tuple(x * 255 for x in group) for group in data]
data = [tuple(int(x) for x in group) for group in data]


quantity = len(data)
divisors = getDivisors(quantity)
if len(divisors) % 2 == 0:
    height = divisors[int((len(divisors)/2.0))-1]
    width = divisors[int((len(divisors)/2.0))]
else:
    height = divisors[int(math.floor(len(divisors)/2.0))]
    width = divisors[int(math.floor(len(divisors)/2.0))]
size = (int(width), int(height))

im = Image.new(size=size,mode="RGB")

c_data = 0
for r in range(0,int(height/lut_size)):
    for c in range (0,int(width/lut_size)):
        for y in range(0, lut_size):
            for x in range(0,lut_size):
                im.putpixel((x+c*lut_size,y+r*lut_size),data[c_data])
                c_data = c_data+1

#im.show() #For testing
im.save(args.name+".png")
print("File created successfully.")

