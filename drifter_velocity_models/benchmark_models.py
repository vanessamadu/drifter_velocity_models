from model_classes import Model

#%%%%%%%%%%%%%%%%%%%%%%%%%%%% BATHTUB MODEL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class BathtubModel(Model):
    '''this is the first of two benchmark models to measure model performance against'''
    
    #==== magic methods ====#
    def __init__(self, loss_type,training_data,test_data):
        super().__init__(loss_type,training_data,test_data)
        self.model_type = "bathtub"