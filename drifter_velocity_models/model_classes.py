'description: hierarchical model framework for the construction of my ocean drifter velocity model'

#%%%%%%%%%%%%%%%%%%%%%%%%%%%% SET UP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
##### import packages #####
import numpy as np
from numpy import linalg
import pandas as pd
import math
from typing import List


##### load data #####
data = pd.read_hdf("ocean_data.h5")

class Model:
    '''
    this class will be the parent class of all ocean models that we will be using
    and it will define attributes and methods common to all specific model classes.
    '''
    def __init__(self, loss_type:str,training_data:List[float],test_data:List[float]):
        ## function specifiers
        self.loss_type = loss_type # specify loss function
        self.model_type = None
        ## data attributes
        self.training_data = training_data # data as pd dataframe
        self.test_data = test_data # data as pd dataframe
        ## for probabilistic regression models
        self.trained_distribution = None
        self.test_distribution = None
    
    def __str__(self):
        ''' if a model is operated on by the string operator, it returns a description of the model'''
        return f"Ocean drifter model with type: {self.model_type} loss: {self.loss_type}, class: {type(self)}"

    #++++++++++++++++++++++++ STATIC METHODS ++++++++++++++++++++++++++++#
    
    #------------------------ error functions --------------------------#
    ''' these methods define methods used for analysis of residuals'''

    @staticmethod
    def residuals(obs:List[float],preds:List[float]):
        '''
        returns residuals between predictions and actual values

        params: 
        [array] obs: array of observations
        [array] preds: array of predicted velocities
        '''
        return np.subtract(obs,preds)

    @staticmethod
    def calculate_loss(obs,preds,loss_function,uncertainty_function):
        loss = np.multiply([100,180/math.pi],loss_function(obs,preds))
        uncertainty = np.multiply([100,180/math.pi],uncertainty_function(obs,preds))
        return loss, uncertainty
    #------------------------ loss functions -------------------------#
    ''' these methods define the loss functions used to measure model prediction performance 
        and the associated incertainty.'''
    
    @staticmethod
    def rmse(obs:List[float],preds:List[float]):
        '''
        returns: root mean square error (rmse) over all the predictions made by the model.

        params: 
        [array] obs: array of observations
        [array] preds: array of predictions
        '''
        squared_residuals = np.square(__class__.residuals(obs,preds))
        return np.sqrt(np.mean(squared_residuals))
        
    '''speed_errs,dir_errs = __class__.speed_dir_prediction_errors(__class__.residuals(obs,preds))
        return [linalg.norm(speed_errs)/np.sqrt(len(speed_errs)), linalg.norm(dir_errs)/np.sqrt(len(dir_errs))]'''
    @staticmethod
    def speed_dir_prediction_errors(errs):
        '''
        returns: prediction errors for speed, and direction for each prediction the model makes

        params:
        [array] errs: velocity prediction errors
        '''
        speed_errs = [linalg.norm(err) for err in errs]
        dir_errs = [np.abs(np.arctan(err)) for err in errs]

        return [speed_errs,dir_errs]
    
    @staticmethod
    def standard_errors(obs,preds):
        '''
        returns: standard error of the residuals for speed and direction.
        
        params: 
        [array] obs: array of velocity observations
        [array] preds: array of predicted velocities
        '''
        speed_errs,dir_errs = __class__.speed_dir_prediction_errors(__class__.residuals(obs,preds))
        return [np.std(speed_errs),np.std(dir_errs)]
    
    # -------------------- validation -------------------- #
    
    ''' these methods are used for widespread validation'''

    @staticmethod
    def check_coordinates(lon:float,lat:float):
        limits = {"lat":90.,"lon":180.}
        values = {"lat":lat,"lon":lon}

        for coord in values.keys():
            try:
                float(values[coord])
            except:
                raise ValueError(f"{coord} must be a real number")
            finally:
                if np.abs(values[coord])>limits[coord]:
                    raise ValueError(f"{coord} must be between -{limits[coord]} and {limits[coord]}")

    #++++++++++++++++++++++ MODEL PROPERTIES AND SETTERS +++++++++++++++++++++#
    # -------------------- properties ---------------------#
    @property
    def loss_type(self):
        '(setter) loss type which acts as a dict key to assign appropriate loss function'
        return self._loss_type
    
    @property
    def uncertainty_type(self):
        return self._uncertainty_type
    
    @property
    def training_data(self):
        '(setter) data used to train'
        return self._training_data
    
    @property
    def test_data(self):
        '(setter) data used to test'
        return self._test_data
    
    #---- 'immutable' properties ----#
    @property
    def loss_function(self):
        '(no setter) assigns appropriate loss function according to loss_type'
        return self.loss_functions[self.loss_type]
    
    @property
    def uncertainty_function(self):
        return self.uncertainty_functions[self.uncertainty_type]
    
    # --------------------- setters ------------------------ #
    @uncertainty_type.setter
    def uncertainty_type(self,name):
            'checks that uncertainty_type is valid'
            if name not in self.uncertainty_functions.keys():
                raise ValueError("uncertainty type not in permitted uncertainty functions")
            else:
                self._uncertainty_type = name
    
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

    loss_functions = {'rmse':rmse}
    uncertainty_functions = {'st_resid_err':standard_errors}

    #++++++++++++++++++++++ INSTANCE METHODS ++++++++++++++++++++++++++#

    def train_loss(self):
        'calculate and return training loss'
        obs = np.array(self.training_data[["u","v"]])
        pred = self.trained_prediction
        return self.calculate_loss(obs,pred,self.loss_function,self.uncertainty_function)
    
    def test_loss(self):
        'calculate and return test loss'
        obs = np.array(self.test_data[["u","v"]])
        pred = self.testing_prediction
        return self.calculate_loss(obs,pred,self.loss_function,self.uncertainty_function)
    