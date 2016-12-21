""" Module to provide tools in writing latex macros """

import os
import numpy as np


def write_to_macro(label, value, macro_file, d=2, sn=1000):
    if os.path.isfile(macro_file):
        macro_dict = _read_macro_file_to_dict(macro_file)
    else:
        macro_dict = dict()

    macro_label = _get_macro_label(label)
    if type(value) == str:
        macro_dict[macro_label] = value
    else:
        macro_dict[macro_label] = _texify_float(value, d, sn)
    _write_dict_to_macro_file(macro_dict, macro_file)


def _read_macro_file_to_dict(macro_file):
    macro_dict = dict()
    with open(macro_file, 'r') as f:
        for line in f:
            idx = line.index('{')
            left = line[:idx]
            right = line[idx+1:]
            key = left.replace('\\def\\', '')
            value = right.replace('}\n', '')
            macro_dict[key] = value
    return macro_dict


def _get_macro_label(label):
    for i in range(10):
        label = label.replace(str(i), _convert_number_to_letters(i))
    label = label.replace('_', '').replace('-', '')
    return label


def _write_dict_to_macro_file(macro_dict, macro_file):
    with open(macro_file, 'w+') as f:
        for key in sorted(macro_dict.keys()):
            line = '\\def\\{}{{{}}}\n'.format(key, macro_dict[key])
            f.write(line)


def _round_to_n(x, n):
    if not x:
        return 0
    power = -int(np.floor(np.log10(abs(x)))) + (n - 1)
    factor = (10 ** power)
    return round(x * factor) / factor


def _texify_float(x, d=1, sn=100):
    if type(x) == str:
        return x
    x = _round_to_n(x, d)
    if 1./sn < abs(x) < sn:
        return str(x)
    else:
        power = int(np.floor(np.log10(abs(x))))
        stem = np.round(x / 10**power, d)
        if d == 1:
            stem = int(stem)
        return r'{}{{\times}}10^{{{}}}'.format(stem, power)


def _convert_number_to_letters(n):
    strings = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
               'eight', 'nine']
    return strings[n]
