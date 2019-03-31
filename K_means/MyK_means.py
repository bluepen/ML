import numpy as np
import random
from matplotlib import pyplot as plt

class K_means(object):
    def __init__(self,X,k,maxIter):
        self.X = X#数据集   是一个矩阵
        self.k = k#所需要分的类的数
        self.maxIter = maxIter#所允许的程序执行的最大的循环次数

    def K_means(self):
        row,col = self.X.shape#得到矩阵的行和列

        dataset = np.zeros((row,col + 1))#新生成一个矩阵，行数不变，列数加1 新的列用来存放分组号别  矩阵中的初始值为0
        dataset[:,:-1] = self.X
        print("begin:dataset:\n" + repr(dataset))
        # centerpoints = dataset[0:2,:]#取数据集中的前两个点为中心点
        centerpoints = dataset[np.random.randint(row,size=k)]#采用随机函数任意取两个点

        centerpoints[:,-1] = range(1,self.k+1)
        oldCenterpoints = None #用来在循环中存放上一次循环的中心点
        iterations = 1 #当前循环次数

        while not self.stop(oldCenterpoints,centerpoints,iterations):
            print("corrent iteration:" + str(iterations))
            print("centerpoint:\n" + repr(centerpoints))
            print("dataset:\n" + repr(dataset))

            oldCenterpoints = np.copy(centerpoints)#将本次循环的点拷贝一份 记录下来
            iterations += 1

            self.updateLabel(dataset,centerpoints)#将本次聚类好的结果存放到矩阵中

            centerpoints = self.getCenterpoint(dataset)#得到新的中心点，再次进行循环计算

        np.save("kmeans.npy", dataset)
        return dataset

    def stop(self,oldCenterpoints,centerpoints,iterations):
        if iterations > self.maxIter:
            return True
        return np.array_equal(oldCenterpoints,centerpoints)#返回两个点多对比结果


    def updateLabel(self,dataset,centerpoints):
        row,col = self.X.shape
        for i in range(0,row):
            dataset[i,-1] = self.getLabel(dataset[i,:-1],centerpoints)
            #[i,j] 表示i行j列

    #返回当前行和中心点之间的距离最短的中心点的类别，即当前点和那个中心点最近就被划分到哪一部分
    def getLabel(self,datasetRow,centerpoints):
        label = centerpoints[0, -1]#先取第一行的标签值赋值给该变量
        minDist = np.linalg.norm(datasetRow-centerpoints[0, :-1])#计算两点之间的直线距离
        for i in range(1, centerpoints.shape[0]):
            dist = np.linalg.norm(datasetRow-centerpoints[i, :-1])
            if dist < minDist:#当该变距离中心点的距离小于预设的最小值，那么将最小值进行更新
                minDist = dist
                label = centerpoints[i,-1]
        print("minDist:" + str(minDist) + ",belong to label:" + str(label))
        return label

    def getCenterpoint(self,dataset):
        newCenterpoint = np.zeros((self.k,dataset.shape[1]))#生成一个新矩阵，行是k值，列是数据集的列的值
        for i in range(1,self.k+1):
            oneCluster = dataset[dataset[:,-1] == i,:-1]#取出上一次分好的类别的所有属于同一类的点，对其求平均值
            #dataset[:,-1] == i 计算dataset中最后一列是否有等于i的值，如果有，则返回一个Ture的布尔值，该布尔值可以用来
            #当做矩阵的索引值，dataset[dataset[:,-1] == i,:-1]的意思是：取出最后一列中等于某一k值得最有行，除了最后一行不取，
            # 也就是取出它们的坐标值
            newCenterpoint[i-1, :-1] = np.mean(oneCluster,axis=0)#axis=1表示对行求平均值，=0表示对列求平均值
            newCenterpoint[i-1, -1] = i#重新对新的中心点进行分类，初始类

        return newCenterpoint

    #将散点图画出来
    def drawScatter(self):
        plt.xlabel("X")
        plt.ylabel("Y")
        dataset = self.K_means()
        x = dataset[:, 0]  # 第一列的数值为横坐标
        y = dataset[:, 1]  # 第二列的数值为纵坐标
        c = dataset[:, -1]  # 最后一列的数值用来区分颜色
        color = ["none", "b", "r", "g", "y","m","c","k"]
        c_color = []

        for i in c:
            c_color.append(color[int(i)])#给每一种类别的点都涂上不同颜色，便于观察

        plt.scatter(x=x, y=y, c=c_color, marker="o")#其中x表示横坐标的值，y表示纵坐标的
        # 值，c表示该点显示出来的颜色，marker表示该点多形状，‘o’表示圆形
        plt.show()


if __name__ == '__main__':


    '''
    关于numpy中的存储矩阵的方法，这里不多介绍，可以自行百度。这里使用的是
    np.save("filename.npy",X)其中X是需要存储的矩阵
    读取的方法就是代码中的那一行代码，可以不用修改任何参数，导出来的矩阵和保存之前的格式一模一样，很方便。
    '''
    # X = np.load("testSet-kmeans.npy")#从文件中读取数据
    #自动生成数据
    X = np.zeros((1,2))
    for i in range(1000):
        X = np.row_stack((X,np.array([random.randint(1,100),random.randint(1,100)])))
    k = 5 #表示待分组的组数

    kmeans = K_means(X=X,k=k,maxIter=100)
    kmeans.drawScatter()