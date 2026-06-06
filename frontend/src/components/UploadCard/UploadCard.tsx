import React, { useState, useRef } from 'react'
import axios from 'axios'
import './UploadCard.css'

/**
 * UploadCard Component
 * 
 * Provides a drag-and-drop interface for CSV file uploads with validation.
 * Supports both drag-and-drop and click-to-upload interactions.
 * 
 * Features:
 * - Drag-and-drop file upload
 * - Click to browse and select file
 * - CSV file validation (extension, size, structure)
 * - Real-time feedback (success/error messages)
 * - Loading state during upload
 * - Automatic redirection to dashboard after successful upload
 * 
 * @component
 * @example
 * ```tsx
 * <UploadCard onUploadSuccess={() => navigate('/dashboard')} />
 * ```
 */
interface UploadCardProps {
  onUploadSuccess?: (batchId: string) => void
  onUploadError?: (error: string) => void
}

const UploadCard: React.FC<UploadCardProps> = ({ 
  onUploadSuccess, 
  onUploadError 
}) => {
  const [isDragging, setIsDragging] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [feedback, setFeedback] = useState<{
    type: 'success' | 'error' | null
    message: string
  }>({ type: null, message: '' })
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  /**
   * Validates CSV file format and structure
   * @param file - File to validate
   * @returns Object with isValid flag and error message if invalid
   */
  const validateFile = (file: File): { isValid: boolean; error?: string } => {
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
  }

  /**
   * Handles file selection and upload
   * @param file - File to upload
   */
  const handleFileUpload = async (file: File) => {
    // Validate file
    const validation = validateFile(file)
    if (!validation.isValid) {
      setFeedback({
        type: 'error',
        message: validation.error || 'Arquivo inválido'
      })
      onUploadError?.(validation.error || 'Arquivo inválido')
      return
    }

    setSelectedFile(file)
    setIsLoading(true)
    setFeedback({ type: null, message: '' })

    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', file)

      // Upload file to API
      const response = await axios.post(
        '/api/v1/upload',
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
      setFeedback({
        type: 'success',
        message: `Arquivo enviado com sucesso! ID do batch: ${batchId}`
      })
      
      // Call success callback
      onUploadSuccess?.(batchId)

      // Reset form after 2 seconds
      setTimeout(() => {
        setSelectedFile(null)
        if (fileInputRef.current) {
          fileInputRef.current.value = ''
        }
      }, 2000)
    } catch (error) {
      // Handle upload error
      let errorMessage = 'Erro ao enviar arquivo. Tente novamente.'
      
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 400) {
          errorMessage = error.response.data?.detail || 'Arquivo inválido ou estrutura incorreta'
        } else if (error.response?.status === 413) {
          errorMessage = 'Arquivo muito grande'
        } else if (error.response?.status === 500) {
          errorMessage = 'Erro no servidor. Tente novamente mais tarde.'
        } else if (error.code === 'ECONNABORTED') {
          errorMessage = 'Tempo limite excedido. Arquivo muito grande?'
        }
      }

      setFeedback({
        type: 'error',
        message: errorMessage
      })
      onUploadError?.(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Handles drag over event
   */
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  /**
   * Handles drag leave event
   */
  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  /**
   * Handles drop event
   */
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileUpload(files[0])
    }
  }

  /**
   * Handles file input change event
   */
  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      handleFileUpload(files[0])
    }
  }

  /**
   * Handles click on upload area to open file browser
   */
  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="upload-card-container">
      <div className="upload-card">
        <div
          className={`upload-area ${isDragging ? 'dragging' : ''} ${isLoading ? 'loading' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              handleClick()
            }
          }}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileInputChange}
            disabled={isLoading}
            style={{ display: 'none' }}
            aria-label="Selecionar arquivo CSV"
          />

          {isLoading ? (
            <div className="upload-loading">
              <div className="spinner"></div>
              <p>Enviando arquivo...</p>
            </div>
          ) : (
            <div className="upload-content">
              <svg
                className="upload-icon"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <h3 className="upload-title">Arraste seu arquivo CSV aqui</h3>
              <p className="upload-subtitle">ou clique para selecionar</p>
              <p className="upload-hint">Máximo 10MB • Formato: .csv</p>
            </div>
          )}
        </div>

        {selectedFile && !isLoading && (
          <div className="selected-file">
            <svg
              className="file-icon"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span className="file-name">{selectedFile.name}</span>
          </div>
        )}

        {feedback.type && (
          <div className={`feedback feedback-${feedback.type}`}>
            <div className="feedback-content">
              {feedback.type === 'success' ? (
                <svg
                  className="feedback-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              ) : (
                <svg
                  className="feedback-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              )}
              <p className="feedback-message">{feedback.message}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default UploadCard
