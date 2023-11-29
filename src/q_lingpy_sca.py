import sys
import lingpy

""" Convert phones from TIMIT IPA set into List (2012)'s
    Sound Class model set (28 possible classes) using Lingpy
    Print output
"""

map_file = sys.argv[1]
# map_file = 'data/notes/timit-ipa-map.txt'
# map_file = 'data/panara/dict_panara_phone_narrow.txt'

with open(map_file, 'r') as f:
    phones = [line.split()[1].strip() for line in f.readlines()]

for phone in phones:
    try:
        print(lingpy.sequence.sound_classes.tokens2class([phone], 'sca')[0])

    except:
        print(f'uhoh: {phone}')
