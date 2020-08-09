<template>
  <v-navigation-drawer v-model="drawer" clipped app disable-resize-watcher>
    <div class="text-center">
      <v-img contain :src="require('@/assets/logo_text_v.svg')" />
    </div>
    <v-divider />
    <v-list v-show="$store.state.user">
      <v-subheader>Customer</v-subheader>
      <v-list-item v-for="item in items" :key="item.title" :to="item.to" color="amber darken-3">
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-subheader>Host</v-subheader>
      <v-list-item v-for="item in hostItems" :key="item.title" :to="item.to" color="amber darken-3">
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <template v-slot:append>
      <template v-if="$store.state.user">
        <v-btn class="mb-3" block dark depressed color="amber darken-3" @click="signOut">sign out</v-btn>
      </template>
      <template v-else>
        <v-dialog v-model="dialog" fullscreen transition="dialog-bottom-transition">
          <template v-slot:activator="{ on }">
            <v-btn class="mb-3" block depressed dark color="amber darken-3" v-on="on">Sign In</v-btn>
          </template>
          <v-card
            style="background: linear-gradient(90deg, #f8ff00 0%, #3ad59f 100%);"
            class="fill-height d-flex align-content-center justify-center flex-wrap"
          >
            <AmplifyAuthen />
          </v-card>
          <v-btn class="my-fab" fab dark @click.stop="dialog = false"><v-icon>mdi-close</v-icon></v-btn>
        </v-dialog>
      </template>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { Auth } from 'aws-amplify';
import AmplifyAuthen from '@/components/Authenticator';
import { EventBus } from '@/common/event-bus';

export default {
  name: 'NavDrawer',
  components: { AmplifyAuthen },
  data: () => ({
    items: [
      { title: 'My Bookings', to: '/myBookings' },
      { title: 'Find Accommodation', to: '/search' }
    ],
    hostItems: [
      { title: 'Reservations', to: '/reservations' },
      { title: 'My Listings', to: '/advertisements' },
      { title: 'Add new accommodation', to: '/create' }
    ],
    drawer: false,
    dialog: false
  }),
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
    }
  },
  beforeMount() {
    EventBus.$on('show-drawer', () => {
      this.drawer = true;
    });
    window.addEventListener(
      'resize',
      () => {
        // console.log(this.$vuetify.breakpoint);
        // const { smAndDown } = this.$vuetify.breakpoint;
        // if (!smAndDown) {
        //   this.drawer = false;
        //   console.log('run');
        // }
        if (this.drawer) {
          this.drawer = window.innerWidth < 960;
        }
      },
      { passive: true }
    );
  },
  beforeDestroy() {
    EventBus.$off('show-drawer');
    window.removeEventListener('resize', () => {});
  }
};
</script>

<style scoped>
.my-fab {
  position: fixed;
  bottom: 10%;
  left: 50%;
  margin-left: -28px;
  background: linear-gradient(90deg, #00d2ff 0%, #3a47d5 100%);
}
</style>
