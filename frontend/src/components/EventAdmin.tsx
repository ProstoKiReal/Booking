import { useMemo, useState, type FormEvent } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  CircleUserRound,
  Home,
  Layers3,
  LoaderCircle,
  LogOut,
  Pencil,
  Plus,
  Trash2,
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'

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

interface EventAdminProps {
  authorizedFetch: (path: string, init?: RequestInit) => Promise<Response>
  userName: string
  authErrorMessage: string
  onGoHome: () => void
  onOpenCategories: () => void
  onOpenProfile: () => void
  onSignOut: () => void
}

const pageSize = 10
const eventsQueryKey = ['admin-events'] as const
const categoriesQueryKey = ['event-admin-categories'] as const

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

function isEvent(value: unknown): value is EventItem {
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

function readResult<T>(
  payload: unknown,
  guard: (value: unknown) => value is T,
  errorMessage: string,
): T[] {
  if (
    !isRecord(payload) ||
    !Array.isArray(payload.result) ||
    !payload.result.every(guard)
  ) {
    throw new Error(errorMessage)
  }
  return payload.result
}

async function responseError(
  response: Response,
  action: string,
): Promise<Error> {
  let message = `${action} (HTTP ${response.status}).`
  if (response.headers.get('content-type')?.includes('application/json')) {
    const payload: unknown = await response.json()
    if (isRecord(payload)) {
      if (typeof payload.error === 'string') message = payload.error
      else if (typeof payload.message === 'string') message = payload.message
      else if (typeof payload.detail === 'string') message = payload.detail
      else if (Array.isArray(payload.detail)) {
        const messages = payload.detail.flatMap((item) =>
          isRecord(item) && typeof item.msg === 'string' ? [item.msg] : [],
        )
        if (messages.length > 0) message = messages.join(' ')
      }
    }
  }
  return new Error(message)
}

async function readEventResponse(
  response: Response,
  action: string,
): Promise<EventItem> {
  if (!response.ok) throw await responseError(response, action)
  const payload: unknown = await response.json()
  if (!isEvent(payload)) {
    throw new Error('Сервер вернул мероприятие в неожиданном формате.')
  }
  return payload
}

function eventFormData(
  name: string,
  description: string,
  categoryId: string,
  images: File[],
): FormData {
  const data = new FormData()
  data.set('name', name.trim())
  data.set('description', description.trim())
  data.set('category_id', categoryId)
  images.forEach((image) => data.append('images', image))
  return data
}

function EventAdmin({
  authorizedFetch,
  userName,
  authErrorMessage,
  onGoHome,
  onOpenCategories,
  onOpenProfile,
  onSignOut,
}: EventAdminProps) {
  const queryClient = useQueryClient()
  const [categoryFilter, setCategoryFilter] = useState('')
  const [offset, setOffset] = useState(0)
  const [isCreateOpen, setIsCreateOpen] = useState(false)
  const [eventToEdit, setEventToEdit] = useState<EventItem | null>(null)
  const [eventToDelete, setEventToDelete] = useState<EventItem | null>(null)
  const [eventName, setEventName] = useState('')
  const [description, setDescription] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [createImages, setCreateImages] = useState<File[]>([])
  const [updateImages, setUpdateImages] = useState<Record<string, File>>({})
  const [imageOrders, setImageOrders] = useState<Record<string, number>>({})
  const [successMessage, setSuccessMessage] = useState('')

  const categoriesQuery = useQuery({
    queryKey: categoriesQueryKey,
    queryFn: async (): Promise<Category[]> => {
      const response = await authorizedFetch(
        '/api/v1/public/categories/?offset=0&limit=100',
      )
      if (!response.ok) {
        throw await responseError(response, 'Не удалось загрузить категории')
      }
      return readResult(
        await response.json(),
        isCategory,
        'Сервис категорий вернул данные в неожиданном формате.',
      )
    },
  })

  const eventsQuery = useQuery({
    queryKey: [...eventsQueryKey, categoryFilter, offset, pageSize],
    queryFn: async (): Promise<EventItem[]> => {
      const params = new URLSearchParams({
        offset: String(offset),
        limit: String(pageSize),
      })
      if (categoryFilter) params.set('category_id', categoryFilter)
      const response = await authorizedFetch(
        `/api/v1/public/events/?${params.toString()}`,
      )
      if (!response.ok) {
        throw await responseError(response, 'Не удалось загрузить мероприятия')
      }
      return readResult(
        await response.json(),
        isEvent,
        'Сервис мероприятий вернул данные в неожиданном формате.',
      )
    },
  })

  const categoriesById = useMemo(
    () =>
      new Map((categoriesQuery.data ?? []).map((category) => [category.id, category.name])),
    [categoriesQuery.data],
  )

  const createMutation = useMutation({
    mutationFn: async () => {
      const response = await authorizedFetch('/api/v1/admin/events/', {
        method: 'POST',
        body: eventFormData(eventName, description, categoryId, createImages),
      })
      return readEventResponse(response, 'Не удалось создать мероприятие')
    },
    onSuccess: async (event) => {
      setIsCreateOpen(false)
      setSuccessMessage(`Мероприятие «${event.name}» создано.`)
      clearForm()
      await queryClient.invalidateQueries({ queryKey: eventsQueryKey })
    },
  })

  const updateMutation = useMutation({
    mutationFn: async (event: EventItem) => {
      const data = new FormData()
      data.set('name', eventName.trim())
      data.set('description', description.trim())
      const orderedImages = [...event.images].sort(
        (first, second) => first.order - second.order,
      )
      for (const image of orderedImages) {
        const file = updateImages[image.uuid]
        if (!file) {
          throw new Error('Выберите новый файл для каждого изображения.')
        }
        const order = imageOrders[image.uuid] ?? image.order
        if (!Number.isInteger(order) || order < 0 || order > 11) {
          throw new Error('Порядок изображения должен быть от 0 до 11.')
        }
        data.append('image_ids', image.uuid)
        data.append('images', file)
        data.append('orders', String(order))
      }
      const orders = orderedImages.map((image) => imageOrders[image.uuid] ?? image.order)
      if (new Set(orders).size !== orders.length) {
        throw new Error('Порядок изображений должен быть уникальным.')
      }
      const response = await authorizedFetch(
        `/api/v1/admin/events/${encodeURIComponent(event.id)}`,
        { method: 'PATCH', body: data },
      )
      return readEventResponse(response, 'Не удалось изменить мероприятие')
    },
    onSuccess: async (event) => {
      setEventToEdit(null)
      setSuccessMessage(`Мероприятие «${event.name}» обновлено.`)
      await queryClient.invalidateQueries({ queryKey: eventsQueryKey })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (event: EventItem) => {
      const response = await authorizedFetch(
        `/api/v1/admin/events/${encodeURIComponent(event.id)}`,
        { method: 'DELETE' },
      )
      if (!response.ok) {
        throw await responseError(response, 'Не удалось удалить мероприятие')
      }
      return event
    },
    onSuccess: async (event) => {
      setEventToDelete(null)
      setSuccessMessage(`Мероприятие «${event.name}» удалено.`)
      await queryClient.invalidateQueries({ queryKey: eventsQueryKey })
    },
  })

  const errorMessage =
    authErrorMessage ||
    (categoriesQuery.error instanceof Error
      ? categoriesQuery.error.message
      : '') ||
    (eventsQuery.error instanceof Error ? eventsQuery.error.message : '') ||
    (createMutation.error instanceof Error
      ? createMutation.error.message
      : '') ||
    (updateMutation.error instanceof Error
      ? updateMutation.error.message
      : '') ||
    (deleteMutation.error instanceof Error
      ? deleteMutation.error.message
      : '')

  function clearForm() {
    setEventName('')
    setDescription('')
    setCategoryId('')
    setCreateImages([])
    setUpdateImages({})
    setImageOrders({})
  }

  function openCreate() {
    clearForm()
    setSuccessMessage('')
    createMutation.reset()
    setIsCreateOpen(true)
  }

  function openEdit(event: EventItem) {
    setEventName(event.name)
    setDescription(event.description)
    setUpdateImages({})
    setImageOrders(
      Object.fromEntries(event.images.map((image) => [image.uuid, image.order])),
    )
    setSuccessMessage('')
    updateMutation.reset()
    setEventToEdit(event)
  }

  function submitCreate(formEvent: FormEvent<HTMLFormElement>) {
    formEvent.preventDefault()
    createMutation.mutate()
  }

  function submitUpdate(formEvent: FormEvent<HTMLFormElement>) {
    formEvent.preventDefault()
    if (eventToEdit) updateMutation.mutate(eventToEdit)
  }

  const initials = userName
    .split(/[\s@._-]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toLocaleUpperCase('ru-RU'))
    .join('')

  return (
    <div className="flex min-h-screen bg-muted/30">
      <aside className="hidden w-64 flex-col border-r bg-card md:flex">
        <div className="flex h-16 items-center gap-3 border-b px-5">
          <span className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <CalendarDays className="size-5" aria-hidden="true" />
          </span>
          <div>
            <p className="font-semibold leading-tight">События</p>
            <p className="text-xs text-muted-foreground">Панель управления</p>
          </div>
        </div>
        <nav aria-label="Главная навигация" className="flex-1 space-y-1 p-3">
          <p className="px-3 pb-1 pt-2 text-xs font-medium text-muted-foreground">
            ОБЗОР
          </p>
          <button
            className="flex h-9 w-full items-center gap-3 rounded-lg px-3 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            onClick={onGoHome}
            type="button"
          >
            <Home className="size-4" aria-hidden="true" />
            Афиша
          </button>
          <p className="px-3 pb-1 pt-5 text-xs font-medium text-muted-foreground">
            УПРАВЛЕНИЕ
          </p>
          <div
            aria-current="page"
            className="flex h-9 items-center gap-3 rounded-lg bg-primary/10 px-3 text-sm font-medium text-primary"
          >
            <CalendarDays className="size-4" aria-hidden="true" />
            Мероприятия
          </div>
          <button
            className="flex h-9 w-full items-center gap-3 rounded-lg px-3 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            onClick={onOpenCategories}
            type="button"
          >
            <Layers3 className="size-4" aria-hidden="true" />
            Категории
          </button>
        </nav>
        <div className="border-t p-3">
          <button
            className="flex w-full items-center gap-3 rounded-lg p-2 text-left transition-colors hover:bg-muted"
            onClick={onOpenProfile}
            type="button"
          >
            <Avatar size="sm">
              <AvatarFallback className="bg-primary/10 text-xs font-medium text-primary">
                {initials || <CircleUserRound className="size-4" />}
              </AvatarFallback>
            </Avatar>
            <span className="min-w-0 flex-1 truncate text-sm font-medium">
              {userName}
            </span>
          </button>
        </div>
      </aside>

      <div className="flex min-h-screen min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b bg-card/95 px-4 backdrop-blur sm:px-6">
          <span className="truncate text-sm text-muted-foreground">
            Панель управления <span className="px-1">/</span>
            <span className="font-medium text-foreground">Мероприятия</span>
          </span>
          <div className="flex items-center gap-2">
            <Button
              className="hidden sm:inline-flex"
              onClick={onGoHome}
              size="sm"
              variant="ghost"
            >
              Афиша
            </Button>
            <Button
              className="hidden sm:inline-flex"
              onClick={onOpenCategories}
              size="sm"
              variant="ghost"
            >
              Категории
            </Button>
            <Button
              className="hidden gap-2 sm:inline-flex"
              onClick={onOpenProfile}
              size="sm"
              variant="ghost"
            >
              <CircleUserRound className="size-4" aria-hidden="true" />
              <span className="max-w-36 truncate">{userName}</span>
            </Button>
            <Button
              aria-label="Выйти"
              onClick={onSignOut}
              size="icon"
              variant="ghost"
            >
              <LogOut aria-hidden="true" />
            </Button>
          </div>
        </header>

        <main className="mx-auto w-full max-w-7xl flex-1 space-y-6 p-4 sm:p-6 lg:p-8">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div className="space-y-1">
              <h1 className="text-2xl font-semibold tracking-tight">
                Мероприятия
              </h1>
              <p className="text-sm text-muted-foreground">
                Создавайте события и управляйте их галереями.
              </p>
            </div>
            <Button className="gap-2" onClick={openCreate}>
              <Plus aria-hidden="true" />
              Добавить мероприятие
            </Button>
          </div>

          {errorMessage && (
            <Alert variant="destructive">
              <AlertDescription>{errorMessage}</AlertDescription>
            </Alert>
          )}
          {successMessage && (
            <Alert
              className="border-emerald-300 bg-emerald-50 text-emerald-950"
              role="status"
            >
              <AlertDescription>{successMessage}</AlertDescription>
            </Alert>
          )}

          <Card className="border-border/70 shadow-sm">
            <CardHeader className="flex flex-col items-stretch justify-between gap-4 space-y-0 sm:flex-row sm:items-center">
              <div className="space-y-1">
                <CardTitle className="text-base">Список мероприятий</CardTitle>
                <CardDescription>
                  Фильтруйте список по категории.
                </CardDescription>
              </div>
              <div className="grid w-full gap-2 sm:max-w-xs">
                <label className="text-sm font-medium" htmlFor="admin-event-category">
                  Категория
                </label>
                <select
                  className="h-9 rounded-lg border border-input bg-background px-3 text-sm"
                  id="admin-event-category"
                  onChange={(event) => {
                    setCategoryFilter(event.target.value)
                    setOffset(0)
                  }}
                  value={categoryFilter}
                >
                  <option value="">Все категории</option>
                  {(categoriesQuery.data ?? []).map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>
            </CardHeader>
            <CardContent className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {eventsQuery.isPending && (
                <p className="col-span-full flex items-center justify-center gap-2 py-12 text-sm text-muted-foreground">
                  <LoaderCircle
                    className="size-4 animate-spin"
                    aria-hidden="true"
                  />
                  Загружаем мероприятия…
                </p>
              )}
              {eventsQuery.data?.map((event) => {
                const cover = [...event.images].sort(
                  (first, second) => first.order - second.order,
                )[0]
                return (
                  <Card className="overflow-hidden" key={event.id}>
                    {cover && (
                      <img
                        alt=""
                        className="aspect-[16/10] w-full object-cover"
                        loading="lazy"
                        src={cover.url}
                      />
                    )}
                    <CardHeader>
                      <CardTitle className="text-base">{event.name}</CardTitle>
                      <CardDescription>
                        {categoriesById.get(event.category_id) ??
                          'Категория недоступна'}
                      </CardDescription>
                      <p className="line-clamp-3 whitespace-pre-wrap text-sm text-muted-foreground">
                        {event.description}
                      </p>
                    </CardHeader>
                    <CardContent className="flex justify-end gap-2">
                      <Button
                        onClick={() => openEdit(event)}
                        size="sm"
                        variant="outline"
                      >
                        <Pencil aria-hidden="true" />
                        Изменить
                      </Button>
                      <Button
                        onClick={() => {
                          deleteMutation.reset()
                          setEventToDelete(event)
                        }}
                        size="sm"
                        variant="destructive"
                      >
                        <Trash2 aria-hidden="true" />
                        Удалить
                      </Button>
                    </CardContent>
                  </Card>
                )
              })}
              {eventsQuery.isSuccess && eventsQuery.data.length === 0 && (
                <div className="col-span-full py-12 text-center">
                  <p className="font-medium">Мероприятия не найдены</p>
                  <p className="mt-2 text-sm text-muted-foreground">
                    Измените фильтр или добавьте первое мероприятие.
                  </p>
                </div>
              )}
            </CardContent>
            <div className="flex items-center justify-between border-t px-4 py-3 sm:px-6">
              <p className="text-sm text-muted-foreground">
                {eventsQuery.data?.length
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
                  onClick={() =>
                    setOffset((current) => Math.max(0, current - pageSize))
                  }
                  size="icon"
                  variant="outline"
                >
                  <ChevronLeft aria-hidden="true" />
                </Button>
                <Button
                  aria-label="Следующая страница"
                  disabled={
                    (eventsQuery.data?.length ?? 0) < pageSize ||
                    eventsQuery.isFetching
                  }
                  onClick={() => setOffset((current) => current + pageSize)}
                  size="icon"
                  variant="outline"
                >
                  <ChevronRight aria-hidden="true" />
                </Button>
              </div>
            </div>
          </Card>
        </main>
      </div>

      <Dialog
        onOpenChange={(open) => {
          if (!createMutation.isPending && !open) setIsCreateOpen(false)
        }}
        open={isCreateOpen}
      >
        <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-xl">
          <form className="grid gap-5" onSubmit={submitCreate}>
            <DialogHeader>
              <DialogTitle>Новое мероприятие</DialogTitle>
              <DialogDescription>
                Заполните информацию и добавьте от 1 до 12 фотографий.
              </DialogDescription>
            </DialogHeader>
            <EventFields
              categories={categoriesQuery.data ?? []}
              categoryId={categoryId}
              description={description}
              eventName={eventName}
              images={createImages}
              onCategoryChange={setCategoryId}
              onDescriptionChange={setDescription}
              onImagesChange={setCreateImages}
              onNameChange={setEventName}
            />
            {createMutation.error instanceof Error && (
              <Alert variant="destructive">
                <AlertDescription>
                  {createMutation.error.message}
                </AlertDescription>
              </Alert>
            )}
            <DialogFooter>
              <Button
                disabled={createMutation.isPending}
                onClick={() => setIsCreateOpen(false)}
                type="button"
                variant="outline"
              >
                Отмена
              </Button>
              <Button
                disabled={
                  createMutation.isPending ||
                  categoriesQuery.isPending ||
                  createImages.length < 1 ||
                  createImages.length > 12
                }
                type="submit"
              >
                {createMutation.isPending && (
                  <LoaderCircle className="animate-spin" aria-hidden="true" />
                )}
                Создать
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <Dialog
        onOpenChange={(open) => {
          if (!updateMutation.isPending && !open) setEventToEdit(null)
        }}
        open={Boolean(eventToEdit)}
      >
        <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-2xl">
          <form className="grid gap-5" onSubmit={submitUpdate}>
            <DialogHeader>
              <DialogTitle>Изменить мероприятие</DialogTitle>
              <DialogDescription>
                Для сохранения галереи выберите файл для каждого изображения.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4">
              <TextField
                id="edit-event-name"
                label="Название"
                maxLength={32}
                minLength={2}
                onChange={setEventName}
                required
                value={eventName}
              />
              <TextField
                id="edit-event-description"
                label="Описание"
                maxLength={256}
                minLength={2}
                onChange={setDescription}
                required
                value={description}
              />
            </div>
            {eventToEdit && (
              <div className="grid gap-4">
                {eventToEdit.images
                  .slice()
                  .sort((first, second) => first.order - second.order)
                  .map((image) => (
                    <div
                      className="grid gap-3 rounded-lg border p-3 sm:grid-cols-[120px_1fr]"
                      key={image.uuid}
                    >
                      <img
                        alt=""
                        className="aspect-square w-full rounded-md object-cover"
                        src={image.url}
                      />
                      <div className="grid content-start gap-3">
                        <label className="grid gap-1 text-sm font-medium">
                          Новый файл для фото
                          <Input
                            accept="image/*"
                            onChange={(inputEvent) => {
                              const file = inputEvent.target.files?.[0]
                              if (file) {
                                setUpdateImages((current) => ({
                                  ...current,
                                  [image.uuid]: file,
                                }))
                              }
                            }}
                            required
                            type="file"
                          />
                        </label>
                        <label className="grid max-w-36 gap-1 text-sm font-medium">
                          Порядок (0–11)
                          <Input
                            max={11}
                            min={0}
                            onChange={(inputEvent) =>
                              setImageOrders((current) => ({
                                ...current,
                                [image.uuid]: Number(inputEvent.target.value),
                              }))
                            }
                            required
                            type="number"
                            value={imageOrders[image.uuid] ?? image.order}
                          />
                        </label>
                      </div>
                    </div>
                  ))}
              </div>
            )}
            {updateMutation.error instanceof Error && (
              <Alert variant="destructive">
                <AlertDescription>
                  {updateMutation.error.message}
                </AlertDescription>
              </Alert>
            )}
            <DialogFooter>
              <Button
                disabled={updateMutation.isPending}
                onClick={() => setEventToEdit(null)}
                type="button"
                variant="outline"
              >
                Отмена
              </Button>
              <Button
                disabled={
                  updateMutation.isPending ||
                  Object.keys(updateImages).length !==
                    (eventToEdit?.images.length ?? 0)
                }
                type="submit"
              >
                {updateMutation.isPending && (
                  <LoaderCircle className="animate-spin" aria-hidden="true" />
                )}
                Сохранить
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      <Dialog
        onOpenChange={(open) => {
          if (!deleteMutation.isPending && !open) setEventToDelete(null)
        }}
        open={Boolean(eventToDelete)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Удалить мероприятие?</DialogTitle>
            <DialogDescription>
              «{eventToDelete?.name}» и его галерея будут удалены. Это действие
              нельзя отменить.
            </DialogDescription>
          </DialogHeader>
          {deleteMutation.error instanceof Error && (
            <Alert variant="destructive">
              <AlertDescription>{deleteMutation.error.message}</AlertDescription>
            </Alert>
          )}
          <DialogFooter>
            <Button
              disabled={deleteMutation.isPending}
              onClick={() => setEventToDelete(null)}
              type="button"
              variant="outline"
            >
              Отмена
            </Button>
            <Button
              disabled={deleteMutation.isPending}
              onClick={() => {
                if (eventToDelete) deleteMutation.mutate(eventToDelete)
              }}
              type="button"
              variant="destructive"
            >
              {deleteMutation.isPending && (
                <LoaderCircle className="animate-spin" aria-hidden="true" />
              )}
              Удалить
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

interface EventFieldsProps {
  categories: Category[]
  categoryId: string
  description: string
  eventName: string
  images: File[]
  onCategoryChange: (value: string) => void
  onDescriptionChange: (value: string) => void
  onImagesChange: (files: File[]) => void
  onNameChange: (value: string) => void
}

function EventFields({
  categories,
  categoryId,
  description,
  eventName,
  images,
  onCategoryChange,
  onDescriptionChange,
  onImagesChange,
  onNameChange,
}: EventFieldsProps) {
  return (
    <div className="grid gap-4">
      <TextField
        id="create-event-name"
        label="Название"
        maxLength={32}
        minLength={2}
        onChange={onNameChange}
        required
        value={eventName}
      />
      <label className="grid gap-1 text-sm font-medium" htmlFor="create-event-description">
        Описание
        <textarea
          className="min-h-24 rounded-lg border border-input bg-transparent px-3 py-2 text-sm outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
          id="create-event-description"
          maxLength={256}
          minLength={2}
          onChange={(event) => onDescriptionChange(event.target.value)}
          required
          value={description}
        />
      </label>
      <label className="grid gap-1 text-sm font-medium" htmlFor="create-event-category">
        Категория
        <select
          className="h-10 rounded-lg border border-input bg-background px-3 text-sm"
          id="create-event-category"
          onChange={(event) => onCategoryChange(event.target.value)}
          required
          value={categoryId}
        >
          <option value="" disabled>
            Выберите категорию
          </option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </label>
      <label className="grid gap-1 text-sm font-medium" htmlFor="create-event-images">
        Фотографии (1–12)
        <Input
          accept="image/*"
          id="create-event-images"
          multiple
          onChange={(event) =>
            onImagesChange(Array.from(event.target.files ?? []))
          }
          required
          type="file"
        />
      </label>
      <p className="text-xs text-muted-foreground">
        Выбрано: {images.length}. Поддерживается до 12 файлов.
      </p>
    </div>
  )
}

interface TextFieldProps {
  id: string
  label: string
  maxLength: number
  minLength: number
  onChange: (value: string) => void
  required?: boolean
  value: string
}

function TextField({
  id,
  label,
  maxLength,
  minLength,
  onChange,
  required = false,
  value,
}: TextFieldProps) {
  return (
    <label className="grid gap-1 text-sm font-medium" htmlFor={id}>
      {label}
      <Input
        id={id}
        maxLength={maxLength}
        minLength={minLength}
        onChange={(event) => onChange(event.target.value)}
        required={required}
        value={value}
      />
    </label>
  )
}

export default EventAdmin
