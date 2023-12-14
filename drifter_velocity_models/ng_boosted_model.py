from model_classes import Model
# import packages
import numpy as np
import ngboost

class NGBoostModel(Model):

    def __init__(self,loss_type,training_data,test_data,covariate_labels):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "ngboost_pr"
        self.covariate_labels = covariate_labels
        self.model_function = None
        self.num_estimators = 10
        self.trained_dist = None
        self.test_dist = None

    #------------------------ model constructions -------------------------#
    def ngboost_pr(self):
        '''return probabilistic regression model'''
        self.model_function = ngboost.NGBoost(Dist=ngboost.distns.MultivariateNormal(2),
                               n_estimators=self.num_estimators)
        
        self.model_function.fit(X=np.array(self.training_data.loc[:,self.covariate_labels]),
                                   Y=np.array(self.training_data.loc[:,["u_av","v_av"]]))
    
    def trained_pred_dist(self):
        if self.model_function is None:
            self.ngboost_pr()
        pred_dist = self.model_function.pred_dist(np.array(self.training_data.loc[:,self.covariate_labels]))
        self.trained_pred_dist = [pred_dist.loc,pred_dist.cov]
    
    def test_pred_dist(self):
        if self.model_function is None:
            self.ngboost_pr()
        pred_dist = self.model_function.pred_dist(np.array(self.test_data.loc[:,self.covariate_labels]))
        self.test_pred_dist = [pred_dist.loc,pred_dist.cov]

    #----------------------- 'immutable' properties -----------------------#
    @property
    def num_estimators(self):
        return self._num_estimators
    
    @num_estimators.setter
    def num_estimators(self,n):
        self._num_estimators = n
