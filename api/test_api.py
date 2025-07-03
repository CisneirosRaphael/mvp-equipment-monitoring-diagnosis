from pathlib import Path
import pytest
from model import Pipeline, Evaluator, Loader
import pandas as pd

def test_accuracy():
    file = Path.cwd() / 'api' / 'MachineLearning' / 'pipeline' / 'nb_diagnosis_pipeline.pkl'
    golden_set = Path.cwd() /'api' / 'MachineLearning' / 'data' / 'golden_dataset.csv'

    # Instantiates classes
    pipeline = Pipeline()
    evaluator = Evaluator()
    loader = Loader()
    
    dataset = loader.load_data(golden_set)

    array = dataset.values
    X = array[:,0:-1]
    y = array[:,-1]

    model = pipeline.load_pipeline(file)
    assert evaluator.evaluate(model,X,y) >= 0.98

    



