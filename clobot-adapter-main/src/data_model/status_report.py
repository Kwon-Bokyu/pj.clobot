from typing import List, Optional
from pydantic import BaseModel
from data_model.protocol_header import ProtocolHeader

class NodePosition(BaseModel):
  x: float
  y: float
  theta: float

class NodeState(BaseModel):
  nodeId: str
  sequenceId: int
  nodePosition: NodePosition
  released: bool

class EdgeState(BaseModel):
  edgeId: str
  sequenceId: int
  released: bool

class BatteryState(BaseModel):
  batteryCharge: float
  charging: bool
  batteryVoltage: Optional[float] = None
  batteryCurrent: Optional[float] = None
  batteryHealth: Optional[float] = None

class Error(BaseModel):
  errorType: str
  errorLevel: str
  errorReferences: List[str]

class AgvPosition(BaseModel):
  x: float
  y: float
  theta: float
  mapId: str
  positionInitialized: bool

class Velocity(BaseModel):
  vx: float
  vy: float
  omega: float

class ActionState(BaseModel):
  actionId: str
  actionStatus: str

class TrayState(BaseModel):
  angle: float

class State(ProtocolHeader, BaseModel):
  orderId: str
  orderUpdateId: int
  lastNodeId: str
  lastNodeSequenceId: int
  nodeStates: List[NodeState]
  edgeStates: List[EdgeState]
  driving: bool
  batteryState: BatteryState
  operatingMode: str
  errors: List[Error]
  agvPosition: AgvPosition
  velocity: Velocity
  actionStates: List[ActionState]
  trayState: Optional[TrayState] = None #문서와 다름
