from model_classes import Model
#import packages
import numpy as np

class LinearRegressionModel(Model):
    
    def __init__(self,loss_type:str,training_data,test_data,covariate_labels):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "lr"
        self.covariate_labels = covariate_labels

    #------------------------ model constructions -------------------------#
    