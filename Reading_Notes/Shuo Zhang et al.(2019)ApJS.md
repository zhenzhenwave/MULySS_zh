# Shuo Zhang et al.(2019)ApJS 240 31
Title:
M-subdwarf Research. I. Identification, Modified Classification System, and Sample Construction

本文实证类，对M dwarf 进行分类：介绍多个分类标准、校准了划分指标，得到更好的分类性能。最后讨论了子类的物理意义。

+ 图表很好看

## 背景

+ M dwarf的子类：dM 普通、dM 贫金属亚矮星 、esdM 极端亚矮星
  
> Gizis, J. E. 1997, AJ, 113, 806 
  
+ M subdwarf的演化是极为缓慢的，其生命周期比哈勃时间长的多。一般位于halo和thick disk

+ 发现了一些位于银心反向，thin disk中的，可能是投影或者俘获

+ 对M subdwarf的研究（金属性、位置、运动学），是对星系形成演化历史有重要意义。

## 主旨、假设


### sdM 贫金属亚矮星   
+ 较冷2400~4000 K ,分子线密集 ，有明显的金属氧化物和氢化物分子吸收带。
+ 在一定的Teff下，金属氧化物消耗掉。
+ 因此，氧化物、氢化物的分子吸收强度之比，可以作为区分依据。


### 划分指标
1. G97
在CaHn-TiO5图上，定义了经验关系，区分sdM和esdM
2. L07
   
   >  Lépine, S., Rich, R. M., & Shara, M. M. 2007, ApJ, 669, 1235

​      在CaH2+ CaH3,  TiO5图上，定义分隔带，区分dM、sdM、esdM

>  $Index = \frac{F_{fea}}{F_{cont}}$·是特征分子吸收线的平均流量与该波段连续谱流量之比

3. $[\alpha / H]$
使用$\zeta_{TiO/CaH}$并不能严格分割，考虑了$\alpha $元素的影响
## 数据来源

+ Dataset：80000个M dwarf光谱（使用Hammer程序(IDL，模板匹配)，分类）

  > Covey, K. R., Ivezic, Z., Schlegel, D., et al. 2007, AJ, 134, 2398 

+ Ground-Truth：人工Hammer程序标记的 325个 + DR2 中的 108个 M subdwarf 

### LAMOST
1. 参数：6.67 m 球面主镜，有效孔径 4 m，视场角 5°
2. 后期：
+ 2D pipeline：暗场、平场、天光、抽光谱、波长定标、降噪、拼接红蓝端光谱
+ 1D pipeline：通过模板匹配，得出天体的红移值Z（sdM不适用）
+ sdM测RV：测量8条线的多普勒频移  --> 与APOGEE有系统性偏移

## 数据分析
### 方法
1. 校准：新标定了分隔符指数 $\zeta$=0.75

   > $\zeta$衡量的是贫金属性导致的TiO线带的强度降低程度:$\zeta = \frac{1-TiO_5}{1-[TiO5]_{Z_{sun}}}$

2. 引入：[CaH1 v.s TiO5]作为分类的必要条件。

3. 检索：用上述条件，检索出10000个候选

4. 核查：使用Hammer光谱工具目视检查，确认2971个sdM

## 结论

1. 发现了LAMOST DR4中的2791个新的M subdwarf(遍布M0~M7型)
2. 基于M subdwarf的光谱模板研究，改进了M subdwarf的**光谱分类**方法。
3. 汇编了新的M subdwarf的目录（rv、光谱指数、误差……）
4. 起初冷的subdwarf是基于运动学分离出来的，但不知道M subdwarf的运动特征是否相同