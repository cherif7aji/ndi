from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .paragraphe import ParagrapheResponse
    from .video import VideoResponse
    from .image import ImageResponse
    from .question import QuestionResponse
    from .solution import SolutionResponse

class ExerciceBase(BaseModel):
    titre: str
    description: str
    type_exercice: str  # QCM, pratique, recherche_faille
    difficulte: Optional[str] = None
    points_max: int = 100
    temps_limite: Optional[int] = None
    ordre: int

class ExerciceCreate(ExerciceBase):
    cours_id: int

class ExerciceUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    type_exercice: Optional[str] = None
    difficulte: Optional[str] = None
    points_max: Optional[int] = None
    temps_limite: Optional[int] = None
    ordre: Optional[int] = None

class ExerciceResponse(ExerciceBase):
    id: int
    cours_id: int
    
    class Config:
        from_attributes = True

# Schémas pour les réponses avec contenu
class ExerciceWithContentResponse(ExerciceResponse):
    """Exercice avec son contenu (paragraphes, vidéos, images, questions)"""
    paragraphes: List['ParagrapheResponse'] = []
    videos: List['VideoResponse'] = []
    images: List['ImageResponse'] = []
    questions: List['QuestionResponse'] = []
    solutions: List['SolutionResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)

# Schémas pour création avec contenu
class ExerciceCreateWithContent(ExerciceCreate):
    """Créer un exercice avec tout son contenu"""
    paragraphes: List[Any] = []
    videos: List[Any] = []
    images: List[Any] = []
    questions: List[Any] = []
    solutions: List[Any] = []

# Rebuild model après import des dépendances
# Ceci sera appelé automatiquement lors de l'import du module __init__.py
