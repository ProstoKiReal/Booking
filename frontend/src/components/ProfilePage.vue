<script setup lang="ts">
import { computed } from 'vue'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Card from 'primevue/card'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import type { UserProfile } from '../composables/useAuth'

const props = defineProps<{
  profile: UserProfile | null
  openPersonalInfo: () => void
  openPasswordSettings: () => void
}>()

const displayName = computed(
  () => props.profile?.name || props.profile?.username || 'Профиль пользователя',
)

const initials = computed(() => {
  const source = props.profile?.name || props.profile?.username || '?'
  return source
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toLocaleUpperCase('ru-RU'))
    .join('')
})

</script>

<template>
  <section aria-labelledby="profile-title" class="profile-page">
    <div class="page-heading">
      <h1 id="profile-title">Мой профиль</h1>
      <p>Личная информация и настройки учётной записи.</p>
    </div>

    <Message v-if="!profile" severity="warn" :closable="false">
      Не удалось получить данные профиля. Попробуйте обновить страницу или войти снова.
    </Message>

    <template v-else>
      <Card class="profile-summary">
        <template #content>
          <div class="profile-identity">
            <Avatar :label="initials" shape="circle" size="xlarge" />
            <div class="profile-identity-text">
              <h2>{{ displayName }}</h2>
              <p>@{{ profile.username || 'пользователь' }}</p>
            </div>
          </div>
        </template>
      </Card>

      <div class="profile-grid">
        <Card>
          <template #title>Личные данные</template>
          <template #subtitle>
            Личные данные вашей учётной записи.
          </template>
          <template #content>
            <div class="profile-form">
              <FloatLabel variant="on">
                <InputText id="profile-username" :model-value="profile.username" readonly fluid />
                <label for="profile-username">Логин</label>
              </FloatLabel>
              <FloatLabel variant="on">
                <InputText id="profile-first-name" :model-value="profile.firstName" readonly fluid />
                <label for="profile-first-name">Имя</label>
              </FloatLabel>
              <FloatLabel variant="on">
                <InputText id="profile-last-name" :model-value="profile.lastName" readonly fluid />
                <label for="profile-last-name">Фамилия</label>
              </FloatLabel>
              <FloatLabel variant="on">
                <InputText
                  id="profile-email"
                  :model-value="profile.email"
                  type="email"
                  readonly
                  fluid
                />
                <label for="profile-email">Электронная почта</label>
              </FloatLabel>
            </div>

            <div class="profile-actions">
              <Button
                type="button"
                label="Изменить личные данные"
                icon="pi pi-user-edit"
                icon-pos="right"
                @click="openPersonalInfo"
              />
              <Button
                type="button"
                label="Изменить пароль"
                severity="secondary"
                outlined
                icon="pi pi-lock"
                icon-pos="right"
                @click="openPasswordSettings"
              />
            </div>
          </template>
        </Card>
      </div>
    </template>
  </section>
</template>
