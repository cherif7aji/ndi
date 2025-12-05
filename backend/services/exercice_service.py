from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Exercice, Question, Solution, Paragraphe, Video, Image
from schemas import ExerciceCreate, ExerciceResponse, ExerciceUpdate, ExerciceCreateWithContent

class ExerciceService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_exercice(self, exercice_data: ExerciceCreate) -> Exercice:
        """Créer un nouvel exercice"""
        db_exercice = Exercice(**exercice_data.dict())
        self.db.add(db_exercice)
        self.db.commit()
        self.db.refresh(db_exercice)
        return db_exercice
    
    def get_exercice_by_id(self, exercice_id: int) -> Exercice:
        """Récupérer un exercice par ID"""
        exercice = self.db.query(Exercice).filter(Exercice.id == exercice_id).first()
        if not exercice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercice not found"
            )
        return exercice
    
    def get_all_exercices(self) -> List[Exercice]:
        """Récupérer tous les exercices"""
        return self.db.query(Exercice).all()
    
    def update_exercice(self, exercice_id: int, exercice_data: ExerciceUpdate) -> Exercice:
        """Mettre à jour un exercice"""
        exercice = self.get_exercice_by_id(exercice_id)
        
        update_data = exercice_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(exercice, field):
                setattr(exercice, field, value)
        
        self.db.commit()
        self.db.refresh(exercice)
        return exercice
    
    def delete_exercice(self, exercice_id: int) -> bool:
        """Supprimer un exercice"""
        exercice = self.get_exercice_by_id(exercice_id)
        self.db.delete(exercice)
        self.db.commit()
        return True
    
    # ============ WITH-CONTENT METHODS ============
    
    def create_exercice_with_content(self, exercice_data: ExerciceCreateWithContent) -> Exercice:
        """Créer un exercice avec tout son contenu (questions, solutions, paragraphes, vidéos, images)"""
        # 1. Créer l'exercice
        exercice_dict = exercice_data.dict(exclude={'questions', 'solutions', 'paragraphes', 'videos', 'images'})
        db_exercice = Exercice(**exercice_dict)
        self.db.add(db_exercice)
        self.db.flush()
        
        # 2. Créer les paragraphes
        for para_data in exercice_data.paragraphes:
            para_dict = para_data.dict() if hasattr(para_data, 'dict') else para_data
            if isinstance(para_dict, dict):
                para_dict = dict(para_dict)
            para_dict['exercice_id'] = db_exercice.id
            para_dict.pop('cours_id', None)
            db_para = Paragraphe(**para_dict)
            self.db.add(db_para)
        
        # 3. Créer les vidéos
        for video_data in exercice_data.videos:
            video_dict = video_data.dict() if hasattr(video_data, 'dict') else video_data
            if isinstance(video_dict, dict):
                video_dict = dict(video_dict)
            video_dict['exercice_id'] = db_exercice.id
            video_dict.pop('cours_id', None)
            db_video = Video(**video_dict)
            self.db.add(db_video)
        
        # 4. Créer les images
        for image_data in exercice_data.images:
            image_dict = image_data.dict() if hasattr(image_data, 'dict') else image_data
            if isinstance(image_dict, dict):
                image_dict = dict(image_dict)
            image_dict['exercice_id'] = db_exercice.id
            image_dict.pop('cours_id', None)
            db_image = Image(**image_dict)
            self.db.add(db_image)
        
        # 5. Créer les questions
        for question_data in exercice_data.questions:
            question_dict = question_data.dict() if hasattr(question_data, 'dict') else question_data
            if isinstance(question_dict, dict):
                question_dict = dict(question_dict)
            question_dict['exercice_id'] = db_exercice.id
            db_question = Question(**question_dict)
            self.db.add(db_question)
        
        # 6. Créer les solutions
        for solution_data in exercice_data.solutions:
            solution_dict = solution_data.dict() if hasattr(solution_data, 'dict') else solution_data
            if isinstance(solution_dict, dict):
                solution_dict = dict(solution_dict)
            solution_dict['exercice_id'] = db_exercice.id
            db_solution = Solution(**solution_dict)
            self.db.add(db_solution)
        
        self.db.commit()
        self.db.refresh(db_exercice)
        return db_exercice
    
    def get_exercice_with_content(self, exercice_id: int) -> Exercice:
        """Récupérer un exercice avec tout son contenu"""
        from sqlalchemy.orm import joinedload
        exercice = self.db.query(Exercice).options(
            joinedload(Exercice.questions),
            joinedload(Exercice.solutions),
            joinedload(Exercice.paragraphes),
            joinedload(Exercice.videos),
            joinedload(Exercice.images)
        ).filter(Exercice.id == exercice_id).first()
        
        if not exercice:
            raise HTTPException(status_code=404, detail="Exercice not found")
        return exercice
    
    def get_all_exercices_with_content(self) -> List[Exercice]:
        """Récupérer tous les exercices avec leur contenu"""
        from sqlalchemy.orm import joinedload
        return self.db.query(Exercice).options(
            joinedload(Exercice.questions),
            joinedload(Exercice.solutions),
            joinedload(Exercice.paragraphes),
            joinedload(Exercice.videos),
            joinedload(Exercice.images)
        ).all()
    
    def update_exercice_with_content(self, exercice_id: int, exercice_data: ExerciceCreateWithContent) -> Exercice:
        """Mettre à jour un exercice et son contenu"""
        exercice = self.get_exercice_by_id(exercice_id)
        
        # 1. Mettre à jour l'exercice
        exercice_dict = exercice_data.dict(exclude={'questions', 'solutions', 'paragraphes', 'videos', 'images'})
        for field, value in exercice_dict.items():
            if hasattr(exercice, field):
                setattr(exercice, field, value)
        
        # 2. Supprimer l'ancien contenu
        self.db.query(Paragraphe).filter(Paragraphe.exercice_id == exercice_id).delete()
        self.db.query(Video).filter(Video.exercice_id == exercice_id).delete()
        self.db.query(Image).filter(Image.exercice_id == exercice_id).delete()
        self.db.query(Question).filter(Question.exercice_id == exercice_id).delete()
        self.db.query(Solution).filter(Solution.exercice_id == exercice_id).delete()
        
        # 3. Recréer le contenu (même logique que create)
        for para_data in exercice_data.paragraphes:
            para_dict = para_data.dict() if hasattr(para_data, 'dict') else para_data
            if isinstance(para_dict, dict):
                para_dict = dict(para_dict)
            para_dict['exercice_id'] = exercice_id
            para_dict.pop('cours_id', None)
            self.db.add(Paragraphe(**para_dict))
        
        for video_data in exercice_data.videos:
            video_dict = video_data.dict() if hasattr(video_data, 'dict') else video_data
            if isinstance(video_dict, dict):
                video_dict = dict(video_dict)
            video_dict['exercice_id'] = exercice_id
            video_dict.pop('cours_id', None)
            self.db.add(Video(**video_dict))
        
        for image_data in exercice_data.images:
            image_dict = image_data.dict() if hasattr(image_data, 'dict') else image_data
            if isinstance(image_dict, dict):
                image_dict = dict(image_dict)
            image_dict['exercice_id'] = exercice_id
            image_dict.pop('cours_id', None)
            self.db.add(Image(**image_dict))
        
        for question_data in exercice_data.questions:
            question_dict = question_data.dict() if hasattr(question_data, 'dict') else question_data
            if isinstance(question_dict, dict):
                question_dict = dict(question_dict)
            question_dict['exercice_id'] = exercice_id
            self.db.add(Question(**question_dict))
        
        for solution_data in exercice_data.solutions:
            solution_dict = solution_data.dict() if hasattr(solution_data, 'dict') else solution_data
            if isinstance(solution_dict, dict):
                solution_dict = dict(solution_dict)
            solution_dict['exercice_id'] = exercice_id
            self.db.add(Solution(**solution_dict))
        
        self.db.commit()
        self.db.refresh(exercice)
        return exercice
