# TODO

- [x] 安装ULySS、IDL、IDL astro
- [ ] ~~检查ULySS源码，看看每个部分的运行规则~~
- [x] 看样例 fit_b16_1.pro （main）例子  table_b16  (input file)  , 字段的信息
- [ ] 按照例子的做法，尝试筛选数据
- [ ] 把筛选数据预处理，主程序

# Overview
## ULySS文件结构
1. ulyss.pro ：主程序  、光谱分析
2. uly_fit.pro ：用非线性模型 fit 光谱
3. uly_solut_twrite.pro  把fit完的结果保存为ASCII文件(.res)
4. uly_solut_swrite.pro 把uly_fit.pro的结果保存为FITS文件
5. ulyss_spec_read.pro  ：从FITS文件中读入光谱
6. uly_test.pro : 测试安装错误、崩溃


+ 设置多项式阶数md=15
+ 用/clean 去除3$\sigma$以外的outlier --> 对比图
+ 用/plot检查拟合的光谱图像 -->  待测谱 vs. 模型谱


恒星大气参数
1. uly_tgm.pro : 	定义 TGM 成分

##  筛选光谱
1. 信噪比范围（SNR>10，10~20，20~30），初始参数范围设置
2. 读入fits的光谱范围3900~7500
3. uly_spect_read.pro相关子程序，真空-空气波长转换
4. M 星 参数初值设定：Teff:3000~4000，多个log g : 3.0,  1.5 ……，Fe_H : -2,  -1,  0  …… default: G star

## 拟合光谱
1. 文件输出file= xxx.fts（流量、谱线） xxx.res（文本，物理参数结果）
2. 个别光谱有gap（流量断点）的，会导致程序断掉，可以在主程序里设个判断+ skip  (non)
## 误差分析
1. 结果是否有物理意义（Teff:2700~50000）（log g:-1~5.9）(Fe_H: 2.7~1.0）
2. 出现问题的地方：数据问题、模型的设置、有效范围、初始值偏差严重、信噪比很低、或数据流量定标有严重问题等

## 验证
用有已知参数的高分辨光谱做验证

# Usage in detail
## 恒星大气参数
1. 读入CFLIB的一个星
```idl
IDL> ; uly_root = '/usr/local/ulyss'  已经写在uly_startup.pro里了
IDL> star = uly_root+'/data/cflib_114642.fits'  
IDL> galaxy = uly_root+'/data/VazMiles_z-0.40t07.94.fits'
```

2. 使用默认参数，确定大气参数（对比太阳）
```idl
IDL> ulyss, star  
```
```idl
IDL Version 8.2.1 (linux x86_64 m64). (c) 2012, Exelis Visual Information Solutions, Inc.

% Compiled module: RESOLVE_ALL.
UNRESOLVED ROUTINES: CGCOLOR CGDEFAULTCOLOR CGERRORMSG CGQUERY CGPLOT CGWINDOW SETDEFAULTVALUE BOOLEAN CGCENTERTLB
IDL> star = uly_root+'/data/cflib_114642.fits'
IDL> ulyss, star
Use default model: Solar spectrum
--------------------------------------------------------------------
INPUT PARAMETERS
--------------------------------------------------------------------
The fits file to be analyze is       /usr/local/ulyss/data/cflib_114642.fits
Name of the output file              output.res
Degree of multiplicative polynomial            10
No additive polynomial  
Component1 (cmp1) file:/usr/local/ulyss/models/sun.fits 
--------------------------------------------------------------------
% ULY_SPECT_READ_LSS: Assume that the dispersion is linear (air wavelength)
% ULY_SPECT_READ_LSS: Dispersion axis is 1 (Air wavelength)
% ULY_SPECT_READ_LSS: Assume that the dispersion is linear (air wavelength)
--------------------------------------------------------------------
PARAMETERS PASSED TO ULY_FIT
--------------------------------------------------------------------
Wavelength range used                 :       3464.9160       9469.5171 [Angstrom]
Sampling in log wavelength            :       20.079155 [km/s]
Number of independent pixels in signal:       15011
Number of pixels fitted               :       15011
DOF factor                            :      1.00000
--------------------------------------------------------------------
number of model evaluations:          35
time=      0.87942600
Number of pixels used for the fit       15007

cz             :       7.5581444 +/- 0.96103474 km/s
dispersion     :       75.070373 +/- 0.88710896 km/s
-----------------------------------------------
estimated SNR  :       12.510639
-----------------------------------------------
cmp #0  cmp1
Weight         :    0.0057345585 +/-    5.3433868e-05 [data_unit/cmp_unit]
-----------------------------------------------
```

3. 使用模型文件Elodie.3.2内插器，确定大气参数，并绘图
```idl
IDL> ulyss, star, MODEL_FILE=uly_root+'/models/elodie32_flux_tgm.fits', /PLOT
```

4. 用导入、卷积的光谱，确定大气参数
```idl
IDL> spectrum = uly_spect_read(galaxy, VELSCALE=velscale)
IDL> spectrum = uly_spect_losvdconvol(spectrum, 0., 30., 0, 0, /OVER)
IDL> ulyss, spectrum, MODEL=uly_root+'/models/PHR_Elodie31.fits'
```

5. 设置cmp,以及波长范围  
default:  /models/elodie32_flux_tgm.fits.
```IDL
IDL> cmp = uly_tgm()
IDL> star = uly_root+'/data/cflib_114642.fits'  
IDL> ulyss, star, cmp, lmin=3900.0, lmax=6800.0, /PLOT
```

## 光谱、绘图
1. 读入光谱、绘图
```idl
IDL> uly_root = '/usr/local/ulyss'
IDL> s = uly_spect_read(uly_root+'/data/VazMiles_z-0.40t07.94.fits')
IDL> uly_spect_plot, s
```

2. 计算模板光谱
```IDL
model = uly_tgm_extr(uly_root+'/data/cflib_114642.fits', $
                              [6400., 4., 0.])
```

3. 绘图参数
+ 用solution代指输出
```IDL
IDL> star = uly_root+'/data/cflib_114642.fits'
IDL> ulyss, star, /plot, /quiet
; 或者写成
IDL> ulyss, star, SOLUTION=solution, /quiet
IDL> uly_solut_splot, solution
```
+ 绘图参数设置，开启两个窗口，不同的绘图模式
```idl
IDL> window, 0
IDL> plot_var = uly_plot_init(POLYCOLOR='Grey', POLYSTYLE=2)  ; 虚线
IDL> uly_solut_splot, solution, TITLE='Example1', PLOT_VAR=plot_var  
IDL> window, 1
IDL> plot_var.polystyle = 1    ; 点线
IDL> uly_solut_splot, solution, TITLE='Example2', PLOT_VAR=plot_var
; 或者直接设置属性
IDL> uly_solut_splot, solution, polycolor='Grey', polystyle=2, $
      title='Example for plotting tutorial'
```
+ 保存、加载设置变量
```IDL
IDL> save, plot_var, filename='plot_var_settings.sav'
IDL> restore, 'plot_var_settings.sav'
```

# [附录](http://ulyss.univ-lyon1.fr/uly.html#ULYSS)
```IDL
ULYSS
[Next Routine] [List of Routines]
 NAME:
                  ULYSS
 PURPOSE:
                  Analyse a spectrum
 USAGE:
                  ulyss,
                  <spectrum>,<cmp> or MODEL_FILE=<model_file>
                  [, POSITION=<position>]
                  [, ERR_SP=<err_sp>][, SNR=<snr>]
                  [, VELSCALE]
                  [, KMOMENT=<kmoment>][, SG=<sg>][, DG=<dg>][, DL=<dl>]
                  [, ADEGREE=<ad>][, MDEGREE=<md>][, POLPEN=<polpen>]
                  [, LMIN=<lmin>][, LMAX=<lmax>]
                  [, NSIMUL=<nsimul>]
                  [, KFIX=<kfix>][, KPEN=<kpen>]
                  [, /CLEAN]
                  [, /QUIET]
                  [, SOLUTION=<solution>]
                  [, /ALL_SOLUTIONS]
                  [, FILE_OUT=<result_file>]
                  [, MODECVG=<modecvg)]
                  [, /PLOT]

 DESCRIPTION:
      Main procedure of the ULySS package.
      Reads the observed spectrum, the models, and makes the fit (with uly_fit).

      ULYSS fits a spectrum with a linear combination of non-linear components
      convolved with a given line-of-sight velocity distribution (LOSVD)
      and multiplied by a polynomial continuum. The linear or non-linear
      parameters may be bounded (for example force a non-negative
      combination of components).

      The fit is a Levenberg-Marquart local minimization for the non-linear
      parameters and a bounded-values least square for the linear ones.
      Any parameter can be bounded of fixed. The algorithm is described
      in ULY_FIT.

      Line-of-sight velocity distribution (LOSVD):

      Velocity dispersion:
      The velocity dispersion computed by the program is
      sigma_ulyss = sqrt(sigma_obs^2 - sigma_model^2). Where
      sigma_obs = sqrt(sigma_physical^2 + sigma_instrumental^2) and
      sigma_model is the dispersion in the model. For ELODIE-based models,
      sigma_model is 13 km/s; For MILES-based models, it is ~58km/s.
      sigma_instrumental is the instrumental broadening of the observation.
      If the relative line-spread function of the spectrograph is injected in
      the model, then sigma_ulyss = sigma_phys.

      Logarithmic sampling:
      The line of sight velocity distribution is measured as a broadening of
      the spectral features due to Doppler shift. The wavelength shift is
      related to the redshift z by: (l1-l0)/l0 = z, where l1 and l0 are
      respectively the shifted and restframe wavelengths. (If we neglect the
      relativistic term, z=v/c, where v is the velocity shift and c the speed
      of light). As the wavelength shift depends on the wavelength, when
      sampled linearly in wavelength, a spectrum is not simply 'translated'.
      However, with a logarithmic sampling the shift becomes a translation,
      and the effect of the LOSVD can be written as a convolution.

      Note also to take care of the composition of the partial shift:
      If a shift z1 is applied in ULY_SPECT_READ, and if ULYSS finds
      a 'residual' shift z2, the total redshift is:
      1 + z = (1 + z1)(1 + z2), when z1xz2 is small it is close to 1+z1+z2.

      Relativistic correction to compute the radial velocity:

      In special relativity, the relation between z and v is:
      1 + z = sqrt(c+v/c-v) = (1 + v/c) / sqrt(1-(v/c)^2).
      (The last term is the Lorentz factor, gamma: 1+z = gamma (1+v/c)).
      At low redshift, the Newtonian approximation is: z=v/c

      This formula can be inverted into:
      v/c = ((1+z)^2 - 1) / ((1+z)^2 + 1)
      (z=1 corresponds to v = 0.6 c = 180000 km/s)

      ULySS determines cz, and no relativistic correction is applied.
      The transformation above must be used to determine v from cz.

      In many cases computing cz is sufficient. The databases, LEDA or NED
      give cz that is somehow inproperly sometime called a 'velocity'.

      Computation of the velocity dispersion:

      ULySS determines the cz dispersion, and in general this shall be
      converted into a *velocity* dispersion to carry on dynamics (for
      example to apply the Virial Theorem).
      Fortunately, sigma_cz and sigma are usually very similar.

      To be rigorous, two effects shall be considered (i) the effect of the
      composition of redshifts, and (ii) the relativistic correction.
      Lets write the redshift of a star with v=sigma, in the galaxy's restframe
      zs = (1 + sigma/c) / sqrt(1-(sigma/c)^2) - 1
      And the residual redshift of the barycenter of the galaxy (after
      de-redshifting the spectrum, for example using ULY_SPECT_READ): zb.
      The cz dispersion is: sigma_cz = c (1+zb) zs
      The two corrective terms are usually negligible at any redshift.
      The first order correction pointed by Harrison (1974 ApJ, 191, L51)
      for clusters of galaxies does not apply here.

 ARGUMENTS:
   <spectrum>     Input
                  File name, or 'spect' structure containing 1d spectrum
                  to be analysed with uly_fit.
                  A 'spect' structure is returned by, e.g. ULY_SPECT_READ.
   <cmp>          Input
                  Array of model's components, see ULY_FIT.
                  Prior calls to ULY_STAR, ULY_TGM, ULY_SSP and/or ULY_LINE
                  can define this array and set the guesses and constraints
                  on the free parameters.
                  MODEL_FILE can be given instead.

 KEYWORDS:

   The following keywords are handled by ULYSS itself, or shared
   by the different tasks.

   MODEL_FILE     Input, filename
                  When <cmp> is not provided, this keyword may give the
                  name of a FITS file containing the model to fit.
                  <cmp> and MODEL_FILE are mutually exclusive.
                  Note that using MODEL_FILE is less flexible that using
                  the component-definition functions. See ULY_SSP, ULY_TGM or
                  other component-definition functions for more capabilities.

   SNR            Input, float
                  Mean signal to noise ratio the of analyzed spectrum.
                  This parameter is used to derive the errors if the error
                  spectrum is not attached to the input spectrum and if ERR_SP
                  is not given.  It will generate a constant error spectrum.
                  SNR is ignored if an error spectrum is available.

   NSIMUL         Input, integer
                  To make Monte-Carlo simulations, set with this keyword
                  the number of simulations. These simulations are
                  made adding a Gaussian noise equivalent to the estimated
                  noise. To take into account the correlation of the noise
                  introduced along the data processing (for example,
                  resulting of an oversampling), the noise is generated
                  on a vector of length npix/dof_factor, and then rebinned
                  to npix. Where npix is the actual number of pixels, and
                  dof_factor characterizes the correlation of the noise.
                  (dof_factor is included in the spect structure,
                  ULY_SPECT_LOGREBIN and the other smoothing or resampling  
                  routines modify it consistently).

   /QUIET       
                  Set this keyword to supress the printing of information and
                  results.

   FILE_OUT       
                  The names of the result file are constructed by appending
                  '.res' and '.fits' to this variable.  
                  The '.res' ASCII file contains the values of the parameters
                  and their uncertainties. If the file pre-exists, new records
                  are appended. This file can be used by ULY_SOLUT_TPRINT,
                  ULY_SOLUT_TPLOT, ...
                  The FITS file contains the spectrum, the bestfit, the
                  polynomials and the mask of good pixels. In can be plotted
                  with ULY_SOLUT_SPLOT.
                  If neither FILE_OUT or SOLUTION are specified, output files
                  with prefix 'output' are created

   SOLUTION
                  Output structure containing all fitted parameters and their
                  respective errors. See ULY_FIT for details.

   /ALL_SOLUTIONS
                  When <cmp> specifies a grid of guesses (for global
                  minimization), this keyword tells to return all the local
                  solutions. By default, only the best solution is returned.

   /PLOT            
                  Set this keyword to display the fit using ULY_SOLUT_SPLOT.

   POSITION
                  When a multidimensional dataset is to be analysed, like a
                  long-slit spectrum, stacked spectra or cube, the keyword
                  specifies the position of the 1D spectrum to analyse. It can
                  be a scalar or an array of the same dimension as the dataset
                  (not counting the spectral dimension).

   VELSCALE       [km/s] default=conserve the number of pixels
                  Sampling. Size of the pixel after the rebinning in logarithm
                  of wavelength.

   The following keywords are handled by the reading function ULY_SPECT_READ,
   and are therefore relevant only if <spectrum> is a file name (if <spectrum>
   is a spect structure, ULY_SPECT_READ is not called).
   Check in the documentation of ULY_SPECT_READ for further information.

   SG             [dimensionless] default=0
                  Guess for the redshift z. This keyword is handled by
                  uly_spect_read to shift the data. (the guess for the
                  minimization is set to 0, and cannot by changed).
                  This value must be quite precise: An error by more than 3 or
                  5 times the velocity dispersion may prevent the fit to
                  converge.

   LMIN,LMAX      [Angstrom]
                  Minimum and maximum wavelength. These parameters can
                  be vectors to define several fitting intervals.

   ERR_SP        
                  Name of a FITS file containing the error spectrum.
                  (In some cases the error spectrum may be included in the
                  same file as the signal, see ULY_SPECT_READ)

   The following keywords are handled by ULY_FIT. Check its documentation
   for further information.

   KMOMENT        
                  Number of terms of the LOSVD.
                  The terms are in the order: [cz, sigma, h3, h4, h5,
                  h6]. By default, KMOMENT=2, i.e. a Gaussian LOSVD
                  is fitted.

   DG             [km/s]
                  Guess or fixed value for the velocity dispersion.
                  This guess is not very critical, and the default value
                  of 1 pixel is generally satisfactory.

   DL             [km/s]
                  2-elements array giving the limits for the fitted velocity dispersion.

   KFIX   
                  Array used to fix some of the parameters of the LOSVD,
                  0 means that the parameter is free; 1 that it is fixed.
                  The parameters are specified in the following order:
                  [cz, sigma, h3, h4, h5, h6]. cz and sigma must be
                  given in km/s.

   KPEN           
                  Kinematics penalty parameter for the Gauss-Hermite
                  coefficients. Default is no penalization (KPEN=0).
                  This penalisation is described in Cappellari & Emmsellem
                  2004, PASP 116, 138. The actual value should be chosen
                  carefully (performing Monte-Carlo simulations), but values
                  in the range 0.5 to 1.0 shall be a good starting guess.
                  See more information in ULY_FIT.

   ADEGREE
                  Default -1; Degree of additive polynomial,
                  -1: no additive polynomial

   MDEGREE
                  Default 10; Degree of multiplicative polynomial  

   POLPEN
                  Automatic selection of significant terms in the
                  multiplicative polynomial. See ULY_FIT_LIN.

   CLEAN
                  Set this keyword to iteratively detect and clip the outiers.
                  The algorithm is described in ULY_FIT.

   MODECVG
                  Keyword passed to ULY_FIT (see the documentation there)

```
