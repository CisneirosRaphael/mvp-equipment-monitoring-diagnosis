from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class EquipmentMonitoring(Base):
    __tablename__ = 'equipments'

    # Primary keys to uniquely identify a equipment being monitored
    type = Column("Type_pk1", String(50), primary_key =True)
    tag = Column("Tag_pk2", String(140), primary_key=True)

    temperature = Column("Temperature", Float)
    pressure = Column("Pressure", Float)
    vibration = Column("Vibration", Float)
    humidity = Column("Humidity", Float)
    outcome = Column("Faulty", Integer, nullable=True)
    date_input = Column(DateTime, default=datetime.now())
    
    def __init__(self, type: String, tag: String, temperature:Float, pressure: Float, 
                 vibration: Float, humidity: Float, outcome:int, 
                 date_input:Union[DateTime, None] = None):
        """
        Instantiate an equipment monitoring object.

        Arguments:
            type: string
                Equipment type.
            tag: str
                Machine Tag number.
            temperature: float
                Temperature reading at the time of observation (°C).
            pressure: float
                Pressure reading at the time of observation (in bar).
            vibration: str
                Vibration amplitude reading (normalized units).
            humidity: float
                Humidity percentage recorded at the location of the equipment.
            outcome: float
                Binary indicator (0 = Not Faulty, 1 = Faulty) to specify whether 
                the equipment is functioning properly or requires maintenance.
        """
        self.type = type.upper()
        self.tag = tag.upper()
        self.temperature = temperature
        self.pressure = pressure
        self.vibration = vibration
        self.humidity = humidity
        self.outcome = outcome

        # If no date is provided, use the system's current date/time
        if date_input:
            self.date_input = date_input