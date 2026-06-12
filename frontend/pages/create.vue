<template>
  <div>
    <h1>NEW REQUEST</h1>

    <form @submit.prevent="submitIdea">
      <input v-model="title" name="title" placeholder="Title" />
      <br /><br />

      <textarea v-model="description" name="description" placeholder="Description"></textarea>
      <br /><br />

      <button type="submit" class="create-button">ADD</button>
    </form>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()

const title = ref('')
const description = ref('')

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop().split(';').shift()
  }
  return null
}

async function submitIdea() {
  if (!title.value || !description.value) return

  const csrfToken = getCookie('csrftoken')

  await $fetch(`${config.public.apiBase}/ideas/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': csrfToken
    },
    body: {
      title: title.value,
      description: description.value
    }
  })

  title.value = ''
  description.value = ''

  await navigateTo('/')
}
</script>

<style src="~/assets/css/create.css"></style>