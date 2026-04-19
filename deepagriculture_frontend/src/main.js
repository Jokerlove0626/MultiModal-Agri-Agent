import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "@material-symbols/font-400/outlined.css";

const app = createApp(App);

app.use(router);

app.mount("#app");
