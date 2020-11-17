import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
# %matplotlib qt

class cata_C(pd.DataFrame):

    def tgm2np(self):
        '''
        Not used in this project
        '''
        self.Teff = self.Teff.to_numpy()
        self.logg = self.logg.to_numpy()
        self.Fe_H = self.Fe_H.to_numpy()
        self.RA = self.RA.to_numpy()
        self.DEC = self.DEC.to_numpy()
        self.Teff_err =  self.Teff_err.to_numpy()
        self.logg_err = self.logg_err.to_numpy()
        self.Fe_H_err = self.Fe_H_err.to_numpy()

    def addCol(self, table_valid):

        # 新增列 
        self['Name'] = None 
        self['Teff_ref'] = np.float('nan')
        self['logg_ref'] = np.float('nan')
        self['Fe_H_ref'] = np.float('nan')
        self['ref_name'] = None

        _ra = table_valid.RA
        ra = self.RA
        dist = np.zeros([len(ra), len(_ra)])

        # 搜寻最接近的 ra
        for i in range(len(ra)):
            for j in range(len(_ra)):
                dist[i][j] = abs(_ra[j] - ra[i])

        # 匹配，并填入列
        index = np.argmin(dist, axis=1)
        self.Name = table_valid.loc[index, 'Name'].to_list()
        self.Teff_ref = table_valid.loc[index, 'Teff'].to_numpy()
        self.logg_ref = table_valid.loc[index, 'logg'].to_numpy() 
        self.Fe_H_ref = table_valid.loc[index, 'Fe_H'].to_numpy()
        self.ref_name = table_valid.loc[index, 'ref_name'].to_list()

    def drawTGM(self, s, ref_name):
        if s=='Teff':
            label = '$T_{eff}$'
            index = 0
        elif s=='logg':
            label = '$log g$'
            index = 1
        elif s=='Fe_H':
            label = '$[Fe/H]$'
            index = 2
        else:
            print('error, plz input "Teff" , "logg" or "Fe_H" ')
            return 0

        plt.figure(figsize = [5,10])

        # 参数
        uly_tgm = np.array([self.Teff.to_numpy(), self.logg.to_numpy(), self.Fe_H.to_numpy()])
        ref_tgm = np.array([self.Teff_ref.to_numpy(), self.logg_ref.to_numpy(), self.Fe_H_ref.to_numpy()])
        ax = plt.axes([0.1, 0.35, 0.9, 0.4])
        xmax = np.max([np.max(uly_tgm[index]), np.max(ref_tgm[index])])
        xmin = np.min([np.min(uly_tgm[index]), np.min(ref_tgm[index])])
        xrange = [xmin - 0.1 * (xmax - xmin), xmax + 0.1 * (xmax - xmin)]
       
        ax.plot(ref_tgm[index],uly_tgm[index], 'b.', markersize=8)
        # 离群点
        outlier_ind = self.outlier(ref_tgm[index], uly_tgm[index])
        ax.plot(ref_tgm[index][outlier_ind], uly_tgm[index][outlier_ind], 'r+', markersize=10)
        ax.plot(xrange, xrange, "g--")

        ax.set_xlim(xrange)
        ax.set_ylim(xrange)
        ax.set_ylabel(label, fontsize=18)
        plt.title('ULy v.s. %s ' %ref_name, fontsize=18)

        # 残差
        error = uly_tgm - ref_tgm
        ax2 = plt.axes([0.1, 0.1, 0.9, 0.25])

        ax2.plot(ref_tgm[index],error[index] , 'c.',markersize=8)
        # 离群点
        outlier_ind = self.outlier(ref_tgm[index], error[index])
        ax2.plot(ref_tgm[index][outlier_ind], error[index][outlier_ind], 'r+', markersize=10)

        ax2.set_xlim(xrange)
        ax2.set_xlabel(label, fontsize=18)
        ax2.set_ylabel('$\Delta \ ' + label[1:], fontsize=18)
        ax2.axhline(np.mean(error[index]), ls="-", c="green")
        ax2.axhline(np.mean(error[index]) + np.std(error[index]), ls="--",c="green")
        ax2.axhline(np.mean(error[index]) - np.std(error[index]), ls="--",c="green")
        
        # 保存
        file_name = ref_name + '_' + s + '.png' 
        plt.savefig(file_name, bbox_inches='tight')
        plt.show()
        print('Saved to ' + file_name)
        return 'done'

    def outlier(self, x, y):
        # 寻找 2 sigma 之外的点
        mu = np.mean(y)
        sigma = np.std(y)
        index = []
        outlier_1 = []
        for i in range(len(y)):
            if (y[i] > (mu + 2*sigma)) or (y[i] < (mu - 2*sigma)):
                outlier_1.append(True)
            else:
                outlier_1.append(False)

        # 聚类
        X  = [[x[i], y[i]] for i in range(len(self))]
        y_pred = DBSCAN(eps = 0.4).fit_predict(X)
        outlier_2 = (y_pred == -1)

        outlier = outlier_1 or outlier_2
        for i in range(len(outlier)):
            if outlier[i]:
                index.append(i)
        
        print('Got outliers: \n',self.Name[index].to_string())
        return index

    def drawTvsG(self):
        tgm = np.array([self.Teff.to_numpy(), self.logg.to_numpy(), self.Fe_H.to_numpy()])

        fig = plt.figure(figsize = [10, 6])
        ax = fig.add_subplot(111)
        ax.plot(np.log10(tgm[0]), tgm[1], 'g.', markersize=10)
        ax.set_xlabel('$log \ T_{eff}$', fontsize=18)
        ax.set_ylabel('$log \ g$', fontsize=18)

        # 保存
        file_name = 'TvsG.png' 
        plt.savefig(file_name, bbox_inches='tight')
        plt.show()
        print('Saved to ' + file_name)
        return 'done'


