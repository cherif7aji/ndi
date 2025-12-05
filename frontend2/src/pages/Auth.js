import React, { useState, useEffect } from 'react';
import { AuthService } from '../services/api';
import { LogIn, UserPlus, Eye, EyeOff, User, Lock, CheckCircle, AlertCircle, ArrowLeft } from 'lucide-react';
import './Auth.css';

const Auth = ({ mode = 'login' }) => {
  const [authMode, setAuthMode] = useState(mode);
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  // Keep internal state in sync when the dropdown selects a different mode
  useEffect(() => {
    setAuthMode(mode);
    setFormData({ username: '', password: '' });
    setMessage({ type: '', text: '' });
  }, [mode]);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Effacer le message d'erreur quand l'utilisateur tape
    if (message.type === 'error') {
      setMessage({ type: '', text: '' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      if (authMode === 'login') {
        const response = await AuthService.login(formData);
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        setMessage({ 
          type: 'success', 
          text: '✅ Connexion réussie ! Redirection en cours...' 
        });
        
        // Redirection après 2 secondes
        setTimeout(() => {
          window.location.reload(); // Recharger pour mettre à jour l'état d'authentification
        }, 2000);
        
      } else {
        await AuthService.register(formData);
        setMessage({ 
          type: 'success', 
          text: '✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter.' 
        });
        setFormData({ username: '', password: '' });
        
        // Passer automatiquement en mode connexion après inscription
        setTimeout(() => {
          setAuthMode('login');
          setMessage({ type: '', text: '' });
        }, 3000);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Une erreur est survenue';
      setMessage({ type: 'error', text: `❌ ${errorMessage}` });
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setAuthMode(authMode === 'login' ? 'register' : 'login');
    setFormData({ username: '', password: '' });
    setMessage({ type: '', text: '' });
  };

  return (
    <div className="auth-page fade-in">
      <div className="auth-container">
        <button 
          className="back-btn"
          onClick={() => {
            // Retourner à l'accueil en réinitialisant le mode auth
            window.dispatchEvent(new CustomEvent('resetAuthMode'));
          }}
          title="Retour à l'accueil"
        >
          <ArrowLeft size={16} />
          Retour
        </button>
        
        <div className="auth-header">
          <div className="auth-icon">
            {authMode === 'login' ? <LogIn size={32} /> : <UserPlus size={32} />}
          </div>
          <h1>{authMode === 'login' ? 'Connexion' : 'Créer un compte'}</h1>
          <p>
            {authMode === 'login' 
              ? 'Accédez à votre espace CyberSec Academy'
              : 'Rejoignez la communauté CyberSec Academy'
            }
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">
              <User size={16} />
              Nom d'utilisateur
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Entrez votre nom d'utilisateur"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              <Lock size={16} />
              Mot de passe
            </label>
            <div className="password-input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Entrez votre mot de passe"
                required
                disabled={loading}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                disabled={loading}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          {message.text && (
            <div className={`auth-message ${message.type}`}>
              {message.type === 'success' ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
              <span>{message.text}</span>
            </div>
          )}

          <button 
            type="submit" 
            className={`auth-submit-btn ${authMode}`}
            disabled={loading || !formData.username || !formData.password}
          >
            {loading ? (
              <div className="loading-spinner" />
            ) : (
              <>
                {authMode === 'login' ? <LogIn size={16} /> : <UserPlus size={16} />}
                {authMode === 'login' ? 'Se connecter' : 'Créer le compte'}
              </>
            )}
          </button>
        </form>

        <div className="auth-switch">
          <p>
            {authMode === 'login' 
              ? "Vous n'avez pas encore de compte ?" 
              : "Vous avez déjà un compte ?"
            }
          </p>
          <button 
            className="switch-mode-btn" 
            onClick={toggleMode}
            disabled={loading}
          >
            {authMode === 'login' ? 'Créer un compte' : 'Se connecter'}
          </button>
        </div>
      </div>

      <div className="auth-background">
        <div className="cyber-grid"></div>
        <div className="floating-elements">
          <div className="floating-element"></div>
          <div className="floating-element"></div>
          <div className="floating-element"></div>
        </div>
      </div>
    </div>
  );
};

export default Auth;
