import { createApp } from "vue";
import App from "./App.vue";
import copyText from "@meforma/vue-copy-to-clipboard";

createApp(App).use(copyText).mount("#app");
