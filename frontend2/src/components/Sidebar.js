import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { 
  Home, 
  BookOpen, 
  Target, 
  AlertTriangle,
  Shield,
  Lock,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ collapsed, onToggle, onNavigate }) => {
  const location = useLocation();

  const menuItems = [
    {
      path: '/',
      icon: Home,
      label: 'Accueil',
      description: 'Tableau de bord principal',
      protected: false
    },
    {
      path: '/cours',
      icon: BookOpen,
      label: 'Cours',
      description: 'Modules d\'apprentissage',
      protected: true
    },
    {
      path: '/exercices',
      icon: Target,
      label: 'Exercices',
      description: 'Défis pratiques',
      protected: true
    },
    {
      path: '/mise-en-pratique',
      icon: AlertTriangle,
      label: 'Mise en pratique',
      description: 'Tutoriels de failles',
      protected: true
    }
  ];

  const sidebarClasses = `sidebar ${collapsed ? 'collapsed' : ''} ${!collapsed ? 'mobile-open' : ''}`;
  return (
    <div className={sidebarClasses}>
      {/* Header du sidebar */}
      <div className="sidebar-header">
        <div className="logo-container">
          <div className="logo-icon">
            <Shield className="shield-icon" size={20} />
            <Lock className="lock-icon" size={12} />
          </div>
          {!collapsed && (
            <div className="logo-text">
              <h2>IRT CyberSec</h2>
              <span>Academy</span>
            </div>
          )}
        </div>
        <button 
          className="toggle-btn"
          onClick={onToggle}
          title={collapsed ? 'Étendre' : 'Réduire'}
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <ul className="nav-list">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <li key={item.path} className="nav-item">
                <NavLink
                  to={item.path}
                  className={`nav-link ${isActive ? 'active' : ''}`}
                  title={collapsed ? item.label : ''}
                  onClick={onNavigate}
                >
                  <div className="nav-icon">
                    <Icon size={20} />
                  </div>
                  {!collapsed && (
                    <div className="nav-content">
                      <div className="nav-label-container">
                        <span className="nav-label">{item.label}</span>
                        {item.protected && <Lock className="protected-icon" size={12} />}
                      </div>
                      <span className="nav-description">{item.description}</span>
                    </div>
                  )}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer du sidebar */}
      {!collapsed && (
        <div className="sidebar-footer">
          <div className="version-info">
            <span>Version 1.0.0</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
