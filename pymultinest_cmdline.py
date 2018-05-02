#!/home/user1/anaconda2/bin/python

import pymultinest
import sys
import corner
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('AGG')

n_params = sys.argv[1]
outputfiles_basename = sys.argv[2]
a = pymultinest.analyse.Analyzer(n_params, outputfiles_basename)

fig = corner.corner(a.get_equal_weighted_posterior())
plt.tight_layout()
plt.savefig('test')
