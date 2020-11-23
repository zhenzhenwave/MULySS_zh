import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
import os
import sys
import numpy as np

def get_fitsNames(path_root):
    file_names = []
    for _, _, files in os.walk(path_root):
        for file in files:
            if file[-4:]=='fits':
                file_names.append(file)
    return file_names

def fits2png(file_name, waverange):
    # 绘图
    plt.figure(figsize=[10,8])
    y = image_data[:,0,:]
    x = np.linspace(waverange[0], waverange[1], len(y[0]))

    # factor = 1/np.median(y[2][(x > 5400.) & (x < 5600.)])
    factor = 1/np.median(y[2])

    obs_spec = factor*y[0]/y[3]
    fit_spec = factor*y[2]/y[3]
    poly_con = y[3]

    ax1 = plt.axes([0.1, 0.5, 0.9, 0.5])
    ax1.plot(x, obs_spec, color='k', label='obs_spec')
    ax1.plot(x, fit_spec, color='b', label='fit_specc')
    ax1.plot(x, poly_con, color='c', label='poly_con')

    index = (y[5]==0)
    index[0] = False
    plt.xlim(waverange)
    plt.title('Solution for '+ file_name[:-5], fontsize=18)
    plt.xticks([])
    # plt.yticks([])

    # 标记坏点、拟合中舍弃的
    ax1.plot(x[index], obs_spec[index], color='r', label='bad pixel')
    ax1.set_ylabel('Relative Flux', fontsize=18)
    plt.legend(loc="upper left")
 
    # 残差
    ax2 = plt.axes([0.1, 0.1, 0.9, 0.4])  
    error = (obs_spec - fit_spec)
    ax2.plot(x, error, color='k', label='Res')
    ax2.axhline(0., color='g', ls="--")
    ax2.plot(x[index], error[index], color='r', label='bad pixel')
    ax2.set_xlabel('Wavelength', fontsize=18)
    ax2.set_ylabel('Residual', fontsize=18)
    plt.legend(loc="upper left")

    plt.tick_params(labelsize=13)
    #plt.show()
    path = './figures/' + file_name[:-5] + '.png'
    plt.savefig(path, bbox_inches='tight')
    print('Saved to figure: '+ path)
    plt.close()

if __name__=='__main__':

    os.chdir(sys.path[0])

    file_names = get_fitsNames('./solution')

    for file_name in file_names:
         # 显示 Header 信息
         #print(repr(fits.getheader(file_name, 0)))

         #print(fits.info('./solution/' + file_name))
         image_data = fits.getdata('./solution/' + file_name, ext=0)
         #print(image_data.shape)

         fits2png(file_name,[4000., 9000.])
     
    print('done!')





