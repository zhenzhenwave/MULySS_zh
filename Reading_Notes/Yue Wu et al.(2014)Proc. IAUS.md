# Yue Wu et al.(2014)Proc. IAUS


## Title
Automatic stellar spectral parameterization pipeline for LAMOST survey

本文式对 LAMOST 的光谱数据 pipeline 进行自动处理\获取参数的 LASP 介绍, 策略, 算法, 过程。

## 数据

LAMOST 巡天项目 2013 年发布了 DR1
- 分辨率 R ~ 1800
- 波长覆盖 3800 ~ 9000 A 
- MDB ：中央数据库 ， MySQL 
- 格式：fits


## 方法

1. CFI ： 相关函数插值法，基于 ATLAS9恒星大气模型的 Kurucz 光谱合成代码。最佳拟合合成谱与观测谱相关系数。

	- 首先，在 Teff 网格中搜素最佳的 Teff
	- 固定 Teff ，搜素 [Fe/H]
	- 固定 Teff, [Fe/H] ，搜素 log g  ( 三个参数可信度依次下降) 

1. ULySS ： 最小化 上述两者的$\chi^2$ 。用 ELODIE 数据库插值
2. LASP : 结合了 CFI 和 ULySS 
  + stage1 ： 观测原始谱
  + stage2：  光谱归一化

## LASP 策略

1. CFI 先粗略、快速地给出初始估计：恒星类型、恒星大气参数
2. 使用 CFI 的结果做初始猜测，选择合适的模板拟合范围，使用 ULySS 拟合参数
3. 减少了拟合时间，提高了 ULySS 精度

## 结论

- 验证：比较了 LAMOST DR1 和 PASTEL 之间的共同源

| 恒星类型 | Teff_err | Log g_err | [Fe/H]_err | V_err |
| -------------- | -------- | --------- | ---------- | -----|
| *            | 110 K     | 0.19 dex  | 0.11 dex   | 4.91 km/s|



