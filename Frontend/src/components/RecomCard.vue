<template>
  <v-card class="card" max-width="250" height="330" @click="viewAd" hover>
    <v-img :src="image" height="200px" class="white--text align-end"></v-img>
    <v-card-title>{{ title }}</v-card-title>

    <!--<v-card-text>{{ rating }}</v-card-text>-->
    <v-rating
      class="rating"
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
  </v-card>
</template>

<script>
export default {
  props: {
    title: String,
    rating: Number,
    image: String,
    id: String,
    checkIn: String,
    checkOut: String
  },
  name: 'RecomCard',
  methods: {
    resolveImg() {
      return require('@/assets/logo_text_v.png');
    },
    viewAd() {
      const url = `/detail/${this.id}`;
      this.$router.push({
        name: 'AdvertisementDetail',
        params: { id: this.id },
        query: {
          checkin: this.checkIn,
          checkout: this.checkOut
        }
      });
    }
  }
};
</script>

<style scoped>
.v-card__text,
.v-card__title {
  word-break: normal; /* maybe !important  */
  font-size: medium;
}

.rating {
  bottom: 0;
  position: absolute;
}

.card {
  margin: auto !important;
  position: relative !important;
}

.card:hover {
  transform: translateY(-10px);
}
</style>
