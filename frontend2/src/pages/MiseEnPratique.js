import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CoursService, AuthService } from '../services/api';
import { AlertTriangle, Clock, Signal, Rocket, Eye, Pencil, Trash2, CheckCircle2, XCircle } from 'lucide-react';
import './CoursList.css';

const MiseEnPratique = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [cours, setCours] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  const loadUser = async () => {
    try {
      const { data } = await AuthService.getCurrentUser();
      setCurrentUser(data);
    } catch (e) {
      console.error('Erreur chargement utilisateur:', e);
    }
  };

  const load = async () => {
    try {
      setLoading(true);
      const { data } = await CoursService.getAll();
      // Filtrer uniquement les cours commençant par "MP"
      const mpCours = (data || []).filter(c => c.titre && c.titre.startsWith('MP'));
      setCours(mpCours);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement des tutoriels');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
    load();
  }, []);

  const isAdmin = currentUser?.role === 'admin';

  const handleDelete = async (id) => {
    const ok = window.confirm('Supprimer ce tutoriel et tout son contenu ?');
    if (!ok) return;
    try {
      await CoursService.deleteWithContent(id);
      await load();
    } catch (e) {
      alert(e.response?.data?.detail || e.message || 'Erreur lors de la suppression');
    }
  };

  return (
    <div className="cours-list-page fade-in">
      <div className="header-row">
        <div className="title-wrap">
          <AlertTriangle className="title-icon" />
          <h1>Mise en pratique</h1>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={() => navigate('/mise-en-pratique/new')}>+ Créer un tutoriel</button>
        )}
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="loader">Chargement...</div>
      ) : (
        <>
          {cours.length === 0 ? (
            <div className="empty-state">
              <Rocket className="empty-icon" />
              <p>Aucun tutoriel de faille pour le moment</p>
            </div>
          ) : (
            <div className="cours-grid">
              {cours.map((c) => (
                <div key={c.id} className="cours-card">
                  <div className="card-top">
                    <div className="badge-level">
                      <Signal size={14} />
                      <span>{c.niveau || 'N/A'}</span>
                    </div>
                    <div className={`badge-status ${c.is_active ? 'on' : 'off'}`}>
                      {c.is_active ? <CheckCircle2 size={14} /> : <XCircle size={14} />}
                      <span>{c.is_active ? 'Actif' : 'Inactif'}</span>
                    </div>
                  </div>

                  <h3 className="card-title" onClick={() => navigate(`/cours/${c.id}`)}>{c.titre}</h3>

                  <div className="card-meta">
                    <div className="meta-item">
                      <Clock size={16} />
                      <span>{c.duree_estimee ?? '-'} min</span>
                    </div>
                    <div className="meta-item">
                      <AlertTriangle size={16} />
                      <span>{new Date(c.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="card-actions">
                    <button className="btn-icon" title="Voir" onClick={() => navigate(`/cours/${c.id}`)}>
                      <Eye size={18} />
                    </button>
                    {isAdmin && (
                      <>
                        <button className="btn-icon" title="Éditer" onClick={() => navigate(`/mise-en-pratique/${c.id}/edit`)}>
                          <Pencil size={18} />
                        </button>
                        <button className="btn-icon danger" title="Supprimer" onClick={() => handleDelete(c.id)}>
                          <Trash2 size={18} />
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default MiseEnPratique;
