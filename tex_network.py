#!/usr/bin/python

""" Find figs based on includegraphics in tex docs and prints the file names"""

import argparse
from termcolor import colored
import glob
import string
import numpy as np


def print_elements(lines, file, splitter, alphabetic=False):
    parts = lines.split(splitter)
    elements = []
    for p in parts[1:]:
        elements.append(p[1+p.find("{"): p.find("}")])
    if alphabetic:
        elements = sorted(elements, key=lambda s: s.lower())

    header = "Printing {} elements in {}:".format(splitter, file)
    print(colored(header, "red"))
    for f in elements:
        print(colored(f, "blue"))

parser = argparse.ArgumentParser(
    description="Print various quantities from .tex files")
parser.add_argument('file', help="The tex file(s) to use", nargs="*")
parser.add_argument("-f", "--figures", action="store_true",
                    help="Print the figure names in the file")
parser.add_argument("-l", "--labels", action="store_true",
                    help="Print the labels in the file")
parser.add_argument("-o", "--other", default=None,
                    help=("Print any arbitary latex element supplied after the"
                          " flag"))
parser.add_argument("-a", "--alphabetic", action="store_true",
                    help=("Print the results alphabetically"))
args = parser.parse_args()

# Getting the list of files and lines
files_list = []
lines_list = []
if len(args.file) == 0:
    # If no files supplied try and find some
    possible_files = glob.glob("*tex")
    for pf in possible_files:
        with open(pf) as f:
            lines = f.read()
        if "begin{document}" in lines:
            lines_list.append(lines)
            files_list.append(pf)
    if len(files_list) == 0:
        mssg = ("No files supplied and none found, are you in the right "
                "directory?")
        raise ValueError(colored(mssg, "red"))
else:
    for file in args.file:
        with open(file, "r") as f:
            lines_list.append(f.read())
            files_list.append(file)


def add_node(ax, x, y, text, s=0.2, color="r"):
    color = np.random.uniform(0, 1, 4)
    circle = plt.Circle((x, y), s, alpha=0.6, color=color)
    ax.add_artist(circle)
    ax.annotate(text, (x, y), size=8)
    return ax


def plot_level(ax, x, y, dx, children):
    n = len(children)
    n = n + n % 2  # Make it even
    yc = y - 1
    xcs = x + np.linspace(-dx/2., dx/2., n)
    xcs = xcs[np.argsort(np.abs(xcs))]  # Fill from center
    children_pos = []
    for xc, c in zip(xcs, children):
        ax = add_node(ax, xc, yc, c)
        children_pos.append((xc, yc))

    return ax, children, children_pos


def get_first_braces(text):
    return text[1+text.find("{"): text.find("}")]


sections = lines.split("\section")[1:]

sec_names = []
subsec_names = []
subsubsec_names = []

for i, sec in enumerate(sections):
    sec_names.append(get_first_braces(sec))
    subsections = sec.split("\subsection")
    for j, subsec in enumerate(subsections):
        subsec_names.append(get_first_braces(subsec))

        #subsubsections = subsec.split("\subsubsection")
        #for k, subsubsec in enumerate(subsubsections):
        #    subsubsec_key = get_first_braces(subsubsec)
        #    network[sec_key][subsec_key][subsubsec_key] = {}
        #    print "{}:{}:{}".format(sec_key, subsec_key, subsubsec_key)
        #    L = len(subsubsec.split(r"\ref"))
        #    network[sec_key][subsec_key][subsubsec_key] = L

print len(sec_names), len(subsec_names)

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x, y = 0, 0

file_name = files_list[0]
ax = add_node(ax, x, y, file_name)

SECTIONS = ["I", "II", "III", "IV", "V", "VI", "VII"]
SUBSECTIONS = list(string.ascii_uppercase)

ax, children, children_pos = plot_level(ax, x, y, 10, network.keys())
for c, cp in zip(children, children_pos):
    print cp
    ax, children, children_pos = plot_level(ax, cp[0], cp[1], 1, network[c].keys())

#n = len(network)
#y -= 1
#x = - 0.5*(n+1)
#for i, (sec_name, subsec) in enumerate(network.iteritems()):
#    sec_name = SECTIONS[i]
#    x += 1
#    ax = add_node(ax, x, y, file_name)
#    n = len(network)
#    y -= 1
#    x = - 0.5*(n+1)
#
#    for j, (subsec_name, subsubsec) in enumerate(subsec.iteritems()):
#        subsec_name = SUBSECTIONS[j]
#        parent_name = sec_name
    #    child_name = "{}:{}".format(sec_name, subsec_name)
    #    G.add_node(child_name)
    #    G.add_edge(parent_name, child_name)
    #    for k, (subsubsec_name, L) in enumerate(subsubsec.iteritems()):
    #        subsubsec_name = str(k)
    #        grandparent_name = sec_name
    #        parent_name = child_name
    #        child_name = "{}:{}:{}".format(grandparent_name, parent_name, subsubsec_name)
    #        G.add_node(child_name)
    #        G.add_edge(parent_name, child_name)

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
plt.show()

