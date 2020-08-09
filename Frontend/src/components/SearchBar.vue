<template>
  <v-row>
    <!-- input location -->
    <v-col cols="12" sm="4">
      <v-combobox
        v-model="destination"
        :loading="isLoading"
        :items="items"
        :search-input.sync="search"
        cache-items
        outlined
        hide-no-data
        label="Where are you going?"
        prepend-inner-icon="mdi-magnify"
        placeholder="Suburb, City"
        return-object
      ></v-combobox>
    </v-col>
    <!-- check in  -->
    <v-col cols="12" sm="2">
      <v-menu
        ref="checkInMenu"
        v-model="checkIn"
        :close-on-content-click="false"
        :return-value.sync="checkInDate"
        :nudge-top="20"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field :value="checkInFormatted" label="Check-In" readonly v-on="on" outlined></v-text-field>
        </template>
        <v-date-picker v-model="checkInDate" no-title scrollable :min="today">
          <v-spacer></v-spacer>
          <v-btn text color="#F57C00" @click="checkIn = false">Cancel</v-btn>
          <v-btn text color="#F57C00" @click="$refs.checkInMenu.save(checkInDate)">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <!-- check out -->
    <v-col cols="12" sm="2">
      <v-menu
        ref="checkOutMenu"
        v-model="checkOut"
        :close-on-content-click="false"
        :return-value.sync="checkOutDate"
        :nudge-top="20"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field :value="checkOutFormatted" label="Check-out" readonly v-on="on" outlined></v-text-field>
        </template>
        <v-date-picker v-model="checkOutDate" no-title scrollable :min="tomorrow">
          <v-spacer></v-spacer>
          <v-btn text color="#F57C00" @click="checkOut = false">Cancel</v-btn>
          <v-btn text color="#F57C00" @click="$refs.checkOutMenu.save(checkOutDate)">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <v-col cols="12" sm="2">
      <v-select v-model="sortType" :items="sortTypeItems" label="Sort by" outlined> </v-select>
    </v-col>
    <v-col cols="12" sm="2">
      <v-btn dark height="54px" block color="amber darken-3" @click="handle">Search</v-btn>
    </v-col>
  </v-row>
</template>

<script>
import algoliasearch from 'algoliasearch';

export default {
  data: () => ({
    checkInDate: '',
    checkOutDate: '',
    checkIn: false,
    checkOut: false,
    destination: '',
    today: '',
    tomorrow: '',
    isLoading: false,
    items: [],
    search: null,
    sortType: 'Best match',
    sortTypeItems: ['Best match', 'Best rated', 'Cheapest']
  }),

  props: {
    destinationProp: { type: String, default: '' },
    sortTypeProp: { type: String, default: '' },
    checkInDateProp: { type: String, default: '' },
    checkOutDateProp: { type: String, default: '' }
  },

  created() {
    const currentDate = new Date();
    this.checkInDate = this.$moment(currentDate)
      .toISOString(true)
      .substr(0, 10);
    currentDate.setDate(currentDate.getDate() + 1);
    this.checkOutDate = this.$moment(currentDate)
      .toISOString(true)
      .substr(0, 10);

    this.destination = this.destinationProp;
    if (this.sortTypeProp != '') {
      this.sortType = this.sortTypeProp;
    }

    if (this.checkInDateProp != '') {
      this.checkInDate = this.checkInDateProp;
    }
    if (this.checkOutDateProp != '') {
      this.checkOutDate = this.checkOutDateProp;
    }
  },

  mounted() {
    this.today = this.$moment(Date.now()).format('YYYY-MM-DD');
    this.tomorrow = new Date(Date.now());
    this.tomorrow.setDate(this.tomorrow.getDate() + 1);
    this.tomorrow = this.$moment(this.tomorrow).format('YYYY-MM-DD');
  },

  methods: {
    formatDateForAPI(date) {
      return this.$moment(date, 'YYYY-MM-DD').format('DD-MM-YYYY');
    },
    handle() {
      console.log(this.formatDateForAPI(this.checkInDate));
      console.log(this.formatDateForAPI(this.checkOutDate));
      console.log('Go', this.destination);
      const checkin = new Date(this.checkInDate);
      const checkout = new Date(this.checkOutDate);
      if (checkin >= checkout) {
        alert('Please choose other dates');
      } else if (!this.destination) {
        alert('Please enter the destination');
      } else {
        this.$router
          .push({
            path: 'search',
            query: {
              destination: this.destination,
              checkin: this.formatDateForAPI(this.checkInDate),
              checkout: this.formatDateForAPI(this.checkOutDate),
              sortType: this.sortType
            }
          })
          .catch((err) => {});
      }
    }
  },
  computed: {
    checkInFormatted() {
      return this.checkInDate ? this.formatDateForAPI(this.checkInDate) : '';
    },

    checkOutFormatted() {
      return this.checkOutDate ? this.formatDateForAPI(this.checkOutDate) : '';
    }
  },
  watch: {
    // these two functions make sure that the checkin date in before the checkout date upon date selection changes.
    checkInDate() {
      const checkin = new Date(this.checkInDate);
      let checkout = new Date(this.checkOutDate);
      if (checkin >= checkout) {
        checkout = new Date(checkin.setDate(checkin.getDate() + 1));
        this.checkOutDate = this.$moment(checkout).format('YYYY-MM-DD');
      }
    },
    checkOutDate() {
      let checkin = new Date(this.checkInDate);
      const checkout = new Date(this.checkOutDate);
      if (checkin >= checkout) {
        checkin = new Date(checkout.setDate(checkout.getDate() - 1));
        this.checkInDate = this.$moment(checkin).format('YYYY-MM-DD');
      }
    },
    search(val) {
      // Items have already been loaded

      if (val === '') {
        this.items = [];
        return;
      }

      if (this.isLoading) return;

      this.isLoading = true;
      const client = algoliasearch('LDOJL787U6', '806ce69c538faebcd93876b815ef996c');
      const index = client.initIndex('searchResults');
      const searchResults = [];
      index.search(val).then(({ hits }) => {
        let hit;
        // eslint-disable-next-line no-restricted-syntax
        for (hit of hits) {
          const { suburb } = hit;
          const { city } = hit;
          const suburbCityString = suburb.concat(', ').concat(city);
          searchResults.push(suburbCityString);
        }
      });
      this.items = searchResults;
      this.isLoading = false;
    }
  }
};
</script>

<style>
div.v-input__control div.v-text-field__details {
  display: none !important;
}
</style>
