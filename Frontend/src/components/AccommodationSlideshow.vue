<template>
  <v-carousel
    cycle
    height="500"
    hide-delimiter-background
    show-arrows-on-hover
    continuous
  >
    <v-carousel-item v-for="(img, i) in images" :key="i">
      <v-sheet height="100%">
          <v-parallax :src="img.src" />
      </v-sheet>
    </v-carousel-item>
  </v-carousel>
</template>

<script>
/* eslint-disable global-require */
export default {
  name: 'AccommodationSlideshow',
  props: {
    images: {
      type: Array,
      default() {
        return [
          {
            src: require('@/assets/beach.jpeg'),
          },
          {
            src: require('@/assets/beachHouse.jpg'),
          },
          {
            src: require('@/assets/sydney2.jpeg'),
          },
        ];
      },
    },
  },

  data() {
    return {};
  },
};
</script>
