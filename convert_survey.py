#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:        practice_plotting
# Purpose:     converts fsdb plotting data into an intermediary format 
#
# Author:      andy
#
# Created:     10/10/2014
#-------------------------------------------------------------------------------
import sys, argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--help", help="Sample input and output", action='store_true')
args = parser.parse_args()

if args.help:
    print "To execute the conversion script, input is the output from print_datafile, filtered through icmp converter."
    print "I use command line argument ./print_datafile it.29.pinger.bz2 | python blocklog_conversion_icmp.py | python convert_survey.py"
    print "Sample input: #fsdb -F t time_since_epoch\tblock\treply_type\t"
    print "Sample output: #fsdb -F t y_offset start duration color"
    sys.exit()

# sets for identifying plottable blocks and hex start of the graph
res = []
block = {}
min_hex = 10000000000000000000

COLORS = {
    '0' : "0000ff",
    '1' : "666666",
    '2' : "008000",
    '3' : "800000"
}
# #0000ff: Blue, shows implied values for non-probing
# #000000: Black, shows ground truth for non-response
# #666666: Gray, shows implied value for non-response
# #008000: Dark Green, shows implied value for echo reply


print ("#fsdb -F t time_since_epoch\tblock\treply_type\t")
for line in sys.stdin:
    line = line.rstrip()
    if line.startswith('#'):
        continue
    if line == "":
        continue

    f = line.strip().split('\t')

    if int(f[1],16) < min_hex:
        min_hex = int(f[1],16)

    f[2] = COLORS[f[2]]

    if f[1] in block.keys():
        block[f[1]].append((f[0], f[2]))
    else:
        block[f[1]] = [(f[0], f[2])]

min_hex = hex(min_hex)
print min_hex
for i in block.keys():
    # plots distance from top of graph
    finalblock = str(int(i,16) - int(min_hex,16))

    # plots status, color
    for (count, returnval) in enumerate(block[i]):
        seq = (finalblock, returnval[0], '1', returnval[1])
        print "\t".join(seq)





