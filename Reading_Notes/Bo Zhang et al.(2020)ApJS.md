# Bo Zhang et al.(2020)ApJS 246 9
Title:
Deriving the Stellar Labels of LAMOST Spectra with the Stellar LAbel Machine (SLAM)

+ 完整的数据准备、训练、测试、不确定性度量的过程。
+ 超参数设置、筛选恒星时参数的设置

## 背景
LAMOST DR5 数据量庞大，需要进行光谱分类。
## 主旨、假设
+ 方法：非线性回归(SVR:支持向量回归)，数据驱动，对高度非线性问题建模，得出恒星光谱型。
+ 模型：SLAM(Stellar LAbel Machine)
## 数据来源
+ DataSet：
1. data：
+ LAMOST DR5 普通星光谱(Teff :4000 ~ 8000 K, S/N_g > 100)
+ LAMOST AFGK ，有可靠参数的、设定筛选范围 
+ LAMOST Stellar Parameter pipeline (LASP)：
> Wu, Y., Luo, A.-L., Li, H.-N., et al. 2011, RAA, 11, 924 

> Wu, Y., Du, B., Luo, A., Zhao, Y., & Yuan, H. 2014, in IAU Symp. 306, Statistical Challenges in 21st Century Cosmology, ed. A. Heavens, J.-L. Starck, & A. Krone-Martins (Cambridge: Cambridge Univ. Press), 340 

+ APOGEE DR15(pipeline：ASPCAP 来得到基本的Star Labels物理量、元素丰度、微观湍流)
> García Pérez, A. E., Allende Prieto, C., Holtzman, J. A., et al. 2016, AJ, 151, 144 

2. Star labels: Teff，log g，\[M / H\]，\[α/ M\]，\[C / M\]，\[N / M\]
3. Ground_Truth：APOGEE DR15的结果

## 数据分析
1. 预处理：
	1. 标准化：（$\mu=0, \sigma=1$）
	+ 连续谱：归一化
	+ Star Labels：同样地，按统计学量标准化。只在最后得出预测时，视为物理量
	2. 平滑：平滑样条函数，排除偏差点，再拟合伪连续谱
	3. 筛选：3900 ~ 5800 A 重新采样，步长1.0A (每个像素)。 超过50个像素则为坏点
2. 方法：python - scikit-learn，

  + 在每个波长处，训练SVR model，RBF核函数，超参数设置，目标函数：MSE

  + 贝叶斯方法：$\theta$是Star Labels，$f_{j,obs}$是第j个像素处，归一化的光谱流量。逐像素计算似然$\prod_{j=1}^{n} p(f_{j,obs}|\theta)\times p(\theta)$先验。得到后验$p(\theta|f_{obs})$

  + 采样方法：Levenberg– Marquardt 最小二乘法优化器-最大似然估计

    > Moré, J. J. 1978, LNM, 630, 105 

  + 优化方法：Hessian矩阵 + scipy.optimize.least_squares 

3. 训练：
	LAMOST DR5 低分辨率光谱

3. 预测：
    + 对观测光谱预测Star Labels(物理量)
	+ 参数空间分布、误差分布

4. 验证：
+ 训练集 ： APOGEE DR15  高分辨(S/N>100) + LAMOST DR5 低分辨(S/N>40)，Teff: 3000~5500 K



6. 不确定性分析

   + 光谱归一化（晚型星的伪连续谱难以确定）
> Jofré, P., Heiter, U., & Soubiran, C. 2019, ARA&A, 57, 571 

   + 训练样本有偏（可能存在极端点，目标函数无法描述富/贫金属星）
   + Star Labels标定错误 
     
+ 交叉检验：K-fold 减少过拟合
1. 参数：100,49 K,0.10 dex,0.037 dex,0.026 dex,0.058 dex,0.106 dex 

## 方法对比
+ LASP 
使用 ULySS在ELODIE光谱库上建立多项式模型，拟合光谱流量。
+ SLAM 
1. 使用RBF核函数，灵活、自适应性。同时训练集也可以依需要变更。
2. 可以使用交叉验证、S/N 来给出不确定度的估计
3. 可以扩展更多Star Labels物理量(eg: [$\alpha / Fe$])
## 结论
1. 与其他数据驱动model性能相同
2. SLAM存在一些偏差、以及适用的范围
3. 用SLAM得到了一些DR5 中 K巨星的labels

+ 本文是一个使用机器学习的方式训练恒星labels的实证型文章
+ 提供了详细的超参数的选取策略、不确定性来源和规模的分析
+ 详细的论证了机器学习方法、数据驱动方法的合理性、可靠性
+ 提供了开源代码