from model_classes import Model
#import packages
import numpy as np
from numpy import linalg

class LinearRegressionModel(Model):
    
    def __init__(self,loss_type:str,training_data,test_data,covariate_labels):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "lr"
        self.covariate_labels = covariate_labels
        self.param_estimate = None

    #------------------------ model constructions -------------------------#
    @staticmethod
    def lr(X,beta):
        '''returns a prediction for the linear regression model'''
        try:
            pred = np.matmul(X,beta)
            return pred
        except:
            ValueError(f"incompatible dimensions covariates : {X.shape}; parameters: {beta.shape}")

    #============== estimate parameter (vector) beta ==================#
    @property
    def design(self):
        '''returns the design matrix associated with the training data'''
        try:
            design_matrix = np.array(self.training_data.loc[:,self.covariate_labels])
            return design_matrix
        except:
            raise KeyError("Covariate(s) were not found in the dataset")
    
    def calculate_param_estimate(self):
        '''returns least squares parameter estimate'''
        lstsq_estimate = linalg.lstsq(self.design,
                                       np.array(self.training_data.loc[:,["u_av","v_av"]]),
                                       rcond=None)
        self.param_estimate= lstsq_estimate[0]

    #----------------------- 'immutable' properties -----------------------#
    @property
    def model_function(self):
        return self.lr

    @property
    def trained_prediction(self):
        ' return prediction for each vector of covariates for seen data'
        if self.param_estimate is None:
            self.calculate_param_estimate()
        pred = self.model_function(self.design,
                                   self.param_estimate)
        return pred
    
    @property
    def testing_prediction(self):
        'return prediction for each vector of covariates in test data'
        pred = self.model_function(np.array(self.test_data.loc[:,self.covariate_labels]),
                                   self.param_estimate)
        return pred
    