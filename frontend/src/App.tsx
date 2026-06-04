import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Upload from './pages/Upload/Upload';
import Dashboard from './pages/Dashboard/Dashboard';
import './App.module.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
=======
import React from 'react'

/**
 * Componente principal da aplicação BiotecPredict
 * 
 * @returns {JSX.Element} Componente App
 */
function App(): JSX.Element {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            BiotecPredict
          </h1>
          <p className="text-gray-600 mt-2">
            Plataforma de Manufatura Preditiva
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Bem-vindo ao BiotecPredict
            </h2>
            <p className="text-gray-600 mb-4">
              Sistema de análise de manufatura biofarmacêutica com machine learning
            </p>
            <div className="space-y-2">
              <p className="text-sm text-gray-500">
                ✓ Upload de dados de sensores
              </p>
              <p className="text-sm text-gray-500">
                ✓ Cálculo de compliance score
              </p>
              <p className="text-sm text-gray-500">
                ✓ Predição de risco com ML
              </p>
              <p className="text-sm text-gray-500">
                ✓ Dashboard analítico
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
