<template>
  <v-card class="mx-auto my-5 search-card" max-width="800" @click="handle" max-height="600px" hover>
    <v-container fluid>
      <v-row>
        <v-col xs="12" sm="12" md="5" lg="5">
          <!-- TODO Change this to carousel -->
          <v-img height="200px" :src="getPhoto" :class="{ 'not-ok': !ok }"> </v-img>
          <v-rating
            v-if="rating != -1"
            v-model="rating"
            background-color="orange lighten-3"
            color="orange"
            half-increments
            medium
            readonly
            class="d-none d-md-flex"
          ></v-rating>
          <v-rating
            v-if="rating == -1"
            v-model="rating"
            background-color="grey lighten-3"
            color="grey"
            half-increments
            medium
            readonly
            class="d-none d-md-flex"
          ></v-rating>
          <v-card-actions class="d-none d-md-flex">
            <v-card-text class="headline">${{ rent }}/night</v-card-text>
          </v-card-actions>
          <div v-if="!ok" class="grey--text ml-4">Not available during selected dates.</div>
        </v-col>
        <v-col xs="12" sm="12" md="7" lg="7">
          <v-row class="justify-space-between">
            <v-col cols="12">
              <v-card-title>{{ title }}</v-card-title>
            </v-col>
            <v-col cols="12" class="d-flex d-md-none">
              <v-rating
                v-if="rating != -1"
                v-model="rating"
                background-color="orange lighten-3"
                color="orange"
                half-increments
                medium
                readonly
              ></v-rating>
              <v-rating
                v-if="rating == -1"
                v-model="rating"
                background-color="grey lighten-3"
                color="grey"
                half-increments
                medium
                readonly
              ></v-rating>
            </v-col>
          </v-row>
          <v-card-text class="headline d-flex d-md-none">${{ rent }}/night</v-card-text>
          <v-card-subtitle class="d-none d-md-flex">{{ truncatedDescription }}</v-card-subtitle>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  name: 'SearchCard',
  props: {
    title: String,
    description: String,
    objectID: String,
    images: Array,
    rating: Number,
    rent: Number,
    ok: Boolean
  },
  data() {
    return {};
  },
  computed: {
    getPhoto() {
      return `${this.$s3_hostname}${this.images[0]}`;
    },
    truncatedDescription() {
      if (this.description.length > 600) {
        return `${this.description.substring(0, 600)}...`;
      }
      return this.description;
    }
  },
  methods: {
    handle() {
      const url = `/detail/${this.objectID}`;
      this.$router.push({
        name: 'AdvertisementDetail',
        params: { id: this.objectID },
        query: {
          checkin: this.$route.query.checkin,
          checkout: this.$route.query.checkout
        }
      });
    }
  }
};
</script>

<style scoped>
.not-ok {
  opacity: 0.4;
  filter: alpha(opacity=40); /* msie */
}
.search-card:hover {
  transform: translateY(-10px);
}
</style>
