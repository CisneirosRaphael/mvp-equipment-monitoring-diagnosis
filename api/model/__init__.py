from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pathlib import Path

# importing the classes defined in the model
from model.base import Base
from model.equipment_monitoring import EquipmentMonitoring
from model.model import Model
from model.pipeline import Pipeline
from model.preprocessor import PreProcessor
from model.evaluator import Evaluator
from model.loader import Loader

# Define the path to the directory where the database will be stored
db_path = Path.cwd() / "database"
# check if the folder exists
if not db_path.exists():
   # create the directory if it does not exist
   Path.mkdir(db_path)

# Define the URL to access the database (using SQLite for local storage)
# The URL points to the 'equipments.sqlite3' file inside the specified directory
db_url = f'sqlite:///{str(db_path)}/equipments.sqlite3'

# Create an engine to connect to the database
engine = create_engine(db_url, echo=False)

# Instantiate a session maker bound to the engine
# The session will be used to perform operations on the database
Session = sessionmaker(bind=engine)

# Check if the database already existst
if not database_exists(engine.url):
    # Create the database if it does not exist
    create_database(engine.url) 

# Create the tables in the database based on the defined models
# If the tables do not exist
Base.metadata.create_all(engine)