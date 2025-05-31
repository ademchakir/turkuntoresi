<template>
  <div class="puzzle-game">
    <div class="game-container">
      <div class="score-board">
        <div class="moves">
          <i class="mdi mdi-gamepad-variant text-purple-500"></i>
          <span>Hamle: {{ moves }}</span>
        </div>
      </div>

      <div class="puzzle-grid" :style="gridStyle">
        <div v-for="(tile, index) in tiles"
             :key="index"
             class="puzzle-tile"
             :class="{ 'empty': tile === 0 }"
             :style="getTileStyle(tile, index)"
             @click="moveTile(index)">
          {{ tile !== 0 ? tile : '' }}
        </div>
      </div>

      <div class="controls">
        <button @click="shufflePuzzle" class="control-button shuffle">
          <i class="mdi mdi-shuffle-variant"></i>
          Karıştır
        </button>
        <button v-if="isComplete" @click="shufflePuzzle" class="control-button new-game">
          <i class="mdi mdi-restart"></i>
          Yeni Oyun
        </button>
      </div>

      <router-link to="/" class="home-button">
        <i class="mdi mdi-home"></i>
        Ana Sayfaya Dön
      </router-link>

      <div v-if="isComplete" class="victory">
        <ConfettiExplosion
          :particleCount="200"
          :force="0.3"
        />
        <div class="victory-message">
          <i class="mdi mdi-trophy text-6xl text-yellow-400 animate-bounce"></i>
          <p class="text-2xl">Tebrikler! Puzzle'ı Tamamladın!</p>
          <p class="text-xl">Toplam Hamle: {{ moves }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ConfettiExplosion from 'vue-confetti-explosion'

export default {
  name: 'PuzzleGame',
  components: {
    ConfettiExplosion
  },
  data() {
    return {
      size: { rows: 2, cols: 3 },
      tiles: [],
      moves: 0,
      isComplete: false
    }
  },
  computed: {
    gridStyle() {
      return {
        gridTemplateColumns: `repeat(${this.size.cols}, 1fr)`,
        gridTemplateRows: `repeat(${this.size.rows}, 1fr)`
      }
    }
  },
  created() {
    this.initializePuzzle()
  },
  methods: {
    initializePuzzle() {
      // 5 sayı + 1 boş kare için toplam 6 kare
      this.tiles = Array.from({ length: 6 }, (_, i) => i)
      this.shufflePuzzle()
      this.moves = 0
      this.isComplete = false
    },
    shufflePuzzle() {
      for (let i = this.tiles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[this.tiles[i], this.tiles[j]] = [this.tiles[j], this.tiles[i]]
      }
      // Ensure puzzle is solvable
      if (!this.isSolvable()) {
        this.shufflePuzzle()
      }
    },
    isSolvable() {
      let inversions = 0
      const tiles = this.tiles.filter(t => t !== 0)

      for (let i = 0; i < tiles.length - 1; i++) {
        for (let j = i + 1; j < tiles.length; j++) {
          if (tiles[i] > tiles[j]) inversions++
        }
      }

      return inversions % 2 === 0
    },
    getTileStyle(tile, index) {
      if (tile === 0) return {}

      // Osmanlı/Türk motifi renklerini kullan
      const colors = [
        '#E81932', // Kırmızı
        '#2E5090', // Lacivert
        '#B39B4B', // Altın
        '#006F47', // Yeşil
        '#7D2E68'  // Mor
      ]

      return {
        background: colors[tile - 1],
        color: '#fff',
        textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
        border: '3px solid #B39B4B',
        boxShadow: '0 4px 8px rgba(0,0,0,0.2), inset 0 1px 1px rgba(255,255,255,0.2)'
      }
    },
    moveTile(index) {
      const emptyIndex = this.tiles.indexOf(0)
      if (!this.isAdjacent(index, emptyIndex)) return

      this.tiles[emptyIndex] = this.tiles[index]
      this.tiles[index] = 0
      this.moves++

      this.checkCompletion()
    },
    isAdjacent(index1, index2) {
      const row1 = Math.floor(index1 / this.size.cols)
      const col1 = index1 % this.size.cols
      const row2 = Math.floor(index2 / this.size.cols)
      const col2 = index2 % this.size.cols

      return Math.abs(row1 - row2) + Math.abs(col1 - col2) === 1
    },
    checkCompletion() {
      this.isComplete = this.tiles.every((tile, index) => {
        return tile === 0 ? index === this.tiles.length - 1 : tile === index + 1
      })
    }
  }
}
</script>

<style scoped>
.puzzle-game {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: 'Comic Sans MS', cursive;
  background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/puzzle-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.game-container {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  width: 90%;
  backdrop-filter: blur(10px);
}

.score-board {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  width: 100%;
}

.moves {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #2E5090, #1a365d);
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  color: white;
  font-size: 1.2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border: 2px solid #B39B4B;
}

.moves i {
  font-size: 1.2rem;
  color: #B39B4B;
}

.puzzle-grid {
  display: grid;
  gap: 0.5rem;
  margin-bottom: 2rem;
  aspect-ratio: 1;
  width: 65%;
}

.puzzle-tile {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2.5rem;
  font-weight: bold;
  background: #e9ecef;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
  aspect-ratio: 1;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 2px solid #2c3e50;
  color: #2c3e50;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.puzzle-tile:not(.empty):hover {
  transform: scale(1.05);
}

.empty {
  background: transparent;
  cursor: default;
}

.controls {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.control-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  font-size: 1.2rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.3s;
}

.shuffle {
  background: #4dabf7;
  color: white;
}

.shuffle:hover {
  background: #339af0;
}

.new-game {
  background: #51cf66;
  color: white;
}

.new-game:hover {
  background: #40c057;
}

.home-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem;
  margin-top: 1rem;
  font-size: 1.2rem;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.3s;
  text-decoration: none;
}

.home-button:hover {
  background: #f57c00;
}

.victory {
  position: relative;
  text-align: center;
  margin-top: 2rem;
}

.victory-message {
  animation: scale-in 0.5s ease-out;
}

@keyframes scale-in {
  0% { transform: scale(0); }
  70% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
</style>
