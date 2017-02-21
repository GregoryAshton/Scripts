#! /home/gregory.ashton/anaconda2/bin/python

import sys

files = sys.argv[1:]

CPU_hours = []
for file in files:
    with open(file, 'r') as f:
        for line in f:
            if 'Total Remote Usage' in line:
                string = line.lstrip(' ').split(' ')[2].rstrip(',')
                h, m , s = [float(u) for u in string.split(':')]
                CPU_hours.append(h + m/60. + s/(60.**2))

print('\nCPU hours summary')
print('  Total: {}'.format(sum(CPU_hours)))
print('  Shortest: {}'.format(min(CPU_hours)))
print('  Longest: {}'.format(max(CPU_hours)))
print('')

try:
    from bashplotlib.histogram import plot_hist
    plot_hist(CPU_hours, bincount=50, xlab=True)
except IOError:
    pass

