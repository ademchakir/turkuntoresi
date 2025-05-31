<!-- filepath: frontend/src/components/Home.vue -->
<template>
  <div class="home-container">
    <h1>Türk'ün Töresi Oyunları</h1>
    <div class="game-buttons">
      <router-link to="/math" class="game-button">
        Matematik Oyunu
      </router-link>
      <router-link to="/puzzle" class="game-button">
        Puzzle Oyunu
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
}

h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.game-buttons {
  display: flex;
  gap: 2rem;
}

.game-button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  text-decoration: none;
  color: white;
  background-color: #42b883;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.game-button:hover {
  background-color: #3aa876;
}
</style>
