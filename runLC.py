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

    if (gta.roi[src_name]['ts'] > 1000. and
        gta.roi[src_name]['SpectrumType'] == 'PowerLaw'):
        gta.set_source_spectrum(src_name, spectrum_type='LogParabola',
                                spectrum_pars={'beta' : {'value' : 0.0, 'scale' : 1.0,
                                                         'min' : 0.0, 'max' : 2.0}})

    gta.free_source(src_name)
    gta.fit()
    gta.free_source(src_name, False)

    loc = gta.localize(src_name, free_radius=1.0, update=True, make_plots=True)

    model = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
    srcs = gta.find_sources(model=model, sqrt_ts_threshold=5.0,
                            min_separation=0.5)
    
    sed = gta.sed(src_name, free_radius=1.0, make_plots=True)
    gta.tsmap(make_plots=True)
    gta.tsmap(prefix='excludeSource', exclude=[src_name], make_plots=True)

    gta.write_roi('fit0')    
    lc = gta.lightcurve(src_name, binsz=86400.*28.0, free_radius=3.0, use_scaled_srcmap=True,
                        multithread=False)

if __name__ == "__main__":
    main()
