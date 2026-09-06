import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from './Navigation.module.css';
import mark from '../../assets/mark.svg';

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <nav className={styles.nav}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>
          <img src={mark} alt="" width={28} height={17} className={styles.logoMark} />
          <span>
            Biotec<em>Predict</em>
          </span>
        </Link>
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
