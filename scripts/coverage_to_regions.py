#!/usr/bin/env python
from __future__ import print_function, division
import sys

if len(sys.argv) < 3:
    print("usage: <bamtools_coverage_output {} fasta_index num_regions >regions.bed".format(sys.argv[0]))
    print("Generates regions with even sequencing coverage, provided an input of coverage per-position as")
    print("generated by bamtools coverage.  In other words, generates regions such that the integral of")
    print("coverage is approximately equal for each.  These can be used when variant calling to reduce")
    print("variance in job runtime.")
    exit(1)

lengths = {}
fai = open(sys.argv[1])
for line in fai.readlines():
    c, l = line.split("\t")[:2]
    lengths[c] = int(l)

positions = []
total_coverage = 0
for line in sys.stdin:
    chrom, pos, depth = line.strip().split("\t")
    pos = int(pos)
    depth = int(depth)
    positions.append([chrom, pos, depth])
    total_coverage += depth

bp_per_region = total_coverage / int(sys.argv[2])

lchrom = None
lpos = 0
bp_in_region = 0

for line in positions:
    chrom, pos, depth = line #line.strip().split("\t")
    if lchrom != chrom:
        if lchrom:
            print(lchrom+":"+str(lpos)+"-"+str(lengths[lchrom]))
            lpos = 0
            lchrom = chrom
            bp_in_region = 0
        else:
            lchrom = chrom
    bp_in_region += depth
    if bp_in_region > bp_per_region:
        print(chrom+":"+str(lpos)+"-"+str(pos)) #, pos - lpos
        lpos = pos
        bp_in_region = 0

print(lchrom+":"+str(lpos)+"-"+str(lengths[lchrom]))
