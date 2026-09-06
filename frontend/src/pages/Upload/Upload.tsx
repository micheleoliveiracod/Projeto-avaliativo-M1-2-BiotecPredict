import React from 'react';
import { useNavigate } from 'react-router-dom';
import UploadCard from '../../components/UploadCard/UploadCard';
import Masthead from '../../components/Masthead/Masthead';
import styles from './Upload.module.css';

const Upload: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.uploadPage}>
      <Masthead />
      <div className={styles.container}>
        <h1>Upload de Arquivo CSV</h1>
        <p className={styles.description}>
          Faça upload de um arquivo CSV com dados de sensores para análise de conformidade e predição de risco.
        </p>
        <UploadCard
          onUploadSuccess={() => {
            // Dá tempo do usuário ver a mensagem de sucesso antes de navegar
            setTimeout(() => navigate('/dashboard'), 1500)
          }}
        />
      </div>
    </div>
  );
};

export default Upload;
