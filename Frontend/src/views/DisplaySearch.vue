<template>
  <div>
    <SearchBar :destinationProp= "destination" :sortTypeProp= "sortType" :checkInDateProp="checkInDate" :checkOutDateProp="checkOutDate"/>
    <v-text-field v-if="loading" color="amber darken-3" loading disabled></v-text-field>
    <!-- <v-progress-circular v-if="loading" color="amber darken-3" size="100" indeterminate /> -->
    <v-alert type="info" v-if="post.length == 0 && this.isSearch == true">No results found</v-alert>
    <div if="post">
      <template v-for="(hit, i) in post">
        <SearchCard v-bind="hit" :key="i" />
      </template>
    </div>
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar';
import SearchCard from '@/components/SearchCard';

export default {
  name: 'DisplaySearch',
  components: { SearchBar, SearchCard },
  created() {
    if (this.$route.query.destination != null) {
      this.destination = this.$route.query.destination;
      this.sortType = this.$route.query.sortType;
      this.checkInDate = this.$moment(this.$route.query.checkin, 'DD-MM-YYYY').format('YYYY-MM-DD');
      this.checkOutDate = this.$moment(this.$route.query.checkout, 'DD-MM-YYYY').format('YYYY-MM-DD');
      this.fetchData();
    }
    window.addEventListener('scroll', () => {
      this.bottom = this.bottomVisible();
    });
  },

  data() {
    return {
      loading: false,
      post: [],
      error: null,
      bottom: false,
      page: 0,
      nbPages: Infinity,
      isSearch: false,
      destination: '',
      sortType: '',
      checkInDate: '',
      checkOutDate: '',
    };
  },

  watch: {
    $route: 'fetchData',
    bottom(bottom) {
      if (bottom && this.page < this.nbPages) {
        console.log('Hit bottom');
        this.scrollData();
      }
    }
  },
  methods: {
    async fetchData() {
      this.isSearch = false;
      this.post = [];
      this.page = 0;
      this.scrollData();
    },
    bottomVisible() {
      const { scrollY } = window;
      const visible = document.documentElement.clientHeight;
      const pageHeight = document.documentElement.scrollHeight;
      const bottomOfPage = visible + scrollY >= pageHeight;
      return bottomOfPage || pageHeight < visible;
    },
    async scrollData() {
      this.error = null;
      // this.post = null;
      this.loading = true;
      await this.$http
        .post(`${this.$api_hostname}/search`, {
          // suburb: 'temp',
          city: this.$route.query.destination,
          checkin: this.$route.query.checkin,
          checkout: this.$route.query.checkout,
          page: this.page,
          sortType: this.$route.query.sortType
        })
        .then((response) => {
          this.nbPages = response.data.nbPages;
          if (this.nbPages == null) {
            this.loading = false;
            this.isSearch = true;
            return;
          }

          this.post = { ...this.post, ...response.data.hits_response };
          
          this.loading = false;
          this.page += 1;
        })
        .catch((error) => {
          console.log(error);
          this.error = error;
        });
    },
    compareData(a, b) {
      const rating1 = a.rating;
      const rating2 = b.rating;

      if (rating1 > rating2) {
        return -1;
      }

      return 1;
    }
  }
};
</script>

<style></style>
