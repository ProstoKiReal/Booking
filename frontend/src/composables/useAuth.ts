import { computed, ref } from 'vue'
import Keycloak from 'keycloak-js'

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8081',
  realm: 'events-realm',
  clientId: 'events-api',
})

export function useAuth() {
  const isReady = ref(false)
  const isAuthenticated = ref(false)
  const errorMessage = ref('')
  const realmRoles = ref<string[]>([])

  const userName = computed(
    () =>
      keycloak.tokenParsed?.preferred_username ??
      keycloak.tokenParsed?.name ??
      'Профиль',
  )

  const canManageCategories = computed(() =>
    realmRoles.value.some((role) => role === 'admin' || role === 'seller'),
  )

  function syncRealmRoles() {
    const claims: unknown = keycloak.tokenParsed
    if (!isRecord(claims) || !isRecord(claims.realm_access)) {
      realmRoles.value = []
      return
    }

    const roles = claims.realm_access.roles
    realmRoles.value = Array.isArray(roles)
      ? roles.filter((role): role is string => typeof role === 'string')
      : []
  }

  async function initialize() {
    try {
      isAuthenticated.value = await keycloak.init({
        pkceMethod: 'S256',
        checkLoginIframe: false,
      })
      syncRealmRoles()
    } catch {
      errorMessage.value =
        'Не удалось подключиться к Keycloak. Проверьте, что сервис запущен.'
    } finally {
      isReady.value = true
    }
  }

  async function signIn() {
    errorMessage.value = ''
    try {
      await keycloak.login()
    } catch {
      errorMessage.value = 'Не удалось открыть страницу входа. Попробуйте ещё раз.'
    }
  }

  async function signOut() {
    errorMessage.value = ''
    try {
      await keycloak.logout({ redirectUri: window.location.origin })
    } catch {
      errorMessage.value = 'Не удалось завершить сеанс. Попробуйте ещё раз.'
    }
  }

  async function authorizedFetch(
    path: string,
    init?: RequestInit,
  ): Promise<Response> {
    await keycloak.updateToken(30)
    syncRealmRoles()
    if (!keycloak.token) {
      throw new Error('Сеанс входа завершён. Войдите снова.')
    }

    const headers = new Headers(init?.headers)
    headers.set('Authorization', `Bearer ${keycloak.token}`)
    if (init?.body) {
      headers.set('Content-Type', 'application/json')
    }

    const gatewayUrl = import.meta.env.VITE_GATEWAY_URL || 'http://localhost:8080'
    return fetch(`${gatewayUrl}${path}`, { ...init, headers })
  }

  return {
    isReady,
    isAuthenticated,
    userName,
    canManageCategories,
    errorMessage,
    initialize,
    signIn,
    signOut,
    authorizedFetch,
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}
