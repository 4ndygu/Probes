#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:        practice_plotting
# Purpose:     converts fsdb plotting data into an intermediary format 
#
# Author:      andy
#
# Created:     10/10/2014
#-------------------------------------------------------------------------------

import sys, os, argparse, collections, time
import numpy as np

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--help", help="Sample input and output", action='store_true')
args = parser.parse_args()

if args.help:
    print "To execute the plotting script, use python practice_plotting_adaptive.py < exc11.txt with appropriate flags."
    print "Sample input is in the form of\n\
    Seconds since epoch   hexip   response\n\
    1412162225  be15a404        1\n\
    1412162225  be15a4c4        1\n\
    1412162225  be15a444        1\n\
    ...\n\
        See Blocklog_convert.py and blocklog_convert_icmp.py for info on converting to the intermediate format."
    print "Sample output: #fsdb -F t y_offset start duration color"
    sys.exit()

block = {}

# magic numbers for finding max time, min time, starting hex for plotting 
min_time = 100000000000000000000
max_time = 0
min_hex = 1000000000000000000000000000

lines = sys.stdin.read().splitlines()
if lines:
        for line in lines:
            if line.startswith("#"):
                    continue;
            line = line.strip()

            if (line == ""):
              continue
            tmp = line.split('\t')

            if int(tmp[0]) > max_time:
                max_time = int(tmp[0])
            if int(tmp[0]) < min_time:
                min_time = int(tmp[0])

            if int(tmp[1],16) < min_hex:
                min_hex = int(tmp[1],16)
            if tmp[1] in block.keys():
                block[tmp[1]].append((tmp[0], tmp[2]))
            else:
                block[tmp[1]] = [(tmp[0], tmp[2])]

y_offset = 0
min_hex = hex(min_hex)
print "#fsdb -F t y_offset start duration color"
RETURNVAL2COLOR1COLOR2 = {
    0 : "0000ff",
    1 : "666666",
    2 : "008000",
    3 : "800000"
}
# #add836: Light blue, shows ground truth for non-probing
# #0000ff: Blue, shows implied values for non-probing
# #000000: Black, shows ground truth for non-response
# #666666: Gray, shows implied value for non-response
# #00ff00: Light Green, shows ground truth for echo reply
# #008000: Dark Green, shows implied value for echo reply
# #0f4797: Red, shows ground truth for error
# #ff0000: Red, shows implied value for error

#repeatedly pulls /24 blocks and plots them as according to old iterations
for i in block.keys():
    hexval = int(i, 16) - int(min_hex, 16)

    for (count, returnval) in enumerate(block[i]):
        finalcolor = RETURNVAL2COLOR1COLOR2[int(returnval[1])]

        if len(block[i]) - count  == 1:
            length = max_time - int(returnval[0])
        else:
            length = int(block[i][count + 1][0]) - int(returnval[0])

        printline = [hexval, returnval[0], length, finalcolor]
        printline = [str(f) for f in printline]
        print "\t".join(printline)
                                                                                                                        92,1          Bot


