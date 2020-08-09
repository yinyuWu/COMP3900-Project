<template>
  <v-container>
    <AccommodationSlideshow />
    <SearchBar />
    <h1 v-if="isRecommendations" class="recommendationTitle">Book for Tonight</h1>
    <v-row no-gutters>
      <v-col class="mt-6" cols="12" md="3" sm="6" v-for="(hit, i) in Advertisements" :key="i">
        <RecomCard v-bind="hit"></RecomCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SearchBar from '@/components/SearchBar';
import AccommodationSlideshow from '@/components/AccommodationSlideshow';
import RecomCard from '@/components/RecomCard';
import ReviewCard from '@/components/ReviewCard';

export default {
  name: 'Home',
  components: {
    SearchBar,
    AccommodationSlideshow,
    RecomCard,
    ReviewCard
  },

  data() {
    return {
      AdvertisementsIDs: [],
      Advertisements: [],
      numberOfAds: 0
    };
  },

  computed: {
    isRecommendations: function() {
      if (this.numberOfAds > 0) {
        return true;
      } else {
        return false;
      }
    }
  },

  created() {
    this.getTonightRecommendations();
  },

  methods: {
    getPhoto(images) {
      return `${this.$s3_hostname}${images[0]}`;
    },
    async getTonightRecommendations() {
      var today = this.$moment(Date.now()).format('YYYY-MM-DD');
      var tomorrow = new Date(Date.now());
      tomorrow.setDate(tomorrow.getDate() + 1);
      tomorrow = this.$moment(tomorrow).format('YYYY-MM-DD');

      let checkIn = this.formatDateForAPI(today);
      let checkOut = this.formatDateForAPI(tomorrow);
      let sortType = 'Best rated';
      let page = 0;
      let city = '';

      let numberOfpages = 1;

      var n;
      for (n = 0; n < numberOfpages; n++) {
        await this.$http
          .post(`${this.$api_hostname}/search`, {
            city: city,
            checkin: checkIn,
            checkout: checkOut,
            page: page,
            sortType: sortType
          })
          .then((response) => {
            numberOfpages = response.data.nbPages;
            for (var i in response.data.hits_response) {
              if (response.data.hits_response[i].ok == true) {
                var Ad = {};
                Ad['title'] = response.data.hits_response[i].title;
                Ad['image'] = this.getPhoto(response.data.hits_response[i].images);
                Ad['rating'] = response.data.hits_response[i].rating;
                Ad['id'] = response.data.hits_response[i].objectID;
                Ad['checkIn'] = checkIn;
                Ad['checkOut'] = checkOut;
                this.Advertisements.push(Ad);
                this.numberOfAds += 1;
                if (this.numberOfAds == 4) {
                  break;
                }
              }
            }
          })
          .catch((error) => {
            console.log(error);
          });
        if (this.numberOfAds == 4) {
          break;
        }
      }
    },
    formatDateForAPI(date) {
      return this.$moment(date, 'YYYY-MM-DD').format('DD-MM-YYYY');
    }
  }
};
</script>

<style scoped>
.recommendationTitle {
  text-align: center;
  padding-bottom: 5px;
  font-size: 1.8em;
  font-weight: normal;
}
</style>
