<script setup lang="ts">
import { defineAsyncComponent, onMounted, ref } from 'vue'
import Message from 'primevue/message'
import AppHeader from './components/AppHeader.vue'
import { useAuth } from './composables/useAuth'

const CategoryAdmin = defineAsyncComponent(
  () => import('./components/CategoryAdmin.vue'),
)

const {
  isReady,
  isAuthenticated,
  userName,
  canManageCategories,
  errorMessage,
  initialize,
  signIn,
  signOut,
  authorizedFetch,
} = useAuth()
const isAdminView = ref(false)

onMounted(initialize)
</script>

<template>
  <div class="page-shell">
    <AppHeader
      :is-ready="isReady"
      :is-authenticated="isAuthenticated"
      :user-name="userName"
      :can-manage-categories="canManageCategories"
      :show-admin-view="isAdminView"
      @sign-in="signIn"
      @sign-out="signOut"
      @open-admin="isAdminView = true"
      @go-home="isAdminView = false"
    />

    <Message v-if="errorMessage" severity="error" :closable="false" role="alert">
      {{ errorMessage }}
    </Message>

    <main v-if="isAdminView && canManageCategories" class="page-content">
      <CategoryAdmin
        :authorized-fetch="authorizedFetch"
        @back="isAdminView = false"
      />
    </main>
  </div>
</template>
