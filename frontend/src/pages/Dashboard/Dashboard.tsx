import React from 'react';
import Dashboard from '../../components/Dashboard/Dashboard';
import styles from './Dashboard.module.css';

const DashboardPage: React.FC = () => {
  return (
    <div className={styles.dashboardPage}>
      <h1>Dashboard Analítico</h1>
      <Dashboard />
    </div>
  );
};

export default DashboardPage;
