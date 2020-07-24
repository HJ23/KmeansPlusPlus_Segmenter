
from source.exceptions import *
from source.kmeansPP import *
import logging

try:
    abc=kmeansPP(k_value=3,image_path="./tree.png")
    abc.start()
except EXCEPTION as exp:
    logging.error(exp.getError())

