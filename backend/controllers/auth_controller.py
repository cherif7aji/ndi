from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import AuthService
from schemas import Token, UtilisateurCreate, UtilisateurResponse, LoginRequest
from models import Utilisateur

router = APIRouter(prefix="/auth", tags=["Authentication"])

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> Utilisateur:
    """Dependency pour obtenir l'utilisateur actuel"""
    return auth_service.get_current_user(credentials.credentials)

def get_current_active_user(current_user: Utilisateur = Depends(get_current_user)) -> Utilisateur:
    """Dependency pour obtenir l'utilisateur actuel actif"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_admin_user(current_user: Utilisateur = Depends(get_current_active_user)) -> Utilisateur:
    """Dependency pour obtenir l'utilisateur admin actuel"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.post("/register", response_model=UtilisateurResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UtilisateurCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Inscription d'un nouvel utilisateur"""
    return auth_service.register_user(user_data)

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Connexion d'un utilisateur"""
    return auth_service.login_user(login_data.username, login_data.password)

@router.get("/me", response_model=UtilisateurResponse)
def get_current_user_info(current_user: Utilisateur = Depends(get_current_active_user)):
    """Obtenir les informations de l'utilisateur connecté"""
    return current_user

@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: Utilisateur = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Rafraîchir le token d'accès"""
    from datetime import timedelta
    from database import settings
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.put("/update-profile", response_model=UtilisateurResponse)
def update_profile(
    profile_data: dict,
    current_user: Utilisateur = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    ⚠️ VULNÉRABILITÉ: Mass Assignment
    Cet endpoint accepte TOUS les champs sans validation!
    Un utilisateur peut modifier son rôle pour devenir admin.
    """
    # VULNÉRABLE: Accepte tous les champs du dictionnaire
    for key, value in profile_data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

# Export du router
auth_router = router
