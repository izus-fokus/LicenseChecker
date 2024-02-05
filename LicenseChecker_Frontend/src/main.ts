import { createApp } from "vue";
import { createPinia } from "pinia";
import "@fortawesome/fontawesome-free/css/all.css";
import App from "./App.vue";
import router from "./router";

import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";
import "@quasar/extras/material-icons/material-icons.css"; // Import icon libraries
import "quasar/src/css/index.sass"; // Import Quasar css
const app = createApp(App).use(Quasar, quasarUserOptions);
// app.use(BootstrapVue3)
app.use(createPinia());
app.use(router);
app.mount("#app");
