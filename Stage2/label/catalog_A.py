from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
# %matplotlib qt

def hms2deg(ra, dec):
    '''
    transform coordinates from hms,dms to degree,
    faster than searching names directly in SkyCoord.from_name
    '''
    if (ra == None) or (dec == None) or (ra == ''):
        print('Cannt find coord, Drop :' )
        return 0, 0
    h,m,s = ra.split(' ')
    if float(h) <= 24:
        ra = h+'h'+m+'m'+s+'s'
    else:
        ra = h+'d'+m+'m'+s+'s'
    d,m,s = dec.split(' ')
    dec = d+'d'+m+'m'+s+'s'                        
    try:
        c = SkyCoord(ra, dec)
        ra, dec = c.ra.deg, c.dec.deg
    except:
        return 0, 0
    return ra, dec

def checkCol(cata):
    '''
    find useful columns in vizier's catalog result,
    add them to my catalog style
    '''
    dict = {
    'Name' : ['Name', 'Star', 'name', 'SimbadName', 'Simbad'],
    'RA' : ['RA', '_RA.icrs', '_RA', 'ra', 'RAJ2000'],
    'DEC' : ['DEC', 'DE', '_DE.icrs', '_DE', 'dec', 'DEJ2000'],
    'SpT' : ['SpT', 'SpType'],
    'Teff' : ['Teff', 'teff', 'Fe_H_Teff'],
    'logg' : ['logg', 'log_g_', 'Fe_H_logg', 'log(g)'],
    'Fe_H' : ['Fe_H', '__Fe_H_', 'Fe_H_Teff', 'Fe_H_Fe_H', '[Fe/H]'],
    'ref_name' : ['ref_name', 'Ref_Name']
    }
    
    for cols in cata.colnames:
        for key in dict.keys():
            if cols in dict[key]:
                dict[key] = cols
                break
    for key in dict.keys():
        if type(dict[key]) == list:
            dict[key] = None

    return dict

def getVizier(table_dict):
    '''
    get catalog results from query vizier
    '''
    Vizier.ROW_LIMIT = -1
    catalog_names = list(table_dict.keys())
    catalog_list = Vizier.get_catalogs(catalog_names)
    print(catalog_list) 
    cata_As = []

    for i in range(len(catalog_list)):
        cata = catalog_list[i]
        print('----- [%d out of %d] ----- \n' %(i+1, len(catalog_list)))
        print('Meta:', cata.meta)
        print('Columns:', cata.colnames) 

        # 本地是否保存了此表
        cata_a_name = './ref_tables/' + table_dict[catalog_names[i]][0] + '.csv'
        if os.path.exists(cata_a_name):
            ref_table = cata_A(pd.read_csv(cata_a_name))
            cata_As.append(ref_table)
            print('Found existed csv file, Read from %s' %cata_a_name)
            continue
        
        dict = checkCol(cata)
        print('\n found useful columns: ', dict)

        if (dict['Name'] or dict['RA']) == None:
            print('\n Skip : Cant locate catalog stars: Missing Name and Coord')
            continue
        else:
            flag = input('Are you sure to proceed? (yes/no)')

        if flag in ['yes', 'y', '1']:
            cata = cata.to_pandas()
            cata_2 = cata.copy()
            for key in dict.keys():
                if dict[key] != None:
                    cata_2[key] = cata[dict[key]]
                else:
                    cata_2[key] = None
            cata_2 = cata_2[dict.keys()]
            cata_2.loc[:, 'ref_name'] = table_dict[catalog_names[i]][0]
            
            # 添加 Error bar
            cata_2.Teff_err = None
            cata_2.logg_err = None
            cata_2.Fe_H_err = None
            T_e, G_e, M_e = table_dict[catalog_names[i]][1].split(',')
            cata_2.loc[:, 'Teff_err'] = float(T_e)
            cata_2.loc[:, 'logg_err'] = float(G_e)
            cata_2.loc[:, 'Fe_H_err'] = float(M_e)

            ref_table = cata_A(cata_2)
            cata_As.append(ref_table)
        elif flag in ['no', 'n', '0']:
            continue

        else:
            break
    return cata_As

class cata_A(pd.DataFrame):
    def fillTGM(self, s):
        '''
        find losting TGM & SpT parameters via SIMBAD query, with given name
        '''
        print('----- %s -----' %self.ref_name[0])
        if s=='Teff':
            label = 'Fe_H_Teff'
        elif s=='logg':
            label = 'Fe_H_log_g'
        elif s=='Fe_H':
            label = 'Fe_H_Fe_H'
        elif s=='SpT':
            label = 'SP_TYPE'
        else:
            print('error, plz input "Teff" , "logg" , "Fe_H" or "SpT"')
            return 0

        if self[s].isnull().any() == False:
            print('Nothing to fill in TGM & SpT...')
            return 0
        print('Searching for %s :' %s)  
        customSimbad = Simbad()
        customSimbad.add_votable_fields('sptype','fe_h','typed_id')
        
        # 查询
        ind = self[s].isnull()
        try:
            res = customSimbad.query_objects(self.Name[ind]).to_pandas()
        except:
            print('Error finding TGM: ',res)
        finally:
            self[s][ind]= res[label]
            print('[%s] from SIMBAD ---- >' %s)
            print('%d parameters found!  (out of %d) :' %(len(ind)-self[s][ind].isna().sum(),len(ind)))
            print(self[s][ind].head())
            if s != 'SpT':
                self.ref_name[ind] = self.ref_name[ind] + '*'
        
    def fillCoord(self):
        '''
        query or transform coordinates, if they are not given or not in degree
        '''
        try:
            float(self.RA[1])
            print('already had coordinate')
            return 0
        except:
            for i in self.index:
                try:
                    # print('Transforing coord for ' , self.Name[i])
                    ra, dec = hms2deg(self.RA[i], self.DEC[i])
                except:
                    print('qeury coords for ', self.Name[i])
                    try:
                        c = SkyCoord.from_name(self.Name[i])
                        ra, dec = c.ra.deg, c.dec.deg
                    except:
                        ra, dec = 0, 0
                finally:
                    if (ra == 0) & (dec == 0):
                        print('Not found.Drop ', self.Name[i])
                        self.drop(self.index[i], inplace=True)
                        continue
                    self.RA[i] = ra
                    self.DEC[i] = dec
            return 1

    def Mstars(self):
        '''
        select only M stars and within some ruled range
        '''
        filter_Teff = ((self.Teff < 5000) & (self.Teff > 3100))
        filter_SpT = self.SpT.str.contains("M")
        filter_DEC = ((self.DEC < 60.0) & (self.DEC > -10.0))

        return (filter_DEC & filter_Teff & filter_SpT)

    def tgm2np(self):
        self.Teff = self.Teff.to_numpy()
        self.logg = self.logg.to_numpy()
        self.Fe_H = self.Fe_H.to_numpy()
        self.RA = self.RA.to_numpy()
        self.DEC = self.DEC.to_numpy()

    def draw_parameter_space(self):
        '''
        plot parameter space pictures,
        log Teff v.s. log g
        log Teff v.s. Fe_H 
        '''
        tgm = np.array([self.Teff.to_numpy(), self.logg.to_numpy(), self.Fe_H.to_numpy()])
        
        # --- log Teff v.s. log g ----------
        fig = plt.figure(figsize = [10, 6])
        ax = fig.add_subplot(111)
        ax.plot(np.log10(list(tgm[0])), tgm[1], 'g.', markersize=10)

        ax.set_xlabel(r'$log  T_{eff}$', fontsize=18)
        ax.set_ylabel(r'$log  g$', fontsize=18)
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

        file_name = 'TvsG.png' 
        plt.savefig(file_name, bbox_inches='tight')
        # plt.show()
        print('Saved to ' + file_name)

        # --- log Teff v.s. Fe_H ------------
        fig = plt.figure(figsize = [10, 6])
        ax = fig.add_subplot(111)
        ax.plot(np.log10(list(tgm[0])), tgm[2], 'k.', markersize=10)

        ax.set_xlabel(r'$log  T_{eff}$', fontsize=18)
        ax.set_ylabel('Fe/H', fontsize=18)
        plt.gca().invert_xaxis()

        file_name = 'TvsM.png' 
        plt.savefig(file_name, bbox_inches='tight')
        # plt.show()
        print('Saved to ' + file_name)

        return 'done'

