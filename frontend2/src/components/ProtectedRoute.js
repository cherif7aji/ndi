import React, { useState, useEffect } from 'react';
import { AuthService } from '../services/api';
import Auth from '../pages/Auth';
import './ProtectedRoute.css';

const ProtectedRoute = ({ children, authMode, onAuthAction }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    checkAuthentication();
  }, []);

  const checkAuthentication = async () => {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      setIsAuthenticated(false);
      setIsLoading(false);
      return;
    }

    try {
      // Vérifier si le token est valide en récupérant les infos utilisateur
      const response = await AuthService.getCurrentUser();
      setCurrentUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      // Token invalide ou expiré
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  // Affichage pendant la vérification
  if (isLoading) {
    return (
      <div className="auth-loading">
        <div className="loading-container">
          <div className="cyber-spinner"></div>
          <p>Vérification de l'authentification...</p>
        </div>
      </div>
    );
  }

  // Si non authentifié, afficher le formulaire d'authentification
  if (!isAuthenticated) {
    return (
      <div className="protected-route-auth">
        <div className="auth-required-message">
          <h2>🔒 Authentification requise</h2>
          <p>Vous devez vous connecter pour accéder à cette page.</p>
        </div>
        <Auth mode={authMode || 'login'} />
      </div>
    );
  }

  // Si authentifié, afficher le contenu protégé
  return children;
};

export default ProtectedRoute;
