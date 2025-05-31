import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  optimizeDeps: {
    exclude: ['@mdi/font']
  },
  server: {
    fs: {
      strict: false
    }
  }
});

