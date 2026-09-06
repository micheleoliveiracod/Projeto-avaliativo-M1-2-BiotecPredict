import React from 'react';
import Dashboard from '../../components/Dashboard/Dashboard';
import styles from './Dashboard.module.css';

const DashboardPage: React.FC = () => {
  return (
    <div className={styles.dashboardPage}>
      <header className={styles.masthead}>
        <img
          src="/logo-lockup.png"
          alt="BiotecPredict — Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia"
          className={styles.mastheadLogo}
        />
      </header>
      <Dashboard />
    </div>
  );
};

export default DashboardPage;
