<template>
  <div v-if="!ready" class="loading-screen"></div>

  <div v-else class="layout" :class="{ 'sidebar-open': sidebarOpen }">
    <div class="drawer-overlay" v-if="sidebarOpen" @click="closeSidebar"></div>

    <div class="sidebar" :class="{ open: sidebarOpen }">
      <button class="sidebar-toggle" @click="toggleSidebar" aria-label="Menu">
        {{ sidebarOpen ? 'CLOSE' : 'MENU' }}
      </button>

      <h2>Whisper Box</h2>

      <div v-if="user" class="user">
        <div class="user-box">
          <img class="user-avatar" src="/img/lotrek.png" alt="avatar" />
          <p>{{ user.username }}</p>
        </div>

        <div class="menu">
          <NuxtLink to="/" @click="closeSidebar">FORUM</NuxtLink>

          <a
            v-if="user.is_superuser"
            href="http://localhost:8000/admin/"
            target="_blank"
            @click="closeSidebar"
          >
            ADMIN DJANGO
          </a>

          <NuxtLink v-else to="/create" @click="closeSidebar">
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
const route = useRoute()
const sidebarOpen = ref(false)

const config = useRuntimeConfig()

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}

async function fetchUser() {
  try {
    const res = await $fetch('/api/auth/me/', {
      credentials: 'include'
    })
    user.value = res
  } catch (e) {
    user.value = null
  } finally {
    ready.value = true

    if (!user.value && route.path !== '/login') {
      await navigateTo('/login')
    }

    if (user.value && route.path === '/login') {
      await navigateTo('/')
    }
  }
}

async function logout() {
  try {
    await $fetch(`${config.public.apiBase}/auth/logout/`, {
      method: 'POST',
      credentials: 'include'
    })
  } finally {
    user.value = null
    closeSidebar()
    await navigateTo('/login')
  }
}

onMounted(fetchUser)
</script>