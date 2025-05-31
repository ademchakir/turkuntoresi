<template>
  <el-container id="app" style="min-height:100vh; background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);">
    <el-header style="text-align:center; background: transparent; padding-top: 2rem;">
      <h1 style="font-size: 2.5rem; color: #2196f3; font-family: 'Comic Sans MS', cursive;">
        <i class="mdi mdi-brain"></i>
        Eğlenceli Oyunlar
      </h1>
    </el-header>
    <el-main>
      <div v-if="$route.path === '/' || $route.path === ''">
        <div class="game-menu">
          <router-link to="/math" class="game-card">
            <i class="mdi mdi-calculator text-5xl text-blue-500"></i>
            <h2>Matematik Oyunu</h2>
            <p>Toplama işlemlerini eğlenerek öğren!</p>
          </router-link>

          <router-link to="/puzzle" class="game-card">
            <i class="mdi mdi-puzzle text-5xl text-purple-500"></i>
            <h2>Puzzle Oyunu</h2>
            <p>Parçaları doğru yere yerleştir!</p>
          </router-link>
        </div>
      </div>
      <router-view v-else></router-view>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Comic Sans MS', cursive;
}

.game-menu {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 2rem;
  flex-wrap: wrap;
}

.game-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  width: 250px;
  text-align: center;
  text-decoration: none;
  color: #333;
  transition: transform 0.3s, box-shadow 0.3s;
}

.game-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.game-card h2 {
  margin: 1rem 0;
  color: #2196f3;
}

.game-card p {
  color: #666;
  margin: 0;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
