import sys
import random

class RPools:
    sample_num_pool = [1]*10 + [2]*40 + [3]*40 + [4]*10
    output_numpage_pool = [2]*10 + [3]*15 + [4]*20 + [5]*25 + [6]*15 + [7]*10 + [8]*5
    DictionaryObject_mutate_freq_per10k_pool = \
        [30]*2 + [60]*4 + [120]*8 + [180]*16 + [240]*20 + [270]*25 + [300]*15 + [330]*10  # mutate n in every 10000 objects
    FloatObject_mutate_freq_per10k_pool = \
        [100]*2 + [200]*4 + [400]*8 + [600]*16 + [800]*20 + [900]*25 + [1000]*15 + [1100]*10  # mutate n in every 10000 objects
    int_mutate_freq_per10k_pool = \
        [100]*2 + [200]*4 + [400]*8 + [600]*16 + [800]*20 + [900]*25 + [1000]*15 + [1100]*10 # mutate n in every 10000 objects
    str_mutate_freq_per10k_pool = \
        [10]*2 + [20]*4 + [40]*8 + [60]*16 + [80]*20 + [90]*25 + [100]*15 + [110]*10  # mutate n in every 10000 objects
    unicode_mutate_freq_per10k_pool = \
        [10]*2 + [20]*4 + [40]*8 + [60]*16 + [80]*20 + [90]*25 + [100]*15 + [110]*10  # mutate n in every 10000 objects
    object_mutate_freq_per10k_pool = [100]  # mutate n in every 10000 objects


class R:
    def select(arr):
        assert isinstance(arr,list)
        return random.choice(arr)
    select = staticmethod(select)

    def percent(division):
        return random.randint(0, 99) < division
    percent = staticmethod(percent)

    def ratio(ratio):
        return random.randint(0, 9999) < ratio*10000
    ratio=staticmethod(ratio)
