## [LAMOST数据格式](http://dr3.lamost.org/doc/data-production-description)
### 命名
spec-MMMMM-YYYY_spXX-FFF.fits
+ MMMMM : 局部修正的儒略日 (LMJD)
+ YYYY : PLAN ID
+ spXX : 光谱仪编号(1~16)
+ FFF : 光纤编号(1~250)
> 如：spec-55859-F5902_sp02-063.fits

### 正式名称 
LAMOST JHHMMSS.ss + DDMMSS.ss
+ HHMMSS.ss ：天体的 赤纬 ra  (hourangle格式)
+ DDMMSS.ss : 天体得 赤经 dec (dms格式)

> 如: LAMOST J220714.91-014549.6 

同一个desig不一定指一个目标星（plan可能会有偏移）可以通过PlanID ,spID 确定同一颗星

### FITS
#### HDU
> NAXIS   =                    2 /
NAXIS1  =                 3909 /
NAXIS2  =                    5 /

数据部为：(3909, 5)的2维数组

### LAMOST数据库目录
+ ra、dec ： 观测目标 赤经、赤纬（从目录中得出） unit: degree
+ $ra_{obs}$、$dec_{obs}$ ：光纤指向的 赤经赤纬 unit：degree
+ offset :  观测期间是否有光纤偏移

+ A、F、G、K 星表中会提供恒星参数
+ M 星表没有恒星参数、提供TiO、CaH的特征谱线1