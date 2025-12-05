from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SolutionBase(BaseModel):
    titre: str
    explication: str
    code_solution: Optional[str] = None
    ressources_supplementaires: Optional[str] = None

class SolutionCreate(SolutionBase):
    exercice_id: int

class SolutionResponse(SolutionBase):
    id: int
    exercice_id: int
    
    class Config:
        from_attributes = True
