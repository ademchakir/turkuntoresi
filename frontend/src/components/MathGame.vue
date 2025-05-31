<template>
  <div class="math-game">
    <div class="game-container">
      <div class="score-board">
        <div class="score">
          <i class="mdi mdi-star text-yellow-400"></i>
          <span>Puan: {{ score }}</span>
        </div>
      </div>

      <div class="question-box" :class="{ shake: isWrong }">
        <div class="numbers">
          <span class="number">{{ num1 }}</span>
          <i class="mdi mdi-plus text-4xl text-blue-500"></i>
          <span class="number">{{ num2 }}</span>
          <i class="mdi mdi-equal text-4xl text-blue-500"></i>
          <input
            v-model.number="userAnswer"
            type="number"
            @keyup.enter="checkAnswer"
            :disabled="showResult"
            class="answer-input"
          >
        </div>
      </div>

      <div class="result" v-if="showResult">
        <div v-if="isCorrect" class="correct">
          <ConfettiExplosion
            :particleCount="200"
            :force="0.3"
          />
          <i class="mdi mdi-emoticon-happy text-6xl text-green-500 animate-bounce"></i>
          <p class="text-2xl animate-pulse">Harika! Doğru cevap!</p>
          <div class="stars-explosion">
            <i v-for="n in 5" :key="n"
               class="mdi mdi-star text-yellow-400 animate-star"
               :style="{ '--delay': n * 0.1 + 's' }"></i>
          </div>
        </div>
        <div v-else class="wrong">
          <i class="mdi mdi-emoticon-sad text-6xl text-red-500"></i>
          <p class="text-2xl">Üzgünümm, tekrar dene!</p>
        </div>
      </div>

      <button @click="nextQuestion" class="next-button">
        <i class="mdi mdi-refresh text-xl"></i>
        Yeni Soru
      </button>

      <router-link to="/" class="home-button">
        <i class="mdi mdi-home"></i>
        Ana Sayfaya Dön
      </router-link>
    </div>
  </div>
</template>

<script>
import ConfettiExplosion from 'vue-confetti-explosion'

export default {
  name: 'MathGame',
  components: {
    ConfettiExplosion
  },
  data() {
    return {
      num1: 0,
      num2: 0,
      userAnswer: null,
      score: 0,
      showResult: false,
      isCorrect: false,
      isWrong: false
    }
  },
  created() {
    this.generateQuestion()
  },
  methods: {
    generateQuestion() {
      this.num1 = Math.floor(Math.random() * 10)
      this.num2 = Math.floor(Math.random() * 10)
      this.userAnswer = null
      this.showResult = false
      this.isWrong = false
    },
    checkAnswer() {
      const correctAnswer = this.num1 + this.num2
      this.isCorrect = this.userAnswer === correctAnswer
      this.showResult = true

      if (this.isCorrect) {
        this.score += 10
      } else {
        this.isWrong = true
        setTimeout(() => {
          this.isWrong = false
        }, 500)
      }
    },
    nextQuestion() {
      this.generateQuestion()
    }
  }
}
</script>

<style scoped>
.math-game {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-family: 'Comic Sans MS', cursive;
}

.game-container {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 90%;
}

.score-board {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
}

.score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.question-box {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.numbers {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  font-size: 2.5rem;
}

.number {
  background: #e9ecef;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  min-width: 60px;
  text-align: center;
}

.answer-input {
  width: 80px;
  height: 60px;
  font-size: 2rem;
  text-align: center;
  border: 2px solid #dee2e6;
  border-radius: 0.5rem;
  outline: none;
}

.answer-input:focus {
  border-color: #4dabf7;
}

.result {
  text-align: center;
  margin: 1rem 0;
}

.next-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem;
  font-size: 1.2rem;
  background: #4dabf7;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.3s;
}

.next-button:hover {
  background: #339af0;
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

.shake {
  animation: shake 0.5s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

@keyframes star-pop {
  0% {
    transform: scale(0) rotate(0deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.5) rotate(180deg);
    opacity: 1;
  }
  100% {
    transform: scale(1) rotate(360deg);
    opacity: 1;
  }
}

.animate-star {
  animation: star-pop 0.5s ease-out forwards;
  animation-delay: var(--delay);
  opacity: 0;
  font-size: 2rem;
}

.stars-explosion {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 1rem;
  z-index: 1;
}

.correct {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  animation: scale-in 0.5s ease-out;
}

@keyframes scale-in {
  0% {
    transform: scale(0);
  }
  70% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

.animate-pulse {
  animation: pulse 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
