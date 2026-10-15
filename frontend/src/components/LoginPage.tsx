import { ArrowRight, CalendarDays, ShieldCheck, Sparkles } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

interface LoginPageProps {
  isReady: boolean
  errorMessage: string
  onSignIn: () => void
}

function LoginPage({ isReady, errorMessage, onSignIn }: LoginPageProps) {
  return (
    <main className="relative isolate flex min-h-[calc(100vh-2rem)] items-center justify-center overflow-hidden rounded-3xl border bg-background px-5 py-12 sm:px-10">
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-primary/10 via-background to-background"
      />
      <div className="grid w-full max-w-5xl items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]">
        <section className="mx-auto max-w-xl">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border bg-background/80 px-3 py-1.5 text-sm text-muted-foreground shadow-sm">
            <CalendarDays className="size-4 text-primary" aria-hidden="true" />
            <span>Афиша впечатлений</span>
          </div>
          <h1 className="text-4xl font-semibold tracking-tight text-balance sm:text-6xl">
            События, которые хочется пережить.
          </h1>
          <p className="mt-6 max-w-lg text-lg leading-8 text-muted-foreground">
            Концерты, спектакли и выставки — соберите свою афишу и возвращайтесь
            к любимым событиям.
          </p>
          <div className="mt-9 flex items-center gap-3 text-sm text-muted-foreground">
            <span className="flex size-9 items-center justify-center rounded-full bg-primary/10 text-primary">
              <Sparkles className="size-4" aria-hidden="true" />
            </span>
            <span>Ваш профиль и настройки доступны после входа.</span>
          </div>
        </section>

        <Card className="mx-auto w-full max-w-md border-border/70 bg-card/95 shadow-xl shadow-primary/5 backdrop-blur">
          <CardHeader className="gap-3 p-7 pb-2">
            <div className="flex size-11 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
              <CalendarDays className="size-5" aria-hidden="true" />
            </div>
            <CardTitle className="text-2xl">Добро пожаловать</CardTitle>
            <CardDescription className="text-sm leading-6">
              Войдите в личный кабинет, чтобы продолжить.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-5 p-7 pt-4">
            {errorMessage && (
              <Alert variant="destructive">
                <AlertDescription>{errorMessage}</AlertDescription>
              </Alert>
            )}
            <Button
              className="h-11 w-full"
              disabled={!isReady}
              onClick={onSignIn}
              size="lg"
            >
              {isReady ? 'Войти через Keycloak' : 'Подключаем защищённый вход…'}
              {isReady && <ArrowRight data-icon="inline-end" />}
            </Button>
            <p className="flex items-center justify-center gap-2 text-center text-xs text-muted-foreground">
              <ShieldCheck className="size-4 shrink-0" aria-hidden="true" />
              Защищённый вход с помощью Keycloak
            </p>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}

export default LoginPage
