import { useState } from 'react'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import {
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  CircleUserRound,
  Home,
  Layers3,
  LoaderCircle,
  LogOut,
  Menu,
  Pencil,
  Plus,
  Search,
  Shield,
  Trash2,
  X,
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

interface Category {
  id: string
  name: string
}

interface CategoryAdminProps {
  authorizedFetch: (path: string, init?: RequestInit) => Promise<Response>
  userName: string
  authErrorMessage: string
  onGoHome: () => void
  onOpenEvents: () => void
  onOpenProfile: () => void
  onSignOut: () => void
}

const categoryNameSchema = z.object({
  name: z
    .string()
    .trim()
    .min(2, 'Название должно содержать не менее 2 символов.')
    .max(32, 'Название должно содержать не более 32 символов.'),
})

type CategoryNameValues = z.infer<typeof categoryNameSchema>

const categoriesQueryKey = ['categories'] as const
const pageSize = 10
const categoryApiPageSize = 100

function categoryWord(count: number): string {
  const lastTwoDigits = count % 100
  if (lastTwoDigits >= 11 && lastTwoDigits <= 14) return 'категорий'
  const lastDigit = count % 10
  if (lastDigit === 1) return 'категория'
  if (lastDigit >= 2 && lastDigit <= 4) return 'категории'
  return 'категорий'
}

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

async function responseError(response: Response, action: string) {
  let message = `${action} (HTTP ${response.status}).`
  if (response.headers.get('content-type')?.includes('application/json')) {
    const payload: unknown = await response.json()
    if (isRecord(payload)) {
      const detail =
        typeof payload.detail === 'string'
          ? payload.detail
          : typeof payload.message === 'string'
            ? payload.message
            : undefined
      if (detail) message = detail
    }
  }
  return new Error(message)
}

async function readCategoryResponse(
  response: Response,
  action: string,
): Promise<Category> {
  if (!response.ok) throw await responseError(response, action)
  const payload: unknown = await response.json()
  if (!isCategory(payload)) {
    throw new Error('Сервер вернул категорию в неожиданном формате.')
  }
  return payload
}

function CategoryAdmin({
  authorizedFetch,
  userName,
  authErrorMessage,
  onGoHome,
  onOpenEvents,
  onOpenProfile,
  onSignOut,
}: CategoryAdminProps) {
  const queryClient = useQueryClient()
  const [searchTerm, setSearchTerm] = useState('')
  const [page, setPage] = useState(1)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [isCreateOpen, setIsCreateOpen] = useState(false)
  const [categoryToEdit, setCategoryToEdit] = useState<Category | null>(null)
  const [categoryToDelete, setCategoryToDelete] = useState<Category | null>(
    null,
  )
  const [successMessage, setSuccessMessage] = useState('')

  const createForm = useForm<CategoryNameValues>({
    resolver: zodResolver(categoryNameSchema),
    defaultValues: { name: '' },
    mode: 'onChange',
  })
  const editForm = useForm<CategoryNameValues>({
    resolver: zodResolver(categoryNameSchema),
    defaultValues: { name: '' },
    mode: 'onChange',
  })

  const categoriesQuery = useQuery({
    queryKey: categoriesQueryKey,
    queryFn: async (): Promise<Category[]> => {
      const categories: Category[] = []

      for (let offset = 0; ; offset += categoryApiPageSize) {
        const response = await authorizedFetch(
          `/api/v1/public/categories/?offset=${offset}&limit=${categoryApiPageSize}`,
        )
        if (!response.ok) {
          throw await responseError(
            response,
            'Не удалось загрузить категории',
          )
        }

        const payload: unknown = await response.json()
        if (
          !isRecord(payload) ||
          !Array.isArray(payload.result) ||
          !payload.result.every(isCategory)
        ) {
          throw new Error(
            'Сервер вернул список категорий в неожиданном формате.',
          )
        }

        const page = payload.result
        categories.push(...page)
        if (page.length < categoryApiPageSize) return categories
      }
    },
  })

  const createMutation = useMutation({
    mutationFn: async (values: CategoryNameValues) => {
      const response = await authorizedFetch('/api/v1/admin/categories/', {
        method: 'POST',
        body: JSON.stringify(values),
      })
      return readCategoryResponse(response, 'Не удалось создать категорию')
    },
    onSuccess: async (category) => {
      createForm.reset()
      setIsCreateOpen(false)
      setSuccessMessage(`Категория «${category.name}» добавлена.`)
      await queryClient.invalidateQueries({ queryKey: categoriesQueryKey })
    },
  })

  const updateMutation = useMutation({
    mutationFn: async ({
      category,
      values,
    }: {
      category: Category
      values: CategoryNameValues
    }) => {
      const response = await authorizedFetch(
        `/api/v1/admin/categories/${encodeURIComponent(category.id)}`,
        {
          method: 'PATCH',
          body: JSON.stringify(values),
        },
      )
      return readCategoryResponse(response, 'Не удалось изменить категорию')
    },
    onSuccess: async (category) => {
      setCategoryToEdit(null)
      setSuccessMessage(`Категория «${category.name}» обновлена.`)
      await queryClient.invalidateQueries({ queryKey: categoriesQueryKey })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (category: Category) => {
      const response = await authorizedFetch(
        `/api/v1/admin/categories/${encodeURIComponent(category.id)}`,
        { method: 'DELETE' },
      )
      if (!response.ok) {
        throw await responseError(response, 'Не удалось удалить категорию')
      }
      return category
    },
    onSuccess: async (category) => {
      setCategoryToDelete(null)
      setSuccessMessage(`Категория «${category.name}» удалена.`)
      await queryClient.invalidateQueries({ queryKey: categoriesQueryKey })
    },
  })

  const categories = categoriesQuery.data ?? []
  const filteredCategories = categories.filter((category) =>
    category.name.toLocaleLowerCase().includes(searchTerm.trim().toLocaleLowerCase()),
  )
  const pageCount = Math.max(1, Math.ceil(filteredCategories.length / pageSize))
  const currentPage = Math.min(page, pageCount)
  const visibleCategories = filteredCategories.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize,
  )
  const errorMessage =
    authErrorMessage ||
    (categoriesQuery.error instanceof Error
      ? categoriesQuery.error.message
      : '') ||
    (createMutation.error instanceof Error ? createMutation.error.message : '') ||
    (updateMutation.error instanceof Error ? updateMutation.error.message : '') ||
    (deleteMutation.error instanceof Error ? deleteMutation.error.message : '')

  function openCreateDialog() {
    createForm.reset({ name: '' })
    createMutation.reset()
    setSuccessMessage('')
    setIsCreateOpen(true)
  }

  function openEditDialog(category: Category) {
    editForm.reset({ name: category.name })
    updateMutation.reset()
    setSuccessMessage('')
    setCategoryToEdit(category)
  }

  function closeCreateDialog(open: boolean) {
    if (createMutation.isPending) return
    setIsCreateOpen(open)
    if (!open) createForm.reset()
  }

  function closeEditDialog(open: boolean) {
    if (updateMutation.isPending) return
    if (!open) {
      setCategoryToEdit(null)
      editForm.reset()
    }
  }

  const initials = userName
    .split(/[\s@._-]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toLocaleUpperCase('ru-RU'))
    .join('')

  return (
    <div className="flex min-h-screen bg-muted/30">
      {isSidebarOpen && (
        <button
          aria-label="Закрыть меню"
          className="fixed inset-0 z-30 bg-black/30 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
          type="button"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r bg-card transition-transform duration-200 md:static md:translate-x-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-16 items-center gap-3 border-b px-5">
          <span className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <CalendarDays className="size-5" aria-hidden="true" />
          </span>
          <div>
            <p className="font-semibold leading-tight">События</p>
            <p className="text-xs text-muted-foreground">Панель управления</p>
          </div>
        </div>

        <nav aria-label="Главная навигация" className="flex-1 space-y-6 p-3">
          <div className="space-y-1">
            <p className="px-3 pb-1 text-xs font-medium text-muted-foreground">
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
          </div>
          <div className="space-y-1">
            <p className="px-3 pb-1 text-xs font-medium text-muted-foreground">
              УПРАВЛЕНИЕ
            </p>
            <button
              className="flex h-9 w-full items-center gap-3 rounded-lg px-3 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              onClick={onOpenEvents}
              type="button"
            >
              <CalendarDays className="size-4" aria-hidden="true" />
              Мероприятия
            </button>
            <div
              aria-current="page"
              className="flex h-9 items-center gap-3 rounded-lg bg-primary/10 px-3 text-sm font-medium text-primary"
            >
              <Layers3 className="size-4" aria-hidden="true" />
              Категории
            </div>
          </div>
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
            <CircleUserRound
              className="size-4 text-muted-foreground"
              aria-hidden="true"
            />
          </button>
        </div>
      </aside>

      <div className="flex min-h-screen min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b bg-card/95 px-4 backdrop-blur sm:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <Button
              aria-label={isSidebarOpen ? 'Закрыть меню' : 'Открыть меню'}
              className="md:hidden"
              onClick={() => setIsSidebarOpen((open) => !open)}
              size="icon"
              variant="ghost"
            >
              {isSidebarOpen ? (
                <X aria-hidden="true" />
              ) : (
                <Menu aria-hidden="true" />
              )}
            </Button>
            <div className="hidden h-5 border-l sm:block" />
            <span className="truncate text-sm text-muted-foreground">
              Панель управления <span className="px-1">/</span>
              <span className="font-medium text-foreground">Категории</span>
            </span>
          </div>

          <div className="flex items-center gap-2">
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
                Категории
              </h1>
              <p className="text-sm text-muted-foreground">
                Создавайте и редактируйте категории мероприятий.
              </p>
            </div>
            <Button className="gap-2" onClick={openCreateDialog}>
              <Plus aria-hidden="true" />
              Добавить категорию
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
                <CardTitle className="text-base">Все категории</CardTitle>
                <CardDescription>
                  Всего {categories.length} {categoryWord(categories.length)}
                </CardDescription>
              </div>
              <div className="relative w-full max-w-xs">
                <Search
                  className="absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground"
                  aria-hidden="true"
                />
                <Input
                  aria-label="Поиск категорий"
                  className="h-9 pl-9"
                  onChange={(event) => {
                    setSearchTerm(event.target.value)
                    setPage(1)
                  }}
                  placeholder="Поиск категорий…"
                  value={searchTerm}
                />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50 hover:bg-muted/50">
                    <TableHead className="pl-6">Название</TableHead>
                    <TableHead className="w-36 pr-6 text-right">
                      Действия
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {categoriesQuery.isPending && (
                    <TableRow>
                      <TableCell className="h-32 text-center" colSpan={2}>
                        <span className="inline-flex items-center gap-2 text-sm text-muted-foreground">
                          <LoaderCircle
                            className="size-4 animate-spin"
                            aria-hidden="true"
                          />
                          Загружаем категории…
                        </span>
                      </TableCell>
                    </TableRow>
                  )}
                  {categoriesQuery.isSuccess &&
                    visibleCategories.map((category) => (
                      <TableRow key={category.id}>
                        <TableCell className="pl-6">
                          <span className="flex items-center gap-3">
                            <span className="flex size-8 items-center justify-center rounded-lg bg-primary/10 text-primary">
                              <Layers3
                                className="size-4"
                                aria-hidden="true"
                              />
                            </span>
                            <span className="font-medium">{category.name}</span>
                          </span>
                        </TableCell>
                        <TableCell className="pr-6">
                          <div className="flex justify-end gap-1">
                            <Button
                              aria-label={`Изменить категорию ${category.name}`}
                              onClick={() => openEditDialog(category)}
                              size="icon-sm"
                              variant="ghost"
                            >
                              <Pencil aria-hidden="true" />
                            </Button>
                            <Button
                              aria-label={`Удалить категорию ${category.name}`}
                              onClick={() => {
                                deleteMutation.reset()
                                setCategoryToDelete(category)
                                setSuccessMessage('')
                              }}
                              size="icon-sm"
                              variant="ghost"
                            >
                              <Trash2
                                className="text-destructive"
                                aria-hidden="true"
                              />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  {categoriesQuery.isSuccess &&
                    visibleCategories.length === 0 && (
                      <TableRow>
                        <TableCell className="h-36 text-center" colSpan={2}>
                          <div className="space-y-1">
                            <p className="font-medium">
                              {searchTerm
                                ? 'Ничего не найдено'
                                : 'Категорий пока нет'}
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {searchTerm
                                ? 'Попробуйте изменить поисковый запрос.'
                                : 'Добавьте первую категорию, чтобы начать.'}
                            </p>
                          </div>
                        </TableCell>
                      </TableRow>
                    )}
                </TableBody>
              </Table>

              <div className="flex flex-wrap items-center justify-between gap-3 border-t px-4 py-3 sm:px-6">
                <p className="text-sm text-muted-foreground">
                  {filteredCategories.length === 0
                    ? 'Нет категорий для отображения'
                    : `${(currentPage - 1) * pageSize + 1}–${Math.min(
                        currentPage * pageSize,
                        filteredCategories.length,
                      )} из ${filteredCategories.length}`}
                </p>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">
                    Страница {currentPage} из {pageCount}
                  </span>
                  <Button
                    aria-label="Предыдущая страница"
                    disabled={currentPage <= 1}
                    onClick={() => setPage((value) => Math.max(1, value - 1))}
                    size="icon-sm"
                    variant="outline"
                  >
                    <ChevronLeft aria-hidden="true" />
                  </Button>
                  <Button
                    aria-label="Следующая страница"
                    disabled={currentPage >= pageCount}
                    onClick={() =>
                      setPage((value) => Math.min(pageCount, value + 1))
                    }
                    size="icon-sm"
                    variant="outline"
                  >
                    <ChevronRight aria-hidden="true" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <p className="flex items-center gap-2 text-xs text-muted-foreground">
            <Shield className="size-3.5" aria-hidden="true" />
            Управление доступно пользователям с ролью администратора или
            продавца.
          </p>
        </main>
      </div>

      <CategoryFormDialog
        description="Категория станет доступна при создании мероприятий."
        error={
          createMutation.error instanceof Error
            ? createMutation.error.message
            : ''
        }
        isOpen={isCreateOpen}
        isPending={createMutation.isPending}
        onOpenChange={closeCreateDialog}
        onSubmit={createForm.handleSubmit((values) => {
          createMutation.reset()
          setSuccessMessage('')
          createMutation.mutate(values)
        })}
        register={createForm.register}
        errors={createForm.formState.errors}
        title="Новая категория"
        submitLabel="Создать категорию"
        isValid={createForm.formState.isValid}
      />

      <CategoryFormDialog
        description="Измените название категории."
        error={
          updateMutation.error instanceof Error
            ? updateMutation.error.message
            : ''
        }
        isOpen={Boolean(categoryToEdit)}
        isPending={updateMutation.isPending}
        onOpenChange={closeEditDialog}
        onSubmit={editForm.handleSubmit((values) => {
          if (!categoryToEdit) return
          updateMutation.reset()
          setSuccessMessage('')
          updateMutation.mutate({ category: categoryToEdit, values })
        })}
        register={editForm.register}
        errors={editForm.formState.errors}
        title="Изменить категорию"
        submitLabel="Сохранить изменения"
        isValid={editForm.formState.isValid}
      />

      <Dialog
        onOpenChange={(open) => {
          if (!deleteMutation.isPending && !open) setCategoryToDelete(null)
        }}
        open={Boolean(categoryToDelete)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Удалить категорию?</DialogTitle>
            <DialogDescription>
              Категория «{categoryToDelete?.name}» будет удалена. Это действие
              нельзя отменить.
            </DialogDescription>
          </DialogHeader>
          {deleteMutation.error instanceof Error && (
            <Alert variant="destructive">
              <AlertDescription>
                {deleteMutation.error.message}
              </AlertDescription>
            </Alert>
          )}
          <DialogFooter>
            <Button
              disabled={deleteMutation.isPending}
              onClick={() => setCategoryToDelete(null)}
              type="button"
              variant="outline"
            >
              Отмена
            </Button>
            <Button
              disabled={deleteMutation.isPending}
              onClick={() => {
                if (categoryToDelete) deleteMutation.mutate(categoryToDelete)
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

interface CategoryFormDialogProps {
  description: string
  error: string
  isOpen: boolean
  isPending: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: React.FormEventHandler<HTMLFormElement>
  register: ReturnType<typeof useForm<CategoryNameValues>>['register']
  errors: ReturnType<typeof useForm<CategoryNameValues>>['formState']['errors']
  title: string
  submitLabel: string
  isValid: boolean
}

function CategoryFormDialog({
  description,
  error,
  isOpen,
  isPending,
  onOpenChange,
  onSubmit,
  register,
  errors,
  title,
  submitLabel,
  isValid,
}: CategoryFormDialogProps) {
  return (
    <Dialog onOpenChange={onOpenChange} open={isOpen}>
      <DialogContent>
        <form className="grid gap-5" onSubmit={onSubmit} noValidate>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            <DialogDescription>{description}</DialogDescription>
          </DialogHeader>
          <div className="grid gap-2">
            <label className="text-sm font-medium" htmlFor={`${title}-name`}>
              Название
            </label>
            <Input
              aria-invalid={Boolean(errors.name)}
              autoFocus
              id={`${title}-name`}
              maxLength={32}
              placeholder="Например, Концерт"
              {...register('name')}
            />
            {errors.name?.message && (
              <p className="text-sm text-destructive">{errors.name.message}</p>
            )}
          </div>
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <DialogFooter>
            <Button
              disabled={isPending}
              onClick={() => onOpenChange(false)}
              type="button"
              variant="outline"
            >
              Отмена
            </Button>
            <Button disabled={isPending || !isValid} type="submit">
              {isPending && (
                <LoaderCircle className="animate-spin" aria-hidden="true" />
              )}
              {submitLabel}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default CategoryAdmin
