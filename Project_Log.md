# Stage1:程序测试
- [x] 预处理：将table_b16中的光谱designation，转换成赤道(degree,degree)坐标。
- [x] 下载数据：从LAMOST DR3 中下载table_b16中的光谱
- [x] 筛选：选择信噪比snri、snrr 高的数据（排除坏点）
- [x] 保存文件：包含文件路径和snrr，以便table_b16_1.pro可以检索到 

## 编译运行/Test/fit_b16_1.pro
```idl
IDL> cd, $indep
IDL> .compile fit_b16_1-c.pro
% Compiled module: FIT_B16_1.
```
## Fix Bugs
### 未找到星表文件
```idl
IDL> fit_b16_1
% Attempt to call undefined procedure/function: 'CGERRORMSG'.
% Execution halted at: READCOL           177 /usr/local/exelis/idl82/lib/pro/misc/readc
  ol.pro
%                      FIT_B16_1          30 /usr/local/ulyss/pgm/indep/fit_b16_1-c.pro
%                      $MAIN$       
```

从星表中分别读入:  DESIG、 spt 、 Teff 、 Zeta 、 Fe/H 、 Volein

```idl
path    = '/usr/local/ulyss/pgm/indep/'
```

### 无法登录数据库
```idl
IDL> fit_b16_1
% Attempt to call undefined procedure/function: 'OPENMYSQL_PP'.
% Execution halted at: FIT_B16_1          53 /usr/local/ulyss/pgm/indep/fit_b16_1-c.pro
%                      $MAIN$   
```
1. 文本处理：从星表table_b16中读取DESIG，存放于/Test/Data_Download/table_b16/Desig_names.txt
2. DESIG是天体的时角Hourangle，使用/Test/Pre-processing/HourAngle2Angle.ipynb将时角转换成角度，存放于/Test/Data_Download/DR3_table_b16/coords_Angle.txt
3. 数据下载：在LAMOST DR3中，使用coords_Angle.txt角度检索，下载2"内匹配的光谱fits文件，存放于/Test/Data_Download/table_b16。下载星表数据/Test/Data_Download/DR3_table_b16/496340.csv
4. 496340.csv的分隔符是'|'，需要改成',' 。以便TopCat识别
5. 筛选星表：使用TopCat读取table_b16_2.csv，筛选R、i波段信噪比snrr、snri>10的文件保留，提高可靠性。
6. 删除掉检索编号相同的文件，保留信噪比高的。保存为/Test/Pre-processing/table_b16_2.csv
7. 文本处理：使用/Test/Pre-processing/csv2text.ipynb将table_b16_2.csv中的DESIG、SNRR、Spec_path保存在/Test/Pre-processing/DataBase_b16.txt中
8. 更新星表：csv2text.ipynb将table_b16与筛选后的DataBase_b16.txt对比，保留72个相同DESIG的目标，存放于/Test/Pre-processing/table_b16_modified

### Fit完成，无图像输出
+ 注释了所有plot后的stop
<img src="C:\Users\dmy\AppData\Roaming\Typora\typora-user-images\image-20200921164057148.png" alt="Teff v.s. log g" style="zoom:50%;" />

+ 存在11条光谱是invalid，其余fit完成。
```idl
IDL> fit_b16_1
% READCOL: 72 valid lines read
1 J003010.59+400741.0 /usr/local/ulyss/pgm/indep/files/spec-56266-M31007N41B1_sp05-090.fits
    0.0064668655
2 J004143.13+312729.9 /usr/local/ulyss/pgm/indep/files/spec-56647-M31010N33M1_sp01-062.fits
    0.0033431053
3 J004613.83+335010.3 /usr/local/ulyss/pgm/indep/files/spec-55911-M31_007N34_B2_sp05-222.fits
    0.0032770634
4 J005242.36+315545.1 /usr/local/ulyss/pgm/indep/files/spec-56647-M31010N33M1_sp07-126.fits
    0.0034291744
-> No valid input fits file.
   4.1007996e-05
6 J012615.42+352030.6 /usr/local/ulyss/pgm/indep/files/spec-56657-M31020N36M1_sp08-104.fits
    0.0048689842
7 J023243.54+073557.0 /usr/local/ulyss/pgm/indep/files/spec-56655-EG024123N083137M01_sp10-184.fits
    0.0065281391
8 J023608.53+095440.9 /usr/local/ulyss/pgm/indep/files/spec-56655-EG024123N083137M01_sp16-197.fits
    0.0035459995
9 J024208.23+065529.0 /usr/local/ulyss/pgm/indep/files/spec-56655-EG024123N083137M01_sp01-141.fits
    0.0032260418
10 J030114.52+244228.6 /usr/local/ulyss/pgm/indep/files/spec-56601-GAC046N25M1_sp03-050.fits
    0.0033600330
11 J032255.61+244336.5 /usr/local/ulyss/pgm/indep/files/spec-56225-GAC051N24M1_sp04-165.fits
    0.0032148361
12 J032348.69+243229.4 /usr/local/ulyss/pgm/indep/files/spec-56225-GAC051N24M1_sp04-197.fits
    0.0034778118
13 J034751.81+254730.6 /usr/local/ulyss/pgm/indep/files/spec-56213-GAC056N24B1_sp12-137.fits
    0.0032231808
14 J035113.75+281105.1 /usr/local/ulyss/pgm/indep/files/spec-56630-GAC055N28M1_sp06-172.fits
    0.0034379959
15 J040301.53+153227.2 /usr/local/ulyss/pgm/indep/files/spec-57016-GAC058N16B2_sp06-109.fits
    0.0037348270
16 J041112.01+011826.0 /usr/local/ulyss/pgm/indep/files/spec-56604-EG041109N021906M01_sp05-127.fits
    0.0032980442
-> No valid input fits file.
   4.1961670e-05
18 J053434.17+221250.6 /usr/local/ulyss/pgm/indep/files/spec-56653-GAC085N22M1_sp10-070.fits
    0.0035600662
19 J055710.69+343159.8 /usr/local/ulyss/pgm/indep/files/spec-56213-GAC090N33B1_sp15-154.fits
    0.0032520294
20 J061642.18+364838.6 /usr/local/ulyss/pgm/indep/files/spec-56722-GAC094N35B1_sp11-099.fits
    0.0035488605
21 J062334.67+265644.1 /usr/local/ulyss/pgm/indep/files/spec-56304-GAC094N27M1_sp08-086.fits
    0.0032260418
-> No valid input fits file.
   3.9815903e-05
23 J062500.70+305648.7 /usr/local/ulyss/pgm/indep/files/spec-56299-GAC096N32M1_sp05-016.fits
    0.0034520626
24 J063257.83+323450.5 /usr/local/ulyss/pgm/indep/files/spec-56246-GAC098N33F1_sp04-139.fits
    0.0052111149
25 J063347.51+235036.2 /usr/local/ulyss/pgm/indep/files/spec-56721-GAC099N24B1_sp10-151.fits
    0.0033521652
26 J065045.65+521346.8 /usr/local/ulyss/pgm/indep/files/spec-56326-GAC101N53V2_sp08-014.fits
    0.0033390522
-> No valid input fits file.
   3.7908554e-05
-> No valid input fits file.
   2.8133392e-05
29 J071758.85+354257.0 /usr/local/ulyss/pgm/indep/files/spec-56632-GAC107N36M1_sp06-207.fits
    0.0034170151
30 J072320.04+253610.9 /usr/local/ulyss/pgm/indep/files/spec-56334-GAC110N25B1_sp15-115.fits
    0.0033020973
-> No valid input fits file.
   7.2002411e-05
32 J073835.27+343953.5 /usr/local/ulyss/pgm/indep/files/spec-56602-GAC112N35M1_sp06-100.fits
    0.0035672188
33 J074444.97+272648.2 /usr/local/ulyss/pgm/indep/files/spec-56657-GAC117N27M1_sp03-152.fits
    0.0033490658
34 J074655.54+281323.6 /usr/local/ulyss/pgm/indep/files/spec-56657-GAC117N27M1_sp15-245.fits
    0.0032241344
35 J074656.72+215025.9 /usr/local/ulyss/pgm/indep/files/spec-57005-GAC116N20B1_sp12-142.fits
    0.0036420822
36 J075423.94+290739.1 /usr/local/ulyss/pgm/indep/files/spec-56657-GAC117N27M1_sp12-051.fits
    0.0062398911
37 J075852.18+215135.0 /usr/local/ulyss/pgm/indep/files/spec-56655-GAC121N22M1_sp10-053.fits
    0.0064039230
38 J075920.76+525928.1 /usr/local/ulyss/pgm/indep/files/spec-56740-GAC120N54B1_sp05-095.fits
    0.0054969788
39 J080633.27+321145.4 /usr/local/ulyss/pgm/indep/files/spec-56251-GAC121N33M1_sp08-166.fits
    0.0034000874
40 J084127.90-011403.2 /usr/local/ulyss/pgm/indep/files/spec-56376-GAC129N00V1_sp07-153.fits
    0.0032989979
41 J084542.20+252123.5 /usr/local/ulyss/pgm/indep/files/spec-56628-HD085527N262435M01_sp10-183.fits
    0.0033600330
42 J084601.17+272302.0 /usr/local/ulyss/pgm/indep/files/spec-56628-HD085527N262435M01_sp14-014.fits
    0.0032448769
43 J091406.72+305034.3 /usr/local/ulyss/pgm/indep/files/spec-55940-B5594004_sp03-009.fits
    0.0032038689
44 J092725.42+171101.0 /usr/local/ulyss/pgm/indep/files/spec-55950-F5595003_sp04-225.fits
    0.0043308735
45 J093756.59+283917.0 /usr/local/ulyss/pgm/indep/files/spec-56739-HD093318N282204M_sp09-012.fits
    0.0064170361
46 J093941.97+275140.9 /usr/local/ulyss/pgm/indep/files/spec-56739-HD093318N282204M_sp06-090.fits
    0.0041539669
47 J095451.13+085152.7 /usr/local/ulyss/pgm/indep/files/spec-56683-HD095839N105737B_sp02-123.fits
    0.0034081936
48 J095805.56+333801.5 /usr/local/ulyss/pgm/indep/files/spec-56633-HD095000N333605M01_sp13-081.fits
    0.0034031868
49 J102516.09+461745.8 /usr/local/ulyss/pgm/indep/files/spec-55952-F5595204_sp04-159.fits
    0.0033760071
50 J103528.96+423846.0 /usr/local/ulyss/pgm/indep/files/spec-56740-GAC161N43V1_sp10-101.fits
    0.0034091473
51 J104352.42+303649.3 /usr/local/ulyss/pgm/indep/files/spec-56668-HD105033N320139M01_sp02-040.fits
    0.0033228397
52 J105220.46+274313.1 /usr/local/ulyss/pgm/indep/files/spec-56685-HD104953N275826M01_sp04-104.fits
    0.0032510757
53 J105240.29+283353.8 /usr/local/ulyss/pgm/indep/files/spec-56685-HD104953N275826M01_sp09-152.fits
    0.0032298565
-> No valid input fits file.
   3.6954880e-05
-> No valid input fits file.
   3.8862228e-05
56 J115914.12+580528.5 /usr/local/ulyss/pgm/indep/files/spec-55950-F5595005_sp13-077.fits
    0.0033090115
57 J120229.03+264514.8 /usr/local/ulyss/pgm/indep/files/spec-56317-HD120242N242647M01_sp11-127.fits
    0.0031819344
58 J124754.95+114026.0 /usr/local/ulyss/pgm/indep/files/spec-56726-HD124814N133310B_sp01-167.fits
    0.0032541752
59 J125207.81+003708.6 /usr/local/ulyss/pgm/indep/files/spec-56684-HD125136N030324B01_sp01-214.fits
    0.0032150745
-> No valid input fits file.
   3.8146973e-05
61 J132823.09+090226.8 /usr/local/ulyss/pgm/indep/files/spec-57155-HD133552N081734B02_sp14-210.fits
    0.0031981468
62 J133222.33+185719.8 /usr/local/ulyss/pgm/indep/files/spec-56308-HD133001N190343F01_sp04-236.fits
    0.0031981468
-> No valid input fits file.
   4.1961670e-05
64 J142332.60+231801.0 /usr/local/ulyss/pgm/indep/files/spec-56751-HD141501N234109B01_sp06-144.fits
    0.0032329559
65 J142714.04+335957.7 /usr/local/ulyss/pgm/indep/files/spec-56798-HD141746N331518M01_sp13-126.fits
    0.0038080215
66 J145811.86+311508.5 /usr/local/ulyss/pgm/indep/files/spec-56726-HD145243N315530M_sp08-142.fits
    0.0065770149
67 J151637.89+340322.6 /usr/local/ulyss/pgm/indep/files/spec-56800-HD150818N334223M01_sp13-222.fits
    0.0035860538
-> No valid input fits file.
   3.6954880e-05
69 J220747.72+001606.0 /usr/local/ulyss/pgm/indep/files/spec-55859-F5902_sp04-172.fits
    0.0032751560
70 J225612.76+061236.3 /usr/local/ulyss/pgm/indep/files/spec-56600-EG230400N063658M01_sp10-010.fits
    0.0038850307
71 J230312.72+044430.7 /usr/local/ulyss/pgm/indep/files/spec-56600-EG230400N063658M01_sp01-159.fits
    0.0063781738
72 J235409.68+281720.2 /usr/local/ulyss/pgm/indep/files/spec-55863-B6302_sp08-052.fits
    0.0059390068
-> valid final out num:           53out of           72
-> Bad fits file num:        0
-> Finish fit_b16_1
```

### 摘取：第58条光谱fit过程
```idl
ulyss:      0.52378607
      0.52987099
58 J124754.95+114026.0 /usr/local/ulyss/pgm/indep/files/spec-56726-HD124814N133310B_sp01-167.fits
--------------------------------------------------------------------
INPUT PARAMETERS
--------------------------------------------------------------------
Name of the output file              /usr/local/ulyss/pgm/indep/res_nc_b16_1/spec-56726-HD124814N133310B_sp01-167.res
Degree of multiplicative polynomial        15
No additive polynomial  
Component1 (cmp49) model:/usr/local/ulyss/pgm/indep/mod/miles_tgm2.fits 
  Guess for Teff: 3800.0000 [K], Logg: 2.0000000 4.0000000 [cm/s2], Fe/H: -0.50000000 [dex]
--------------------------------------------------------------------
--------------------------------------------------------------------
PARAMETERS PASSED TO ULY_FIT
--------------------------------------------------------------------
Wavelength range used                 :       3999.4475       7302.9781 [Angstrom]
Sampling in log wavelength            :       69.029764 [km/s]
Number of independent pixels in signal:        2615
Number of pixels fitted               :        2615
DOF factor                            :      1.00000
--------------------------------------------------------------------
Perform global optimization, number of nodes:           2
number of model evaluations:          38
node:           0 chi2:        73.715989
number of model evaluations:          38
node:           1 chi2:        73.715894
time=      0.43243909
Number of pixels used for the fit        2588

cz             :       102.00702 +/- 4.2398389 km/s
dispersion     :       63.573611 +/- 5.4441028 km/s
-----------------------------------------------
estimated SNR  :       12.008923
-----------------------------------------------
cmp #0  cmp49
Weight         :       120.07479 +/-      0.021295554 [data_unit/cmp_unit]
Teff           :       3880.3173 +/- 21.101771 K
Logg           :       4.7252245 +/- 0.039178593 cm/s2
Fe/H           :     -0.65920263 +/- 0.046833622 dex
-----------------------------------------------
```

# Stage2:制作星表，交叉验证
- [ ] 下载数据：从lamost下载数据，按照正式名称筛选，下载fits，保存成csv--> 得到星表：（包含名称、属性数据，可以筛选信息）
- [ ] 首先制作星表：与其他的已知参数的星表比对，这样得到的数据是已知结果的，自己做出的结果可以得到验证
- [ ] 第二步：通过筛选后的星表，再结合新的筛选信息（如：信噪比>100）再挑选一次（pandas read csv）。最后下载里面的fits光谱数据。
- [ ] 最后，把下载的光谱输入到程序中得到参数
- [ ] 保存，输出结果
