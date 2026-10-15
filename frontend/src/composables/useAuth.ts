import { useCallback, useContext } from 'react'
import { useKeycloak } from '@react-keycloak/web'
import { AuthStateContext } from '../auth/AuthProvider'

export interface UserProfile {
  username: string
  name: string
  firstName: string
  lastName: string
  email: string
  roles: string[]
}

const KEYCLOAK_URL =
  import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8081'
const KEYCLOAK_REALM = 'events-realm'

export function useAuth() {
  const { keycloak, initialized } = useKeycloak()
  const authState = useContext(AuthStateContext)

  if (!authState) {
    throw new Error('useAuth must be used inside AuthProvider.')
  }
  const { errorMessage, setErrorMessage } = authState

  const profile = keycloak.authenticated
    ? getProfile(keycloak.tokenParsed)
    : null

  const signIn = useCallback(async () => {
    setErrorMessage('')
    try {
      await keycloak.login()
    } catch {
      setErrorMessage(
        'Не удалось открыть страницу входа. Попробуйте ещё раз.',
      )
    }
  }, [keycloak, setErrorMessage])

  const signOut = useCallback(async () => {
    setErrorMessage('')
    try {
      await keycloak.logout({ redirectUri: window.location.origin })
    } catch {
      setErrorMessage('Не удалось завершить сеанс. Попробуйте ещё раз.')
    }
  }, [keycloak, setErrorMessage])

  const keycloakApiFetch = useCallback(
    async (path: string, init?: RequestInit): Promise<Response> => {
      await keycloak.updateToken(30)
      if (!keycloak.token) {
        throw new Error('Сеанс входа завершён. Войдите снова.')
      }

      const headers = new Headers(init?.headers)
      headers.set('Authorization', `Bearer ${keycloak.token}`)
      if (init?.body) {
        headers.set('Content-Type', 'application/json')
      }

      if (init?.body && !headers.has('Content-Type')) {
        headers.set('Content-Type', 'application/json')
      }

      return fetch(
        `${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}${path}`,
        { ...init, headers },
      )
    },
    [keycloak],
  )

  const authorizedFetch = useCallback(
    async (path: string, init?: RequestInit): Promise<Response> => {
      await keycloak.updateToken(30)
      if (!keycloak.token) {
        throw new Error('Сеанс входа завершён. Войдите снова.')
      }

      const headers = new Headers(init?.headers)
      headers.set('Authorization', `Bearer ${keycloak.token}`)
      if (init?.body) {
        headers.set('Content-Type', 'application/json')
      }

      const gatewayUrl =
        import.meta.env.VITE_GATEWAY_URL || 'http://localhost:8080'
      return fetch(`${gatewayUrl}${path}`, { ...init, headers })
    },
    [keycloak],
  )

  const roles = profile?.roles ?? []

  return {
    isReady: initialized || authState.isReady,
    isAuthenticated: Boolean(keycloak.authenticated),
    userName: profile?.username || profile?.name || 'Профиль',
    profile,
    keycloakApiFetch,
    canManageCategories: roles.some(
      (role) => role === 'admin' || role === 'seller',
    ),
    errorMessage,
    signIn,
    signOut,
    authorizedFetch,
  }
}

function getProfile(claims: unknown): UserProfile | null {
  if (!isRecord(claims)) return null

  const realmAccess = isRecord(claims.realm_access) ? claims.realm_access : null
  const roles = realmAccess?.roles

  return {
    username: stringClaim(claims.preferred_username),
    name: stringClaim(claims.name),
    firstName: stringClaim(claims.given_name),
    lastName: stringClaim(claims.family_name),
    email: stringClaim(claims.email),
    roles: Array.isArray(roles)
      ? roles.filter((role): role is string => typeof role === 'string')
      : [],
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function stringClaim(value: unknown): string {
  return typeof value === 'string' ? value : ''
}
