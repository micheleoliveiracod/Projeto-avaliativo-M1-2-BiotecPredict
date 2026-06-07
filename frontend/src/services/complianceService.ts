import api from './api';

export interface Compliance {
  batch_id: string;
  compliance_score: number;
  classification: 'ACCEPTABLE' | 'WARNING' | 'CRITICAL';
  details: {
    temperature_status: string;
    ph_status: string;
    dissolved_oxygen_status: string;
    pressure_status: string;
    agitator_speed_status: string;
  };
}

// GET /compliance/{batch_id} - Score de conformidade
export const getCompliance = async (batchId: string): Promise<Compliance> => {
  try {
    const response = await api.get<Compliance>(`/compliance/${batchId}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar compliance para batch ${batchId}:`, error);
    throw error;
  }
};

export default {
  getCompliance,
};
