import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ExerciceService, AuthService } from '../services/api';
import { Target, Eye, Pencil, Trash2, Play, Timer, Gem, Tag, Rocket } from 'lucide-react';
import './ExercicesList.css';

const ExercicesList = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [exercices, setExercices] = useState([]);
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
      const { data } = await ExerciceService.getAll();
      setExercices(data || []);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement des exercices');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
    load();
  }, []);

  const handleDelete = async (id) => {
    const ok = window.confirm('Supprimer cet exercice et tout son contenu ?');
    if (!ok) return;
    try {
      await ExerciceService.deleteWithContent(id);
      await load();
    } catch (e) {
      alert(e.response?.data?.detail || e.message || 'Erreur lors de la suppression');
    }
  };

  const isAdmin = currentUser?.role === 'admin';

  return (
    <div className="exercices-list-page fade-in">
      <div className="header-row">
        <div className="title-wrap">
          <Target className="title-icon" />
          <h1>Exercices</h1>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={() => navigate('/exercices/new')}>+ Créer un exercice</button>
        )}
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="loader">Chargement...</div>
      ) : (
        <>
          {exercices.length === 0 ? (
            <div className="empty-state">
              <Rocket className="empty-icon" />
              <p>Aucun exercice pour le moment</p>
            </div>
          ) : (
            <div className="ex-grid">
              {exercices.map((ex) => (
                <div key={ex.id} className="ex-card">
                  <div className="ex-top">
                    <div className="ex-type">
                      <Tag size={14} />
                      <span>{ex.type_exercice || 'QCM'}</span>
                    </div>
                    <div className={`ex-diff ${(ex.difficulte || 'moyen').toLowerCase()}`}>
                      {(ex.difficulte || 'moyen').toLowerCase()}
                    </div>
                  </div>

                  <h3 className="ex-title" onClick={() => navigate(`/exercices/${ex.id}`)}>{ex.titre}</h3>

                  <div className="ex-meta">
                    <div className="meta-item"><Gem size={16} /><span>{ex.points_max ?? 100} pts</span></div>
                    <div className="meta-item"><Timer size={16} /><span>{ex.temps_limite ? `${ex.temps_limite} min` : '—'}</span></div>
                  </div>

                  <div className="ex-actions">
                    <button className="btn-icon" title="Voir" onClick={() => navigate(`/exercices/${ex.id}`)}>
                      <Eye size={18} />
                    </button>
                    <button className="btn-icon success" title="Répondre" onClick={() => navigate(`/exercices/${ex.id}/play`)}>
                      <Play size={18} />
                    </button>
                    {isAdmin && (
                      <>
                        <button className="btn-icon" title="Éditer" onClick={() => navigate(`/exercices/${ex.id}/edit`)}>
                          <Pencil size={18} />
                        </button>
                        <button className="btn-icon danger" title="Supprimer" onClick={() => handleDelete(ex.id)}>
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

export default ExercicesList;
