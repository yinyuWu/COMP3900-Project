import Vue from 'vue';
import Amplify, * as AmplifyModules from 'aws-amplify';
import { AmplifyPlugin } from 'aws-amplify-vue';
import axios from 'axios';
import Lingallery from 'lingallery';
import InstantSearch from 'vue-instantsearch';
import moment from 'moment';
import aws_exports from './aws-exports';
import vuetify from './plugins/vuetify';
import store from './store';
import router from './router';
import App from './App.vue';

Amplify.configure(aws_exports);
Vue.use(AmplifyPlugin, AmplifyModules);
Vue.use(InstantSearch);
Vue.component('lingallery', Lingallery);

Vue.config.productionTip = false;
Vue.prototype.$http = axios;
Vue.prototype.$moment = moment;
Vue.prototype.$api_hostname = 'https://0rfkxyvpxe.execute-api.ap-southeast-2.amazonaws.com/Prod';
Vue.prototype.$s3_hostname = 'https://taxidi-photo.s3-ap-southeast-2.amazonaws.com/';

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App)
}).$mount('#app');
