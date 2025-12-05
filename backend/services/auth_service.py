from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import hashlib
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Utilisateur
from schemas import UtilisateurCreate, Token
from database import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifier un mot de passe"""
        # Utilisation de SHA256 pour simplifier (en production, utiliser bcrypt)
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    
    def get_password_hash(self, password: str) -> str:
        """Hacher un mot de passe"""
        # Utilisation de SHA256 pour simplifier (en production, utiliser bcrypt)
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Utilisateur]:
        """Authentifier un utilisateur"""
        user = self.db.query(Utilisateur).filter(Utilisateur.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Créer un token d'accès JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Vérifier et décoder un token JWT"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
    
    def register_user(self, user_data: UtilisateurCreate) -> Utilisateur:
        """Inscrire un nouvel utilisateur"""
        # Vérifier si l'utilisateur existe déjà
        existing_user = self.db.query(Utilisateur).filter(
            Utilisateur.username == user_data.username
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Créer le nouvel utilisateur (toujours avec le rôle "user")
        hashed_password = self.get_password_hash(user_data.password)
        db_user = Utilisateur(
            username=user_data.username,
            password_hash=hashed_password,
            role="user"  # Toujours "user" lors de l'inscription
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def login_user(self, username: str, password: str) -> Token:
        """Connecter un utilisateur"""
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    def get_current_user(self, token: str) -> Utilisateur:
        """Obtenir l'utilisateur actuel à partir du token"""
        username = self.verify_token(token)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = self.db.query(Utilisateur).filter(Utilisateur.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        return user
