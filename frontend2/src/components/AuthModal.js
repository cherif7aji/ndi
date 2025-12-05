import React from 'react';
import { X, LogIn, UserPlus } from 'lucide-react';
import './AuthModal.css';

const AuthModal = ({ isOpen, onClose, onSelectAction, currentMode }) => {
  if (!isOpen) return null;

  const handleSelectLogin = () => {
    console.log('Login button clicked');
    if (onSelectAction) {
      onSelectAction('login');
    }
    if (onClose) {
      onClose(); // Fermer le modal après sélection
    }
  };

  const handleSelectRegister = () => {
    console.log('Register button clicked');
    if (onSelectAction) {
      onSelectAction('register');
    }
    if (onClose) {
      onClose(); // Fermer le modal après sélection
    }
  };

  return (
    <div className="auth-modal">
      <div className="auth-modal-header">
        <h3>🛡️ Authentification</h3>
        <button className="close-btn" onClick={onClose}>
          <X size={20} />
        </button>
      </div>
      
      <div className="auth-modal-content">
        <p>Choisissez une action pour continuer :</p>
        
        <div className="auth-actions">
          <button 
            className={`auth-action-btn login-btn ${currentMode === 'login' ? 'active' : ''}`}
            onClick={handleSelectLogin}
          >
            <LogIn size={24} />
            <div className="action-content">
              <h4>Se connecter</h4>
              <p>Accédez à votre compte existant</p>
            </div>
          </button>
          
          <button 
            className={`auth-action-btn register-btn ${currentMode === 'register' ? 'active' : ''}`}
            onClick={handleSelectRegister}
          >
            <UserPlus size={24} />
            <div className="action-content">
              <h4>Créer un compte</h4>
              <p>Rejoignez l'Academy</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;
