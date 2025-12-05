import React from 'react';
import { Shield, BookOpen, Target, Trophy, Lock, Code, Zap, Award, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-modern">
      <div className="home-container">
        {/* Hero Section */}
        <div className="hero-section">
          <div className="hero-badge">🎓 Plateforme d'Excellence en Cybersécurité</div>
          <h1 className="hero-title">IRT CyberSec Academy</h1>
          <p className="hero-subtitle">
            Votre passerelle vers l'expertise en sécurité des applications web
          </p>
        </div>

        {/* Définition Section */}
        <div className="definition-section">
          <div className="definition-header">
            <Shield className="definition-icon" />
            <h2 className="section-title">Qu'est-ce que la Sécurité des Applications Web ?</h2>
          </div>
          <div className="definition-content">
            <p className="definition-text">
              La <strong>sécurité des applications web</strong> est l'ensemble des pratiques, techniques et processus 
              visant à <span className="highlight-text">protéger les applications web</span> contre les menaces, 
              vulnérabilités et attaques malveillantes. Elle englobe la protection des données sensibles, 
              l'authentification sécurisée, la prévention des injections de code, et la défense contre 
              les exploitations de failles comme le <strong>Cross-Site Scripting (XSS)</strong>, 
              les <strong>injections SQL</strong>, et les attaques <strong>CSRF</strong>.
            </p>
            <div className="definition-stats">
              <div className="def-stat">
                <Lock className="def-stat-icon" />
                <div className="def-stat-text">
                  <strong>Protection 24/7</strong>
                  <span>Contre les cybermenaces</span>
                </div>
              </div>
              <div className="def-stat">
                <Code className="def-stat-icon" />
                <div className="def-stat-text">
                  <strong>Code Sécurisé</strong>
                  <span>Bonnes pratiques OWASP</span>
                </div>
              </div>
              <div className="def-stat">
                <Zap className="def-stat-icon" />
                <div className="def-stat-text">
                  <strong>Réponse Rapide</strong>
                  <span>Aux incidents de sécurité</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Importance Section */}
        <div className="importance-section">
          <h2 className="section-title">Pourquoi est-ce Crucial Aujourd'hui ?</h2>
          <div className="importance-grid">
            <div className="importance-card">
              <div className="importance-number">6 000 Mds $</div>
              <h3>Impact Économique</h3>
              <p>
                Coût annuel des cyberattaques dans le monde, dépassant le PIB de nombreux pays. 
                Chaque entreprise est une cible potentielle.
              </p>
            </div>
            <div className="importance-card">
              <div className="importance-number">4,9 Mds</div>
              <h3>Utilisateurs Exposés</h3>
              <p>
                Personnes utilisant Internet quotidiennement, dont les données personnelles 
                doivent être protégées contre le vol et l'exploitation.
              </p>
            </div>
            <div className="importance-card">
              <div className="importance-number">+150%</div>
              <h3>Menaces Croissantes</h3>
              <p>
                Augmentation des attaques ransomware depuis 2020. Les vulnérabilités web 
                restent le vecteur d'attaque le plus exploité.
              </p>
            </div>
            <div className="importance-card">
              <div className="importance-number">3,5M</div>
              <h3>Opportunités de Carrière</h3>
              <p>
                Postes en cybersécurité non pourvus dans le monde. Un marché de 345 milliards 
                de dollars d'ici 2026.
              </p>
            </div>
          </div>
        </div>

        {/* Ce que nous offrons */}
        <div className="offerings-section">
          <h2 className="section-title">Ce que IRT CyberSec Academy Vous Offre</h2>
          <div className="offerings-grid">
            <div className="offering-card">
              <div className="offering-icon-wrapper">
                <BookOpen className="offering-icon" />
              </div>
              <h3>Cours Interactifs</h3>
              <p>
                Modules théoriques complets couvrant les vulnérabilités OWASP Top 10, 
                avec des explications détaillées et des exemples concrets.
              </p>
              <div className="offering-badge">Théorie + Pratique</div>
            </div>
            <div className="offering-card">
              <div className="offering-icon-wrapper">
                <Target className="offering-icon" />
              </div>
              <h3>Exercices QCM</h3>
              <p>
                Testez vos connaissances en temps réel avec des questionnaires à choix multiples 
                et suivez votre progression pas à pas.
              </p>
              <div className="offering-badge">Auto-évaluation</div>
            </div>
            <div className="offering-card">
              <div className="offering-icon-wrapper">
                <Trophy className="offering-icon" />
              </div>
              <h3>Défis Pratiques</h3>
              <p>
                Exploitez des failles réelles dans un environnement sécurisé de type 
                Capture The Flag pour affiner vos compétences.
              </p>
              <div className="offering-badge">Hands-on Labs</div>
            </div>
            <div className="offering-card">
              <div className="offering-icon-wrapper">
                <Award className="offering-icon" />
              </div>
              <h3>Suivi de Progression</h3>
              <p>
                Système de notation avancé pour tracker votre évolution, débloquer des niveaux 
                et obtenir des certifications.
              </p>
              <div className="offering-badge">Gamification</div>
            </div>
          </div>
        </div>

        {/* CTA Final */}
        <div className="cta-final">
          <div className="cta-content">
            <h2 className="cta-title">Prêt à Devenir un Expert en Cybersécurité ?</h2>
            <p className="cta-text">
              Rejoignez IRT CyberSec Academy et commencez votre parcours d'apprentissage dès aujourd'hui. 
              Connectez-vous pour accéder à nos cours exclusifs et défis pratiques.
            </p>
            <div className="cta-buttons">
              <button className="btn-primary" onClick={() => navigate('/cours')}>
                <span>Explorer les Cours</span>
                <ArrowRight className="btn-icon" />
              </button>
              <button className="btn-secondary" onClick={() => navigate('/exercices')}>
                Commencer les Exercices
              </button>
            </div>
            <p className="cta-note">
              💡 <strong>Astuce :</strong> Connectez-vous pour sauvegarder votre progression et débloquer tous les contenus
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
