from sklearn import svm
import numpy as np

x = [[2, 0], [1, 1], [2, 3]]
y = [0, 0, 1]
clf = svm.SVC(kernel = 'linear')
clf.fit(x, y)

print ("分类器的定义：" + repr(clf))

# get support vectors
print ("满足划分超平面的点的坐标：" + repr(clf.support_vectors_))
# get indices of support vectors
print ("满足SVM划分超平面的点，在样本列表中的下标号码：" + repr(clf.support_))
# get number of support vectors for each class
print ("对于划分的两边所找到的支持向量（也就是相切的点）:" + repr(clf.n_support_))
#预测一个新的点属于那一边
z = [4,5]
z = np.array(z).reshape([-1,1])
print("预测点[4,5]:" + clf.predict([[4., 5.]]))