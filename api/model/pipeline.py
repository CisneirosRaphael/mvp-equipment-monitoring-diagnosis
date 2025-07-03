import pickle

class Pipeline:
    
    def __init__(self):
        """Instantiate pipeline"""
        self.pipeline = None
    
    def load_pipeline(self, path):
        """Load pipeline built with a trainned model
        """
        
        with open(path, 'rb') as file:
             self.pipeline = pickle.load(file)
        return self.pipeline