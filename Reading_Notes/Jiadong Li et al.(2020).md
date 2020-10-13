# Jiadong Li et al.(2020)


Title
STELLAR PARAMETRIZATION OF LAMOST M DWARF STARS

本文是[SLAM]()的适用于M dwarfs的衍生模型[MDM]()
使用APOGEE pipeline和BT-Settl模型做训练集，使用SLAM训练了M 矮星的模型。

## 背景
+ M dwarfs 是银河中最常见的恒星，寿命长于哈勃时间。用于研究银河化学演化。
+ 观测M dwarfs可以用于研究太阳邻居。但M dwarfs的参数很难得到。
+ M dwarfs介于棕矮星和主序星（燃烧H）之间，处于HR图的主序的末尾。

## 主旨、假设
+ M dwarfs谱线充满了分子吸收带、无法使用等值宽度，很难定参数。只能通过光谱合成方法。
+ 往期工作：都是使用BT-Settl大气模型，Cannon - M15 ， B20， SLAM

### 方法
1. SLAM
+ 确定超参数、预处理、训练SVR、基于光谱预测恒星labels
+ 使用SVR恒星光谱分析
> Liu, C., Bailer-Jones, C. A. L., Sordo, R., et al. 2012,
MNRAS, 426, 2463,
doi: 10.1111/j.1365-2966.2012.21797.x

> Liu, C., Deng, L.-C., Carlin, J. L., et al. 2014, ApJ, 790,
110, doi: 10.1088/0004-637X/790/2/110

> Liu, C., Fang, M., Wu, Y., et al. 2015, ApJ, 807, 4,
doi: 10.1088/0004-637X/807/1/4

2. BT-Settl
+ 用于小质量恒星、棕矮星的研究


## 数据来源
1. LAMOST DR6 、GAIA 筛选出可靠的 M dwarfs
2. 训练集：
+ 使用ASPCAP带参数的光谱：1330个
Teff : 3575K to 5168K, 
Teff_err < 120K, 
1.2 < [M/H] < 0.5dex   err < 0.7 dex

+ BT-Settl模型生成光谱。
Teff ： 2200K ~ 7000K

## 数据分析
+ 分为 Teff、Metallicity、Stellar Mass 分别于已有参数的结果对比分析


## 结论
+ MDM 基于 SLAM 进行了M dwarfs 的适配
+ 分析了适配的参数范围、误差范围
缺陷：
+ SLAM也是基于BT-Settl模型、数据驱动。
+ 局限于训练集的选择、模型的选择。可能适用性不太好

