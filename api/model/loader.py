import pandas as pd

class Loader:

    def __init__(self):
        """Instantiate the loader"""
        pass

    def load_data(self, url: str):
        """ Load and return a pandas DataFrame from a csv file.
        """
        
        return pd.read_csv(url, header=0,
                           skiprows=0, delimiter=',') 
    