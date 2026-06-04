import React from 'react';
import UploadCard from '../../components/UploadCard/UploadCard';
import styles from './Upload.module.css';

const Upload: React.FC = () => {
  return (
    <div className={styles.uploadPage}>
      <div className={styles.container}>
        <h1>Upload de Arquivo CSV</h1>
        <p className={styles.description}>
          Faça upload de um arquivo CSV com dados de sensores para análise de conformidade e predição de risco.
        </p>
        <UploadCard />
      </div>
    </div>
  );
};

export default Upload;
