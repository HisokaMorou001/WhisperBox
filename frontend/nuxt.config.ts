// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  vite: {
    server: {
      hmr: {
        protocol: 'ws',
        host: 'localhost',
        port: 80,
        clientPort: 80,
        path: '/_nuxt',
      },
    },
  },

  css: [
    '~/assets/css/forum.css',
  ],

  runtimeConfig: {
    public: {
      apiBase: '/api',
    }
  }
})