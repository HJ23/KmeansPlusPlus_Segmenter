import sys
sys.path.append("./source")
from exceptions import *
from kmeans_plus_plus import kmeans_plus_plus

try:
    abc=kmeans_plus_plus(k_value=3,image_path="./tree.png")
    abc.start()
except exception as exp:
    print(exp.getError())

