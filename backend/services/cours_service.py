from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models import Cours, Paragraphe, Video, Image
from schemas import CoursCreate, CoursResponse, CoursUpdate, CoursCreateWithContent, CoursWithContentResponse

class CoursService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_cours(self, cours_data: CoursCreate) -> Cours:
        """Créer un nouveau cours"""
        db_cours = Cours(**cours_data.dict())
        self.db.add(db_cours)
        self.db.commit()
        self.db.refresh(db_cours)
        return db_cours
    
    def get_cours_by_id(self, cours_id: int) -> Cours:
        """Récupérer un cours par ID"""
        cours = self.db.query(Cours).filter(Cours.id == cours_id).first()
        if not cours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cours not found"
            )
        return cours
    
    def get_all_cours(self) -> List[Cours]:
        """Récupérer tous les cours"""
        return self.db.query(Cours).all()
    
    def update_cours(self, cours_id: int, cours_data: CoursUpdate) -> Cours:
        """Mettre à jour un cours"""
        cours = self.get_cours_by_id(cours_id)
        
        update_data = cours_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(cours, field):
                setattr(cours, field, value)
        
        self.db.commit()
        self.db.refresh(cours)
        return cours
    
    def delete_cours(self, cours_id: int) -> bool:
        """Supprimer un cours"""
        cours = self.get_cours_by_id(cours_id)
        self.db.delete(cours)
        self.db.commit()
        return True
    
    def create_cours_with_content(self, cours_data: CoursCreateWithContent) -> dict:
        """Créer un cours avec son contenu (paragraphes, vidéos, images)"""
        # Créer le cours
        cours_dict = cours_data.dict(exclude={'paragraphes', 'videos', 'images'})
        db_cours = Cours(**cours_dict)
        self.db.add(db_cours)
        self.db.commit()
        self.db.refresh(db_cours)
        
        # Ajouter les paragraphes
        for i, paragraphe_data in enumerate(cours_data.paragraphes or []):
            para_dict = paragraphe_data.dict() if hasattr(paragraphe_data, 'dict') else paragraphe_data
            paragraphe = Paragraphe(
                cours_id=db_cours.id,
                titre=para_dict.get('titre', f'Paragraphe {i + 1}'),
                contenu=para_dict.get('contenu', ''),
                type_paragraphe=para_dict.get('type_paragraphe', 'contenu'),
                ordre=para_dict.get('ordre', i + 1)
            )
            self.db.add(paragraphe)
        
        # Ajouter les vidéos
        for i, video_data in enumerate(cours_data.videos or []):
            vid_dict = video_data.dict() if hasattr(video_data, 'dict') else video_data
            video = Video(
                cours_id=db_cours.id,
                titre=vid_dict.get('titre', f'Vidéo {i + 1}'),
                url_video=vid_dict.get('url_video', ''),
                duree=vid_dict.get('duree', 0),
                ordre=vid_dict.get('ordre', i + 1)
            )
            self.db.add(video)
        
        # Ajouter les images
        for i, image_data in enumerate(cours_data.images or []):
            img_dict = image_data.dict() if hasattr(image_data, 'dict') else image_data
            image = Image(
                cours_id=db_cours.id,
                nom_fichier=img_dict.get('nom_fichier', f'image_{i + 1}'),
                extension=img_dict.get('extension', '.jpg'),
                alt_text=img_dict.get('alt_text', ''),
                description=img_dict.get('description', ''),
                contenu_base64=img_dict.get('contenu_base64', ''),
                taille_fichier=img_dict.get('taille_fichier', 0),
                ordre=img_dict.get('ordre', i + 1)
            )
            self.db.add(image)
        
        self.db.commit()
        self.db.refresh(db_cours)
        
        # Retourner le cours avec son contenu
        return self.get_cours_with_content(db_cours.id)
    
    def get_all_cours_with_content(self) -> List[dict]:
        """Récupérer tous les cours avec leur contenu complet"""
        cours_list = self.get_all_cours()
        
        result = []
        for cours in cours_list:
            cours_with_content = self.get_cours_with_content(cours.id)
            result.append(cours_with_content)
        
        return result
    
    def get_cours_with_content(self, cours_id: int) -> dict:
        """Récupérer un cours avec tout son contenu"""
        cours = self.get_cours_by_id(cours_id)
        
        # Récupérer le contenu séparément
        paragraphes = self.db.query(Paragraphe).filter(Paragraphe.cours_id == cours_id).order_by(Paragraphe.ordre).all()
        videos = self.db.query(Video).filter(Video.cours_id == cours_id).order_by(Video.ordre).all()
        images = self.db.query(Image).filter(Image.cours_id == cours_id).order_by(Image.ordre).all()
        
        # Construire la réponse
        return {
            "id": cours.id,
            "titre": cours.titre,
            "description": cours.description,
            "niveau": cours.niveau,
            "duree_estimee": cours.duree_estimee,
            "created_at": cours.created_at,
            "updated_at": cours.updated_at,
            "is_active": cours.is_active,
            "paragraphes": [
                {
                    "id": p.id,
                    "titre": p.titre,
                    "contenu": p.contenu,
                    "type_paragraphe": p.type_paragraphe,
                    "ordre": p.ordre
                } for p in paragraphes
            ],
            "videos": [
                {
                    "id": v.id,
                    "titre": v.titre,
                    "url_video": v.url_video,
                    "duree": v.duree,
                    "ordre": v.ordre
                } for v in videos
            ],
            "images": [
                {
                    "id": i.id,
                    "nom_fichier": i.nom_fichier,
                    "extension": i.extension,
                    "alt_text": i.alt_text,
                    "description": i.description,
                    "contenu_base64": i.contenu_base64,
                    "taille_fichier": i.taille_fichier,
                    "ordre": i.ordre
                } for i in images
            ],
            "exercices": []
        }
    
    def update_cours_with_content(self, cours_id: int, cours_data: CoursCreateWithContent) -> dict:
        """Mettre à jour un cours et son contenu"""
        cours = self.get_cours_by_id(cours_id)
        
        # Mettre à jour les données du cours
        cours_dict = cours_data.dict(exclude={'paragraphes', 'videos', 'images'})
        for field, value in cours_dict.items():
            if hasattr(cours, field) and value is not None:
                setattr(cours, field, value)
        
        # Supprimer l'ancien contenu
        self.db.query(Paragraphe).filter(Paragraphe.cours_id == cours_id).delete()
        self.db.query(Video).filter(Video.cours_id == cours_id).delete()
        self.db.query(Image).filter(Image.cours_id == cours_id).delete()
        
        # Ajouter le nouveau contenu
        for i, paragraphe_data in enumerate(cours_data.paragraphes or []):
            paragraphe = Paragraphe(
                cours_id=cours_id,
                titre=paragraphe_data.get('titre', f'Paragraphe {i + 1}'),
                contenu=paragraphe_data.get('contenu', ''),
                type_paragraphe=paragraphe_data.get('type_paragraphe', 'contenu'),
                ordre=paragraphe_data.get('ordre', i + 1)
            )
            self.db.add(paragraphe)
        
        for i, video_data in enumerate(cours_data.videos or []):
            video = Video(
                cours_id=cours_id,
                titre=video_data.get('titre', f'Vidéo {i + 1}'),
                url_video=video_data.get('url_video', ''),
                duree=video_data.get('duree', 0),
                ordre=video_data.get('ordre', i + 1)
            )
            self.db.add(video)
        
        for i, image_data in enumerate(cours_data.images or []):
            image = Image(
                cours_id=cours_id,
                nom_fichier=image_data.get('nom_fichier', f'image_{i + 1}'),
                extension=image_data.get('extension', '.jpg'),
                alt_text=image_data.get('alt_text', ''),
                description=image_data.get('description', ''),
                contenu_base64=image_data.get('contenu_base64', ''),
                taille_fichier=image_data.get('taille_fichier', 0),
                ordre=image_data.get('ordre', i + 1)
            )
            self.db.add(image)
        
        self.db.commit()
        self.db.refresh(cours)
        
        # Retourner le cours avec son contenu mis à jour
        return self.get_cours_with_content(cours_id)
