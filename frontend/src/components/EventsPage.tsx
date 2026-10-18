import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  LoaderCircle,
  RefreshCw,
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import EventDetailsPage from './EventDetailsPage'

interface Category {
  id: string
  name: string
}

interface EventImage {
  uuid: string
  url: string
  order: number
}

interface EventItem {
  id: string
  category_id: string
  name: string
  description: string
  images: EventImage[]
}

interface EventsPageProps {
  authorizedFetch: (path: string, init?: RequestInit) => Promise<Response>
}

const pageSize = 9
const categoryPageSize = 100

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function isCategory(value: unknown): value is Category {
  return (
    isRecord(value) &&
    typeof value.id === 'string' &&
    typeof value.name === 'string'
  )
}

function isEventImage(value: unknown): value is EventImage {
  return (
    isRecord(value) &&
    typeof value.uuid === 'string' &&
    typeof value.url === 'string' &&
    typeof value.order === 'number'
  )
}

function isEventItem(value: unknown): value is EventItem {
  return (
    isRecord(value) &&
    typeof value.id === 'string' &&
    typeof value.category_id === 'string' &&
    typeof value.name === 'string' &&
    typeof value.description === 'string' &&
    Array.isArray(value.images) &&
    value.images.every(isEventImage)
  )
}

function readList<T>(
  payload: unknown,
  isItem: (value: unknown) => value is T,
  errorMessage: string,
): T[] {
  const items =
    isRecord(payload) && Array.isArray(payload.result) ? payload.result : null
  if (!items || !items.every(isItem)) throw new Error(errorMessage)
  return items
}

function EventsPage({ authorizedFetch }: EventsPageProps) {
  const [categoryId, setCategoryId] = useState('')
  const [offset, setOffset] = useState(0)
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null)

  const categoriesQuery = useQuery({
    queryKey: ['public-categories'],
    queryFn: async (): Promise<Category[]> => {
      const categories: Category[] = []

      for (let offset = 0; ; offset += categoryPageSize) {
        const response = await authorizedFetch(
          `/api/v1/public/categories/?offset=${offset}&limit=${categoryPageSize}`,
        )
        if (!response.ok) {
          throw new Error(
            `Не удалось загрузить категории (HTTP ${response.status}).`,
          )
        }

        const page = readList(
          await response.json(),
          isCategory,
          'Сервис категорий вернул данные в неожиданном формате.',
        )
        categories.push(...page)

        if (page.length < categoryPageSize) return categories
      }
    },
  })

  const eventsQuery = useQuery({
    queryKey: ['public-events', { categoryId, offset, limit: pageSize }],
    queryFn: async (): Promise<EventItem[]> => {
      const params = new URLSearchParams({
        offset: String(offset),
        limit: String(pageSize),
      })
      if (categoryId) params.set('category_id', categoryId)
      const response = await authorizedFetch(
        `/api/v1/public/events/?${params.toString()}`,
      )
      if (!response.ok) {
        throw new Error(
          `Не удалось загрузить мероприятия (HTTP ${response.status}).`,
        )
      }
      return readList(
        await response.json(),
        isEventItem,
        'Сервис мероприятий вернул данные в неожиданном формате.',
      )
    },
  })

  const errorMessage =
    eventsQuery.error instanceof Error
      ? eventsQuery.error.message
      : categoriesQuery.error instanceof Error
        ? categoriesQuery.error.message
        : ''

  if (selectedEventId) {
    return (
      <EventDetailsPage
        authorizedFetch={authorizedFetch}
        eventId={selectedEventId}
        categoryName={
          categoriesQuery.data?.find(
            (category) =>
              eventsQuery.data?.find((event) => event.id === selectedEventId)
                ?.category_id === category.id,
          )?.name
        }
        onBack={() => setSelectedEventId(null)}
      />
    )
  }

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

      <div className="flex flex-col gap-2 sm:max-w-xs">
        <label className="text-sm font-medium" htmlFor="event-category-filter">
          Категория
        </label>
        <select
          className="h-10 rounded-lg border border-input bg-background px-3 text-sm"
          id="event-category-filter"
          onChange={(event) => {
            setCategoryId(event.target.value)
            setOffset(0)
          }}
          value={categoryId}
        >
          <option value="">Все категории</option>
          {(categoriesQuery.data ?? []).map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      {errorMessage && (
        <Alert className="items-center justify-between gap-4" variant="destructive">
          <AlertDescription>{errorMessage}</AlertDescription>
          <Button
            disabled={eventsQuery.isFetching || categoriesQuery.isFetching}
            onClick={() => {
              void eventsQuery.refetch()
              void categoriesQuery.refetch()
            }}
            size="sm"
            variant="outline"
          >
            <RefreshCw
              className={
                eventsQuery.isFetching || categoriesQuery.isFetching
                  ? 'animate-spin'
                  : ''
              }
              aria-hidden="true"
            />
            Повторить
          </Button>
        </Alert>
      )}

      {eventsQuery.isPending && (
        <p
          aria-live="polite"
          className="flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground"
        >
          <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
          Загружаем мероприятия…
        </p>
      )}

      {eventsQuery.isSuccess && eventsQuery.data.length === 0 && (
        <Card className="border-border/70 shadow-sm">
          <CardContent className="flex flex-col items-center gap-3 py-12 text-center">
            <span className="flex size-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">
              <CalendarDays className="size-6" aria-hidden="true" />
            </span>
            <div>
              <CardTitle>Мероприятия не найдены</CardTitle>
              <CardDescription className="mt-2">
                {categoryId
                  ? 'В этой категории пока нет событий.'
                  : 'Новые события появятся здесь.'}
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
          {eventsQuery.data.map((event) => {
            const cover = [...event.images].sort(
              (first, second) => first.order - second.order,
            )[0]
            return (
              <Card
                className="overflow-hidden border-border/70 shadow-sm transition-shadow hover:shadow-md"
                key={event.id}
              >
                <button
                  className="block w-full text-left"
                  onClick={() => setSelectedEventId(event.id)}
                  type="button"
                >
                  {cover && (
                    <img
                      alt=""
                      className="aspect-[16/10] w-full object-cover"
                      loading="lazy"
                      src={cover.url}
                    />
                  )}
                  <CardHeader>
                    <CardTitle>{event.name}</CardTitle>
                    <CardDescription className="line-clamp-4 whitespace-pre-wrap">
                      {event.description}
                    </CardDescription>
                  </CardHeader>
                </button>
              </Card>
            )
          })}
        </section>
      )}

      {eventsQuery.isSuccess && (
        <nav
          aria-label="Страницы мероприятий"
          className="flex items-center justify-between border-t pt-4"
        >
          <p className="text-sm text-muted-foreground">
            {eventsQuery.data.length > 0
              ? `${offset + 1}–${offset + eventsQuery.data.length}`
              : 'Нет мероприятий'}
          </p>
          <div className="flex items-center gap-3">
            <span className="text-sm text-muted-foreground">
              Страница {Math.floor(offset / pageSize) + 1}
            </span>
            <Button
              aria-label="Предыдущая страница"
              disabled={offset === 0 || eventsQuery.isFetching}
              onClick={() => setOffset((current) => Math.max(0, current - pageSize))}
              size="icon"
              variant="outline"
            >
              <ChevronLeft aria-hidden="true" />
            </Button>
            <Button
              aria-label="Следующая страница"
              disabled={
                eventsQuery.data.length < pageSize || eventsQuery.isFetching
              }
              onClick={() => setOffset((current) => current + pageSize)}
              size="icon"
              variant="outline"
            >
              <ChevronRight aria-hidden="true" />
            </Button>
          </div>
        </nav>
      )}
    </main>
  )
}

export default EventsPage
