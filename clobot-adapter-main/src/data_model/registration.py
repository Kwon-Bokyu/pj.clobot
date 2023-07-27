from typing import List, Optional
from pydantic import BaseModel
from data_model.protocol_header import ProtocolHeader, OptionalProtocolHeader

class InstantAction(BaseModel):
  actionId: str
  actionType: str
  blockingType: str

class PhysicalParameters(BaseModel):
  accelerationMax: float
  decelerationMax: float
  speedMax: float
  rotationSpeedMax: float
  tiltAngleMax: int
  tiltSpeedMax: int

class Connection(ProtocolHeader, BaseModel):
  connectionState: str

class InstantActions(OptionalProtocolHeader, BaseModel):
  actions: Optional[List[InstantAction]] = None

class Factsheet(ProtocolHeader, BaseModel):
  physicalParameters: Optional[PhysicalParameters] = None
