import sys
from fermipy import utils
utils.init_matplotlib_backend()
from fermipy.gtanalysis import *
from fermipy.roi_model import *
from fermipy.config import *
from fermipy.utils import *
import yaml
import pprint
from fermipy.logger import *
import numpy

from fermipy.gtanalysis import GTAnalysis

novaname = sys.argv[1] #'V679Car'

gta = GTAnalysis(sys.argv[2])

gta.setup()
gta.optimize()

loc = gta.localize(novaname, free_radius=1.0, update=True)

lc = gta.lightcurve(novaname, binsz=86400.*28.0, free_radius=3.0, use_scaled_srcmap=True)
