from pydantic import BaseModel, Field
from typing import Optional

class Event(BaseModel):
    '''  
    Calendar event
    '''
    summary: str
    description: str
    start_iso_date_time: str
    end_iso_date_time: str
    location: str
    
class Todo(BaseModel):
    '''
    TODO task.
    '''
    description: str 
    details: str 
    deadline_iso_datetime: Optional[str]

class EmailAnalysis(BaseModel):
    '''
    Result of an analysis.
    '''
    sender: str 
    events: list[Event] | None  
    todos: list[Todo] | None 
    priority: str 
    summary: str 
