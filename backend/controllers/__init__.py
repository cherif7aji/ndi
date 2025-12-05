from .auth_controller import auth_router
from .utilisateur_controller import utilisateur_router
from .cours_controller import cours_router
from .exercice_controller import exercice_router
from .question_controller import question_router
from .image_controller import image_router
from .video_controller import video_router
from .paragraphe_controller import paragraphe_router

__all__ = [
    "auth_router",
    "utilisateur_router",
    "cours_router", 
    "exercice_router",
    "question_router",
    "image_router",
    "video_router",
    "paragraphe_router"
]
