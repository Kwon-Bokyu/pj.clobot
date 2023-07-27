from typing import List, Optional
from pydantic import BaseModel
from data_model.protocol_header import ProtocolHeader

class NodePosition(BaseModel):
  x: float
  y: float
  theta: float

class ActionParameter(BaseModel):
  key: str
  value: float

class InstantAction(BaseModel):
  actionId: str
  actionType: str
  blockingType: str
  actionParameters: Optional[List[ActionParameter]] = None

class Node(BaseModel):
  nodeId: Optional[str] = None
  sequenceId: int
  nodePosition: NodePosition
  actions: Optional[List[InstantAction]] = None # tilt: require, others: X

class Edge(BaseModel):
  edgeId: Optional[str] = None
  sequenceId: int
  maxSpeed: float
  maxAcceleration: float
  maxDeceleration: float
  startNodeId: Optional[str] = None
  endNodeId: Optional[str] = None
  avoidance: bool

class Order(ProtocolHeader, BaseModel):
  orderId: str
  orderUpdateId: int
  nodes: List[Node]
  edges: Optional[List[Edge]] = None
