import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ExerciceService, SubmissionService } from '../services/api';
import './ExercicePlayer.css';

const ExercicePlayer = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [exercice, setExercice] = useState(null);
  const [reponses, setReponses] = useState({});
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(null);

  const load = async () => {
    try {
      setLoading(true);
      const { data } = await ExerciceService.getWithContent(id);
      setExercice(data);
      // Initialiser le timer si temps limite
      if (data.temps_limite) {
        setTimeLeft(data.temps_limite * 60); // en secondes
      }
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // Timer countdown
  useEffect(() => {
    if (timeLeft === null || timeLeft <= 0) return;
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          handleSubmit(); // Auto-submit quand le temps est écoulé
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLeft]);

  const handleReponseChange = (questionId, value) => {
    setReponses((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const reponsesArray = Object.entries(reponses).map(([qId, rep]) => ({
        question_id: Number(qId),
        reponse_utilisateur: rep
      }));

      const payload = {
        exercice_id: Number(id),
        reponses: reponsesArray,
        temps_passe: exercice.temps_limite ? (exercice.temps_limite * 60 - (timeLeft || 0)) : 0
      };

      const { data } = await SubmissionService.submit(payload);
      setResult(data);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors de la soumission');
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) return <div className="exercice-player-page"><div className="loader">Chargement...</div></div>;
  if (error && !exercice) return <div className="exercice-player-page"><div className="alert alert-error">{error}</div></div>;
  if (!exercice) return null;

  if (result) {
    return (
      <div className="exercice-player-page fade-in">
        <div className="result-card">
          <h1>✅ Exercice soumis !</h1>
          <div className="score-display">
            <div className="score-circle">
              <span className="score-value">{result.pourcentage_obtenu?.toFixed(1) || 0}%</span>
            </div>
            <div className="score-details">
              <div className="score-item">
                <span className="label">Note obtenue:</span>
                <span className="value">{result.note_obtenue || 0} / {result.note_maximale || 100}</span>
              </div>
              <div className="score-item">
                <span className="label">Bonnes réponses:</span>
                <span className="value">{result.nombre_bonnes_reponses || 0} / {result.nombre_questions || 0}</span>
              </div>
              <div className="score-item">
                <span className="label">Temps passé:</span>
                <span className="value">{Math.floor((result.temps_passe || 0) / 60)} min {(result.temps_passe || 0) % 60} sec</span>
              </div>
            </div>
          </div>
          <div className="actions">
            <button className="btn btn-primary" onClick={() => navigate('/exercices')}>Retour aux exercices</button>
            <button className="btn btn-secondary" onClick={() => navigate(`/exercices/${id}`)}>Voir les solutions</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="exercice-player-page fade-in">
      <div className="header-row">
        <h1>{exercice.titre}</h1>
        <div className="actions">
          {timeLeft !== null && (
            <div className={`timer ${timeLeft < 60 ? 'warning' : ''}`}>
              ⏱️ {formatTime(timeLeft)}
            </div>
          )}
          <button className="btn" onClick={() => navigate(`/exercices/${id}`)}>Annuler</button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="card">
        <div className="meta">
          <div><span className="label">Type:</span> {exercice.type_exercice}</div>
          <div><span className="label">Points max:</span> {exercice.points_max}</div>
          <div><span className="label">Questions:</span> {exercice.questions?.length || 0}</div>
        </div>
        {exercice.description && <p className="desc">{exercice.description}</p>}
      </div>

      <form onSubmit={handleSubmit} className="questions-form">
        {exercice.questions?.map((q, idx) => (
          <div key={q.id} className="question-card card">
            <div className="question-header">
              <span className="question-number">Question {idx + 1}</span>
              <span className="question-points">{q.points} points</span>
            </div>
            <p className="question-text">{q.texte_question}</p>

            {(q.type_question === 'multiple_choice' || q.type_question === 'choix_multiple') && (
              <div className="options">
                {['A', 'B', 'C', 'D'].map((opt) => {
                  const optionText = q[`option_${opt.toLowerCase()}`];
                  if (!optionText) return null;
                  return (
                    <label key={opt} className="option-label">
                      <input
                        type="radio"
                        name={`question_${q.id}`}
                        value={opt}
                        checked={reponses[q.id] === opt}
                        onChange={(e) => handleReponseChange(q.id, e.target.value)}
                      />
                      <span className="option-text">{opt}. {optionText}</span>
                    </label>
                  );
                })}
              </div>
            )}

            {q.type_question === 'text' && (
              <textarea
                className="text-answer"
                rows={3}
                placeholder="Votre réponse..."
                value={reponses[q.id] || ''}
                onChange={(e) => handleReponseChange(q.id, e.target.value)}
              />
            )}

            {q.type_question === 'code' && (
              <textarea
                className="code-answer"
                rows={6}
                placeholder="Votre code..."
                value={reponses[q.id] || ''}
                onChange={(e) => handleReponseChange(q.id, e.target.value)}
              />
            )}
          </div>
        ))}

        <div className="submit-section">
          <button type="submit" className="btn btn-primary btn-large" disabled={submitting}>
            {submitting ? 'Soumission en cours...' : 'Soumettre mes réponses'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ExercicePlayer;
