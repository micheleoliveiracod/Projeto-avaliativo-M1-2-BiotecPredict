import api from './api';

export interface Prediction {
  batch_id: string;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  confidence_score: number;
  model_version: string;
  prediction_timestamp: string;
}

// GET /prediction/{batch_id} - Predição de risco
export const getPrediction = async (batchId: string): Promise<Prediction> => {
  try {
    const response = await api.get<Prediction>(`/prediction/${batchId}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar predição para batch ${batchId}:`, error);
    throw error;
  }
};

export default {
  getPrediction,
};
