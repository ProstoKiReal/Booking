import { computed, ref } from 'vue'
import Keycloak from 'keycloak-js'

export interface UserProfile {
  username: string
  name: string
  firstName: string
  lastName: string
  email: string
  roles: string[]
}

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8081',
  realm: 'events-realm',
  clientId: 'events-api',
})

export function useAuth() {
  const isReady = ref(false)
  const isAuthenticated = ref(false)
  const errorMessage = ref('')
  const profileClaims = ref<UserProfile | null>(null)

  const userName = computed(
    () => profileClaims.value?.username || profileClaims.value?.name || 'Профиль',
  )

  const canManageCategories = computed(() =>
    (profileClaims.value?.roles ?? []).some(
      (role) => role === 'admin' || role === 'seller',
    ),
  )

  function syncRealmRoles() {
    const claims: unknown = keycloak.tokenParsed
    if (!isRecord(claims)) {
      profileClaims.value = null
      return
    }

    const realmAccess = isRecord(claims.realm_access)
      ? claims.realm_access
      : null
    const roles = realmAccess?.roles

    profileClaims.value = {
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

  async function initialize() {
    try {
      isAuthenticated.value = await keycloak.init({
        pkceMethod: 'S256',
        checkLoginIframe: false,
      })
      syncRealmRoles()
    } catch {
      errorMessage.value =
        'Не удалось подключиться к сервису авторизации. Попробуйте позже.'
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

  function openAccountPage(section: 'personal-info' | 'password') {
    errorMessage.value = ''
    try {
      const accountUrl = new URL(keycloak.createAccountUrl())
      const accountPath = accountUrl.pathname.replace(/\/+$/, '')
      accountUrl.pathname =
        section === 'personal-info'
          ? `${accountPath}/`
          : `${accountPath}/account-security/signing-in`
      accountUrl.searchParams.set('kc_locale', 'ru')
      window.location.assign(accountUrl.toString())
    } catch {
      errorMessage.value = 'Не удалось открыть настройки учётной записи.'
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
    profile: computed(() => profileClaims.value),
    openPersonalInfo: () => openAccountPage('personal-info'),
    openPasswordSettings: () => openAccountPage('password'),
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

function stringClaim(value: unknown): string {
  return typeof value === 'string' ? value : ''
}
