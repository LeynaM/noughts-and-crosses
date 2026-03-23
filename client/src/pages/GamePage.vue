<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Board from '@/components/Board.vue'
import { useGame } from '@/composables/useGame'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const route = useRoute()
const router = useRouter()

const { game, joinGame, makeMove } = useGame()
joinGame(route.params.gameId, route.query.username)

const inviteLink = computed(() => {
  const joinHref = router.resolve({ name: ROUTES.JOIN, query: { gameId: route.params.gameId } }).href

  return new URL(joinHref, window.location.origin).href
})
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <template v-if="!game">
      Loading...
    </template>
    <template v-else>
      {{ game.status }}
      <Board
        :board="game.board"
        @make-move="makeMove"
      />
      <div class="game-link">
        Copy link to invite opponent: {{ inviteLink }}
      </div>
    </template>
  </MainLayout>
</template>
