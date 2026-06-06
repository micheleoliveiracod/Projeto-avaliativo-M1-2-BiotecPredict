import React from 'react';
import Dashboard from '../../components/Dashboard/Dashboard';
import styles from './Dashboard.module.css';

const DashboardPage: React.FC = () => {
  return (
    <div className={styles.dashboardPage}>
      <h1>Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia</h1>
      <Dashboard />
    </div>
  );
};

export default DashboardPage;
