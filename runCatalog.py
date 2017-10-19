import numpy as np
import yaml
import os
from astropy.io import fits
from astropy.table import Table, Column, hstack
import glob


def stack_files(files, outfile, new_cols=None):

    h = fits.open(files[0])

    tables = []
    for hdu in h:
        if isinstance(hdu,fits.BinTableHDU):
            tables += [stack_tables(files,hdu.name,new_cols=new_cols)]

    hdus = [fits.PrimaryHDU()]
    hdus += [fits.table_to_hdu(t) for t in tables]
    hdulist = fits.HDUList(hdus)
    hdulist.writeto(outfile,overwrite=True)



def stack_tables(files, hdu=None, new_cols=None):
    
    tables = []
    for f in sorted(files):
        tables += [Table.read(f,hdu=hdu)]

    cols = []
    for c in tables[0].colnames:

        col = tables[0][c]
        cols += [Column(name=col.name, unit=col.unit, shape=col.shape,
                        dtype=col.dtype)]

    tab = Table(cols,meta=tables[0].meta)

    for t in tables:
        row = [ t[c] for c in tables[0].colnames ]
        tab.add_row(row)

    if new_cols is not None:

        for col in new_cols:
            tab.add_column(col)
                    
    return tab

def getPosition(fitsFile):
    hdulist = fits.open(fitsFile)
    locData = hdulist[2].data
    hdulist.close()
    return locData['ra'][0], locData['dec'][0], locData['glon'][0], locData['glat'][0]

def getLC(CLFile):
    hdulist = fits.open(fitsFile)
    return hdulist['LIGHTCURVE'].data

def getSourcesFromYaml(yamlName, LCpath):
    with open(yamlName, 'r') as stream:
       try:
          yFile = yaml.load(stream)
       except yaml.YAMLError as exc:
          print(exc)

    sourceList = []
    LCFileList = []
    raList = []
    decList = []
    lonList = []
    latList = []
    print "found %i sources"%len(yFile)
    for s in yFile.keys():
       LCfile = "%s/%s/%s_lightcurve.fits"%(LCpath,s,s.lower())
       print s
       if os.path.exists(LCfile):
          LCFileList.append(LCfile)
       else:
          print "LC file not found %s"%LCfile
          continue
       Locfile = "%s/%s/%s_loc.fits"%(LCpath,s,s.lower())
       if os.path.exists(Locfile):
          ra, dec, lon, lat = getPosition(Locfile)
       else:
          print "localization file not found %s"%Locfile
          continue
       raList.append(ra)
       decList.append(dec)
       lonList.append(lon)
       latList.append(lat)
       sourceList.append(s)

    new_cols=[Column(name='Source_name',data=sourceList),Column(name='RAJ2000',data=raList),Column(name='DEJ2000',data=decList), Column(name='GLON',data=lonList), Column(name='GLAT',data=latList)]
    return new_cols, LCFileList


yamlName = 'sourceListAll2283.yaml'
LCpath = '/nfs/farm/g/glast/g/neutrino/shared/MonthlyLC1GeV/'
new_cols, LCFileList = getSourcesFromYaml(yamlName, LCpath)
tab = stack_tables(LCFileList, hdu=None, new_cols=new_cols)
tab.write(yamlName.replace('.yaml','.fits'), format='fits')   


