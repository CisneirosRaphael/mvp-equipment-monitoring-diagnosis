from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS

# API data
info = Info(title="API - Equipment Monitoring", version="1.0.0")
app = OpenAPI(__name__, info=info, static_folder='../front', static_url_path='/front')
CORS(app)

# Define tags for API endpoints
home_tag = Tag(name="Documentation", description="Select documentation type")
equipments_monitoring_tag = Tag(name="EquipmentsMonitoring", 
                          description="Add, delete and visualize equipment monitoring data to the database")

@app.get('/', tags=[home_tag])
def home():
    """ Redirect to index.html of the front end.
    """
    return redirect('/front/index.html')

@app.get('/docs', tags=[home_tag])
def docs():
    """ Redirect to /openapi, the screen which allows to choose the documentation type.
    """
    return redirect('/openapi')


@app.post('/equipment_monitoring', tags=[equipments_monitoring_tag],
          responses={"200": EquipmentMonitoringViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_equipment_monitoring(form: EquipmentMonitoringSchema):
    """
    Add new Equipment monitoring data to the database.

    Returns:
      Representation of the equipments monitoring data and its diagnosis prediction
    (faulty/not faulty).
    """
    
    # Instantiates classes
    preprocessor = PreProcessor()
    pipeline = Pipeline()
        
    # Prepare data for the model
    X_input = preprocessor.prepare_form(form)
    # load model
    model_path = './MachineLearning/pipeline/nb_diagnosis_pipeline.pkl' 
    model = pipeline.load_pipeline(model_path)
    # Executing prediction
    outcome = int(model.predict(X_input)[0])

    equipment_monitoring = EquipmentMonitoring(
        type = form.type,
        tag = form.tag,
        temperature = form.temperature,
        pressure = form.pressure,
        vibration = form.vibration,
        humidity = form.humidity,
        outcome = outcome
        )
    
    logger.debug(f"Adding equipment monitoring data: '{equipment_monitoring.type} \
                 {equipment_monitoring.tag}'")
    try:
        # connect to the base
        session = Session()
        # add new equipment monitoring to the database
        session.add(equipment_monitoring)
        session.commit()

        logger.debug(f"Added equipment monitoring data for '{equipment_monitoring.type}\
                     {equipment_monitoring.tag}'")
        return show_equipment_monitoring(equipment_monitoring), 200
    except IntegrityError as e:
        # handle duplicate entries (IntegrityError)
        error_msg = "Equipment monitoring data already exists in the database."
        logger.warning(f"Failed to add equipment monitoring data for '{equipment_monitoring.type} \
                       {equipment_monitoring.tag}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Handle unexpected errors
        error_msg = "It was not possible to save this equipment monitoring data to the database."
        logger.warning(f"Failed to add '{equipment_monitoring.type} \
                       {equipment_monitoring.tag}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/equipments_monitoring', tags=[equipments_monitoring_tag],
         responses={"200": EquipmentMonitoringListSchema, "404": ErrorSchema, "500": ErrorSchema})
def get_equipments_monitoring():
    """ 
    Retrieve all equipments monitoring data stored in the database.

    Returns:
        List of equipments monitoring data.
    """
    logger.debug(f"Retrieving equipments monitoring data from the database")

    # Connect to the database
    session = Session()
    # Query all equipment monitoring data
    equipments_monitoring = session.query(EquipmentMonitoring).all()
    print(equipments_monitoring)
    if not equipments_monitoring:
        logger.debug("No equipment monitoring data found in the database.")
        return {"Equipments": []}, 200
    else:
        logger.debug(f"Found {len(equipments_monitoring)} equipment(s) monitoring data in the database")
        # Return a representation of the equipment monitoring data
        return show_equipments_monitoring(equipments_monitoring), 200

@app.get('/equipment_monitoring', tags=[equipments_monitoring_tag],
         responses={"200": EquipmentMonitoringViewSchema, "404": ErrorSchema})
def get_equipment_monitoring_data(query: EquipmentMonitoringSearchSchema): 
    """ 
    Search for a specific equipment monitoring data based on equipment type and tag number.

    Returns: 
        Representation of the found equipment monitoring data.
    """
    
    equipment_monitoring_type = query.type.upper()
    equipment_monitoring_tag = query.tag.upper()
    
    logger.debug(f"Searching for equipment monitoring data for '{equipment_monitoring_type} \
                 {equipment_monitoring_tag}'")
    
    # Connect to the database
    session = Session()
    # Do the search
    equipment_monitoring = session.query(EquipmentMonitoring).filter( 
        EquipmentMonitoring.type == equipment_monitoring_type, 
        EquipmentMonitoring.tag == equipment_monitoring_tag).first()

    if not equipment_monitoring:
        error_msg = "Equipment monitoring data not found in the database."
        logger.warning(f"Failed to find '{equipment_monitoring_type} \
                       {equipment_monitoring_tag}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Equipment monitoring data found: '{equipment_monitoring_type} \
                     {equipment_monitoring_tag}'")
        # Return a representation of the equipment monitoring data
        return show_equipment_monitoring(equipment_monitoring), 200


@app.delete('/equipment_monitoring', tags=[equipments_monitoring_tag],
            responses={"200": EquipmentMonitoringDelSchema, "404": ErrorSchema})
def del_equipment_monitoring(query: EquipmentMonitoringSearchSchema):
    """
    Delete Equipment monitoring data based on equipment type and tag number.

    Returns:
        Confirmation of deletion or error message.
    """
    equipment_monitoring_type = unquote(query.type).upper()
    equipment_monitoring_tag = unquote(query.tag).upper()

    logger.debug(f"Deleting equipment monitoring data '{equipment_monitoring_type} \
                 '{equipment_monitoring_tag}'")
    
    # Connect to the database
    session = Session()
    # Delete equipment monitoring data
    count = session.query(EquipmentMonitoring).filter( 
        EquipmentMonitoring.type == equipment_monitoring_type, 
        EquipmentMonitoring.tag == equipment_monitoring_tag).delete()
    session.commit()

    if count:
        logger.debug(f"Equipment monitoring data deleted: '{equipment_monitoring_type} \
                       {equipment_monitoring_tag}'")
        return {"Type": equipment_monitoring_type, \
                "Tag": equipment_monitoring_tag}, 200
    else:
        error_msg = "Equipment monitoring data not found in the database."
        logger.warning(f"Failed to delete equipment monitoring data for '{equipment_monitoring_type} \
                       {equipment_monitoring_tag}', {error_msg}")
        return {"message": error_msg}, 404

    
if __name__ == '__main__':
    app.run(debug=True)