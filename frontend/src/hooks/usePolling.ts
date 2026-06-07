import { useEffect, useRef, useState, useCallback } from 'react'

export interface UsePollingOptions {
  interval?: number // Intervalo em ms (default: 30000 = 30 segundos)
  enabled?: boolean // Se o polling está ativo (default: true)
  onError?: (error: Error) => void // Callback de erro
}

/**
 * Hook customizado para polling de dados
 * Executa uma função periodicamente e atualiza o estado
 *
 * @param callback - Função a ser executada periodicamente
 * @param options - Opções de configuração
 * @returns { lastUpdate, isPolling, stop, start }
 */
export function usePolling(
  callback: () => Promise<void>,
  options: UsePollingOptions = {}
) {
  const { interval = 30000, enabled = true, onError } = options

  const [lastUpdate, setLastUpdate] = useState<Date | null>(null)
  const [isPolling, setIsPolling] = useState(enabled)
  const intervalIdRef = useRef<NodeJS.Timeout | null>(null)
  const isMountedRef = useRef(true)

  // Função para executar o callback
  const executeCallback = useCallback(async () => {
    try {
      await callback()
      if (isMountedRef.current) {
        setLastUpdate(new Date())
      }
    } catch (error) {
      if (isMountedRef.current) {
        const err = error instanceof Error ? error : new Error(String(error))
        onError?.(err)
      }
    }
  }, [callback, onError])

  // Iniciar polling
  const start = useCallback(() => {
    if (intervalIdRef.current) return // Já está rodando

    setIsPolling(true)

    // Executar imediatamente
    executeCallback()

    // Configurar intervalo
    intervalIdRef.current = setInterval(() => {
      if (isMountedRef.current) {
        executeCallback()
      }
    }, interval)
  }, [executeCallback, interval])

  // Parar polling
  const stop = useCallback(() => {
    if (intervalIdRef.current) {
      clearInterval(intervalIdRef.current)
      intervalIdRef.current = null
    }
    setIsPolling(false)
  }, [])

  // Efeito para iniciar/parar polling
  useEffect(() => {
    isMountedRef.current = true

    if (enabled) {
      start()
    } else {
      stop()
    }

    return () => {
      isMountedRef.current = false
      stop()
    }
  }, [enabled, start, stop])

  return {
    lastUpdate,
    isPolling,
    stop,
    start,
  }
}

export default usePolling
