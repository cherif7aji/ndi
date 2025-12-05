import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ExerciceService, CoursService } from '../services/api';
import './ExerciceForm.css';

const emptyExercice = {
  titre: '',
  description: '',
  type_exercice: 'QCM',
  difficulte: 'moyen',
  points_max: 100,
  temps_limite: '',
  ordre: 1,
  cours_id: ''
};

const ExerciceForm = ({ mode = 'create' }) => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = useMemo(() => mode === 'edit' && id, [mode, id]);

  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [cours, setCours] = useState([]);

  const [base, setBase] = useState(emptyExercice);
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    const loadCours = async () => {
      try {
        const { data } = await CoursService.getAll();
        setCours(data || []);
      } catch (e) {
        console.error('Erreur chargement cours:', e);
      }
    };
    loadCours();
  }, []);

  useEffect(() => {
    const load = async () => {
      if (!isEdit) return;
      try {
        setLoading(true);
        const { data } = await ExerciceService.getWithContent(id);
        setBase({
          titre: data.titre || '',
          description: data.description || '',
          type_exercice: data.type_exercice || 'QCM',
          difficulte: data.difficulte || 'moyen',
          points_max: data.points_max || 100,
          temps_limite: data.temps_limite || '',
          ordre: data.ordre || 1,
          cours_id: data.cours_id || ''
        });
        setQuestions(data.questions || []);
      } catch (e) {
        setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [isEdit, id]);

  const handleBaseChange = (e) => {
    const { name, value } = e.target;
    setBase((prev) => ({ ...prev, [name]: value }));
  };

  // Questions QCM uniquement
  const addQuestion = () => setQuestions((q) => [...q, { texte_question: '', type_question: 'choix_multiple', points: 10, ordre: q.length + 1, option_a: '', option_b: '', option_c: '', option_d: '', bonne_reponse: 'A' }]);
  const updateQuestion = (idx, key, value) => setQuestions((q) => q.map((it, i) => i === idx ? { ...it, [key]: value } : it));
  const removeQuestion = (idx) => setQuestions((q) => q.filter((_, i) => i !== idx).map((it, i) => ({ ...it, ordre: i + 1 })));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaving(true);
    
    const payload = {
      ...base,
      cours_id: Number(base.cours_id),
      points_max: Number(base.points_max) || 100,
      temps_limite: Number(base.temps_limite) || null,
      ordre: Number(base.ordre) || 1,
      questions: questions.map((q, i) => ({ ...q, ordre: i + 1, points: Number(q.points) || 10, exercice_id: isEdit ? Number(id) : undefined })),
      solutions: [],
      paragraphes: [],
      videos: [],
      images: []
    };
    
    try {
      if (isEdit) {
        await ExerciceService.updateWithContent(id, payload);
      } else {
        await ExerciceService.createWithContent(payload);
      }
      navigate('/exercices');
    } catch (e) {
      console.error('Erreur création exercice:', e);
      console.error('Response:', e.response);
      console.error('Payload envoyé:', payload);
      const errorMsg = e.response?.data?.detail || e.message || 'Erreur lors de la sauvegarde';
      setError(`${errorMsg} - Vérifiez la console (F12) pour plus de détails`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="exercice-form-page"><div className="loader">Chargement...</div></div>;

  return (
    <div className="exercice-form-page fade-in">
      <div className="header-row">
        <h1>{isEdit ? 'Modifier l\'exercice' : 'Créer un exercice'}</h1>
        <button className="btn" onClick={() => navigate('/exercices')}>Retour</button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <form onSubmit={handleSubmit} className="form">
        <div className="card">
          <h3>Informations de base</h3>
          <div className="grid-2">
            <div className="field">
              <label>Titre *</label>
              <input name="titre" value={base.titre} onChange={handleBaseChange} required />
            </div>
            <div className="field">
              <label>Cours *</label>
              <select name="cours_id" value={base.cours_id} onChange={handleBaseChange} required>
                <option value="">Sélectionner un cours</option>
                {cours.map((c) => <option key={c.id} value={c.id}>{c.titre}</option>)}
              </select>
            </div>
            <input type="hidden" name="type_exercice" value="QCM" />
            <div className="field">
              <label>Difficulté</label>
              <select name="difficulte" value={base.difficulte} onChange={handleBaseChange}>
                <option value="facile">Facile</option>
                <option value="moyen">Moyen</option>
                <option value="difficile">Difficile</option>
              </select>
            </div>
            <div className="field">
              <label>Points max</label>
              <input name="points_max" type="number" value={base.points_max} onChange={handleBaseChange} />
            </div>
            <div className="field">
              <label>Temps limite (min)</label>
              <input name="temps_limite" type="number" value={base.temps_limite} onChange={handleBaseChange} />
            </div>
            <div className="field">
              <label>Ordre</label>
              <input name="ordre" type="number" value={base.ordre} onChange={handleBaseChange} />
            </div>
            <div className="field col-span-2">
              <label>Description *</label>
              <textarea name="description" rows={3} value={base.description} onChange={handleBaseChange} required />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="row-header">
            <h3>Questions</h3>
            <button type="button" className="btn btn-secondary" onClick={addQuestion}>+ Ajouter</button>
          </div>
          {questions.length === 0 && <div className="muted">Aucune question</div>}
          {questions.map((q, idx) => (
            <div key={idx} className="item-block">
              <div className="grid-2">
                <div className="field col-span-2">
                  <label>Question</label>
                  <textarea rows={2} value={q.texte_question || ''} onChange={(e)=>updateQuestion(idx,'texte_question',e.target.value)} />
                </div>
                <input type="hidden" value="choix_multiple" />
                <div className="field">
                  <label>Points</label>
                  <input type="number" value={q.points || 10} onChange={(e)=>updateQuestion(idx,'points',e.target.value)} />
                </div>
                <div className="field"><label>Option A</label><input value={q.option_a || ''} onChange={(e)=>updateQuestion(idx,'option_a',e.target.value)} /></div>
                <div className="field"><label>Option B</label><input value={q.option_b || ''} onChange={(e)=>updateQuestion(idx,'option_b',e.target.value)} /></div>
                <div className="field"><label>Option C</label><input value={q.option_c || ''} onChange={(e)=>updateQuestion(idx,'option_c',e.target.value)} /></div>
                <div className="field"><label>Option D</label><input value={q.option_d || ''} onChange={(e)=>updateQuestion(idx,'option_d',e.target.value)} /></div>
                <div className="field">
                  <label>Bonne réponse</label>
                  <select value={q.bonne_reponse || 'A'} onChange={(e)=>updateQuestion(idx,'bonne_reponse',e.target.value)}>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                  </select>
                </div>
              </div>
              <div className="row-actions">
                <button type="button" className="btn btn-danger" onClick={()=>removeQuestion(idx)}>Supprimer</button>
              </div>
            </div>
          ))}
        </div>

        <div className="actions end">
          <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Enregistrement...' : (isEdit ? 'Mettre à jour' : 'Créer')}</button>
        </div>
      </form>
    </div>
  );
};

export default ExerciceForm;
