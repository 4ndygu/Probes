#!/usr/bin/evn python

"""Copyright (C) <2015> Andy Gu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>"""

#-------------------------------------------------------------------------------
# Name:        practice_plotting
# Purpose:     Plots a /24 block
#
# Author:      andy
#
# Created:     10/10/2014
#-------------------------------------------------------------------------------


import sys, os, argparse, time
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--output", help="Chooses directory to save images", default='sample.images')
parser.add_argument("--format", help="Selects the file format for image.", default="pdf")
parser.add_argument("--help", help="Sample input and output", action='store_true')
parser.add_argument("--start", help="Set left bound of graph", default = "0")
parser.add_argument("--end", help="Set right bound of graph", default = "1000000000000000")
parser.add_argument("--name", help="Set the name of the document", default = "multiblock")
parser.add_argument("--height", help="Set the height of the figure", default = "5")
args = parser.parse_args()

if args.help:
    print "To execute the plotting script, use python block_plotting_dumb.py < exc11.txt with appropriate flags."
    print "Sample input is in the form of\n\
    #fsdb -F t y_offset start duration color\n\
	3416    1409131981      5280    000D4C\n\
	3417    1409131919      5280    000D4D\n\
	3418    1409131877      5280    000D4E\n\
	3419    1409131960      5280    000D4F\n\
	3420    1409132107      5280    000D50\n\
    ...\n\
	Where y_offset denotes position from top of graph, start the start of the outage, duration the duration, and color the hex color of each block."
    print "Sample input can be found at /ANT_SVN/trunk/lander_code/outage_detection/strip_charts/tw_outage_binsize_2hr_block_color_format.fsdb"
    print "Sample output can be found at /ANT_SVN/trunk/lander_code/outage_detection/strip_charts/practice_plotting/multiblock.pdf"
    print "Command line options:"
    print " --output: selects the directory to save images"
    print " --format: selects the file format for saved images"
    print " --start and --end: sets the left and right bounds of the graph in terms of UTC time. Default doesn't limit."
    print " --name: sets the name of the file"
    print " --height: sets the height of the figure in inches"
    print "Sample output for bounded graph can be foundat /ANT_SVN/trunk/lander_code/outage_detection/strip_charts/multiblock_bounded.pdf"
    sys.exit()

if not os.path.exists(args.output):
    os.makedirs(args.output)
    os.chdir(args.output)
else:
    os.chdir(args.output)

FIGLENGTH = 11
FIGHEIGHT = int(args.height)
DOTPERINCH = 100

block = []
temp = {}
fig = plt.figure(num=None, figsize=(FIGLENGTH, FIGHEIGHT), dpi=DOTPERINCH)
plt.ioff()
rect = fig.add_subplot(111)
nrows = 0

min_time = 1000000000000000
max_time = 0

for line in sys.stdin:
    # Checks for FSDB format
    if line.startswith("#"):
	    continue;
    line = line.strip()

    if (line == ""):
      continue
    tmp = line.split('\t')

    if len(tmp) != 4:
	print str(tmp) + " isn't valid"
	continue

    if int(tmp[1]) < int(args.start):
        continue
    if int(tmp[1]) > int(args.end):
        continue

    # Measures min/max time, series of plots at each y-axis point
    # Most of the time, there should be only one line / y-axis point
    if int(tmp[1]) < min_time:
           min_time = int(tmp[1])
    elif int(tmp[2]) + int(tmp[1]) > max_time:
           max_time = int(tmp[2]) + int(tmp[1])

    if int(tmp[0]) > nrows:
    	nrows = int(tmp[0])

    #grabs everything
    block.append( (tmp[0], tmp[1], tmp[2], tmp[3]) )
    temp[tmp[0]] = 1


print "min time: %s" % min_time
print "max time: %s" % max_time

# reorders everything by their y_offset
file_name = args.name

ncols = max_time - min_time
rect_start = 0
length = 0

# setting the background
r1 = ptch.Rectangle((0,0), ncols, nrows, color="#e0e0ff", fill=True)
rect.add_patch(r1)

RECT_HEIGHT = 1

# This goes through the file, counting rectangles to find differences and plot
# Across widths
for items in block:
    rect_y = float(items[0])
    rect_x = int(items[1])
    rect_w = float(items[2])
    #determines facecolor of rectangle
    fc = "#" + str(items[3])

    r1 = ptch.Rectangle((rect_x, rect_y), rect_w, RECT_HEIGHT,
        facecolor=fc, linewidth=0, edgecolor="None", antialiased=False)
    rect.add_patch(r1)

# layout
plt.ylim([0, nrows])

# Inverts axis, sets title
plt.gca().invert_yaxis()
plt.tick_params(axis='y', right='off', direction='out')
plt.xlabel('Time (UTC Time)')
plt.ylabel('Blocks')
plt.tight_layout()

# Sets time ticks for measurement
if int(args.start) != 0:
    min_time = int(args.start)
if int(args.end) != 1000000000000000:
    max_time = int(args.end)
rect.set_xlim(min_time, max_time)

xaxisbotlabel = [time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(float(x)))[:-1] for x in np.arange(min_time, max_time, (max_time - min_time) / 10)]

rect.set_xticks(np.arange(min_time, max_time, (max_time - min_time) / 10))
rect.set_xticklabels(xaxisbotlabel, rotation=50, ha="right")

xaxistoplabel = [int(x / 660) for x in np.arange(0, max_time - min_time, (max_time - min_time) / 10)]

rect2 = rect.twiny()
rect2.set_xticks(np.arange(min_time, max_time, (max_time - min_time) / 10))
rect2.set_xticklabels(xaxistoplabel)
rect2.set_xlabel('Time (11-minute rounds)')

rect2.xaxis.tick_top()
rect2.tick_params(axis='x', which='both', labelsize=8, direction='out')
rect2.set_xlim(min_time, max_time)

#Saving with help of the flags
file_name += "." + args.format
plt.savefig(file_name, bbox_inches='tight', transparent=True)
print "Generated image " + file_name

plt.close()


