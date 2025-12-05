from .utilisateur import UtilisateurBase, UtilisateurCreate, UtilisateurResponse, UtilisateurUpdate
from .cours import CoursBase, CoursCreate, CoursResponse, CoursUpdate, CoursWithContentResponse, CoursCreateWithContent, CoursCreateComplete
from .paragraphe import ParagrapheBase, ParagrapheCreate, ParagrapheResponse, ParagrapheUpdate
from .video import VideoBase, VideoCreate, VideoResponse, VideoUpdate
from .image import ImageCreate, ImageResponse, ImageUpdate
from .question import QuestionBase, QuestionCreate, QuestionResponse, QuestionUpdate
from .solution import SolutionBase, SolutionCreate, SolutionResponse
from .exercice import ExerciceBase, ExerciceCreate, ExerciceResponse, ExerciceUpdate, ExerciceWithContentResponse, ExerciceCreateWithContent
from .note import NoteBase, NoteCreate, NoteResponse, NoteUpdate
from .auth import Token, TokenData, LoginRequest
from .submission import ReponseSubmission, ExerciceSubmission, NoteCalculeeResponse

# Rebuild models pour résoudre les forward references
ExerciceWithContentResponse.model_rebuild()
CoursWithContentResponse.model_rebuild()
__all__ = [
    "UtilisateurBase", "UtilisateurCreate", "UtilisateurResponse", "UtilisateurUpdate",
    "CoursBase", "CoursCreate", "CoursResponse", "CoursUpdate", "CoursWithContentResponse", "CoursCreateWithContent", "CoursCreateComplete",
    "ParagrapheBase", "ParagrapheCreate", "ParagrapheResponse", "ParagrapheUpdate",
    "VideoBase", "VideoCreate", "VideoResponse", "VideoUpdate",
    "ImageCreate", "ImageResponse", "ImageUpdate",
    "ExerciceBase", "ExerciceCreate", "ExerciceResponse", "ExerciceUpdate", "ExerciceWithContentResponse", "ExerciceCreateWithContent",
    "QuestionBase", "QuestionCreate", "QuestionResponse", "QuestionUpdate",
    "SolutionBase", "SolutionCreate", "SolutionResponse",
    "NoteBase", "NoteCreate", "NoteResponse", "NoteUpdate",
    "Token", "TokenData", "LoginRequest",
    "ReponseSubmission", "ExerciceSubmission", "NoteCalculeeResponse"
]
