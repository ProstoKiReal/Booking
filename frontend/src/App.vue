<script setup lang="ts">
import { defineAsyncComponent, onMounted, ref } from 'vue'
import Message from 'primevue/message'
import AppHeader from './components/AppHeader.vue'
import { useAuth } from './composables/useAuth'

const CategoryAdmin = defineAsyncComponent(
  () => import('./components/CategoryAdmin.vue'),
)
const ProfilePage = defineAsyncComponent(
  () => import('./components/ProfilePage.vue'),
)

const {
  isReady,
  isAuthenticated,
  userName,
  profile,
  openPersonalInfo,
  openPasswordSettings,
  canManageCategories,
  errorMessage,
  initialize,
  signIn,
  signOut,
  authorizedFetch,
} = useAuth()
const currentView = ref<'home' | 'profile' | 'admin'>('home')

onMounted(initialize)
</script>

<template>
  <div class="page-shell">
    <AppHeader
      :is-ready="isReady"
      :is-authenticated="isAuthenticated"
      :user-name="userName"
      :can-manage-categories="canManageCategories"
      :show-admin-view="currentView === 'admin'"
      :show-profile="currentView === 'profile'"
      @sign-in="signIn"
      @sign-out="signOut"
      @open-admin="currentView = 'admin'"
      @open-profile="currentView = 'profile'"
      @go-home="currentView = 'home'"
    />

    <Message v-if="errorMessage" severity="error" :closable="false" role="alert">
      {{ errorMessage }}
    </Message>

    <main v-if="currentView === 'admin' && canManageCategories" class="page-content">
      <CategoryAdmin
        :authorized-fetch="authorizedFetch"
        @back="currentView = 'home'"
      />
    </main>
    <main v-else-if="currentView === 'profile' && isAuthenticated" class="page-content">
      <ProfilePage
        :profile="profile"
        :open-personal-info="openPersonalInfo"
        :open-password-settings="openPasswordSettings"
      />
    </main>
  </div>
</template>
