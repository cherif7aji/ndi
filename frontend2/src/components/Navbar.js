import React, { useState, useEffect } from 'react';
import { 
  User, 
  LogOut,
  Menu,
  LogIn
} from 'lucide-react';
import AuthModal from './AuthModal';
import './Navbar.css';

const Navbar = ({ onToggleSidebar, onAuthAction, currentAuthMode }) => {
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  // Vérifier l'authentification au chargement et écouter les changements
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        setIsAuthenticated(true);
        // Récupérer les infos utilisateur via API
        try {
          const response = await fetch('http://localhost:8000/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (response.ok) {
            const userData = await response.json();
            setCurrentUser(userData);
          } else {
            setCurrentUser({ username: 'Utilisateur', role: 'user' });
          }
        } catch (error) {
          console.error('Erreur lors de la récupération des données utilisateur:', error);
          setCurrentUser({ username: 'Utilisateur', role: 'user' });
        }
      } else {
        setIsAuthenticated(false);
        setCurrentUser(null);
      }
    };

    checkAuth();

    // Écouter les changements du localStorage (connexion/déconnexion)
    const handleStorageChange = () => {
      checkAuth();
    };

    window.addEventListener('storage', handleStorageChange);
    
    // Écouter aussi les changements internes (même onglet)
    const originalSetItem = localStorage.setItem;
    const originalRemoveItem = localStorage.removeItem;
    
    localStorage.setItem = function(key, value) {
      originalSetItem.apply(this, arguments);
      if (key === 'access_token') {
        checkAuth();
      }
    };
    
    localStorage.removeItem = function(key) {
      originalRemoveItem.apply(this, arguments);
      if (key === 'access_token') {
        checkAuth();
      }
    };

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      localStorage.setItem = originalSetItem;
      localStorage.removeItem = originalRemoveItem;
    };
  }, []);


  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setCurrentUser(null);
    setShowUserDropdown(false);
    window.location.reload();
  };

  const handleAuthModalSelect = (action) => {
    console.log('Auth modal select:', action);
    setShowAuthModal(false); // Fermer le modal après sélection
    if (onAuthAction) {
      onAuthAction(action);
    }
  };

  const handleAuthButtonClick = () => {
    console.log('Auth button clicked, current modal state:', showAuthModal);
    // Toujours basculer l'état du modal
    const newModalState = !showAuthModal;
    setShowAuthModal(newModalState);
    
    // Si on ferme le modal, réinitialiser le mode auth
    if (!newModalState && onAuthAction) {
      console.log('Closing modal, resetting auth mode');
      onAuthAction(null);
    }
  };

  return (
    <header className="navbar">
      {/* Section gauche - vide */}
      <div className="navbar-left">
        <button 
          className="mobile-menu-btn"
          onClick={onToggleSidebar}
          title="Menu"
        >
          <Menu size={20} />
        </button>
      </div>

      {/* Section droite */}
      <div className="navbar-right">
        {isAuthenticated ? (
          <div className="user-menu">
            <button 
              className="user-btn"
              onClick={() => setShowUserDropdown(!showUserDropdown)}
            >
              <div className="user-avatar">
                <User size={16} />
              </div>
            </button>

            {showUserDropdown && (
              <div className="user-dropdown">
                <div className="dropdown-header">
                  <div className="user-avatar large">
                    <User size={20} />
                  </div>
                  <div>
                    <div className="dropdown-user-name">{currentUser?.username || 'Utilisateur'}</div>
                    <div className="dropdown-user-email">{currentUser?.role === 'admin' ? 'Administrateur' : 'Membre'}</div>
                  </div>
                </div>
                
                <div className="dropdown-divider"></div>
                
                <div className="dropdown-menu">
                  <button className="dropdown-item logout" onClick={handleLogout}>
                    <LogOut size={16} />
                    <span>Déconnexion</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Bouton de connexion (icône seulement) */
          <div className="auth-btn-container">
            <button 
              className="user-btn"
              onClick={handleAuthButtonClick}
              title="Se connecter / Créer un compte"
            >
              <div className="user-avatar">
                <LogIn size={18} />
              </div>
            </button>
            {/* Modal d'authentification */}
            {showAuthModal && (
              <AuthModal 
                isOpen={showAuthModal}
                onClose={() => setShowAuthModal(false)}
                onSelectAction={handleAuthModalSelect}
                currentMode={currentAuthMode}
              />
            )}
          </div>
        )}
      </div>

      {/* Overlay invisible pour fermer les dropdowns */}
      {showUserDropdown && (
        <div 
          className="dropdown-overlay"
          onClick={() => {
            setShowUserDropdown(false);
          }}
        />
      )}
    </header>
  );
};

export default Navbar;
