import sys
from fermipy import utils
utils.init_matplotlib_backend()
from fermipy.gtanalysis import GTAnalysis
from fermipy.utils import *
import yaml
import pprint
import numpy
import argparse

from fermipy.gtanalysis import GTAnalysis

def main():
        
    usage = "usage: %(prog)s [config file]"
    description = "Run fermipy analysis chain."
    parser = argparse.ArgumentParser(usage=usage,description=description)

    parser.add_argument('--config', default = 'sample_config.yaml')
    parser.add_argument('--source', default = None)

    args = parser.parse_args()
    gta = GTAnalysis(args.config)

    if args.source is None:
        src_name = gta.roi.sources[0].name
    
    gta.setup()
    gta.optimize()

    loc = gta.localize(src_name, free_radius=1.0, update=True, make_plots=True)

    model = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
    srcs = gta.find_sources(model=model, sqrt_ts_threshold=5.0,
                            min_separation=0.5)
    
    sed = gta.sed(src_name, free_radius=1.0, make_plots=True)
    gta.tsmap(make_plots=True)
    gta.write_roi('fit0')
    # make sure bins are shifted to line up with the end of the time window (where the neutrino arrived)    
    tmax = 528835414
    LCbins = tmax-119*28*24*3600 + numpy.linspace(0,119,120)*28*24*3600
    lc = gta.lightcurve(src_name, time_bins=list(LCbins), free_radius=3.0, use_scaled_srcmap=True,
                        multithread=False, shape_ts_threshold=100)



if __name__ == "__main__":
    main()
