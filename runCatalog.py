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
        if isinstance(hdu, fits.BinTableHDU):
            tables += [stack_tables(files, hdu.name, new_cols=new_cols)]

    hdus = [fits.PrimaryHDU()]
    hdus += [fits.table_to_hdu(t) for t in tables]
    hdulist = fits.HDUList(hdus)
    hdulist.writeto(outfile, overwrite=True)


def stack_tables(files, hdu=None, new_cols=None):

    tables = []
    for f in sorted(files):
        tables += [Table.read(f, hdu=hdu)]

    data = {}
    for i, t in enumerate(tables):
        for c in tables[0].colnames:
            data.setdefault(c, [])
            data[c] += [t[c].data]

    data = {k: np.stack(v) for k, v in data.items()}
    cols = []
    for c in tables[0].colnames:
        col = tables[0][c]
        cols += [Column(name=col.name, unit=col.unit, shape=col.shape,
                        dtype=col.dtype, data=data[c])]

    tab = Table(cols, meta=tables[0].meta)
    if new_cols is not None:

        for col in new_cols:
            tab.add_column(col)

    return tab


def getPosition(fitsFile):
    hdulist = fits.open(fitsFile)
    locData = hdulist[2].data
    hdulist.close()
    return locData['ra'][0], locData['dec'][0], locData['glon'][0], locData['glat'][0]


def getFlux(fitsFile, sourceName):
    hdulist = fits.open(fitsFile)
    catData = hdulist['catalog'].data
    hdulist.close()
    mask = catData['Source_Name'] == sourceName.replace('_',' ')
    return catData[mask]['flux'][0], catData[mask]['flux_err'][0], catData[mask]['flux_ul95'][0], catData[mask]['eflux'][0], catData[mask]['eflux_err'][0], catData[mask]['eflux_ul95'][0]


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
    fluxList = []
    fluxErrList = []
    efluxList = []
    efluxErrList = []
    fluxULList = []
    efluxULList = []


    keys = sorted(yFile.keys())
    print "found %i sources" % len(yFile)
    # for s in yFile.keys():
    for s in keys:
        LCfile = "%s/%s/%s_lightcurve.fits" % (LCpath, s, s.lower())
        print s
        if os.path.exists(LCfile):
            LCFileList.append(LCfile)
        else:
            print "LC file not found %s" % LCfile
            continue
        Locfile = "%s/%s/%s_loc.fits" % (LCpath, s, s.lower())
        if os.path.exists(Locfile):
            ra, dec, lon, lat = getPosition(Locfile)
        else:
            print "localization file not found %s" % Locfile
            continue
        resFile = "%s/%s/fit0.fits" % (LCpath, s)
        if os.path.exists(resFile):
            flux, flux_err, fluxUL, eflux, eflux_err, efluxUL = getFlux(resFile, s)
        else:
            continue

        raList.append(ra)
        decList.append(dec)
        lonList.append(lon)
        latList.append(lat)
        sourceList.append(s)
        fluxList.append(flux)
        fluxErrList.append(flux_err)
        efluxList.append(eflux)
        efluxErrList.append(eflux_err)
        fluxULList.append(fluxUL)
        efluxULList.append(efluxUL)


    new_cols = [Column(name='Source_Name', data=sourceList),
                Column(name='RAJ2000', data=raList),
                Column(name='DEJ2000', data=decList),
                Column(name='GLON', data=lonList),
                Column(name='GLAT', data=latList),
                Column(name='Flux', data=fluxList),
                Column(name='Energy_Flux', data=efluxList),
                Column(name='Flux_Unc', data=fluxErrList),
                Column(name='Energy_Flux_Unc', data=efluxErrList),
                Column(name='Flux_UL95', data=fluxULList),
                Column(name='Energy_Flux_UL95', data=efluxULList)]
    return new_cols, LCFileList


def main():
    yamlName = 'sourceListAll2283.yaml'
    LCpath = '/nfs/farm/g/glast/g/neutrino/shared/MonthlyLC1GeV/'
    new_cols, LCFileList = getSourcesFromYaml(yamlName, LCpath)
    tab = stack_tables(LCFileList, hdu=None, new_cols=new_cols)
    tab.write(yamlName.replace('.yaml', '.fits'),
              format='fits', overwrite=True)


if __name__ == "__main__":
    main()
