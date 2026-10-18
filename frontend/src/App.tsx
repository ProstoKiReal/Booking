import { Suspense, lazy, useState } from 'react'
import { LoaderCircle } from 'lucide-react'
import { useAuth } from './composables/useAuth'
import AppHeader from './components/AppHeader'
import LoginPage from './components/LoginPage'
import { Alert, AlertDescription } from '@/components/ui/alert'

const CategoryAdmin = lazy(() => import('./components/CategoryAdmin'))
const EventAdmin = lazy(() => import('./components/EventAdmin'))
const EventsPage = lazy(() => import('./components/EventsPage'))
const ProfilePage = lazy(() => import('./components/ProfilePage'))

type CurrentView = 'home' | 'profile' | 'admin' | 'admin-events'

function App() {
  const auth = useAuth()
  const [currentView, setCurrentView] = useState<CurrentView>('home')

  if (!auth.isReady) {
    return (
      <main className="flex min-h-screen items-center justify-center gap-2 text-sm text-muted-foreground">
        <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
        Проверяем сеанс…
      </main>
    )
  }

  if (!auth.isAuthenticated) {
    return (
      <div className="mx-auto w-full max-w-7xl p-4 sm:p-6">
        <LoginPage
          isReady={auth.isReady}
          errorMessage={auth.errorMessage}
          onSignIn={auth.signIn}
        />
      </div>
    )
  }

  if (currentView === 'admin' && auth.canManageCategories) {
    return (
      <Suspense
        fallback={
          <p className="flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground">
            <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
            Загрузка…
          </p>
        }
      >
        <CategoryAdmin
          authorizedFetch={auth.authorizedFetch}
          userName={auth.userName}
          authErrorMessage={auth.errorMessage}
          onGoHome={() => setCurrentView('home')}
          onOpenEvents={() => setCurrentView('admin-events')}
          onOpenProfile={() => setCurrentView('profile')}
          onSignOut={auth.signOut}
        />
      </Suspense>
    )
  }

  if (currentView === 'admin-events' && auth.canManageCategories) {
    return (
      <Suspense
        fallback={
          <p className="flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground">
            <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
            Загрузка…
          </p>
        }
      >
        <EventAdmin
          authorizedFetch={auth.authorizedFetch}
          userName={auth.userName}
          authErrorMessage={auth.errorMessage}
          onGoHome={() => setCurrentView('home')}
          onOpenCategories={() => setCurrentView('admin')}
          onOpenProfile={() => setCurrentView('profile')}
          onSignOut={auth.signOut}
        />
      </Suspense>
    )
  }

  return (
    <div className="mx-auto w-full max-w-5xl p-4 sm:p-6">
      <AppHeader
        isAuthenticated={auth.isAuthenticated}
        userName={auth.userName}
        canManageCategories={auth.canManageCategories}
        showAdminView={currentView === 'admin'}
        showProfile={currentView === 'profile'}
        onSignOut={auth.signOut}
        onOpenAdmin={() => setCurrentView('admin')}
        onOpenProfile={() => setCurrentView('profile')}
        onGoHome={() => setCurrentView('home')}
      />

      {auth.errorMessage && (
        <Alert className="mt-4" variant="destructive">
          <AlertDescription>{auth.errorMessage}</AlertDescription>
        </Alert>
      )}

      <Suspense
        fallback={
          <p className="flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground">
            <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
            Загрузка…
          </p>
        }
      >
        {currentView === 'home' && (
          <EventsPage authorizedFetch={auth.authorizedFetch} />
        )}
        {currentView === 'profile' && auth.isAuthenticated && (
          <main className="py-6">
            <ProfilePage
              profile={auth.profile}
              keycloakApiFetch={auth.keycloakApiFetch}
            />
          </main>
        )}
      </Suspense>
    </div>
  )
}

export default App
