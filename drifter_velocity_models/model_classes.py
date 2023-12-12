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
class Model:
    '''
    this class will be the parent class of all ocean models that we will be using
    and it will define attributes and methods common to all specific model classes.
    '''
    ## magic methods ##
    def __init__(self, loss_type,data):
        self.loss_type = loss_type # specify loss function
        self.data = data # data as pd dataframe
    
    def __str__(self):
        ''' if a model is operated on by the string operator, it returns a description of the model'''
        return f"Ocean drifter model with type: {self.model_type}, loss: {self.loss_type}, class: {type(self)}"       