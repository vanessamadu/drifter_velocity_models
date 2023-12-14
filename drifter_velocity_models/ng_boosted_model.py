from model_classes import Model
# import packages
import numpy as np
import ngboost

class NGBoostModel(Model):

    def __init__(self,loss_type,training_data,test_data,covariate_labels):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "ngboost"
        self.covariate_labels = covariate_labels