#!/usr/bin/python

""" Find figs based on includegraphics in tex docs and prints the file names"""

import argparse
from termcolor import colored
import glob
import string


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

def get_first_braces(text):
    return text[1+text.find("{"): text.find("}")]

network = {}
sections = lines.split("\section")[1:]


for sec in sections:
    sec_key = get_first_braces(sec)
    network[sec_key] = {}
    subsections = sec.split("\subsection")
    for subsec in subsections:
        subsec_key = get_first_braces(subsec)
        network[sec_key][subsec_key] = {}
        subsubsections = subsec.split("\subsubsection")
        for subsubsec in subsubsections:
            subsubsec_key = get_first_braces(subsubsec)
            network[sec_key][subsec_key][subsubsec_key] = {}
            print "{}:{}:{}".format(sec_key, subsec_key, subsubsec_key)
            L = len(subsubsec.split(r"\ref"))
            network[sec_key][subsec_key][subsubsec_key] = L

import matplotlib.pyplot as plt
import networkx as nx

file_name = files_list[0]
G = nx.DiGraph()
G.add_node(file_name)

SECTIONS = ["I", "II", "III", "IV", "V", "VI", "VII"]
SUBSECTIONS = list(string.ascii_uppercase)

for i, (sec_name, subsec) in enumerate(network.iteritems()):
    sec_name = SECTIONS[i]
    G.add_node(sec_name)
    G.add_edge(file_name, sec_name)
    for j, (subsec_name, subsubsec) in enumerate(subsec.iteritems()):
        subsec_name = SUBSECTIONS[j]
        parent_name = sec_name
        child_name = "{}:{}".format(sec_name, subsec_name)
        G.add_node(child_name)
        G.add_edge(parent_name, child_name)
        for k, (subsubsec_name, L) in enumerate(subsubsec.iteritems()):
            subsubsec_name = str(k)
            grandparent_name = sec_name
            parent_name = child_name
            child_name = "{}:{}:{}".format(grandparent_name, parent_name, subsubsec_name)
            G.add_node(child_name)
            G.add_edge(parent_name, child_name)


#nx.write_dot(G, 'test.dot')
pos = nx.graphviz_layout(G, prog='dot')
nx.draw(G,pos, with_labels=True, arrows=True)

plt.show()

