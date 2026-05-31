import { useState, useCallback } from 'react'
import axios from 'axios'

/**
 * Upload Hook
 * 
 * Custom hook for handling file uploads with validation and error handling.
 * Encapsulates upload logic for reusability across components.
 * 
 * @returns Object containing upload state and handlers
 * 
 * @example
 * ```tsx
 * const { file, loading, error, upload, reset } = useUpload()
 * 
 * const handleUpload = async (file: File) => {
 *   const batchId = await upload(file)
 *   if (batchId) {
 *     navigate(`/dashboard/${batchId}`)
 *   }
 * }
 * ```
 */
interface UseUploadReturn {
  file: File | null
  loading: boolean
  error: string | null
  success: boolean
  upload: (file: File) => Promise<string | null>
  reset: () => void
}

export const useUpload = (): UseUploadReturn => {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  /**
   * Validates CSV file format and structure
   * @param file - File to validate
   * @returns Object with isValid flag and error message if invalid
   */
  const validateFile = useCallback((file: File): { isValid: boolean; error?: string } => {
    // Check file extension
    if (!file.name.endsWith('.csv')) {
      return {
        isValid: false,
        error: 'Por favor, selecione um arquivo CSV válido (.csv)'
      }
    }

    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      return {
        isValid: false,
        error: 'O arquivo é muito grande. Tamanho máximo: 10MB'
      }
    }

    // Check file type
    if (file.type && !file.type.includes('text') && file.type !== 'application/vnd.ms-excel') {
      return {
        isValid: false,
        error: 'Tipo de arquivo inválido. Por favor, selecione um arquivo CSV'
      }
    }

    return { isValid: true }
  }, [])

  /**
   * Uploads file to API
   * @param file - File to upload
   * @returns Batch ID if successful, null otherwise
   */
  const upload = useCallback(async (file: File): Promise<string | null> => {
    // Validate file
    const validation = validateFile(file)
    if (!validation.isValid) {
      setError(validation.error || 'Arquivo inválido')
      setSuccess(false)
      return null
    }

    setFile(file)
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', file)

      // Upload file to API
      const response = await axios.post(
        'http://localhost:8000/api/v1/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          timeout: 30000 // 30 second timeout
        }
      )

      // Handle successful upload
      const batchId = response.data.batch_id || response.data.id
      setSuccess(true)
      setError(null)
      return batchId
    } catch (err) {
      // Handle upload error
      let errorMessage = 'Erro ao enviar arquivo. Tente novamente.'
      
      if (axios.isAxiosError(err)) {
        if (err.response?.status === 400) {
          errorMessage = err.response.data?.detail || 'Arquivo inválido ou estrutura incorreta'
        } else if (err.response?.status === 413) {
          errorMessage = 'Arquivo muito grande'
        } else if (err.response?.status === 500) {
          errorMessage = 'Erro no servidor. Tente novamente mais tarde.'
        } else if (err.code === 'ECONNABORTED') {
          errorMessage = 'Tempo limite excedido. Arquivo muito grande?'
        }
      }

      setError(errorMessage)
      setSuccess(false)
      return null
    } finally {
      setLoading(false)
    }
  }, [validateFile])

  /**
   * Resets upload state
   */
  const reset = useCallback(() => {
    setFile(null)
    setLoading(false)
    setError(null)
    setSuccess(false)
  }, [])

  return {
    file,
    loading,
    error,
    success,
    upload,
    reset
  }
}
