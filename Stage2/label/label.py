from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np
from catalog_A import getVizier,cata_A
import os
import sys
import warnings

warnings.filterwarnings("ignore")

def saveCoord(table, path):
    c = table[['RA', 'DEC']]
    with open(path, 'w+') as f:
        for _ , line in c.iterrows():
            f.writelines(str(line['RA']) + ',' + str(line['DEC']) + ',2.0' + '\n')
    print('Saved to Coord_file: ', path)

def delSameStar(table):
    sameIndex = []
    for i in range(len(table)):
        for j in range(i+1, len(table)):
            if (i in sameIndex) or (j in sameIndex):
                continue
            else:
                # k = (i if np.random.rand(1) >= 0.5 else j)
                if (table.Name[i] == table.Name[j]):
                    sameIndex.append(j)
                    print('delete same Name  : %s' %table.Name[j])
                    continue
                elif (abs(table.RA[i]-table.RA[j]) <= 0.0005) and (abs(table.DEC[i]-table.DEC[j]) <= 0.0005):
                    sameIndex.append(j)
                    print('delete same Coord : %s  (%s)' %(table.Name[j],table.Name[i]))
    table.drop(table.index[sameIndex], inplace=True)

def readCataName(file_path):
    catalog_names = []
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            catalog_names.append(line[:-1])  # 去除末尾的 "\n"

    return catalog_names

if __name__=='__main__':
    
    os.chdir(sys.path[0])

    other_table = pd.read_csv('./other_ref/Mald2020.csv')
    catalog_names = readCataName('./catalog_names.txt')
    print(catalog_names)

    cata_As = getVizier(catalog_names)
    
    i = 0
    concat_A = [] 
    for cata_a in cata_As:
        cata_a.fillTGM()
        cata_a.fillCoord()
        cata_a.tgm2np()

        table_a = cata_a[cata_a.Mstars()].copy()
        print('table %d out of %d: ----> ' %(i+1, len(cata_As)))
        print('Select %d M stars out of %d stars' %(len(table_a), len(cata_a)))
        print(table_a.head(),'\n')
        
        concat_A.append(table_a)
    
    # 拼接
    concat_As = pd.concat(concat_A, axis=0)
    concat_As = pd.concat([concat_As, other_table], axis=0, join="inner")
    concat_As = concat_As.sample(frac=1.0) # 打乱顺序
    concat_As.reset_index(drop=True, inplace=True)
    print('got %d M stars in total \n' %len(concat_As))

    # 消除重复元素
    delSameStar(concat_As)
    concat_As.reset_index(drop=True, inplace=True)
    print('Concat Table: ----> ')
    print(concat_As, '\n')

    # 保存数据
    concat_As.to_csv('../fit/catalog_A.csv')
    print('Saved to ../fit/catalog_A.csv')
    saveCoord(concat_As, '../data/coord_A.txt')

    # 绘制参数分布
    concat_As = cata_A(concat_As)
    concat_As.draw_parameter_space()

    print('done!')
    
