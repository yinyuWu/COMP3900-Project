<template>
  <v-container>
    <hr>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      {{ review_text }}
    </v-card-text>
    <v-row align="center" class="mx-0">
      <v-rating :value="rating" color="amber" dense half-increments readonly size="14"></v-rating>

      <div class="grey--text ml-4">{{ rating }}</div>
    </v-row>
  </v-container>

</template>

<script>
export default {
  props: ['title', 'text', 'rating'],
  name: 'ReviewCard',
  data() {
    return {
      review_text: this.text === ' ' ? 'No comment by this user' : this.text
    }
  }
};
</script>
