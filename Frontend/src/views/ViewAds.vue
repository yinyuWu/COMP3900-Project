<template>
  <!-- Table -->
  <v-data-table :headers="headers" :items="properties" class="elevation-1">
    <!-- Toolbar -->
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>My Accommodation Listing</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
      </v-toolbar>
    </template>

    <!-- Cancel/Edit  -->

    <!-- Each Item -->
    <template v-slot:item.detail="{ item }">
      <v-btn small dark color="amber darken-3" @click="viewDetail(item)">
        View Listing
      </v-btn>
    </template>

    <template v-slot:item.edit="{ item }">
      <v-btn small dark color="amber darken-3" @click="editDetail(item)">
        Edit Listing
      </v-btn>
    </template>

    <template v-slot:no-data>
      <p>No accommodation listings found.</p>
    </template>
  </v-data-table>
</template>

<script>
/* eslint-disable no-restricted-syntax */
export default {
  name: 'ViewAds',
  components: {},
  data() {
    return {
      adId: 0,
      resData: [],
      properties: [],
      email: this.$store.state.user.signInUserSession.idToken.payload.email,
      headers: [
        {
          text: 'Listing Title',
          align: 'start',
          sortable: false,
          value: 'name'
        },
        { text: 'City', value: 'location', sortable: false },
        { text: 'Price', value: 'price', sortable: false },
        { text: 'Listing', value: 'detail', sortable: false },
        { text: 'Edit Listing' , value: 'edit', sortable: false }
      ]
    };
  },

  created() {
    this.initialize();
  },

  methods: {
    replaceNull(value) {
      return value == null ? '' : value;
    },

    async initialize() {
      const res = await this.$http.get(`${this.$api_hostname}/getAdvertisements/${this.email}`);
      this.resData = await res.data;

      let r;
      for (r of this.resData) {
        const item = {};
        item.name = this.replaceNull(r.title);
        item.location = this.replaceNull(r.city);
        item.price = `$${this.replaceNull(r.rent)}/night`;
        this.properties.push(item);
      }
    },

    viewDetail(item) {
      const index = this.properties.indexOf(item);
      const id = this.resData[index].ID;
      this.adId = id;
      this.$router.push(`/detail/${id}`);
    },

    editDetail(item) {
      const index = this.properties.indexOf(item);
      const id = this.resData[index].ID;
      this.adId = id;
      this.$router.push(`/editDetail/${id}`);
    }
  }
};
</script>
