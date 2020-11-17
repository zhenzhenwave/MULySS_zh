from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import numpy as np
from astropy.io import fits
import os
import sys
import pandas as pd
from catalog_B import cata_B

if __name__=='__main__':
    
    os.chdir(sys.path[0])

    path_root = './spectrum/'
    # Read fits files names
    input_table = cata_B(path_root)

    # guess the initial parameters
    input_table.addCol()
    print(input_table.head())
    print('... ...')
    
    # Save to csv
    input_table.to_csv('../fit/catalog_B.csv')
    print('We got %d stars , saved to ../fit/catalog_B.csv' %len(input_table))


