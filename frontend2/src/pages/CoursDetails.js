import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { CoursService, AuthService } from '../services/api';
import { BookOpen, Clock, Calendar, Edit, Trash2, ArrowLeft } from 'lucide-react';
import './CoursDetails.css';

const CoursDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [cours, setCours] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);

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
      const { data } = await CoursService.getWithContent(id);
      setCours(data);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Erreur lors du chargement du cours');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const isAdmin = currentUser?.role === 'admin';

  // Combiner paragraphes et images par ordre
  const getContentBlocks = () => {
    if (!cours) return [];
    const blocks = [];
    const paras = (cours.paragraphes || []).sort((a,b) => a.ordre - b.ordre);
    const imgs = (cours.images || []).sort((a,b) => a.ordre - b.ordre);
    
    paras.forEach(p => blocks.push({ type: 'paragraph', ordre: p.ordre, data: p }));
    imgs.forEach(i => blocks.push({ type: 'image', ordre: i.ordre, data: i }));
    
    return blocks.sort((a,b) => a.ordre - b.ordre);
  };

  const handleDelete = async () => {
    const ok = window.confirm('Supprimer ce cours et tout son contenu ?');
    if (!ok) return;
    try {
      await CoursService.deleteWithContent(id);
      navigate('/cours');
    } catch (e) {
      alert(e.response?.data?.detail || e.message || 'Suppression impossible');
    }
  };

  if (loading) return <div className="cours-details-page"><div className="loader">Chargement...</div></div>;
  if (error) return <div className="cours-details-page"><div className="alert alert-error">{error}</div></div>;
  if (!cours) return null;

  const contentBlocks = getContentBlocks();

  return (
    <div className="cours-details-page fade-in">
      {/* Header */}
      <div className="course-header">
        <button className="btn-back" onClick={() => navigate('/cours')}>
          <ArrowLeft size={20} />
          <span>Retour aux cours</span>
        </button>
        {isAdmin && (
          <div className="course-actions">
            <button className="btn-icon" onClick={() => navigate(`/cours/${id}/edit`)} title="Éditer">
              <Edit size={20} />
            </button>
            <button className="btn-icon danger" onClick={handleDelete} title="Supprimer">
              <Trash2 size={20} />
            </button>
          </div>
        )}
      </div>

      {/* Hero */}
      <div className="course-hero">
        <h1 className="course-title">{cours.titre}</h1>
        {cours.description && <p className="course-description">{cours.description}</p>}
        <div className="course-meta">
          <div className="meta-item">
            <BookOpen size={18} />
            <span>{cours.niveau || 'Tous niveaux'}</span>
          </div>
          <div className="meta-item">
            <Clock size={18} />
            <span>{cours.duree_estimee ?? '-'} min</span>
          </div>
          <div className="meta-item">
            <Calendar size={18} />
            <span>{new Date(cours.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      {/* Article Content */}
      <div className="course-article">
        {contentBlocks.length === 0 && (
          <div className="empty-content">Aucun contenu disponible</div>
        )}
        {contentBlocks.map((block, idx) => (
          <div key={idx} className="content-block">
            {block.type === 'paragraph' && (
              <div className="paragraph-block">
                {block.data.titre && <h2 className="paragraph-title">{block.data.titre}</h2>}
                {block.data.contenu && <p className="paragraph-content">{block.data.contenu}</p>}
              </div>
            )}
            {block.type === 'image' && block.data.contenu_base64 && (
              <div className="image-block">
                <img 
                  src={`data:image/${(block.data.extension || '.jpg').replace('.', '')};base64,${block.data.contenu_base64}`}
                  alt={block.data.alt_text || block.data.nom_fichier || 'Image du cours'}
                  className="course-image"
                />
                {(block.data.titre || block.data.alt_text) && (
                  <p className="image-caption">{block.data.titre || block.data.alt_text}</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CoursDetails;
