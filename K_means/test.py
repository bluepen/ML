import numpy as np
import random,re
from matplotlib import pyplot as plt

# X = np.zeros((1,2))
# for i in range(100):
#     X = np.row_stack((X,np.array([random.randint(1,100),random.randint(1,100)])))
# np.save("testSet-kmeans.npy",X)
#
#
def drawScatter(dataset):
    plt.xlabel("X")
    plt.ylabel("Y")

    x = dataset[:, 0]  # 第一列的数值为横坐标
    y = dataset[:, 1]  # 第二列的数值为纵坐标
    c = dataset[:,-1]  # 最后一列的数值用来区分颜色
    color = ["h", "b", "r", "g", "y", "m"]
    c_color = []

    for i in c:
        c_color.append(color[int(i)])


    plt.scatter(x=x, y=y, c=c_color, marker="o")
    plt.show()

if __name__ == '__main__':

    a = np.load("kmeans.npy")
    # a = np.array([[1,2,1],[2,3,2],[4,5,3]])
    drawScatter(a)
    # print(a)