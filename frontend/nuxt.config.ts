// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  css: [
    '~/assets/css/forum.css',
  ],

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
    }
  }
})