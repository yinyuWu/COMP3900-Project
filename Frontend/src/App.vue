<template>
  <v-app>
    <NavDrawer />
    <NavBar />
    <v-content>
      <v-container fluid :class="{ 'my-width-lg': $vuetify.breakpoint.lgAndUp, 'my-width-md': $vuetify.breakpoint.md }">
        <router-view ></router-view>
      </v-container>
    </v-content>
    <Footer v-if="['Home'].indexOf($route.name) !== -1" />
  </v-app>
</template>

<script>
import { Auth } from 'aws-amplify';
import NavBar from '@/components/NavBar';
import Footer from '@/components/Footer';
import NavDrawer from '@/components/NavDrawer';

export default {
  name: 'App',
  components: { NavBar, Footer, NavDrawer },
  data: () => ({}),
  created() {
    this.findUser();
  },
  methods: {
    async findUser() {
      try {
        const user = await Auth.currentAuthenticatedUser();
        this.$store.commit('setUser', user);
      } catch (err) {
        this.$store.commit('setUser', null);
      }
    }
  }
};
</script>

<style scoped>
.my-width-lg {
  width: 90%;
}
.my-width-md {
  width: 100%;
}
</style>
