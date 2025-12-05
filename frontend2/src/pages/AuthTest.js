import React, { useState } from 'react';
import { AuthService } from '../services/api';
import './AuthTest.css';

const AuthTest = () => {
  const [registerData, setRegisterData] = useState({ username: '', password: '' });
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [result, setResult] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token') || '');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await AuthService.register(registerData);
      setResult(`✅ Inscription réussie: ${JSON.stringify(response.data, null, 2)}`);
      setRegisterData({ username: '', password: '' });
    } catch (error) {
      setResult(`❌ Erreur inscription: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await AuthService.login(loginData);
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setToken(access_token);
      setResult(`✅ Connexion réussie! Token: ${access_token.substring(0, 50)}...`);
      setLoginData({ username: '', password: '' });
    } catch (error) {
      setResult(`❌ Erreur connexion: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleGetCurrentUser = async () => {
    try {
      const response = await AuthService.getCurrentUser();
      setCurrentUser(response.data);
      setResult(`✅ Utilisateur actuel: ${JSON.stringify(response.data, null, 2)}`);
    } catch (error) {
      setResult(`❌ Erreur récupération utilisateur: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLogout = () => {
    AuthService.logout();
    setToken('');
    setCurrentUser(null);
    setResult('✅ Déconnexion réussie');
  };

  return (
    <div className="auth-test fade-in">
      <h1>🧪 Test d'Authentification</h1>
      <p>Interface de test pour la nouvelle structure utilisateur (username + password uniquement)</p>

      <div className="test-grid">
        {/* Inscription */}
        <div className="test-card">
          <h3>📝 Inscription</h3>
          <form onSubmit={handleRegister}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={registerData.username}
                onChange={(e) => setRegisterData({...registerData, username: e.target.value})}
                placeholder="Nom d'utilisateur"
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={registerData.password}
                onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                placeholder="Mot de passe"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">S'inscrire</button>
          </form>
        </div>

        {/* Connexion */}
        <div className="test-card">
          <h3>🔐 Connexion</h3>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={loginData.username}
                onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                placeholder="Nom d'utilisateur"
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={loginData.password}
                onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                placeholder="Mot de passe"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">Se connecter</button>
          </form>
        </div>

        {/* Actions utilisateur */}
        <div className="test-card">
          <h3>👤 Utilisateur actuel</h3>
          <div className="user-actions">
            <button 
              onClick={handleGetCurrentUser} 
              className="btn btn-secondary"
              disabled={!token}
            >
              Récupérer infos utilisateur
            </button>
            <button 
              onClick={handleLogout} 
              className="btn btn-danger"
              disabled={!token}
            >
              Se déconnecter
            </button>
          </div>
          
          {currentUser && (
            <div className="user-info">
              <h4>Informations utilisateur:</h4>
              <p><strong>ID:</strong> {currentUser.id}</p>
              <p><strong>Username:</strong> {currentUser.username}</p>
              <p><strong>Rôle:</strong> {currentUser.role}</p>
              <p><strong>Actif:</strong> {currentUser.is_active ? 'Oui' : 'Non'}</p>
              <p><strong>Jokers:</strong> {currentUser.joker_1 ? '🃏' : '❌'} {currentUser.joker_2 ? '🃏' : '❌'} {currentUser.joker_3 ? '🃏' : '❌'}</p>
            </div>
          )}
        </div>

        {/* État du token */}
        <div className="test-card">
          <h3>🎫 Token JWT</h3>
          <div className="token-info">
            {token ? (
              <>
                <p className="token-status success">✅ Token présent</p>
                <p className="token-preview">{token.substring(0, 50)}...</p>
              </>
            ) : (
              <p className="token-status error">❌ Aucun token</p>
            )}
          </div>
        </div>
      </div>

      {/* Résultats */}
      {result && (
        <div className="result-section">
          <h3>📊 Résultat:</h3>
          <pre className="result-output">{result}</pre>
        </div>
      )}
    </div>
  );
};

export default AuthTest;
