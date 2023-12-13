from model_classes import Model
# import packages
import numpy as np

#%%%%%%%%%%%%%%%%%%%%%%%%%%%% BATHTUB MODEL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class BathtubModel(Model):
    '''benchmark model - predicts all velocities to be zero at all positions and for all times.'''
    
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
        return [self.model_function(lon,lat) for lon,lat in np.array(self.training_data[["lon","lat"]])]
    
    @property
    def testing_prediction(self):
        return [self.model_function(lon,lat) for lon,lat in np.array(self.training_data[["lon","lat"]])]


#%%%%%%%%%%%%%%%%%%%%%%%%%%%% SBR MODEL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class SBRModel(Model):
    '''benchmark model: predicts velocities according to a steady solid body rotation model.'''

    #==== magic methods ====#
    def __init__(self,loss_type:str,training_data,test_data,f0:float):
        super().__init__(loss_type,training_data,test_data)
        self.f0 = f0 # coriolis parameter
        self.model_type = 'sbr'
    
    #++++++++++++++++++++++++ STATIC METHODS ++++++++++++++++++++++++++++# 
    #------------------------ model constructions -------------------------#
    @staticmethod
    def sbr(lon,lat,f0):
        __class__.check_coordinates(lon,lat)

        try:
            float(f0)
        except:
            raise ValueError("coriolis parameter, f0, must be a real number")
        
        return np.array([-f0*lat,f0*lon])