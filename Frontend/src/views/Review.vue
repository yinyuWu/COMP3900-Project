<template>
  <v-container align="center" style="width: 90%">
    <!-- Advertisement Image  -->
    <v-row>
      <v-col cols="12">
        <v-img :src="imgsrc" :aspect-ratio="16 / 9" max-height="500"></v-img>
      </v-col>
    </v-row>
    <br />

    <!-- Advertisement Info -->
    <v-row>
      <p class="ad-title">{{ title }}</p>
    </v-row>
    <v-row>
      <p class="ad-time">
        From <b>{{ checkin['date'] }} {{ checkin['month'] }} {{ checkin['year'] }}</b> <br />
        To <b>{{ checkout['date'] }} {{ checkout['month'] }} {{ checkout['year'] }}</b>
      </p>
    </v-row>
    <v-row>
      <h2>What do you think of {{ title }}?</h2>
    </v-row>
    <v-row>
      <v-col cols="8">
        <hr />
      </v-col>
    </v-row>

    <!-- Ratings -->
    <v-row>
      <v-col cols="3">
        <p>Rating:</p>
      </v-col>
      <v-col cols="6">
        <v-rating v-model="rating" hover color="yellow darken-3"></v-rating>
      </v-col>
    </v-row>

    <!-- Review -->
    <v-row>
      <v-col cols="8">
        <v-text-field label="Your review title (optional)" outlined v-model="review_title"></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8">
        <v-textarea label="Your review (optional)" outlined v-model="review"></v-textarea>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="9">
        <v-btn x-large color="#FFA726" dark @click="submit">Submit My Review</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AdvertisementDetail',
  components: {},
  data() {
    return {
      monthNames: [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
      ],
      booking_id: '',
      ad_id: '',
      resData: [],
      title: '',

      checkin: {
        date: '',
        month: '',
        year: ''
      },
      checkout: {
        date: '',
        month: '',
        year: ''
      },
      imgsrc: '',

      rating: 3,
      review_title: ' ',
      review: ' '
    };
  },

  created() {
    this.init();
  },

  methods: {
    async convertTime(from, to) {
      const checkIn = from.split('-');
      const checkOut = to.split('-');
      const date1 = await new Date(checkIn[2], checkIn[1], checkIn[0]);
      const date2 = await new Date(checkOut[2], checkOut[1], checkOut[0]);

      this.checkin.date = date1.getDate();
      this.checkin.month = this.monthNames[date1.getMonth() - 1];
      this.checkin.year = date1.getFullYear();

      this.checkout.date = date2.getDate();
      this.checkout.month = this.monthNames[date2.getMonth() - 1];
      this.checkout.year = date2.getFullYear();
    },

    async getAd() {
      const res = await this.$http.get(`${this.$api_hostname}/advertisement/${this.ad_id}`);
      this.imgsrc = this.$s3_hostname + res.data.photoURLs[0];
      this.title = res.data.title;
    },

    async parseInfo() {
      const from_date = this.resData.from;
      const to_date = this.resData.to;
      await this.convertTime(from_date, to_date);
      this.ad_id = this.resData.advertisementID;
      await this.getAd();
    },

    async init() {
      this.booking_id = this.$route.params.id;
      const res = await this.$http.get(`${this.$api_hostname}/getBooking/${this.booking_id}`);
      this.resData = res.data;
      await this.parseInfo();
    },

    async submit() {
      const reviewApi = `${this.$api_hostname}/review`;
      const reviewParams = {
        advertisementID: this.ad_id,
        bookingID: this.booking_id,
        rating: this.rating,
        review: this.review,
        reviewer: this.$store.state.user.signInUserSession.idToken.payload.email
      };
      console.log(reviewParams);
      await this.$http.post(reviewApi, reviewParams).then(
        (res) => {
          console.log('response', res);
          if (res.status !== 200) {
            this.errors.push('The request returned an error.');
          } else {
            this.$router.push({ path: '/mybookings' });
          }
        },
        (err) => {
          this.errors.push('There was an error sending the request.');
          console.log('failed request', err);
        }
      );
    }

  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Gotu&display=swap');
@import url('https://fonts.googleapis.com/css?family=Oswald&display=swap');
h2 {
  color: chocolate;
  font-size: 30px;
  font-family: 'Gotu', sans-serif;
}
.ad-title {
  color: chocolate;
  font-size: 24px;
  font-family: 'Oswald', sans-serif;
}
.ad-time {
  font-size: 18px;
  font-family: 'Oswald', sans-serif;
}
</style>
