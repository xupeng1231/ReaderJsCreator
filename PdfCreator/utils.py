import random

class RPools:
    sample_num_pool = [1]*10 + [2]*40 + [3]*40 + [4]*10
    output_numpage_pool = [2]*10 + [3]*15 + [4]*20 + [5]*25 + [6]*15 + [7]*10 + [8]*5

class R:
    def select(arr):
        assert isinstance(arr,list)
        return random.choice(arr)
    select = staticmethod(select)

    def percent(division):
        return random.randint(0, 99) < division
    percent = staticmethod(percent)
