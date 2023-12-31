from model_classes import Model
# import packages
import numpy as np

class BathtubModel(Model):
    '''benchmark model - predicts all velocities to be zero at all positions and for all times.'''
    
    def __init__(self, loss_type, uncertainty_type,training_data,test_data):
        super().__init__(loss_type,uncertainty_type,training_data,test_data)
        self.model_type = "bathtub"

    #------------------------ model constructions -------------------------#
    @staticmethod
    def bathtub(lon,lat):
        __class__.check_coordinates(lon,lat)
        return np.zeros(2)

    #----------------------- 'immutable' properties -----------------------#
    @property
    def model_function(self):
        return self.bathtub
    
    @property
    def trained_prediction(self):
        return [self.model_function(lon,lat) for lon,lat in np.array(self.training_data[["lon","lat"]])]
    
    @property
    def testing_prediction(self):
        return [self.model_function(lon,lat) for lon,lat in np.array(self.training_data[["lon","lat"]])]

class SBRModel(Model):
    '''benchmark model: predicts velocities according to a steady solid body rotation model.'''

    def __init__(self,loss_type:str,uncertainty_type:str,training_data,test_data):
        super().__init__(loss_type,uncertainty_type,training_data,test_data)
        self.f0 = 7.27e-5 # coriolis parameter at 30 degrees N
        self.model_type = 'sbr'

    #------------------------ model constructions -------------------------#
    @staticmethod
    def sbr(lon:float,lat:float,f0:float):
        __class__.check_coordinates(lon,lat)
        
        return np.array([-f0*lat,f0*lon])
    # -------------------------properties and setters ------------------------------#
    @property
    def f0(self):
        return self._f0
    
    @f0.setter
    def f0(self,val):
        try:
            float(val)
        except:
            raise ValueError("coriolis parameter, f0, must be a real number")
        self._f0 = val

    # -----------'immutable' properties -----------#
    @property
    def model_function(self):
        return self.sbr
    
    @property
    def trained_prediction(self):
        return [self.model_function(lon,lat,self.f0) for lon,lat in np.array(self.training_data[["lon","lat"]])]
    
    @property
    def testing_prediction(self):
        return [self.model_function(lon,lat,self.f0) for lon,lat in np.array(self.test_data[["lon","lat"]])]

class FixedCurrentModel(Model):
    '''benchmark model: predicts all drifter velocities to be the average velocity across the 
       drifter data'''
    
    def __init__(self, loss_type:str,uncertainty_type:str,training_data,test_data):
        super().__init__(loss_type,uncertainty_type,training_data,test_data)
        self.model_type = "fixedcurrent"
        self.av_drifter_velocity = None
    
    #------------------------ model constructions -------------------------#
    @staticmethod
    def fixedcurrent(lon:float,lat:float,current):
        __class__.check_coordinates(lon,lat)
        return current
    
    #----------------------- 'immutable' properties -----------------------#
    @property
    def av_drifter_velocity(self):
        return self._av_drifter_velocity
    
    @av_drifter_velocity.setter
    def av_drifter_velocity(self,val):
        if val is None:
            self._av_drifter_velocity = np.mean(np.array(self.training_data[["u","v"]]),axis=0)
        else:
            self._av_drifter_velocity = val
            
    @property
    def model_function(self):
        return self.fixedcurrent
    
    @property
    def trained_prediction(self):
        return [self.model_function(lon,lat,self.av_drifter_velocity)\
                 for lon,lat in np.array(self.training_data[["lon","lat"]])]
    
    @property
    def testing_prediction(self):
        return [self.model_function(lon,lat,self.av_drifter_velocity)\
                 for lon,lat in np.array(self.training_data[["lon","lat"]])]
