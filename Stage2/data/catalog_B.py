from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import numpy as np
from astropy.io import fits
import os
import pandas as pd

# catalog_B is the input tabel for ULySS. 

def get_fitsNames(path_root):
    file_names = []
    for _, _, files in os.walk(path_root):
        for file in files:
            file_names.append(file)
    return file_names

class cata_B(pd.DataFrame):
    def __init__(self, path_root = './spectrum/'):
        file_names = get_fitsNames(path_root)
        index = range(len(file_names))
        columns = ['lamost', 'file_name', 'snrr', 'teffin', 'loggin', 'fehin', 'RA', 'DEC']
        pd.DataFrame.__init__(self, index = index, columns = columns)
        self.path_root = path_root 
        self.file_names = file_names

    def addCol(self):
        for i in range(len(self.file_names)):
            file_path = self.path_root + self.file_names[i]

            # Read fits files and get attribute from them
            with fits.open(file_path) as f:
                data = f[0]
                c = SkyCoord(data.header['RA'], data.header['DEC'], unit='deg', frame='icrs')
                lamost_desig = data.header['DESIG'][7:]
                snrr = data.header['SNRR']
                # Query to get parameters' initial guesses
                t,g,m = self.paraQuery(c)
                self.at[i] = lamost_desig, self.file_names[i], snrr, t, g, m, c.ra.deg, c.dec.deg

    def paraQuery(self, coord):
        '''
        parameters initial guess, 
        query SIMBAD to get TGM 
        ''' 
        customSimbad = Simbad()
        customSimbad.add_votable_fields('fe_h') 
        # Query using coordinates
        res = customSimbad.query_region(coord, radius='0d0m2s')
        para = res['Fe_H_Teff', 'Fe_H_log_g', 'Fe_H_Fe_H'].filled(999)
        t,g,m = para[0]
        # Make sure parameters meaningful
        t,g,m = self.paraCheck(t,g,m)
        return t,g,m

    def paraCheck(self, t, g, m):
        a, b, c = float(t), float(g), float(m)
        if (a<3100)or(a>5000):
            a = 3500.0
        if (b<4)or(b>5.9):
            b = 5.
        if (c<-1.)or(c>1.):
            c = -0.05
        return np.round(a,1),np.round(b,1),np.round(c,2)
