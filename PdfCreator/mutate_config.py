import random
from PyPDF2.generic import DictionaryObject, FloatObject, NumberObject, TextStringObject, ByteStringObject, NameObject
from PyPDF2.rutils import RPools

class MutateCls:
    Mutate_cls = (DictionaryObject, FloatObject, NumberObject, TextStringObject, ByteStringObject, NameObject)
    Cls_mutate_ratio={
        DictionaryObject: lambda :random.choice(RPools.DictionaryObject_mutate_freq_per10k_pool)/10000.,
        FloatObject: lambda :random.choice(RPools.FloatObject_mutate_freq_per10k_pool)/10000.,
        NumberObject: lambda : random.choice(RPools.int_mutate_freq_per10k_pool)/10000.,
        TextStringObject: lambda : random.choice(RPools.str_mutate_freq_per10k_pool)/10000.,
        ByteStringObject: lambda : random.choice(RPools.unicode_mutate_freq_per10k_pool)/10000.,
        NameObject: lambda: random.choice(RPools.unicode_mutate_freq_per10k_pool) / 10000.,
    }
