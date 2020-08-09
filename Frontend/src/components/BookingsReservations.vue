<template>
  <!-- Table -->
  <v-data-table :headers="headers" :items="bookings" class="elevation-1">
    <!-- Toolbar -->
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>{{ type == 'Bookings' ? "Bookings I've Made": "Bookings To My Accommodation" }}</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
      </v-toolbar>
    </template>

    <template v-slot:item.cancelled="{ item }">
      <v-simple-checkbox v-model="item.cancelled" disabled></v-simple-checkbox>
    </template>
    <template v-slot:item.linkDesc="{ item }">
      <a v-if="item.link != ''" :href="item.link">{{ item.linkDesc }}</a>
      <div v-else>{{ item.linkDesc }}</div>
    </template>
    <!-- Each Item Action-->
    <template v-slot:item.actions="{ item }">
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon :disabled="item.cancelled" v-on="on">
            <v-icon dark color="amber darken-3">mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(action, i) in actions" :key="i" @click="takeAction(item, action)">
            <v-list-item-title>{{ action }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>

    <template v-slot:no-data v-if="type == 'Bookings'">
      <p style="text-transform:capitalize;">You have no booking, book one</p>
    </template>
    <template v-slot:no-data v-else>
      <p style="text-transform:capitalize;">No reservations made to your properties</p>
    </template>
    
  </v-data-table>
</template>

<script>
import { Auth } from 'aws-amplify';

export default {
  name: 'BookingsReservations',
  components: {
  },
  props: ['type'], // type should be "Bookings" or "Reservations"
  data() {
    return {
      adId: 0,
      resData: [],
      bookings: [],
      email: '',
      headers: [
        { text: 'Property details', value: 'linkDesc', sortable: false }, // TODO
        { text: 'From', value: 'from', sortable: false },
        { text: 'To', value: 'to', sortable: false },
        { text: 'Cancelled', value: 'cancelled', sortable: false },
        { text: '', value: 'actions', sortable: false },
      ],
      actions: ['cancel'],
    };
  },

  created() {
    // this.setEmail()
    this.initialize();
    this.headers.unshift({
      text: this.type == 'Bookings' ? 'Owner' : 'Tenant',
      align: 'start',
      sortable: false,
      value: this.type == 'Bookings' ? 'owner' : 'tenant',
    });
    if (this.type == 'Bookings') {
      this.actions.push('review');
    }
  },

  methods: {
    async cancel(item) {
      if (confirm('Are you sure you want to cancel this booking')) {
        const body = {
          bookingID: item.ID,
        };
        const res = await this.$http.post(
          `${this.$api_hostname}/cancelbooking`,
          body,
        );
        this.$router.go();
      }
    },

    async review(item) {
      const url = `/review/${item.ID}`;
      this.$router.push(url).catch((err) => {});
    },

    async takeAction(item, action) {
      if (action == 'cancel') {
        this.cancel(item);
      } else if (action == 'review') {
        this.review(item);
      }
    },

    replaceNull(value) {
      return value == null ? '' : value;
    },
    setEmail() {
      this.email = this.$store.state.user.signInUserSession.idToken.payload.email;
      console.log(this.email);
    },


    async initialize() {
      const user = await Auth.currentAuthenticatedUser();
      this.email = user.attributes.email;
      let resTenant;
      if (this.type == 'Reservations') {
        resTenant = await this.$http.get(
          `${this.$api_hostname}/getBookingsByOwner/${this.email}`,
        );
      } else {
        resTenant = await this.$http.get(
          `${this.$api_hostname}/getBookingsByTenant/${this.email}`,
        );
      }
      resTenant = resTenant.data;
      let r;
      for (r of resTenant) {
        const item = {};
        // console.log(r);
        item.ID = r.ID;
        item.tenant = r.tenant;
        item.cancelled = r.cancelled;
        item.from = r.from;
        item.to = r.to;
        item.link = '';
        item.linkDesc = 'loading...';
        item.advertisementID = r.advertisementID;
        const ad = await this.$http
          .get(`${this.$api_hostname}/advertisement/${r.advertisementID}`)
          .then(
            (response) => {
              item.link = `detail/${r.advertisementID}`;
              item.linkDesc = response.data.title;
              item.owner = response.data.owner;
            },
            (response) => {
              item.linkDesc = 'Advertisement was deleted';
              console.log(response, 'error');
            },
          );
        console.log('link: ');
        console.log(item.link);
        this.bookings.push(item);
      }
    },
  },
};
</script>
