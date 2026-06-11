<template>
  <div v-if="!ready" class="loading-screen"></div>

  <div v-else class="layout">
    <div class="sidebar">
      <h2>Whisper Box</h2>

      <div v-if="user" class="user">
        <div class="user-box">
          <img class="user-avatar" src="/img/lotrek.png" alt="avatar" />
          <p>{{ user.username }}</p>
        </div>

        <div class="menu">
          <NuxtLink to="/">FORUM</NuxtLink>

          <a
            v-if="user.is_superuser"
            href="http://localhost:8000/admin/"
            target="_blank"
          >
            ADMIN DJANGO
          </a>

          <NuxtLink v-else to="/create">
            NEW REQUEST
          </NuxtLink>

          <button id="logout-button" @click="logout">LOGOUT</button>
        </div>
      </div>

      <h5 v-if="user" id="h5">MADE BY ZANI DIEGO</h5>

      <div v-else>
        <NuxtLink to="/login">Login</NuxtLink>
      </div>
    </div>

    <div class="content">
      <slot />
    </div>
  </div>
</template>

<script setup>
const user = ref(null)
const ready = ref(false)

const config = useRuntimeConfig()

async function fetchUser() {
  try {
    user.value = await $fetch(`${config.public.apiBase}/api/auth/me/`, {
      credentials: 'include'
    })
  } catch {
    user.value = null
  } finally {
    ready.value = true
  }
}

async function logout() {
  try {
    await $fetch(`${config.public.apiBase}/api/auth/logout/`, {
      method: 'POST',
      credentials: 'include'
    })
  } finally {
    user.value = null
    await navigateTo('/login')
  }
}

onMounted(fetchUser)
</script>