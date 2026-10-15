import { CalendarDays, LogOut, Shield, UserRound } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface AppHeaderProps {
  isAuthenticated: boolean
  userName: string
  canManageCategories: boolean
  showAdminView: boolean
  showProfile: boolean
  onSignOut: () => void
  onOpenAdmin: () => void
  onOpenProfile: () => void
  onGoHome: () => void
}

function AppHeader({
  isAuthenticated,
  userName,
  canManageCategories,
  showAdminView,
  showProfile,
  onSignOut,
  onOpenAdmin,
  onOpenProfile,
  onGoHome,
}: AppHeaderProps) {
  return (
    <header className="flex min-h-16 items-center justify-between gap-4 rounded-2xl border bg-card px-4 shadow-sm sm:px-6">
      <Button
        className="gap-2 px-2 text-base font-semibold"
        onClick={onGoHome}
        variant="ghost"
      >
        <CalendarDays className="size-5 text-primary" aria-hidden="true" />
        События
      </Button>
      <nav
        className="flex items-center justify-end gap-1 sm:gap-2"
        aria-label="Учётная запись"
      >
        {isAuthenticated && (
          <>
            <span className="hidden text-sm text-muted-foreground sm:inline">
              {userName}
            </span>
            <Button
              className="gap-2"
              disabled={showProfile}
              onClick={onOpenProfile}
              size="sm"
              variant="ghost"
            >
              <UserRound className="size-4" aria-hidden="true" />
              Профиль
            </Button>
            {canManageCategories && (
              <Button
                className="gap-2"
                onClick={showAdminView ? onGoHome : onOpenAdmin}
                size="sm"
                variant="outline"
              >
                <Shield className="size-4" aria-hidden="true" />
                {showAdminView ? 'На главную' : 'Админка'}
              </Button>
            )}
            <Button onClick={onSignOut} size="sm" variant="ghost">
              <LogOut className="size-4 sm:mr-1" aria-hidden="true" />
              Выйти
            </Button>
          </>
        )}
      </nav>
    </header>
  )
}

export default AppHeader
