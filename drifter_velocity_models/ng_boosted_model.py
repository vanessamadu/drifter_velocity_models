from model_classes import Model
# import packages
import numpy as np
import ngboost

class NGBoostModel(Model):

    def __init__(self,loss_type,training_data,test_data,covariate_labels):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "ngboost_pr"
        self.covariate_labels = covariate_labels
        self.fit_model = None

    #------------------------ model constructions -------------------------#
    def ngboost_pr(self,num_estimators):
        '''return probabilistic regression model'''
        model = ngboost.NGBoost(Dist=ngboost.distns.MultivariateNormal(2),
                               n_estimators=num_estimators)
        
        self.fit_model = model.fit(X=np.array(self.training_data.loc[:,self.covariate_labels]),
                                   Y=np.array(self.training_data.loc[:,["u_av","v_av"]]))
    
    
    
