<template>
  <div>
    <h1>FORUM REQUESTS</h1>

    <div
      v-for="idea in ideas"
      :key="idea.id"
      :class="[
        'card',
        idea.status === 'approved'
          ? 'approved'
          : idea.status === 'rejected'
          ? 'rejected'
          : ''
      ]"
    >
      <div class="card-content">
        <h3>{{ idea.title }}</h3>
        <p>{{ idea.description }}</p>

        <small>Created: {{ formatDate(idea.created_at) }}</small>

        <small v-if="idea.approved_at">
          | Approved: {{ formatDate(idea.approved_at) }}
        </small>

        <small v-if="idea.rejected_at">
          | Rejected: {{ formatDate(idea.rejected_at) }}
        </small>
      </div>

      <button class="btn-comment" @click="toggleComments(idea.id)">
        COMMENTS
      </button>

      <div class="comments-container" v-show="openComments[idea.id]">
        <div class="comments-list">
              <div
                v-for="comment in comments[idea.id]"
                :key="comment.id"
                class="comment"
                :class="{ 'admin-comment': comment.is_admin }"
              >
                {{ comment.text }}
              </div>
        </div>

        <div class="comment-input-box">
          <input
            v-model="newComment[idea.id]"
            type="text"
            placeholder="Write a comment..."
          />

          <button @click="addComment(idea.id, newComment[idea.id])">
            SEND
          </button>
        </div>
      </div>
    </div>

    <p v-if="!ideas || ideas.length === 0">No requests yet.</p>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()


const ideas = ref([])

async function loadIdeas() {
  ideas.value = await $fetch(
    `${config.public.apiBase}/ideas/`,
    {
      credentials: 'include'
    }
  )
}

onMounted(loadIdeas)

const openComments = ref({})
const comments = ref({})
const newComment = ref({})

async function toggleComments(ideaId) {
  openComments.value[ideaId] = !openComments.value[ideaId]

  if (openComments.value[ideaId]) {
    await loadComments(ideaId)
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop().split(';').shift()
  }
  return null
}

async function loadComments(ideaId) {
  try {
    const res = await $fetch(
      `${config.public.apiBase}/ideas/${ideaId}/comments/`,
      {
        credentials: 'include'
      }
    )

    comments.value[ideaId] = res
  } catch {
    comments.value[ideaId] = []
  }
}

async function addComment(ideaId, text) {
  const clean = text?.trim()
  if (!clean) return

  const csrfToken = getCookie('csrftoken')

  await $fetch(
    `${config.public.apiBase}/ideas/${ideaId}/comments/`,
    {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: { text: clean }
    }
  )

  newComment.value[ideaId] = ''
  await loadComments(ideaId)
}

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleString('it-IT')
}
</script>