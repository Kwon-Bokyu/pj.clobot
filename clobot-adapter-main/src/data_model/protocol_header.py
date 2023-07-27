from typing import Optional
from pydantic import BaseModel

class ProtocolHeader(BaseModel):
  headerId: int
  timestamp: str
  version: str
  manufacturer: str
  serialNumber: str

class OptionalProtocolHeader(BaseModel):
  headerId: Optional[int] = None
  timestamp: Optional[str] = None
  version: Optional[str] = None
  manufacturer: Optional[str] = None
  serialNumber: Optional[str] = None
