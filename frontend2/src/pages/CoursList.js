import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CoursService, AuthService } from '../services/api';
import { BookOpen, Clock, Signal, Rocket, Eye, Pencil, Trash2, CheckCircle2, XCircle } from 'lucide-react';
import './CoursList.css';

const CoursList = () => {
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
      // Exclure les cours commençant par "MP" (Mise en pratique)
      const normalCours = (data || []).filter(c => !c.titre || !c.titre.startsWith('MP'));
      setCours(normalCours);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement des cours');
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
    const ok = window.confirm('Supprimer ce cours et tout son contenu ?');
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
          <BookOpen className="title-icon" />
          <h1>Cours</h1>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={() => navigate('/cours/new')}>+ Créer un cours</button>
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
              <p>Aucun cours pour le moment</p>
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
                      <BookOpen size={16} />
                      <span>{new Date(c.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="card-actions">
                    <button className="btn-icon" title="Voir" onClick={() => navigate(`/cours/${c.id}`)}>
                      <Eye size={18} />
                    </button>
                    {isAdmin && (
                      <>
                        <button className="btn-icon" title="Éditer" onClick={() => navigate(`/cours/${c.id}/edit`)}>
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

export default CoursList;
