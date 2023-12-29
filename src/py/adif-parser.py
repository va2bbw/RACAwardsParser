#!/bin/python3.10

import adif_io
import sys

from awards.canadaward    import Canadaward
from awards.ccca          import CCCA
#from awards.wana          import WANA
from awards.warac         import WARAC

from termcolor import colored

#print(sys.argv[1:])

qsos, header = adif_io.read_from_file(sys.argv[1])

canadaward = Canadaward(qsos)
ccca = CCCA(qsos)
warac = WARAC(qsos) 
#wana = WANA(qsos)



