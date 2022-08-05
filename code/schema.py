from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

class record(BaseModel):
    id: int
    dt: datetime
    file_address: str
    ticket: str
    finished: bool
    result: Optional[str]

class records(BaseModel):
    record_ls:List[record]

class uploadLink(BaseModel):
    address:str

class ticket(BaseModel):
    ticket:str

class tickets(BaseModel):
    ticket_ls: List[str]

class extraction(BaseModel):
    EXTRACT_PW:str
