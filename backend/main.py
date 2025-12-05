from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables

# Import des routers
from controllers import (
    auth_router,
    utilisateur_router,
    cours_router,
    exercice_router,
    question_router,
    image_router,
    video_router,
    paragraphe_router
)
from controllers.submission_controller import submission_router

# Créer l'application FastAPI
app = FastAPI(
    title="Security Learning Platform API",
    description="API pour une plateforme d'apprentissage de la sécurité web avec JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer les tables au démarrage
@app.on_event("startup")
def startup_event():
    create_tables()
    print("🚀 Security Learning Platform API started!")
    print("📖 Documentation: http://localhost:8000/docs")

# Inclure tous les routers
app.include_router(auth_router)
app.include_router(utilisateur_router)
app.include_router(cours_router)
app.include_router(exercice_router)
app.include_router(question_router)
app.include_router(image_router)
app.include_router(video_router)
app.include_router(paragraphe_router)
app.include_router(submission_router)

@app.get("/")
def read_root():
    """Route de base"""
    return {
        "message": "Security Learning Platform API",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "JWT Authentication",
            "User Management", 
            "Course Management",
            "Exercise System",
            "Question & Answer System",
            "Progress Tracking",
            "Unified Image Management",
            "Unified Video Management", 
            "Unified Content Management"
        ],
        "documentation": "/docs"
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "database": "connected",
        "authentication": "enabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
