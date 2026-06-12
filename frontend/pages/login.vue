<template>
  <div class="login-page">
    <div class="login-box">
      <h2>Login</h2>

      <form @submit.prevent="login">
        <input
          v-model="username"
          class="login-input"
          type="text"
          placeholder="Username"
          required
        />

        <input
          v-model="password"
          class="login-input"
          type="password"
          placeholder="Password"
          required
        />

        <button class="login-button" type="submit">
          ENTER
        </button>
      </form>

      <p v-if="error" class="error-text">
        INVALID CREDENTIALS
      </p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})

const config = useRuntimeConfig()

const username = ref('')
const password = ref('')
const error = ref(false)

async function login() {
  error.value = false

  try {
    // 1. LOGIN (crea sessione Django)
      await $fetch(`${config.public.apiBase}/auth/login/`, {
      method: 'POST',
      credentials: 'include',
      body: {
        username: username.value,
        password: password.value
      }
    })

    // 2. FORZA SET COOKIE CSRF (IMPORTANTISSIMO per POST successivi)
    await $fetch(`${config.public.apiBase}/auth/me/`, {
      credentials: 'include'
    })

    // 3. redirect app
    await navigateTo('/', { replace: true })

  } catch (err) {
    console.error('Login error:', err)
    error.value = true
  }
}
</script>

<style src="~/assets/css/style.css"></style>