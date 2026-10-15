import { useQuery } from '@tanstack/react-query'
import { CalendarDays, LoaderCircle, RefreshCw } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

interface EventItem {
  id: string | number
  name: string
  description: string
}

interface EventsPageProps {
  authorizedFetch: (path: string, init?: RequestInit) => Promise<Response>
}

const eventsQueryKey = ['public-events'] as const

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function isEventItem(value: unknown): value is EventItem {
  return (
    isRecord(value) &&
    (typeof value.id === 'string' || typeof value.id === 'number') &&
    typeof value.name === 'string' &&
    typeof value.description === 'string'
  )
}

async function loadEvents(
  authorizedFetch: EventsPageProps['authorizedFetch'],
): Promise<EventItem[]> {
  const response = await authorizedFetch('/api/v1/public/events/')
  if (!response.ok) {
    throw new Error(`Не удалось загрузить мероприятия (HTTP ${response.status}).`)
  }

  const payload: unknown = await response.json()
  const events = Array.isArray(payload)
    ? payload
    : isRecord(payload) && Array.isArray(payload.result)
      ? payload.result
      : null

  if (!events || !events.every(isEventItem)) {
    throw new Error(
      'Сервис мероприятий вернул данные в неожиданном формате. Попробуйте позже.',
    )
  }

  return events
}

function EventsPage({ authorizedFetch }: EventsPageProps) {
  const eventsQuery = useQuery({
    queryKey: eventsQueryKey,
    queryFn: () => loadEvents(authorizedFetch),
  })

  return (
    <main aria-labelledby="events-title" className="space-y-6 py-6">
      <header className="space-y-2">
        <div className="flex items-center gap-2 text-sm font-medium text-primary">
          <CalendarDays className="size-4" aria-hidden="true" />
          Афиша впечатлений
        </div>
        <h1 id="events-title" className="text-3xl font-semibold tracking-tight">
          Мероприятия
        </h1>
        <p className="text-muted-foreground">
          Найдите событие, которое захочется пережить.
        </p>
      </header>

      {eventsQuery.isPending && (
        <p
          aria-live="polite"
          className="flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground"
        >
          <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
          Загружаем мероприятия…
        </p>
      )}

      {eventsQuery.isError && (
        <Alert className="items-center justify-between gap-4" variant="destructive">
          <AlertDescription>{eventsQuery.error.message}</AlertDescription>
          <Button
            disabled={eventsQuery.isFetching}
            onClick={() => void eventsQuery.refetch()}
            size="sm"
            variant="outline"
          >
            <RefreshCw
              className={eventsQuery.isFetching ? 'animate-spin' : ''}
              aria-hidden="true"
            />
            Повторить
          </Button>
        </Alert>
      )}

      {eventsQuery.isSuccess && eventsQuery.data.length === 0 && (
        <Card className="border-border/70 shadow-sm">
          <CardContent className="flex flex-col items-center gap-3 py-12 text-center">
            <span className="flex size-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">
              <CalendarDays className="size-6" aria-hidden="true" />
            </span>
            <div>
              <CardTitle>Пока нет мероприятий</CardTitle>
              <CardDescription className="mt-2">
                Новые события появятся здесь.
              </CardDescription>
            </div>
          </CardContent>
        </Card>
      )}

      {eventsQuery.data && eventsQuery.data.length > 0 && (
        <section
          aria-label="Список мероприятий"
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
          {eventsQuery.data.map((event) => (
            <Card
              className="border-border/70 shadow-sm transition-shadow hover:shadow-md"
              key={event.id}
            >
              <CardHeader>
                <CardTitle>{event.name}</CardTitle>
                <CardDescription className="line-clamp-4 whitespace-pre-wrap">
                  {event.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </section>
      )}
    </main>
  )
}

export default EventsPage
