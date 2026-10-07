<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'

interface Category {
  id: string
  name: string
}

const props = defineProps<{
  authorizedFetch: (path: string, init?: RequestInit) => Promise<Response>
}>()

const emit = defineEmits<{
  back: []
}>()

const categories = ref<Category[]>([])
const categoryName = ref('')
const categoryToEdit = ref<Category | null>(null)
const editedName = ref('')
const categoryToDelete = ref<Category | null>(null)
const isEditDialogVisible = ref(false)
const isDeleteDialogVisible = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const isSubmitting = ref(false)
const isUpdating = ref(false)
const isDeleting = ref(false)
const isMutating = computed(
  () => isSubmitting.value || isUpdating.value || isDeleting.value,
)
const dialogStyle = { width: 'min(28rem, calc(100vw - 2rem))' }

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

function reportError(error: unknown, fallback: string) {
  errorMessage.value = error instanceof Error ? error.message : fallback
}

async function loadCategories() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await props.authorizedFetch('/api/v1/public/categories/')
    if (!response.ok) {
      throw new Error(`Не удалось загрузить категории (HTTP ${response.status}).`)
    }

    const payload: unknown = await response.json()
    if (
      !isRecord(payload) ||
      !Array.isArray(payload.result) ||
      !payload.result.every(isCategory)
    ) {
      throw new Error('Сервер вернул список категорий в неожиданном формате.')
    }

    categories.value = payload.result
  } catch (error) {
    reportError(error, 'Не удалось загрузить категории.')
  } finally {
    isLoading.value = false
  }
}

async function createCategory() {
  const name = categoryName.value.trim()
  if (name.length < 2 || name.length > 32) {
    errorMessage.value = 'Название должно содержать от 2 до 32 символов.'
    return
  }

  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  try {
    const response = await props.authorizedFetch('/api/v1/admin/categories/', {
      method: 'POST',
      body: JSON.stringify({ name }),
    })

    if (!response.ok) {
      throw new Error(`Не удалось создать категорию (HTTP ${response.status}).`)
    }

    const payload: unknown = await response.json()
    if (!isCategory(payload)) {
      throw new Error('Сервер вернул созданную категорию в неожиданном формате.')
    }

    categories.value = [
      payload,
      ...categories.value.filter((category) => category.id !== payload.id),
    ]
    categoryName.value = ''
    successMessage.value = `Категория «${payload.name}» добавлена.`
  } catch (error) {
    reportError(error, 'Не удалось создать категорию.')
  } finally {
    isSubmitting.value = false
  }
}

function openEditDialog(category: Category) {
  categoryToEdit.value = category
  editedName.value = category.name
  errorMessage.value = ''
  isEditDialogVisible.value = true
}

async function updateCategory() {
  const category = categoryToEdit.value
  const name = editedName.value.trim()
  if (!category) {
    return
  }
  if (name.length < 2 || name.length > 32) {
    errorMessage.value = 'Название должно содержать от 2 до 32 символов.'
    return
  }

  errorMessage.value = ''
  successMessage.value = ''
  isUpdating.value = true

  try {
    const response = await props.authorizedFetch(
      `/api/v1/admin/categories/${encodeURIComponent(category.id)}`,
      {
        method: 'PATCH',
        body: JSON.stringify({ name }),
      },
    )
    if (!response.ok) {
      throw new Error(`Не удалось изменить категорию (HTTP ${response.status}).`)
    }

    const payload: unknown = await response.json()
    if (!isCategory(payload)) {
      throw new Error('Сервер вернул обновлённую категорию в неожиданном формате.')
    }

    categories.value = categories.value.map((item) =>
      item.id === payload.id ? payload : item,
    )
    isEditDialogVisible.value = false
    successMessage.value = `Категория «${payload.name}» обновлена.`
  } catch (error) {
    reportError(error, 'Не удалось изменить категорию.')
  } finally {
    isUpdating.value = false
  }
}

async function deleteCategory() {
  const category = categoryToDelete.value
  if (!category) {
    return
  }

  errorMessage.value = ''
  successMessage.value = ''
  isDeleting.value = true

  try {
    const response = await props.authorizedFetch(
      `/api/v1/admin/categories/${encodeURIComponent(category.id)}`,
      { method: 'DELETE' },
    )
    if (!response.ok) {
      throw new Error(`Не удалось удалить категорию (HTTP ${response.status}).`)
    }

    categories.value = categories.value.filter((item) => item.id !== category.id)
    isDeleteDialogVisible.value = false
    successMessage.value = `Категория «${category.name}» удалена.`
  } catch (error) {
    reportError(error, 'Не удалось удалить категорию.')
  } finally {
    isDeleting.value = false
  }
}

onMounted(loadCategories)
</script>

<template>
  <section aria-labelledby="category-admin-title">
    <div class="page-heading">
      <h1 id="category-admin-title">Категории</h1>
      <p>Управление категориями товаров.</p>
    </div>

    <Button
      label="Назад"
      severity="secondary"
      text
      class="back-button"
      @click="emit('back')"
    />

    <Card>
      <template #title>Добавить категорию</template>
      <template #content>
        <form class="category-form" @submit.prevent="createCategory">
          <InputText
            v-model="categoryName"
            aria-label="Название категории"
            autocomplete="off"
            maxlength="32"
            minlength="2"
            placeholder="Название категории"
            required
            :disabled="isMutating"
          />
          <Button
            type="submit"
            label="Добавить"
            :disabled="isMutating || categoryName.trim().length < 2"
            :loading="isSubmitting"
          />
        </form>
      </template>
    </Card>

    <Message v-if="errorMessage" severity="error" :closable="false" role="alert">
      {{ errorMessage }}
    </Message>
    <Message v-if="successMessage" severity="success" :closable="false" role="status">
      {{ successMessage }}
    </Message>

    <Card class="category-table-card">
      <template #title>Список категорий</template>
      <template #content>
        <DataTable
          :value="categories"
          data-key="id"
          :loading="isLoading"
          striped-rows
          table-style="min-width: 32rem"
        >
          <Column field="name" header="Название" />
          <Column header="Действия" :exportable="false" style="width: 12rem">
            <template #body="{ data }: { data: Category }">
              <div class="category-actions">
                <Button
                  label="Изменить"
                  severity="secondary"
                  outlined
                  size="small"
                  :disabled="isMutating"
                  @click="openEditDialog(data)"
                />
                <Button
                  label="Удалить"
                  severity="danger"
                  outlined
                  size="small"
                  :disabled="isMutating"
                  @click="
                    categoryToDelete = data;
                    isDeleteDialogVisible = true
                  "
                />
              </div>
            </template>
          </Column>
          <template #empty>Категорий пока нет.</template>
        </DataTable>
      </template>
    </Card>

    <Dialog
      v-model:visible="isEditDialogVisible"
      header="Изменить категорию"
      modal
      :style="dialogStyle"
      :closable="!isUpdating"
    >
      <form class="dialog-form" @submit.prevent="updateCategory">
        <InputText
          v-model="editedName"
          aria-label="Новое название категории"
          autocomplete="off"
          maxlength="32"
          minlength="2"
          required
          autofocus
          fluid
          :disabled="isUpdating"
        />
        <div class="dialog-actions">
          <Button
            type="button"
            label="Отмена"
            severity="secondary"
            outlined
            :disabled="isUpdating"
            @click="isEditDialogVisible = false"
          />
          <Button
            type="submit"
            label="Сохранить"
            :disabled="
              isUpdating ||
              editedName.trim().length < 2 ||
              editedName.trim() === categoryToEdit?.name
            "
            :loading="isUpdating"
          />
        </div>
      </form>
    </Dialog>

    <Dialog
      v-model:visible="isDeleteDialogVisible"
      header="Удалить категорию?"
      modal
      :style="dialogStyle"
      :closable="!isDeleting"
    >
      <p>
        Категория «{{ categoryToDelete?.name }}» будет удалена. Это действие нельзя
        отменить.
      </p>
      <template #footer>
        <Button
          label="Отмена"
          severity="secondary"
          outlined
          :disabled="isDeleting"
          @click="isDeleteDialogVisible = false"
        />
        <Button
          label="Удалить"
          severity="danger"
          :loading="isDeleting"
          :disabled="isDeleting"
          @click="deleteCategory"
        />
      </template>
    </Dialog>
  </section>
</template>
