import pandas as pd
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import os
import sys
import math

def editCol(table):
    table['RA'] = None
    table['DEC'] = None
    table['Teff_err'] = None
    table['logg_err'] = None
    table['Fe_H_err'] = None

    for s in ['Teff', 'logg', 'Fe_H']:
        for i in table.index:
            try:
                a,b = table.loc[i, s].split('±')
                table.loc[i, s] = float(a)
                table.loc[i, s + '_err'] = float(b)
            except:
                print('Error in: ',table.loc[i,:])

            if table.loc[i, 'Fe_H'] == 999:
                print('999 Error: ', table.Name[i])
                customSimbad = Simbad()
                customSimbad.add_votable_fields('fe_h')
                try:
                    res = customSimbad.query_object(table.Name[i]).to_pandas()
                    table.at[i, 'Fe_H'] = float(res['Fe_H_Fe_H'])
                    print('Found Fe_H = ', table.Fe_H[i])
                    table.at[i, 'ref_name'] = table.at[i, 'ref_name'] + '*'
                    if table.Fe_H[i] < 3:
                        pass
                    else:
                        print('Nan error, drop: ',table.Name[i])
                        # table.drop(i, inplace=True)
                        table.Fe_H[i] = float('nan')
                except:
                    print('Error finding Fe_H, Drop : ', table.Name[i], table.Fe_H[i])
                    table.drop(i, inplace=True)
                    
def fillCoord(name_list):
    RA = []
    DEC = []
    nan = float('nan')
    for name in name_list:
        try:
            c = SkyCoord.from_name(name)
            ra, dec = c.ra.deg, c.dec.deg
        except:
            ra, dec = nan,nan
        finally:
            RA.append(ra)
            DEC.append(dec)
    return RA, DEC

if __name__=='__main__':
    os.chdir(sys.path[0])
    sys.path.append("..")
    from catalog_A import cata_A

    path = 'table_a1.csv'
    ref_name = 'Mald2020'  # arXiv:2010.14867/Table_A1
    df = cata_A(pd.read_csv(path))

    df.columns=['Name','Teff','SpT','Fe_H','logg']
    df['ref_name'] = [ref_name for i in range(len(df))]
    editCol(df)
    df.reset_index(drop=True, inplace=True)

    # 补全坐标
    RA,DEC = fillCoord(df.Name)
    df.RA = RA
    df.DEC = DEC
    # df.fillTGM('Fe_H')

    # 删掉 Nan 行
    df = df.dropna(axis=0,how='any') 
    df.reset_index(drop=True, inplace=True)
    print(df)

    # 保存数据
    df.to_csv('Mald2020.csv')
    print('Saved to Mald2020.csv')
