import numpy as np
from matplotlib import pyplot as plt

def drawScatter():
    plt.xlabel("X")
    plt.ylabel("Y")
    x = [1,2,3,4]

    print(x)
    y = [3,4,5,6]
    plt.scatter(x,y,c=["b","r","g","y"])
    plt.show()

if __name__ == '__main__':
    drawScatter()