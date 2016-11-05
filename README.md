1. my_tools:
----

load_iris,load_banana,load_fig2: 加载各种数据集
draw_scatter: 画散点图
count_cos: 计算余弦距离
count_euclidean: 计算欧氏距离

2. cluster
----

count_distance: 计算距离，返回距离矩阵（补全）
count_density: 计算每个点的局部密度（Gaussian kernel）
_count_density: 计算每个点的局部密度 (cut-off kernel 不用了)
draw: 画决策图
choose_cluster_centers: 测试用，暂时没用（手工查看聚类中心坐标）
count_dc: 自动计算阈值 dc，sort 之后卡第2%那个distance
auto_choose_center: 根据决策图，手工输入聚类中心个数，返回 density*deta 最大的n个点。
draw4center: 决策图，把选出来的聚类中心变个颜色，测试时用的。
cluster: 聚类算法，返回 labeled 之后的所有点 list
draw_clustered: 画聚类之后的数据图（2d）

3. 说明
----

a. 所有函数的参数都是数据集，默认为 iris。现在仅仅支持iris和fig2两个数据集，但可以通过给 load_points 方法增加 case 实现,只需要把数据集中每个样本的 name／feature／label／ 三个属性封装到point类中就行，其他代码都可以复用。（amazing！）

b. 主要功能：
my_tools.draw_scatter(x,y) 输入 x,y 两个 list，分别以其为横纵坐标，画出最简单的散点图
cluster.count_distance(dataset) 得到 dataset 的距离矩阵
cluster.draw(dataset)  画 dataset 的决策图
cluster.draw_clustered(dataset)  画聚类之后的数据散点图  

c. 算法实现时有两个细节，一是选取聚类中心时需要回避聚类中心相近的点都具有相近的 density／deta，不排除就相当于少选了。第二就是聚类中心选好之后聚类时用简单的计算距离的方式划分类效果一般，需要用文中的 core／halo 方式优化。（这个需要想一个快点的实现方式。)

d. 运行环境：
python 3.4 
第三方依赖： matplotlib,numpy,# cluster
