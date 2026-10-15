import { useEffect, useState, type ReactNode } from 'react'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useForm, type UseFormRegisterReturn } from 'react-hook-form'
import { z } from 'zod'
import { KeyRound, LoaderCircle, Mail, UserRound } from 'lucide-react'
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
import { Input } from '@/components/ui/input'
import type { UserProfile } from '../composables/useAuth'

interface ProfilePageProps {
  profile: UserProfile | null
  keycloakApiFetch: (path: string, init?: RequestInit) => Promise<Response>
}

interface AccountProfile extends UserProfile {
  id?: string
}

const accountProfileQueryKey = ['account-profile'] as const

const profileFormSchema = z.object({
  firstName: z.string().trim().min(1, 'Укажите имя.').max(128),
  lastName: z.string().trim().min(1, 'Укажите фамилию.').max(128),
  email: z.string().trim().email('Введите корректный адрес электронной почты.'),
})

const passwordFormSchema = z
  .object({
    currentPassword: z.string().min(1, 'Введите текущий пароль.').max(256),
    newPassword: z.string().min(1, 'Введите новый пароль.').max(256),
    confirmPassword: z.string().min(1, 'Подтвердите новый пароль.').max(256),
  })
  .refine((values) => values.newPassword === values.confirmPassword, {
    message: 'Пароли не совпадают.',
    path: ['confirmPassword'],
  })
  .refine((values) => values.currentPassword !== values.newPassword, {
    message: 'Новый пароль должен отличаться от текущего.',
    path: ['newPassword'],
  })

type ProfileFormValues = z.infer<typeof profileFormSchema>
type PasswordFormValues = z.infer<typeof passwordFormSchema>

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function accountProfileFrom(
  value: unknown,
  fallback: UserProfile | null,
): AccountProfile {
  if (!isRecord(value)) {
    throw new Error('Keycloak вернул профиль в неожиданном формате.')
  }

  const username =
    typeof value.username === 'string' ? value.username : fallback?.username ?? ''
  const firstName =
    typeof value.firstName === 'string'
      ? value.firstName
      : fallback?.firstName ?? ''
  const lastName =
    typeof value.lastName === 'string'
      ? value.lastName
      : fallback?.lastName ?? ''
  const email =
    typeof value.email === 'string' ? value.email : fallback?.email ?? ''

  return {
    id: typeof value.id === 'string' ? value.id : undefined,
    username,
    firstName,
    lastName,
    email,
    name:
      [firstName, lastName].filter(Boolean).join(' ') ||
      fallback?.name ||
      username,
    roles: fallback?.roles ?? [],
  }
}

async function throwForResponse(response: Response, action: string) {
  if (!response.ok) {
    let message = `${action} (HTTP ${response.status}).`
    if (response.headers.get('content-type')?.includes('application/json')) {
      const body: unknown = await response.json()
      if (isRecord(body) && typeof body.message === 'string') {
        message = body.message
      }
    }
    throw new Error(message)
  }
}

function ProfilePage({ profile: tokenProfile, keycloakApiFetch }: ProfilePageProps) {
  const queryClient = useQueryClient()
  const [isEditingProfile, setIsEditingProfile] = useState(false)
  const [isChangingPassword, setIsChangingPassword] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  const profileQuery = useQuery({
    queryKey: accountProfileQueryKey,
    queryFn: async () => {
      const response = await keycloakApiFetch('/account')
      await throwForResponse(response, 'Не удалось загрузить профиль')
      return accountProfileFrom(await response.json(), tokenProfile)
    },
    initialData: tokenProfile
      ? accountProfileFrom(tokenProfile, tokenProfile)
      : undefined,
    staleTime: 0,
  })

  const profile = profileQuery.data

  const profileForm = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      firstName: profile?.firstName ?? '',
      lastName: profile?.lastName ?? '',
      email: profile?.email ?? '',
    },
    mode: 'onChange',
  })

  const passwordForm = useForm<PasswordFormValues>({
    resolver: zodResolver(passwordFormSchema),
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    },
    mode: 'onChange',
  })

  useEffect(() => {
    if (!profile) return
    profileForm.reset({
      firstName: profile.firstName,
      lastName: profile.lastName,
      email: profile.email,
    })
  }, [profile?.firstName, profile?.lastName, profile?.email])

  const updateProfileMutation = useMutation({
    mutationFn: async (values: ProfileFormValues) => {
      const response = await keycloakApiFetch('/account', {
        method: 'POST',
        body: JSON.stringify(values),
      })
      await throwForResponse(response, 'Не удалось сохранить личные данные')
      return values
    },
    onSuccess: async (values) => {
      queryClient.setQueryData<AccountProfile>(
        accountProfileQueryKey,
        (current) => ({
          ...(current ?? accountProfileFrom(tokenProfile, tokenProfile)),
          ...values,
          name: [values.firstName, values.lastName].filter(Boolean).join(' '),
        }),
      )
      setIsEditingProfile(false)
      setSuccessMessage('Личные данные обновлены.')
      await queryClient.invalidateQueries({
        queryKey: accountProfileQueryKey,
      })
    },
  })

  const changePasswordMutation = useMutation({
    mutationFn: async (values: PasswordFormValues) => {
      const response = await keycloakApiFetch('/self-service/password', {
        method: 'POST',
        body: JSON.stringify({
          currentPassword: values.currentPassword,
          newPassword: values.newPassword,
        }),
      })
      await throwForResponse(response, 'Не удалось изменить пароль')
    },
    onSuccess: () => {
      passwordForm.reset()
      setIsChangingPassword(false)
      setSuccessMessage('Пароль изменён.')
    },
  })

  const displayName =
    profile?.name || profile?.username || 'Профиль пользователя'
  const initials = (profile?.name || profile?.username || '?')
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toLocaleUpperCase('ru-RU'))
    .join('')

  const errorMessage =
    (profileQuery.error instanceof Error && profileQuery.error.message) ||
    (updateProfileMutation.error instanceof Error &&
      updateProfileMutation.error.message) ||
    (changePasswordMutation.error instanceof Error &&
      changePasswordMutation.error.message)

  return (
    <section aria-labelledby="profile-title" className="space-y-6">
      <header className="space-y-2">
        <h1 id="profile-title" className="text-3xl font-semibold tracking-tight">
          Мой профиль
        </h1>
        <p className="text-muted-foreground">
          Личная информация и настройки учётной записи.
        </p>
      </header>

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

      {!profile ? (
        <Alert className="border-amber-300 bg-amber-50 text-amber-950">
          <AlertDescription>
            Не удалось получить данные профиля. Попробуйте обновить страницу или
            войти снова.
          </AlertDescription>
        </Alert>
      ) : (
        <>
          <Card className="border-border/70 shadow-sm">
            <CardContent className="flex flex-wrap items-center gap-4 p-6">
              <Avatar className="size-14" size="lg">
                <AvatarFallback className="bg-primary/10 text-lg font-semibold text-primary">
                  {initials}
                </AvatarFallback>
              </Avatar>
              <div className="min-w-0 flex-1">
                <h2 className="text-xl font-semibold">{displayName}</h2>
                <p className="mt-1 text-sm text-muted-foreground">
                  @{profile.username || 'пользователь'}
                </p>
              </div>
            </CardContent>
          </Card>

          <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,3fr)_minmax(16rem,2fr)]">
            <Card className="border-border/70 shadow-sm">
              <CardHeader>
                <CardTitle>Личные данные</CardTitle>
                <CardDescription>
                  Данные сохраняются в вашей учётной записи.
                </CardDescription>
              </CardHeader>
              <CardContent>
                {isEditingProfile ? (
                  <form
                    className="grid gap-5"
                    onSubmit={profileForm.handleSubmit((values) => {
                      setSuccessMessage('')
                      updateProfileMutation.reset()
                      updateProfileMutation.mutate(values)
                    })}
                    noValidate
                  >
                    <ProfileInput
                      error={profileForm.formState.errors.firstName?.message}
                      label="Имя"
                      registration={profileForm.register('firstName')}
                    />
                    <ProfileInput
                      error={profileForm.formState.errors.lastName?.message}
                      label="Фамилия"
                      registration={profileForm.register('lastName')}
                    />
                    <ProfileInput
                      error={profileForm.formState.errors.email?.message}
                      label="Электронная почта"
                      registration={profileForm.register('email')}
                      type="email"
                    />
                    <div className="flex flex-wrap gap-3">
                      <Button
                        disabled={
                          updateProfileMutation.isPending ||
                          !profileForm.formState.isValid
                        }
                        type="submit"
                      >
                        {updateProfileMutation.isPending && (
                          <LoaderCircle
                            className="animate-spin"
                            aria-hidden="true"
                          />
                        )}
                        Сохранить изменения
                      </Button>
                      <Button
                        disabled={updateProfileMutation.isPending}
                        onClick={() => {
                          profileForm.reset()
                          updateProfileMutation.reset()
                          setIsEditingProfile(false)
                        }}
                        type="button"
                        variant="outline"
                      >
                        Отмена
                      </Button>
                    </div>
                  </form>
                ) : (
                  <>
                    <dl className="grid gap-x-6 gap-y-5 sm:grid-cols-2">
                      <ProfileField
                        icon={<UserRound aria-hidden="true" />}
                        label="Логин"
                        value={profile.username}
                      />
                      <ProfileField label="Имя" value={profile.firstName} />
                      <ProfileField label="Фамилия" value={profile.lastName} />
                      <ProfileField
                        icon={<Mail aria-hidden="true" />}
                        label="Электронная почта"
                        value={profile.email}
                      />
                    </dl>
                    <div className="mt-7">
                      <Button
                        onClick={() => {
                          setSuccessMessage('')
                          profileForm.reset({
                            firstName: profile.firstName,
                            lastName: profile.lastName,
                            email: profile.email,
                          })
                          setIsEditingProfile(true)
                        }}
                      >
                        Изменить личные данные
                      </Button>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>

            <Card className="border-border/70 shadow-sm">
              <CardHeader>
                <CardTitle>Безопасность</CardTitle>
                <CardDescription>
                  Пароль хранится и проверяется Keycloak.
                </CardDescription>
              </CardHeader>
              <CardContent>
                {isChangingPassword ? (
                  <form
                    className="grid gap-4"
                    onSubmit={passwordForm.handleSubmit((values) => {
                      setSuccessMessage('')
                      changePasswordMutation.reset()
                      changePasswordMutation.mutate(values)
                    })}
                    noValidate
                  >
                    <ProfileInput
                      autoComplete="current-password"
                      error={
                        passwordForm.formState.errors.currentPassword?.message
                      }
                      label="Текущий пароль"
                      registration={passwordForm.register('currentPassword')}
                      type="password"
                    />
                    <ProfileInput
                      autoComplete="new-password"
                      error={passwordForm.formState.errors.newPassword?.message}
                      label="Новый пароль"
                      registration={passwordForm.register('newPassword')}
                      type="password"
                    />
                    <ProfileInput
                      autoComplete="new-password"
                      error={
                        passwordForm.formState.errors.confirmPassword?.message
                      }
                      label="Повторите новый пароль"
                      registration={passwordForm.register('confirmPassword')}
                      type="password"
                    />
                    <div className="flex flex-wrap gap-3">
                      <Button
                        disabled={
                          changePasswordMutation.isPending ||
                          !passwordForm.formState.isValid
                        }
                        type="submit"
                      >
                        {changePasswordMutation.isPending && (
                          <LoaderCircle
                            className="animate-spin"
                            aria-hidden="true"
                          />
                        )}
                        Изменить пароль
                      </Button>
                      <Button
                        disabled={changePasswordMutation.isPending}
                        onClick={() => {
                          passwordForm.reset()
                          changePasswordMutation.reset()
                          setIsChangingPassword(false)
                        }}
                        type="button"
                        variant="outline"
                      >
                        Отмена
                      </Button>
                    </div>
                  </form>
                ) : (
                  <Button
                    onClick={() => {
                      setSuccessMessage('')
                      passwordForm.reset()
                      changePasswordMutation.reset()
                      setIsChangingPassword(true)
                    }}
                    variant="outline"
                  >
                    <KeyRound data-icon="inline-start" aria-hidden="true" />
                    Изменить пароль
                  </Button>
                )}
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </section>
  )
}

function ProfileField({
  icon,
  label,
  value,
}: {
  icon?: ReactNode
  label: string
  value: string
}) {
  return (
    <div className="grid min-w-0 gap-1.5">
      <dt className="flex items-center gap-2 text-sm text-muted-foreground">
        {icon && <span className="[&_svg]:size-4">{icon}</span>}
        {label}
      </dt>
      <dd className="m-0 min-h-5 break-words font-medium">{value || '—'}</dd>
    </div>
  )
}

function ProfileInput({
  autoComplete,
  error,
  label,
  registration,
  type = 'text',
}: {
  autoComplete?: string
  error?: string
  label: string
  registration: UseFormRegisterReturn
  type?: string
}) {
  const id = `profile-${label.toLocaleLowerCase('ru').replaceAll(' ', '-')}`

  return (
    <div className="grid gap-2">
      <label className="text-sm font-medium" htmlFor={id}>
        {label}
      </label>
      <Input
        autoComplete={autoComplete}
        id={id}
        aria-invalid={Boolean(error)}
        type={type}
        {...registration}
      />
      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}

export default ProfilePage
