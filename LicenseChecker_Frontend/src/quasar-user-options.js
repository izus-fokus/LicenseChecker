import "./styles/quasar.sass";
import "@quasar/extras/roboto-font/roboto-font.css";
import "@quasar/extras/material-icons/material-icons.css";
import { Loading } from "quasar";
import { Notify } from "quasar";

// To be used on app.use(Quasar, { ... })
export default {
  plugins: { Loading, Notify },
  config: {},
};
