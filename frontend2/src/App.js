import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Auth from './pages/Auth';
import AuthTest from './pages/AuthTest';
import CoursList from './pages/CoursList';
import CoursForm from './pages/CoursForm';
import CoursDetails from './pages/CoursDetails';
import ExercicesList from './pages/ExercicesList';
import ExerciceForm from './pages/ExerciceForm';
import ExerciceDetails from './pages/ExerciceDetails';
import ExercicePlayer from './pages/ExercicePlayer';
import MiseEnPratique from './pages/MiseEnPratique';
import MiseEnPratiqueForm from './pages/MiseEnPratiqueForm';
import './styles/App.css';

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [authMode, setAuthMode] = useState(null); // 'login' ou 'register'
  const [showAuthForm, setShowAuthForm] = useState(false); // Contrôler l'affichage du formulaire

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const handleAuthAction = (action) => {
    console.log('Auth action:', action);
    setAuthMode(action);
    // Si action est null, on réinitialise et cache le formulaire
    if (action === null) {
      console.log('Resetting auth mode');
      setShowAuthForm(false);
    } else {
      // Si on a une action (login/register), on affiche le formulaire
      setShowAuthForm(true);
    }
  };

  const handleNavigation = () => {
    console.log('Navigation clicked, resetting auth mode');
    setAuthMode(null); // Réinitialiser le mode auth lors de la navigation
    setShowAuthForm(false); // Cacher le formulaire
  };

  // Écouter l'événement de réinitialisation du mode auth
  useEffect(() => {
    const handleResetAuthMode = () => {
      console.log('Reset auth mode event received');
      setAuthMode(null);
      setShowAuthForm(false);
    };

    window.addEventListener('resetAuthMode', handleResetAuthMode);
    return () => {
      window.removeEventListener('resetAuthMode', handleResetAuthMode);
    };
  }, []);

  return (
    <Router>
      <div className="app">
        <Sidebar collapsed={sidebarCollapsed} onToggle={toggleSidebar} onNavigate={handleNavigation} />
        <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
          <Navbar onToggleSidebar={toggleSidebar} onAuthAction={handleAuthAction} currentAuthMode={authMode} />
          <div className="content-area">
            <Routes>
              {/* Page d'accueil - accessible sans authentification */}
              <Route path="/" element={showAuthForm ? <Auth mode={authMode} /> : <Home />} />
              
              {/* Pages protégées - authentification requise */}
              <Route path="/cours" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <CoursList />
                </ProtectedRoute>
              } />

              <Route path="/cours/new" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <CoursForm mode="create" />
                </ProtectedRoute>
              } />

              <Route path="/cours/:id/edit" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <CoursForm mode="edit" />
                </ProtectedRoute>
              } />

              <Route path="/cours/:id" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <CoursDetails />
                </ProtectedRoute>
              } />
              
              <Route path="/exercices" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <ExercicesList />
                </ProtectedRoute>
              } />

              <Route path="/exercices/new" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <ExerciceForm mode="create" />
                </ProtectedRoute>
              } />

              <Route path="/exercices/:id/edit" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <ExerciceForm mode="edit" />
                </ProtectedRoute>
              } />

              <Route path="/exercices/:id/play" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <ExercicePlayer />
                </ProtectedRoute>
              } />

              <Route path="/exercices/:id" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <ExerciceDetails />
                </ProtectedRoute>
              } />
              
              <Route path="/mise-en-pratique" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <MiseEnPratique />
                </ProtectedRoute>
              } />

              <Route path="/mise-en-pratique/new" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <MiseEnPratiqueForm mode="create" />
                </ProtectedRoute>
              } />

              <Route path="/mise-en-pratique/:id/edit" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <MiseEnPratiqueForm mode="edit" />
                </ProtectedRoute>
              } />
              
              <Route path="/auth-test" element={
                <ProtectedRoute authMode={authMode} onAuthAction={handleAuthAction}>
                  <AuthTest />
                </ProtectedRoute>
              } />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
