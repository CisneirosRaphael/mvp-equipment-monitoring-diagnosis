from sklearn.metrics import accuracy_score

class Evaluator:
    
    def __init__(self):
        """Instantiate the evaluator"""
        pass

    def evaluate(self, model, X_test, Y_test):
        """ 
        Predict and evaluate the model.
        """
        predictions = model.predict(X_test)
        
        return accuracy_score(Y_test, predictions)