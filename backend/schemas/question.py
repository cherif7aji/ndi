from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionBase(BaseModel):
    texte_question: str
    type_question: str
    points: int = 10
    ordre: int
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    bonne_reponse: Optional[str] = None
    reponse_attendue: Optional[str] = None

class QuestionCreate(QuestionBase):
    exercice_id: int

class QuestionUpdate(BaseModel):
    texte_question: Optional[str] = None
    type_question: Optional[str] = None
    points: Optional[int] = None
    ordre: Optional[int] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    bonne_reponse: Optional[str] = None
    reponse_attendue: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: int
    exercice_id: int
    
    class Config:
        from_attributes = True
