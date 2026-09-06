import React from 'react';
import styles from './Masthead.module.css';

/**
 * Faixa com a arte da marca (logo-lockup), usada no topo das páginas de
 * Upload e Dashboard. Ver frontend/DESIGN.md.
 */
const Masthead: React.FC = () => {
  return (
    <header className={styles.masthead}>
      <img
        src="/logo-lockup.png"
        alt="BiotecPredict — Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia"
        className={styles.logo}
      />
    </header>
  );
};

export default Masthead;
