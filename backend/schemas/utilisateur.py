from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UtilisateurBase(BaseModel):
    username: str
    role: str = "user"

class UtilisateurCreate(BaseModel):
    username: str
    password: str
    # Le rôle n'est pas inclus - sera toujours "user"

class UtilisateurUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UtilisateurResponse(UtilisateurBase):
    id: int
    created_at: datetime
    is_active: bool
    joker_1: bool
    joker_2: bool
    joker_3: bool
    
    class Config:
        from_attributes = True
