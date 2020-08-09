<template>
  <v-app-bar id="important" app>
    <v-app-bar-nav-icon class="hidden-md-and-up" @click.stop="clickNavIcon" />
    <router-link to="/">
      <v-img contain :src="require('@/assets/logo_text_h.svg')" height="40" width="150" />
    </router-link>
    <v-spacer></v-spacer>
    <!-- If logged in  -->
    <div class="hidden-sm-and-down flex-nowrap">
      <template v-if="getUser">
        <template v-if="this.$store.state.host">
          <v-btn text to="/reservations">Bookings to My Accommodation</v-btn>
          <v-btn text to="/advertisements">My Accommodation Listings</v-btn>
          <v-btn text to="/create">Add Accommodation</v-btn>
        </template>

        <template v-else>
          <v-btn text to="/myBookings">Bookings I've Made</v-btn>
          <v-btn text to="/search">Search Accommodation</v-btn>
          <!--<v-btn text @click="host()">Host</v-btn>-->
        </template>
        <v-btn class="ml-5" color="amber darken-1" dark depressed @click.prevent="toggleUserType">
          <div v-if="this.$store.state.host">Switch to Booking Mode</div>
          <div v-else>Switch to Hosting Mode</div>
        </v-btn>
        <v-btn class="ml-5" depressed dark color="amber darken-3" @click="signOut">sign out</v-btn>
      </template>
      <!-- If not sign in -->
      <template v-if="!getUser">
        <v-dialog v-model="dialog" width="500" hide-overlay overlay-opacity="0">
          <template v-slot:activator="{ on }">
            <v-btn depressed dark color="amber darken-3" v-on="on">Sign In</v-btn>
          </template>
          <AmplifyAuthen />
        </v-dialog>
      </template>
    </div>
  </v-app-bar>
</template>

<script>
import { Auth } from 'aws-amplify';
import AmplifyAuthen from '@/components/Authenticator';
import { EventBus } from '@/common/event-bus';

export default {
  name: 'NavBar',
  components: { AmplifyAuthen },
  data: () => ({
    dialog: false
  }),
  computed: {
    getUser() {
      return this.$store.state.user;
    },
    getHost() {
      return this.$store.state.host;
    }
  },
  methods: {
    signOut() {
      Auth.signOut()
        .then((data) => {
          this.$store.commit('setUser', null);
          this.$router.push({ name: 'Home' }).catch((err) => {});
        })
        .catch((err) => console.log(err));
    },
    toggleUserType() {
      this.$store.state.host = !this.$store.state.host;
    },
    clickNavIcon() {
      EventBus.$emit('show-drawer');
    }
  },
  beforeMount() {
    window.addEventListener(
      'resize',
      () => {
        this.dialog = false;
      },
      { passive: true }
    );
  }
};
</script>

<style scoped></style>
