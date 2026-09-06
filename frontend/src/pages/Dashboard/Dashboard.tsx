import React from 'react';
import Dashboard from '../../components/Dashboard/Dashboard';
import Masthead from '../../components/Masthead/Masthead';
import styles from './Dashboard.module.css';

const DashboardPage: React.FC = () => {
  return (
    <div className={styles.dashboardPage}>
      <Masthead />
      <Dashboard />
    </div>
  );
};

export default DashboardPage;
