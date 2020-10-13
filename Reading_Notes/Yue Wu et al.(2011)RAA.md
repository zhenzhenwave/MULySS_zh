# Yue Wu et al.(2011)RAA 11,8

## Title
Automatic determination of stellar atmospheric parameters and
construction of stellar spectral templates of the Guoshoujing Telescope (LAMOST)

+ 介绍了ULySS原理、R=2000的数据选择
+ 用ULySS确定了LAMOST模板光谱数据库
+ 解释了内插器ELODIE数据库的模板来源
+ 用高分辨光谱数据验证拟合结果

## 背景
研究银河系的演变是天体物理中的关键方向。需要了解恒星的特性：质量、年龄、元素丰度、运动学特征……

## 主旨、假设
### 方法
快速、自动地从光谱提取恒星大气参数的方法可以分为：**MDM（最小距离）和ANN（神经网络）**

+ MDM ： 对N维的光谱，在N维空间中与模板光谱匹配，找到最短距离的模板（类似KNN）
1. 建立模板光谱数据库。库中光谱已确定了准确的参数。
2. 然后对目标光谱进行MDM处理（如：最小化$\chi^2$，加权平均、KNN等）
3. 通过插值的方法，确定目标光谱精确的TGM

+ ANN ： 使用神经网络，找到input：N维光谱 和 output： 3维 参数TGM之间的映射。训练集：预处理好的光谱、参数；或者模板合成的光谱

### 原理
1. ULySS 用 模板插值的方式，在每个波长pixil处，拟合目标光谱的流量，确定可能的参数。
$$
Obs(\lambda) = P_n(\lambda) \times [TGM(T_{eff},log\,g,[Fe/H],\lambda)]\otimes G(v_{sys},\sigma)
$$
+ TGM ：ELODIE模板库的插值。它由内部的T、G、M、波长等参数的非线性函数进行线性组合而成。
+ $P_n(\lambda)$： 是一个n阶多项式。用于校准误差：流量校准、银河消光等。*代替了其他方法所需的伪连续谱校准、归一化的步骤* 。  
+ $G(v_{sys},\sigma)$： 是高斯轮廓函数，V_sys：包含了星表视向速度不确定性。sigma：包含了仪器展宽和恒星自旋影响

2. 最小化：优化参数Teff 、log g、Fe/H 、 v_sys 、sigma 、 阶数n

## 数据来源
1. CFLIB数据库：
+ KPNO，3460–9464 A，R ~5000，1273个恒星。
+ 重新筛选、并重采样R~2000（降低分辨率、以便与对应LAMOST的中分辨率数据）
+ labels：在ULySS的论文中以及得到验证。

2. SDSS的高分辨、高SNR光谱：
+ labels：通过SSPP （混合了多种方法的pipeline）确定的大气参数
+ 重采样到R~2000。ULySS拟合高分辨的模板光谱，并与SSPP的高中低SNR中随机挑选的样本结果对比

3. SEGUE SSPP：SDSS/SEGUE 的样本
+ 是亮星、高信噪比、高分辨率
+ 可以作为验证、校准ULySS的结果

## 数据分析
### LAMOST大气参数
1. 拟合策略
+ 鉴于波长范围，使用ELODIE的模板数据库
+ 只用SNR低一些的蓝端，不需要流量校准和伪连续谱归一化
+ 选择3个不同的起始位置，同时拟合。通过ULySS收敛图工具，确保收敛于全局最小点。

2. 大气参数确定
+ 711个LAMOST恒星样本
+ 误差：39K，0.21 dex和0.11 dex 
+ 富金属星拟合较好

3. 与SSPP的结果比较
+ 筛选：每个光谱仪的光谱数据中，挑了几个F8星，目视确定参数。排除了一些低SNR的样本。
+ 结果：Teff、Fe/H 保持一致。log g系统偏移了0.6 dex（可能是因为LAMOST 的 SNR低，而且SSPP是针对SDSS进行了调整）。

### 建立LAMOST模板光谱
+ 模板库需要覆盖宽波段 3700 - 9000 A，所有将红、蓝端光谱拼接起来。
+ LAMOST 的 SNR较低：通过目视、筛选出120个质量好的光谱和labels，构建模板库。
+ labels范围：4339∼8507K，1.80∼4.72dex , −0.81 ∼ 0.30 dex  (F，G，K)

## 结论
1. 本文给出了ULySS确定大气参数的原理
2. 对比了ULySS结果和SDSS光谱参数，验证合理性
3. 应用ULySS到LAMOST的恒星大气参数pipeline上
4. 用ULySS建立了LAMOST的光谱模板库v1

> Wu, Y., Singh, H. P., Prugniel, P., Gupta, R., & Koleva, M. 2011, A&A, 525, A71
