

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class EnvironmentVariable(BaseModel):
    key: str
    value: str


class VsCodeStatus(Enum):
    RUNNING ="running"
    DELETED = "deleted"
    CREATED = "created"
    EXTENDED = "extended"


class VSCodeRequest(BaseModel):
    username: str
    minutes:  Optional[int] = 60
    seconds: Optional[int] = 0
    environmentVariables: Optional[List[EnvironmentVariable]] = []  

class VsCodeResponse(BaseModel):
    username: str
    message: Optional[str] = None
    status: Optional[VsCodeStatus]
    error_message: Optional[str] = None
    url: Optional[str] = None

class NamespaceResponse(BaseModel):    
    deployments :  List
