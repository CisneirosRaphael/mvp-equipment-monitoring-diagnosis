from sklearn.model_selection import train_test_split
import pickle
import numpy as np

class PreProcessor:

    def __init__(self):
        """Instantiate preprocessor"""
        pass

    def train_test_split(self, dataset, percentual_test, seed=8):
        """ Method wich executes the preprocessing. """
        # Data cleaning and outliers elimination

        # feature selection

        # Split between train and test
        X_train, X_test, Y_train, Y_test = self.__prepare_holdout(dataset,
                                                                  percentual_test,
                                                                  seed)
        
        return (X_train, X_test, Y_train, Y_test)
    
    def __prepare_holdout(self, dataset, percentual_test, seed):
        """ 
        Split data between trainning and test with holdout method.
        It considers that last variable is the target one.
        The parameter test_size is the percentual of data test.
        """
        data = dataset.values
        X = data[:, 0:-1]
        Y = data[:, -1]
        return train_test_split(X, Y, test_size=percentual_test, random_state=seed)
    
    def prepare_form(self, form):
        """ Prepare data from the front end to be used in model. """
        X_input = np.array([form.temperature, 
                            form.pressure, 
                            form.vibration, 
                            form.humidity
                        ])

        # reshape the input to fit the model
        X_input = X_input.reshape(1, -1)
        return X_input
    
    def scaler(self, X_train):
        """ Normalization of the data. """
        # normalization
        scaler = pickle.load(open('./MachineLearning/scalers/minmax_scaler_machinery.pkl', 'rb'))
        reescaled_X_train = scaler.transform(X_train)
        return reescaled_X_train