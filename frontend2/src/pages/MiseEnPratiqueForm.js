import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { CoursService } from '../services/api';
import './CoursForm.css';

const emptyCours = {
  titre: '',
  description: '',
  niveau: '',
  duree_estimee: ''
};

const MiseEnPratiqueForm = ({ mode = 'create' }) => {
  const navigate = useNavigate();
  const { id } = useParams();

  const isEdit = useMemo(() => mode === 'edit' && id, [mode, id]);

  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const [base, setBase] = useState(emptyCours);
  const [paragraphes, setParagraphes] = useState([]);
  const [images, setImages] = useState([]);

  useEffect(() => {
    const load = async () => {
      if (!isEdit) return;
      try {
        setLoading(true);
        const { data } = await CoursService.getWithContent(id);
        // Retirer le préfixe "MP - " pour l'édition
        const titreWithoutPrefix = data.titre?.startsWith('MP - ') 
          ? data.titre.substring(5) 
          : data.titre || '';
        setBase({
          titre: titreWithoutPrefix,
          description: data.description || '',
          niveau: data.niveau || '',
          duree_estimee: data.duree_estimee || ''
        });
        setParagraphes(data.paragraphes || []);
        setImages((data.images || []).map((img, idx) => ({
          nom_fichier: img.nom_fichier,
          extension: img.extension || '.jpg',
          alt_text: img.alt_text || `Image ${idx + 1}`,
          description: img.description || '',
          contenu_base64: img.contenu_base64 || '',
          ordre: img.ordre || (idx + 1)
        })));
      } catch (e) {
        setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement du tutoriel');
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

  const addParagraphe = () => setParagraphes((p) => [...p, { titre: '', contenu: '', type_paragraphe: 'contenu', ordre: p.length + 1 }]);
  const updateParagraphe = (idx, key, value) => setParagraphes((p) => p.map((it, i) => i === idx ? { ...it, [key]: value } : it));
  const removeParagraphe = (idx) => setParagraphes((p) => p.filter((_, i) => i !== idx).map((it, i) => ({ ...it, ordre: i + 1 })));

  const addImage = () => setImages((p) => [...p, { extension: '.jpg', alt_text: '', description: '', contenu_base64: '', ordre: p.length + 1 }]);
  const updateImageMeta = (idx, key, value) => setImages((p) => p.map((it, i) => i === idx ? { ...it, [key]: value } : it));
  const removeImage = (idx) => setImages((p) => p.filter((_, i) => i !== idx).map((it, i) => ({ ...it, ordre: i + 1 })));

  const onFileChange = async (idx, file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = (reader.result || '').toString().split(',')[1] || '';
      const ext = '.' + (file.name.split('.').pop() || 'jpg');
      setImages((p) => p.map((it, i) => i === idx ? { ...it, contenu_base64: base64, extension: ext, nom_fichier: file.name } : it));
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaving(true);
    try {
      // Ajouter automatiquement le préfixe "MP - " au titre
      const titreWithPrefix = base.titre.startsWith('MP - ') ? base.titre : `MP - ${base.titre}`;
      
      if (isEdit) {
        const payload = {
          titre: titreWithPrefix,
          description: base.description,
          niveau: base.niveau,
          duree_estimee: Number(base.duree_estimee) || null,
          paragraphes: paragraphes.map((p, i) => ({ ...p, ordre: i + 1 })),
          videos: [],
          images: images.map((img, i) => ({
            nom_fichier: img.nom_fichier || `image_${i + 1}${img.extension || '.jpg'}`,
            extension: img.extension || '.jpg',
            alt_text: img.alt_text || `Image ${i + 1}`,
            description: img.description || '',
            contenu_base64: img.contenu_base64 || '',
            taille_fichier: img.contenu_base64 ? Math.ceil((img.contenu_base64.length * 3) / 4) : 0,
            ordre: i + 1
          }))
        };
        await CoursService.updateWithContent(id, payload);
      } else {
        const payload = {
          titre: titreWithPrefix,
          description: base.description,
          niveau: base.niveau,
          duree_estimee: Number(base.duree_estimee) || null,
          paragraphes: paragraphes.map((p, i) => ({ ...p, ordre: i + 1 })),
          videos: [],
          images_base64: images.map((img, i) => ({
            extension: img.extension || '.jpg',
            alt_text: img.alt_text || `Image ${i + 1}`,
            description: img.description || '',
            contenu_base64: img.contenu_base64 || '',
            ordre: i + 1
          }))
        };
        await CoursService.createWithContent(payload);
      }
      navigate('/mise-en-pratique');
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="cours-form-page"><div className="loader">Chargement...</div></div>;

  return (
    <div className="cours-form-page fade-in">
      <div className="header-row">
        <h1>{isEdit ? 'Modifier le tutoriel' : 'Créer un tutoriel de faille'}</h1>
        <div className="actions">
          <button className="btn" onClick={() => navigate('/mise-en-pratique')}>Retour à la liste</button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <form onSubmit={handleSubmit} className="form">
        <div className="card">
          <h3>Informations de base</h3>
          <div className="grid-2">
            <div className="field col-span-2">
              <label>Titre (le préfixe "MP - " sera ajouté automatiquement)</label>
              <input name="titre" value={base.titre} onChange={handleBaseChange} required placeholder="Ex: SQL Injection" />
            </div>
            <div className="field">
              <label>Niveau</label>
              <input name="niveau" value={base.niveau} onChange={handleBaseChange} placeholder="Débutant / Intermédiaire / Avancé" />
            </div>
            <div className="field">
              <label>Durée estimée (min)</label>
              <input name="duree_estimee" type="number" value={base.duree_estimee} onChange={handleBaseChange} />
            </div>
            <div className="field col-span-2">
              <label>Description</label>
              <textarea name="description" rows={3} value={base.description} onChange={handleBaseChange} />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="row-header">
            <h3>Paragraphes</h3>
            <button type="button" className="btn btn-secondary" onClick={addParagraphe}>+ Ajouter</button>
          </div>
          {paragraphes.length === 0 && <div className="muted">Aucun paragraphe</div>}
          {paragraphes.map((p, idx) => (
            <div key={idx} className="grid-2 item-block">
              <div className="field">
                <label>Titre</label>
                <input value={p.titre || ''} onChange={(e)=>updateParagraphe(idx,'titre',e.target.value)} />
              </div>
              <div className="field">
                <label>Type</label>
                <select value={p.type_paragraphe || 'contenu'} onChange={(e)=>updateParagraphe(idx,'type_paragraphe',e.target.value)}>
                  <option value="contenu">Contenu</option>
                  <option value="avertissement">Avertissement</option>
                  <option value="info">Info</option>
                </select>
              </div>
              <div className="field col-span-2">
                <label>Contenu</label>
                <textarea rows={3} value={p.contenu || ''} onChange={(e)=>updateParagraphe(idx,'contenu',e.target.value)} />
              </div>
              <div className="row-actions">
                <button type="button" className="btn btn-danger" onClick={()=>removeParagraphe(idx)}>Supprimer</button>
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="row-header">
            <h3>Images</h3>
            <button type="button" className="btn btn-secondary" onClick={addImage}>+ Ajouter</button>
          </div>
          {images.length === 0 && <div className="muted">Aucune image</div>}
          {images.map((img, idx) => (
            <div key={idx} className="grid-2 item-block">
              <div className="field">
                <label>Fichier</label>
                <input type="file" accept="image/*" onChange={(e)=>onFileChange(idx, e.target.files?.[0])} />
              </div>
              <div className="field">
                <label>Alt text</label>
                <input value={img.alt_text || ''} onChange={(e)=>updateImageMeta(idx,'alt_text',e.target.value)} />
              </div>
              <div className="field col-span-2">
                <label>Description</label>
                <input value={img.description || ''} onChange={(e)=>updateImageMeta(idx,'description',e.target.value)} />
              </div>
              <div className="row-actions">
                <button type="button" className="btn btn-danger" onClick={()=>removeImage(idx)}>Supprimer</button>
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

export default MiseEnPratiqueForm;
