'description: hierarchical model framework for the construction of my ocean drifter velocity model'

####################################### SET UP ##############################################
##### import packages #####
import numpy as np
from numpy import linalg
import pandas as pd
import math
from scipy import stats
# plotting #
import matplotlib.pyplot as plt

##### load data #####
data = pd.read_hdf("ocean_data.h5")

####################################### MODEL CLASS ##########################################