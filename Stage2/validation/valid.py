import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from catalog_C import cata_C
import os
import sys

if __name__=='__main__':

    os.chdir(sys.path[0])

    ref_name = 'fit'
    
    df_out = pd.read_csv('../fit/catalog_C.csv')
    df_out.drop(['index'], axis=1, inplace=True) 
    df_valid = pd.read_csv('../fit/catalog_A.csv')

    output_table = cata_C(df_out)
    ref_table = cata_C(df_valid)

    # 匹配参数和名称
    output_table.addCol(ref_table)

    # 绘图
    output_table.drawTGM('Teff', ref_name)
    output_table.drawTGM('logg', ref_name)
    output_table.drawTGM('Fe_H', ref_name)
    output_table.draw_parameter_space()

    output_table.to_csv('catalog_D.csv')
    print('We got %d stars , saved to catalog_D.csv' %len(output_table))