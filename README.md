# MVP - Equipment Monitoring Diagnosis

The **Equipment Monitoring Diagnosis** is a simplified version of an artificial inteligence application to verify if an equipment is Faulty or not based on operating parameters data.
The API is built with python script and the dataset to train the model was imported and simplified to have only numerical data from this dataset: https://www.kaggle.com/datasets/dnkumars/industrial-equipment-monitoring-dataset


The application saves key parameters to an SQlite database, utilizing the SQLAlchemy library for database interactions. Eeach equipment is uniquely identified in the database by a composite primary key which consists of **"Type"** and **"Tag"** of the equipment.


## How to run the application

It is recommended to set up a dedicated virtual environment to run the application.  If you are using Conda to create a virtual environment, refer to the link: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html.

Open conda prompt and type:

```
conda create -n myenv --no-default-packages python
```


### Step 1: Install Dependencies

After creating the virtual environment, install all required libraries listed in the requirements.txt file.
Navigate to the folder containing the `requirements.txt` (/api) file and execute the following command:

```
(env)$ pip install -r requirements.txt
```

### Step 2: Run the API

To start the API, navigate to the folder containing the `app.py` file (/api) and use the following command:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

#### Optional: Development Mode
For development purposes, it is recommended to use the --reload flag. This allows the server to automatically restart whenever changes are made to the code:

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

### Step 3: Verify API Execution
Open http://localhost:5000/#/ in your browser to confirm the API is running successfully.

#### Swagger Documentation

The complete API documentation is available through the Swagger interface. This allows you to explore and test all available endpoints, including those not yet implemented in the HTML front-end.

To access the Swagger documentation, start the application and navigate to: http://localhost:5000/docs


