import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  ImageOff,
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

interface EventDetailsPageProps {
  authorizedFetch: (path: string, init?: RequestInit) => Promise<Response>
  eventId: string
  categoryName?: string
  onBack: () => void
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function isImage(value: unknown): value is EventImage {
  return (
    isRecord(value) &&
    typeof value.uuid === 'string' &&
    typeof value.url === 'string' &&
    typeof value.order === 'number'
  )
}

function isEvent(value: unknown): value is EventItem {
  return (
    isRecord(value) &&
    typeof value.id === 'string' &&
    typeof value.category_id === 'string' &&
    typeof value.name === 'string' &&
    typeof value.description === 'string' &&
    Array.isArray(value.images) &&
    value.images.every(isImage)
  )
}

async function loadEvent(
  authorizedFetch: EventDetailsPageProps['authorizedFetch'],
  eventId: string,
): Promise<EventItem> {
  const response = await authorizedFetch(
    `/api/v1/public/events/${encodeURIComponent(eventId)}`,
  )
  if (!response.ok) {
    throw new Error(
      response.status === 404
        ? 'Мероприятие не найдено.'
        : `Не удалось загрузить мероприятие (HTTP ${response.status}).`,
    )
  }

  const payload: unknown = await response.json()
  if (!isEvent(payload)) {
    throw new Error(
      'Сервис мероприятий вернул данные в неожиданном формате.',
    )
  }
  return payload
}

function EventDetailsPage({
  authorizedFetch,
  eventId,
  categoryName,
  onBack,
}: EventDetailsPageProps) {
  const [activeImageIndex, setActiveImageIndex] = useState(0)
  const eventQuery = useQuery({
    queryKey: ['public-event', eventId],
    queryFn: () => loadEvent(authorizedFetch, eventId),
  })

  const images = eventQuery.data?.images
    .slice()
    .sort((first, second) => first.order - second.order) ?? []
  const activeImage = images[activeImageIndex]

  function showPreviousImage() {
    setActiveImageIndex((index) => (index - 1 + images.length) % images.length)
  }

  function showNextImage() {
    setActiveImageIndex((index) => (index + 1) % images.length)
  }

  return (
    <main aria-labelledby="event-details-title" className="space-y-6 py-6">
      <Button className="-ml-2 gap-2" onClick={onBack} variant="ghost">
        <ArrowLeft aria-hidden="true" />
        К мероприятиям
      </Button>

      {eventQuery.isPending && (
        <p
          aria-live="polite"
          className="flex items-center justify-center gap-2 py-16 text-sm text-muted-foreground"
        >
          <LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
          Загружаем мероприятие…
        </p>
      )}

      {eventQuery.isError && (
        <Alert
          className="items-center justify-between gap-4"
          variant="destructive"
        >
          <AlertDescription>{eventQuery.error.message}</AlertDescription>
          <Button
            disabled={eventQuery.isFetching}
            onClick={() => void eventQuery.refetch()}
            size="sm"
            variant="outline"
          >
            <RefreshCw
              className={eventQuery.isFetching ? 'animate-spin' : ''}
              aria-hidden="true"
            />
            Повторить
          </Button>
        </Alert>
      )}

      {eventQuery.data && (
        <article className="space-y-6">
          <header className="space-y-2">
            {categoryName && (
              <p className="text-sm font-medium text-primary">{categoryName}</p>
            )}
            <h1
              className="text-3xl font-semibold tracking-tight sm:text-4xl"
              id="event-details-title"
            >
              {eventQuery.data.name}
            </h1>
          </header>

          {activeImage ? (
            <section aria-label="Фотографии мероприятия" className="space-y-3">
              <div className="relative overflow-hidden rounded-2xl border bg-muted">
                <img
                  alt={`${eventQuery.data.name}, фото ${activeImageIndex + 1}`}
                  className="max-h-[70vh] min-h-64 w-full object-contain"
                  src={activeImage.url}
                />
                {images.length > 1 && (
                  <>
                    <Button
                      aria-label="Предыдущее фото"
                      className="absolute top-1/2 left-3 -translate-y-1/2 rounded-full bg-background/90 shadow-md hover:bg-background"
                      onClick={showPreviousImage}
                      size="icon-lg"
                      variant="outline"
                    >
                      <ChevronLeft aria-hidden="true" />
                    </Button>
                    <Button
                      aria-label="Следующее фото"
                      className="absolute top-1/2 right-3 -translate-y-1/2 rounded-full bg-background/90 shadow-md hover:bg-background"
                      onClick={showNextImage}
                      size="icon-lg"
                      variant="outline"
                    >
                      <ChevronRight aria-hidden="true" />
                    </Button>
                    <span className="absolute right-3 bottom-3 rounded-full bg-background/90 px-3 py-1 text-sm font-medium">
                      {activeImageIndex + 1} / {images.length}
                    </span>
                  </>
                )}
              </div>

              {images.length > 1 && (
                <div
                  aria-label="Выбрать фотографию"
                  className="flex gap-2 overflow-x-auto py-1"
                  role="group"
                >
                  {images.map((image, index) => (
                    <button
                      aria-label={`Показать фото ${index + 1}`}
                      aria-pressed={index === activeImageIndex}
                      className={`size-16 shrink-0 overflow-hidden rounded-lg border-2 transition-colors sm:size-20 ${
                        index === activeImageIndex
                          ? 'border-primary'
                          : 'border-transparent opacity-70 hover:opacity-100'
                      }`}
                      key={image.uuid}
                      onClick={() => setActiveImageIndex(index)}
                      type="button"
                    >
                      <img
                        alt=""
                        className="size-full object-cover"
                        src={image.url}
                      />
                    </button>
                  ))}
                </div>
              )}
            </section>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center gap-2 py-12 text-center text-muted-foreground">
                <ImageOff className="size-8" aria-hidden="true" />
                <p>У этого мероприятия пока нет фотографий.</p>
              </CardContent>
            </Card>
          )}

          <Card className="border-border/70 shadow-sm">
            <CardHeader>
              <CardTitle>Об мероприятии</CardTitle>
              {categoryName && (
                <CardDescription>Категория: {categoryName}</CardDescription>
              )}
            </CardHeader>
            <CardContent>
              <p className="whitespace-pre-wrap leading-relaxed">
                {eventQuery.data.description}
              </p>
            </CardContent>
          </Card>
        </article>
      )}
    </main>
  )
}

export default EventDetailsPage
