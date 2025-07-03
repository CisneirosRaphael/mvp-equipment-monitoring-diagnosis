from pydantic import BaseModel
from typing import Optional, List
from model.equipment_monitoring import EquipmentMonitoring
import json
import numpy as np

class EquipmentMonitoringSchema(BaseModel):
    """ 
    Defines the structure for inserting new equipment monitoring data.
    """
    type: str = "Pump"
    tag: str = "B-1225001A"
    temperature: float = 80
    pressure: float = 34
    vibration: float = 1.7
    humidity: float = 58
    
class EquipmentMonitoringViewSchema(BaseModel):
    """    
    Defines the structure for returning an equipment monitoring data from the database.    
    """
    type: str = "Pump"
    tag: str = "B-1225001A"
    temperature: float = 80
    pressure: float = 34
    vibration: float = 1.7
    humidity: float = 58
    outcome: int = None

    
class EquipmentMonitoringSearchSchema(BaseModel):
    """    
    Defines the structure for searching equipment monitoring data based on 
    equipment type and tag number.     
    """
    type: str = "Pump"
    tag: str = "B-1225001A"

class EquipmentMonitoringListSchema(BaseModel):
    """
    Defines the structure for returning a list of monitored equipment.
    """
    EquipmentMonitoring: List[EquipmentMonitoringViewSchema]

def show_equipment_monitoring(EquipmentMonitoring: EquipmentMonitoring):
    """ 
    Returns a structured representation of a monitored equipment data based on 
    EquipmentMonitoringViewSchema definition.
    """

    return {"type": EquipmentMonitoring.type,
            "tag": EquipmentMonitoring.tag,
            "temperature": EquipmentMonitoring.temperature,
            "pressure": EquipmentMonitoring.pressure,
            "vibration": EquipmentMonitoring.vibration,
            "humidity": EquipmentMonitoring.humidity,
            "outcome": EquipmentMonitoring.outcome
    }


def show_equipments_monitoring(equipments_monitoring: List[EquipmentMonitoring]):
    """ 
    Returns a structured representation of monitored equipment data 
    based on the EquipmentMonitoringViewSchema definition.
    """

    result = []
    for equipment in equipments_monitoring:
        result.append({"type": equipment.type,
                       "tag": equipment.tag,
                       "pressure": equipment.pressure,
                       "temperature": equipment.temperature,
                       "vibration": equipment.vibration,
                       "humidity": equipment.humidity,
                       "outcome": equipment.outcome})
    
    return {"EquipmentsMonitoring": result}



class EquipmentMonitoringDelSchema(BaseModel):
    """Defines the structure to show the equipament monitoring data after a deletion request.
    """
    type: str # equipment type
    tag: str # equipment tag


