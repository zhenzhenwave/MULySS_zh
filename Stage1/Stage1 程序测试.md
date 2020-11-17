

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

+ 存在11条光谱是invalid，其余fit完成。
```idl
IDL> fit_b16_1
% READCOL: 72 valid lines read
...
3 J004613.83+335010.3 /usr/local/ulyss/pgm/indep/files/spec-55911-M31_007N34_B2_sp05-222.fits
    0.0032770634
4 J005242.36+315545.1 /usr/local/ulyss/pgm/indep/files/spec-56647-M31010N33M1_sp07-126.fits
    0.0034291744
-> No valid input fits file.
   4.1007996e-05
...
-> valid final out num:           53out of           72
-> Bad fits file num:        0
-> Finish fit_b16_1
```

### question
1. 物理量是什么
```idl
readcol, infile, designation, spt, teffin, zeta, fehin, veloin,format='A,F,F,F,F,F'
```
2. 拟合失败（list 5 为例）

   + 输入的地址没有检索到。
   + DataBase_b16中数据格式不一致。snrr应为4个字符，若只有三位则导致后续文件名读取出错。文件读写程序不够鲁棒。
   + ~~解决：把三位、五位的snrr手动添加到4位（补0）~~
   + 修正：fit_b16_1.pro 中的从文件中读取字符串的部分。
   
```idl
-> valid final out num:           63out of           72
-> Bad fits file num:        0
```


绘图结果

文献中的样例

<img src="./figures/log Teff logg.png" alt="log Teff logg" style="zoom: 33%;" />

+ [log Teff v.s. FeH](./Test/logTeff-FeH.png)

文献中的样例

<img src="./figures/log Teff M.png" alt="log Teff M" style="zoom:33%;" />

文献中的样例， 横轴：input（参考文献的），纵轴：output（ULySS的结果）

<img src="./figures/Teff ref.png" alt="Teff ref" style="zoom:35%;" />

5. outout 变量的含义 ( 二维数组 )

| 0    | 1    | 2    | 3    | 4     | 5     | 6     | 7      | 8    |
| ---- | ---- | ---- | ---- | ----- | ----- | ----- | ------ | ---- |
| T    | G    | M    | RV   | T_err | G_err | M_err | RV_err | snr  |



