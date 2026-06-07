import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from './Navigation.module.css';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <nav className={styles.nav}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <Link to="/">BiotecPredict</Link>
        </div>
        <ul className={styles.menu}>
          <li>
            <Link 
              to="/" 
              className={location.pathname === '/' ? styles.active : ''}
            >
              Upload
            </Link>
          </li>
          <li>
            <Link 
              to="/dashboard" 
              className={location.pathname === '/dashboard' ? styles.active : ''}
            >
              Dashboard
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;
