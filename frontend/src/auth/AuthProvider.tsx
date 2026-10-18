import {
  createContext,
  useCallback,
  useMemo,
  useState,
  type PropsWithChildren,
} from 'react'
import { ReactKeycloakProvider } from '@react-keycloak/web'
import Keycloak from 'keycloak-js'

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8081',
  realm: 'events-realm',
  clientId: 'events-api',
})

const initOptions = {
  onLoad: 'check-sso' as const,
  silentCheckSsoRedirectUri: `${window.location.origin}/silent-check-sso.html`,
  pkceMethod: 'S256' as const,
  checkLoginIframe: false,
}

export const AuthStateContext = createContext<{
  isReady: boolean
  errorMessage: string
  setErrorMessage: (message: string) => void
} | null>(null)

export function AuthProvider({ children }: PropsWithChildren) {
  const [isReady, setIsReady] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleEvent = useCallback(
    (eventType: string, error?: { error_description?: string }) => {
      if (eventType === 'onInitError' || eventType === 'onAuthError') {
        if (eventType === 'onInitError') setIsReady(true)
        setErrorMessage(
          error?.error_description ||
            'Не удалось подключиться к сервису авторизации. Попробуйте позже.',
        )
      } else if (
        eventType === 'onReady' ||
        eventType === 'onAuthSuccess' ||
        eventType === 'onAuthRefreshSuccess' ||
        eventType === 'onAuthLogout'
      ) {
        if (eventType === 'onReady') setIsReady(true)
        setErrorMessage('')
      } else if (eventType === 'onAuthRefreshError') {
        setErrorMessage('Не удалось обновить сеанс. Войдите снова.')
      }
    },
    [],
  )

  const contextValue = useMemo(
    () => ({ isReady, errorMessage, setErrorMessage }),
    [isReady, errorMessage],
  )

  return (
    <AuthStateContext.Provider value={contextValue}>
      <ReactKeycloakProvider
        authClient={keycloak}
        initOptions={initOptions}
        onEvent={handleEvent}
      >
        {children}
      </ReactKeycloakProvider>
    </AuthStateContext.Provider>
  )
}
