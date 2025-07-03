import pickle

class Model:
    
    def __init__(self):
        """Instantiate the model"""
        self.model = None
    
    def load_model(self, path):
        """Load a .pkl model
        """
        
        if path.suffix('.pkl'):
            with open(path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            raise Exception('Not supported file extension!')
        return self.model
    
    def predictor(self, X_input):
        """Predict the healthy status of a machinery (faulty/ not faulty) based on a trainned model
        """
        if self.model is None:
            raise Exception('Model was not loaded. First, execute load_model().')
        diagnosis = self.model.predict(X_input)
        return diagnosis