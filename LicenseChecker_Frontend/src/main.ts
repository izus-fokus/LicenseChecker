import { createApp } from "vue";
// import { createPinia } from "pinia";
import "@fortawesome/fontawesome-free/css/all.css";
import App from "./App.vue";
import router from "./router";
import './styles/quasar.sass';
import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";
import "@quasar/extras/material-icons/material-icons.css"; // Import icon libraries
import "quasar/src/css/index.sass"; // Import Quasar css
import store from '@//store';

const app = createApp(App).use(Quasar, quasarUserOptions);
// const pinia = createPinia();
// app.use(BootstrapVue3)
// app.use(pinia);
app.use(store)
app.use(router);
app.mount("#app");
