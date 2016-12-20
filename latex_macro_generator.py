""" Module to provide tools in writing latex macros """

import os


def write_to_macro(label, value, macro_file):
    if os.path.isfile(macro_file):
        macro_dict = _read_macro_file_to_dict(macro_file)
    else:
        macro_dict = dict()

    print macro_dict

    macro_label = _get_macro_label(label)
    macro_dict[macro_label] = value
    _write_dict_to_macro_file(macro_dict, macro_file)


def _read_macro_file_to_dict(macro_file):
    macro_dict = dict()
    with open(macro_file, 'r') as f:
        for line in f:
            left, right = line.split('{')
            key = left.replace('\\def\\', '')
            value = right.replace('}\n', '')
            macro_dict[key] = value
    return macro_dict


def _get_macro_label(label):
    return label.replace('_', '').replace('-', '')


def _write_dict_to_macro_file(macro_dict, macro_file):
    with open(macro_file, 'w+') as f:
        for key, val in macro_dict.iteritems():
            line = '\\def\\{}{{{}}}\n'.format(key, val)
            f.write(line)
