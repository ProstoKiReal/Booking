<script setup lang="ts">
import Button from 'primevue/button'
import Toolbar from 'primevue/toolbar'

defineProps<{
  isReady: boolean
  isAuthenticated: boolean
  userName: string
  canManageCategories: boolean
  showAdminView: boolean
}>()

const emit = defineEmits<{
  signIn: []
  signOut: []
  openAdmin: []
  goHome: []
}>()

function toggleAdminView(showAdminView: boolean) {
  if (showAdminView) {
    emit('goHome')
  } else {
    emit('openAdmin')
  }
}
</script>

<template>
  <Toolbar>
    <template #start>
      <Button label="События" text @click="$emit('goHome')" />
    </template>
    <template #end>
      <div class="account">
        <template v-if="isAuthenticated">
          <span>{{ userName }}</span>
          <Button
            v-if="canManageCategories"
            :label="showAdminView ? 'На главную' : 'Админка'"
            severity="secondary"
            outlined
            @click="toggleAdminView(showAdminView)"
          />
          <Button label="Выйти" severity="secondary" outlined @click="$emit('signOut')" />
        </template>
        <Button
          v-else
          :label="isReady ? 'Войти' : 'Подключаем вход…'"
          :disabled="!isReady"
          @click="$emit('signIn')"
        />
      </div>
    </template>
  </Toolbar>
</template>
