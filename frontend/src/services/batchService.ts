import api from './api';

export interface Batch {
  id: string;
  upload_date: string;
  status: 'ACCEPTABLE' | 'WARNING' | 'CRITICAL';
  compliance_score: number;
  risk_prediction: 'LOW' | 'MEDIUM' | 'HIGH';
}

export interface BatchResponse {
  batches: Batch[];
  total: number;
  page: number;
  page_size: number;
}

// GET /batches - Listar todos os batches
export const getBatches = async (
  page: number = 1,
  page_size: number = 10,
  filters?: {
    start_date?: string;
    end_date?: string;
    status?: string;
    min_score?: number;
    max_score?: number;
  }
): Promise<BatchResponse> => {
  try {
    const params = {
      page,
      page_size,
      ...filters,
    };
    const response = await api.get<BatchResponse>('/batches', { params });
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar batches:', error);
    throw error;
  }
};

// GET /batch/{id} - Detalhes do batch
export const getBatchById = async (batchId: string): Promise<Batch> => {
  try {
    const response = await api.get<Batch>(`/batch/${batchId}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar batch ${batchId}:`, error);
    throw error;
  }
};

export default {
  getBatches,
  getBatchById,
};
