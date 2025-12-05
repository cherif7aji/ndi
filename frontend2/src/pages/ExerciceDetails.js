import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ExerciceService, AuthService } from '../services/api';
import './ExerciceDetails.css';

const ExerciceDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [exercice, setExercice] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [showSolutions, setShowSolutions] = useState(false);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const groupedByParagraphe = useMemo(() => {
    if (!exercice) return [];
    const map = {};
    const paras = exercice?.paragraphes || [];
    const vids = exercice?.videos || [];
    const imgs = exercice?.images || [];
    for (const p of paras) {
      map[p.ordre] = { p, videos: [], images: [] };
    }
    for (const v of vids) {
      const k = v.ordre;
      if (!map[k]) map[k] = { p: null, videos: [], images: [] };
      map[k].videos.push(v);
    }
    for (const i of imgs) {
      const k = i.ordre;
      if (!map[k]) map[k] = { p: null, videos: [], images: [] };
      map[k].images.push(i);
    }
    const keys = Object.keys(map).map(Number).sort((a,b)=>a-b);
    return keys.map(k => ({ ordre: k, ...map[k] }));
  }, [exercice]);

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
      const { data } = await ExerciceService.getWithContent(id);
      setExercice(data);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  const checkSubmission = async () => {
    try {
      // Vérifier si l'utilisateur a déjà soumis cet exercice en vérifiant ses notes
      const response = await fetch('http://localhost:8000/submissions/mes-notes', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (response.ok) {
        const notes = await response.json();
        const hasNote = notes.some(note => note.exercice_id === parseInt(id));
        setHasSubmitted(hasNote);
      }
    } catch (e) {
      console.error('Erreur vérification soumission:', e);
    }
  };

  useEffect(() => {
    loadUser();
    load();
    checkSubmission();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const handleDelete = async () => {
    const ok = window.confirm('Supprimer cet exercice et tout son contenu ?');
    if (!ok) return;
    try {
      await ExerciceService.deleteWithContent(id);
      navigate('/exercices');
    } catch (e) {
      alert(e.response?.data?.detail || e.message || 'Suppression impossible');
    }
  };

  const isAdmin = currentUser?.role === 'admin';

  if (loading) return <div className="exercice-details-page"><div className="loader">Chargement...</div></div>;
  if (error) return <div className="exercice-details-page"><div className="alert alert-error">{error}</div></div>;
  if (!exercice) return null;

  return (
    <div className="exercice-details-page fade-in">
      <div className="header-row">
        <h1>{exercice.titre}</h1>
        <div className="actions">
          <button className="btn" onClick={() => navigate('/exercices')}>← Retour</button>
          <button className="btn btn-success" onClick={() => navigate(`/exercices/${id}/play`)}>Répondre</button>
          {isAdmin && (
            <>
              <button className="btn btn-secondary" onClick={() => navigate(`/exercices/${id}/edit`)}>Éditer</button>
              <button className="btn btn-danger" onClick={handleDelete}>Supprimer</button>
            </>
          )}
        </div>
      </div>

      <div className="card">
        <h3>Informations</h3>
        <div className="meta">
          <div><span className="label">Type:</span> <span>{exercice.type_exercice || '-'}</span></div>
          <div><span className="label">Difficulté:</span> <span className={`badge badge-${exercice.difficulte || 'moyen'}`}>{exercice.difficulte || 'moyen'}</span></div>
          <div><span className="label">Points max:</span> <span>{exercice.points_max ?? 100}</span></div>
          <div><span className="label">Temps limite:</span> <span>{exercice.temps_limite ? `${exercice.temps_limite} min` : 'Aucun'}</span></div>
        </div>
        {exercice.description && (
          <div className="desc">
            <h4>Description</h4>
            <p>{exercice.description}</p>
          </div>
        )}
      </div>

      {groupedByParagraphe.length > 0 && (
        <div className="paragraphe-list">
          {groupedByParagraphe.map((grp) => (
            <div key={grp.ordre} className="paragraphe-row">
              <div className="paragraphe-left card">
                <div className="row between">
                  <div className="title">{grp.p?.titre || `Section ${grp.ordre}`}</div>
                  <span className="chip">{grp.p?.type_paragraphe || 'contenu'}</span>
                </div>
                {grp.p?.contenu && <p className="content">{grp.p.contenu}</p>}
              </div>
              <div className="paragraphe-right">
                {grp.videos.length > 0 && (
                  <div className="card">
                    <h4>Vidéos ({grp.videos.length})</h4>
                    {grp.videos.map((v) => (
                      <div key={v.id || v.ordre} className="item-block">
                        <div className="row">
                          <div className="title">{v.titre || `Vidéo ${v.ordre}`}</div>
                          {v.url_video && <a className="link" href={v.url_video} target="_blank" rel="noreferrer">Ouvrir</a>}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {exercice.images && exercice.images.length > 0 && (
        <div className="card">
          <h3>Images</h3>
          {exercice.images.map((img, i) => (
            <div key={img.id || i} style={{ marginBottom: '20px' }}>
              {(img.titre || img.alt_text) && (
                <div style={{ fontWeight: '500', marginBottom: '8px', color: '#ddd' }}>
                  {img.titre || img.alt_text}
                </div>
              )}
              {img.contenu_base64 && (
                <img 
                  src={`data:image/${(img.extension || '.jpg').replace('.', '')};base64,${img.contenu_base64}`}
                  alt={img.alt_text || img.nom_fichier || 'Image'}
                  className="exercice-image"
                  style={{ maxWidth: '100%', borderRadius: '8px', display: 'block' }}
                />
              )}
            </div>
          ))}
        </div>
      )}

      <div className="card">
        <div className="row between" style={{ marginBottom: '16px' }}>
          <h3>Questions ({exercice.questions?.length || 0})</h3>
          {hasSubmitted ? (
            <button 
              className="btn btn-secondary" 
              onClick={() => setShowSolutions(!showSolutions)}
            >
              {showSolutions ? '🔒 Masquer les solutions' : '👁️ Voir les solutions'}
            </button>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ color: '#888', fontSize: '14px' }}>
                🔒 Soumettez l'exercice pour voir les solutions
              </span>
              <button 
                className="btn btn-success" 
                onClick={() => navigate(`/exercices/${id}/play`)}
              >
                Répondre
              </button>
            </div>
          )}
        </div>
        {(!exercice.questions || exercice.questions.length === 0) && <div className="muted">Aucune question</div>}
        {exercice.questions?.map((q, idx) => (
          <div key={q.id || idx} className="item-block">
            <div className="row between">
              <div className="title">Question {idx + 1}</div>
              <span className="chip">{q.type_question}</span>
            </div>
            <p className="content">{q.texte_question}</p>
            {(q.type_question === 'multiple_choice' || q.type_question === 'choix_multiple') && (
              <div className="options">
                {q.option_a && <div className={`option ${showSolutions && q.bonne_reponse === 'A' ? 'correct-answer' : ''}`}>A. {q.option_a} {showSolutions && q.bonne_reponse === 'A' && <span className="badge-correct">✓ Bonne réponse</span>}</div>}
                {q.option_b && <div className={`option ${showSolutions && q.bonne_reponse === 'B' ? 'correct-answer' : ''}`}>B. {q.option_b} {showSolutions && q.bonne_reponse === 'B' && <span className="badge-correct">✓ Bonne réponse</span>}</div>}
                {q.option_c && <div className={`option ${showSolutions && q.bonne_reponse === 'C' ? 'correct-answer' : ''}`}>C. {q.option_c} {showSolutions && q.bonne_reponse === 'C' && <span className="badge-correct">✓ Bonne réponse</span>}</div>}
                {q.option_d && <div className={`option ${showSolutions && q.bonne_reponse === 'D' ? 'correct-answer' : ''}`}>D. {q.option_d} {showSolutions && q.bonne_reponse === 'D' && <span className="badge-correct">✓ Bonne réponse</span>}</div>}
              </div>
            )}
            {showSolutions && q.reponse_attendue && (
              <div className="expected-answer">
                <strong>Réponse attendue:</strong> {q.reponse_attendue}
              </div>
            )}
            <div className="meta-row"><span>Points: {q.points}</span></div>
          </div>
        ))}
      </div>

      {showSolutions && exercice.solutions && exercice.solutions.length > 0 && (
        <div className="card">
          <h3>Solutions ({exercice.solutions.length})</h3>
          {exercice.solutions.map((s, idx) => (
            <div key={s.id || idx} className="item-block">
              <div className="title">{s.titre || `Solution ${idx + 1}`}</div>
              {s.explication && <p className="content">{s.explication}</p>}
              {s.code_solution && (
                <pre className="code-block">{s.code_solution}</pre>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ExerciceDetails;
