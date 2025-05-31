import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '@mdi/font/css/materialdesignicons.min.css';
import router from './router';

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.mount('#app');
