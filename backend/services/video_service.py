from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Video
from schemas import VideoCreate, VideoResponse, VideoUpdate

class VideoService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_video(self, video_data: VideoCreate) -> Video:
        """Créer une nouvelle vidéo"""
        db_video = Video(**video_data.dict())
        self.db.add(db_video)
        self.db.commit()
        self.db.refresh(db_video)
        return db_video
    
    def get_video_by_id(self, video_id: int) -> Video:
        """Récupérer une vidéo par ID"""
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found"
            )
        return video
    
    def get_all_videos(self) -> List[Video]:
        """Récupérer toutes les vidéos"""
        return self.db.query(Video).all()
    
    def update_video(self, video_id: int, video_data: VideoUpdate) -> Video:
        """Mettre à jour une vidéo"""
        video = self.get_video_by_id(video_id)
        
        update_data = video_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(video, field):
                setattr(video, field, value)
        
        self.db.commit()
        self.db.refresh(video)
        return video
    
    def delete_video(self, video_id: int) -> bool:
        """Supprimer une vidéo"""
        video = self.get_video_by_id(video_id)
        self.db.delete(video)
        self.db.commit()
        return True
