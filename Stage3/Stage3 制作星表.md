# Stage3:制作星表

- [ ] 下载数据：从lamost下载数据，按照正式名称筛选，下载fits，保存成csv--> 得到星表：（包含名称、属性数据，可以筛选信息）
- [ ] 首先制作星表：与其他的已知参数的星表比对，这样得到的数据是已知结果的，自己做出的结果可以得到验证
- [ ] 第二步：通过筛选后的星表，再结合新的筛选信息（如：信噪比>100）再挑选一次（pandas read csv）。最后下载里面的fits光谱数据。