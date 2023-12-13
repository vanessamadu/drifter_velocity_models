from model_classes import Model
# import packages
import numpy as np

#%%%%%%%%%%%%%%%%%%%%%%%%%%%% BATHTUB MODEL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class BathtubModel(Model):
    '''this is the first of two benchmark models to measure model performance against'''
    
    #==== magic methods ====#
    def __init__(self, loss_type,training_data,test_data):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "bathtub"

    #++++++++++++++++++++++++ STATIC METHODS ++++++++++++++++++++++++++++# 
    #------------------------ model constructions -------------------------#

    @staticmethod
    def bathtub(lon,lat):
        __class__.check_coordinates(lon,lat)
        return np.zeros(2)
    
    #++++++++++++++++++++++ MODEL PROPERTIES AND SETTERS +++++++++++++++++++++#
    #========== 'immutable' properties ==========#

    @property
    def model_function(self):
        return self.bathtub
    
    @property
    def trained_prediction(self):
        return [self.model_function(lon,lat) for lon,lat in self.training_data["lon","lat"]]
    
    @property
    def testing_prediction(self):
        return [self.model_function(lon,lat) for lon,lat in self.training_data["lon","lat"]]