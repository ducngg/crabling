import time
import numpy as np

# Deer
HUOU = "huou"

# Gourd
BAU = "bau"

# Rooster
GA = "ga"

# Fish
CA = "ca"

# Crab
CUA = "cua"

# Shrimp
TOM = "tom"

CELLS = [HUOU, BAU, GA, CA, CUA, TOM]
def cell_mapper(a):
    '''
    Maps from index([0, 5]) to string and vice versa.
    '''
    if a == HUOU:
        return 0
    if a == BAU:
        return 1
    if a == GA:
        return 2
    if a == CA:
        return 3
    if a == CUA:
        return 4
    if a == TOM:
        return 5
    if a == 0:
        return HUOU
    if a == 1:
        return BAU
    if a == 2:
        return GA
    if a == 3:
        return CA
    if a == 4:
        return CUA
    if a == 5:
        return TOM
    return None

def emoji_mapper(a):
    if a == 0:
        return '🦌'
    if a == 1:
        return '🧉'
    if a == 2:
        return '🐓'
    if a == 3:
        return '🐟'
    if a == 4:
        return '🦀'
    if a == 5:
        return '🍤'
    return None