<template>
  <v-footer id="important" app absolute>
    <v-row align="center" justify="center">
      <span class="trademark">Copyright © 2020 Taxidi and related marks are registered trademarks of Taxidi Inc.</span>
      <v-spacer></v-spacer>
      <v-btn text style="margin: 0px; padding: 0px;" @click="aboutPage">About</v-btn>
      <v-btn text style="margin: 0px; padding: 0px;" onclick="location.href='mailto:taxidi.notifications@gmail.com';"
        >Contact us</v-btn
      >
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {};
  },
  methods: {
    aboutPage () {
      this.$router.push(`/about`);
    }
  }
};
</script>

<style>
#important {
  background: linear-gradient(90deg, #e3ffe7 0%, #d9e7ff 100%);
}

.trademark {
  margin-left: 10px !important;
}
</style>
