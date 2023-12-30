from model_classes import Model
# import packages
import numpy as np
import ngboost
from scipy import stats

class NGBoostModel(Model):

    def __init__(self,loss_type,training_data,test_data,covariate_labels,num_estimators):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "ngboost_pr"
        self.covariate_labels = covariate_labels
        self.num_estimators = num_estimators
        # model specification
        self.model_function = None
        # predictions (save for reuse)
        self.trained_realisations = None
        self.test_realisations = None
        ## average of predictions for rmse
        self.trained_prediction = None
        self.testing_prediction = None

    #------------------------ model constructions -------------------------#
    def ngboost_pr(self):
        '''return probabilistic regression model'''
        self.model_function = ngboost.NGBoost(Dist=ngboost.distns.MultivariateNormal(2),
                               n_estimators=self.num_estimators)
        
        self.model_function.fit(X=np.array(self.training_data.loc[:,self.covariate_labels]),
                                   Y=np.array(self.training_data.loc[:,["u","v"]]))
    
    def trained_pred_dist(self):
        if self.model_function is None:
            self.ngboost_pr()
        pred_dist = self.model_function.pred_dist(np.array(self.training_data.loc[:,self.covariate_labels]))
        self.trained_distribution =[stats.multivariate_normal(pred_dist.loc[ii,:],pred_dist.cov[ii,:,:]) for ii in range(pred_dist.loc.shape[0])]
    
    def test_pred_dist(self):
        if self.model_function is None:
            self.ngboost_pr()
        pred_dist = self.model_function.pred_dist(np.array(self.test_data.loc[:,self.covariate_labels]))
        self.test_distribution = [stats.multivariate_normal(pred_dist.loc[ii,:],pred_dist.cov[ii,:,:]) for ii in range(pred_dist.loc.shape[0])]

    #----------------------- 'immutable' properties -----------------------#
    @property
    def num_estimators(self):
        return self._num_estimators
    
    @num_estimators.setter
    def num_estimators(self,n):
        self._num_estimators = n

    #----------------------- predictions -----------------------#
    def trained_predictions(self,num_pred):
        if self.trained_distribution is None:
            self.trained_pred_dist()
        self.trained_realisations = [distribution.rvs(num_pred) for distribution in self.trained_distribution]
    
    def testing_predictions(self,num_pred):
        if self.test_distribution is None:
            self.test_pred_dist()
        self.test_realisations = [distribution.rvs(num_pred) for distribution in self.test_distribution]

    def calculate_trained_prediction(self):
        if self.trained_realisations is None:
            raise AttributeError("no realisations of the trained mvn distribution. First run `self.trained_predictions(num_pred)`.")
        self.trained_prediction = np.mean(self.trained_realisations,axis=1)

    def calculate_testing_prediction(self):
        if self.test_realisations is None:
            raise AttributeError("no realisations of the test mvn distribution. First run `self.testing_predictions(num_pred)`.")
        self.testing_prediction =  np.mean(self.test_realisations,axis=1)

    

    