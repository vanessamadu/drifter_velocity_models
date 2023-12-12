'description: hierarchical model framework for the construction of my ocean drifter velocity model'

#%%%%%%%%%%%%%%%%%%%%%%%%%%%% SET UP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%% MODEL CLASS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class Model:
    '''
    this class will be the parent class of all ocean models that we will be using
    and it will define attributes and methods common to all specific model classes.
    '''
    #==== magic methods ====#
    def __init__(self, loss_type,training_data,test_data):
        self.loss_type = loss_type # specify loss function
        self.training_data = training_data # data as pd dataframe
        self.test_data = test_data # data as pd dataframe
    
    def __str__(self):
        ''' if a model is operated on by the string operator, it returns a description of the model'''
        return f"Ocean drifter model with type: {self.model_type}, loss: {self.loss_type}, class: {type(self)}"

    #++++++++++++++++++++++++ STATIC METHODS ++++++++++++++++++++++++++++#
    #------------------------ loss functions -------------------------#
    ''' these methods define the loss functions used to measure model prediction performance'''
    
    @staticmethod
    def rmse(obs,preds):
        '''
        returns: root mean square error (rmse) over all the predictions made by the model.

        params: 
        [array] obs: array of velocity observations
        [array] preds: array of predicted velocities
        '''
        errs,speed_errs,dir_errs = __class__.prediction_errors(obs,preds)
        return linalg.norm(speed_errs)/np.sqrt(len(speed_errs)), linalg.norm(dir_errs)/np.sqrt(len(dir_errs))
    
    #------------------------ error analysis --------------------------#
    ''' these methods define methods used for analysis of residuals'''

    @staticmethod
    def prediction_errors(obs,preds):
        '''
        returns: prediction errors for velocity, speed, and direction for each prediction the model makes

        params:
        [array] obs: array of velocity observations
        [array] preds: array of predicted velocities
        '''
        errs = [x-x_pred for x,x_pred in zip(obs,preds)]
        speed_errs = [linalg.norm(err) for err in errs]
        dir_errs = [np.abs(np.arctan(err)) for err in errs]

        return errs,speed_errs,dir_errs

    #++++++++++++++++++++++ MODEL PROPERTIES AND SETTERS +++++++++++++++++++++#
    # -------------------- properties ---------------------#
    @property
    def loss_type(self):
        '(setter) loss type which acts as a dict key to assign appropriate loss function'
        return self._loss_types
    
    @property
    def training_data(self):
        '(setter) data used to train'
        return self._training_data
    
    @property
    def test_data(self):
        '(setter) data used to test'
        return self._test_data
    #========== 'immutable' properties ==========#
    @property
    def loss_function(self):
        '(no setter) assigns appropriate loss function according to loss_type'
        return self.loss_functions[self.loss_type]
    
    # --------------------- setters ------------------------ #
    @loss_type.setter
    def loss_type(self,loss_type_name):
            'checks that loss_type is valid'
            if loss_type_name not in self.loss_functions.keys():
                raise ValueError("loss type not in permitted loss functions")
            else:
                self._loss_type = loss_type_name    
    
    @training_data.setter
    def training_data(self,data_subset):
        'changes the value of the training_data property'
        self._training_data = data_subset

    @test_data.setter
    def test_data(self,data_subset):
        'changes the value of the test_data property'
        self._test_data = data_subset
    

    
 

    #++++++++++++++++++++++ CLASS VARIABLES +++++++++++++++++++++++++++#

    #===== permitted loss functions =====#
    loss_functions = {'rmse':rmse}