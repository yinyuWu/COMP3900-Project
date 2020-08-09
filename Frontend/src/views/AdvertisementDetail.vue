<template>
  <v-container fluid>
    <!----------------------------------------------------------------------->
    <v-col cols="12">
      <v-tabs v-model="tab" background-color="transparent" grow color="amber darken-3">
        <v-tab v-for="item in tabToShow" :key="item.key">
          {{ item.name }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item key="1">
          <br />
          <v-sheet>
            <lingallery align="center" :items="photos" />
          </v-sheet>
        </v-tab-item>
        <v-tab-item v-show="has360" key="2">
          <br />
          <v-sheet height="600">
            <Pano v-for="s in photos_360" :source="s" :key="s"></Pano>
          </v-sheet>
        </v-tab-item>
      </v-tabs-items>
    </v-col>
    <!---------------------------------------------------------------------------->

    <v-card-title>{{ title }}</v-card-title>
    <v-row>
      <v-col cols="12" md="6">
        <v-card-text class="description">{{ description }} </v-card-text>
      </v-col>
      <v-col cols="12" md="6">
        <div class="rightCard" flat :key="$route.fullPath">
          <div class="myDivision">
            <div class="myTitle">Address:</div>
            <a target="_blank" class="content" v-bind:href="'https://maps.google.com/?q=' + address">{{ address }}</a>
          </div>
          <div class="myDivision">
            <div class="myTitle">Contact Owner:</div>
            <a class="content" v-bind:href="'mailto:' + owner">{{ owner }} </a>
          </div>

          <div class="myDivision">
            <div class="myTitle">Average rating:</div>
            <span class="content">
              <v-rating
                v-if="this.avgReview != -1"
                v-model="this.avgReview"
                background-color="orange lighten-3"
                color="orange"
                half-increments
                medium
                readonly
              ></v-rating>
              <v-rating
                v-if="this.avgReview == -1"
                v-model="this.avgReview"
                background-color="grey lighten-3"
                color="grey"
                half-increments
                medium
                readonly
              ></v-rating>
            </span>
          </div>

          <div v-if="showTotal" class="myDivision">
            <div class="myTitle">Dates:</div>
            <div class="content" style="padding-right: 20px">
              From: {{ checkIn.getDate() }}-{{ checkIn.getMonth() }}-{{ checkIn.getFullYear() }}
            </div>
            <div class="content">
              To: {{ checkOut.getDate() }}-{{ checkOut.getMonth() }}-{{ checkOut.getFullYear() }}
            </div>
          </div>
          <div class="myDivision">
            <div class="myTitle">Price:</div>
            <div v-if="showTotal" class="content">${{ rent }}/night x {{ nights }} nights = ${{ total }}</div>
            <div class="content" v-else>${{ rent }}/night</div>
          </div>
          <div v-if="showTotal" class="myDivision">
            <div class="myTitle" style="color: red;">Total:</div>
            <div class="content">{{ total }} $AUD</div>
          </div>
          <div  v-if="showDatePicker" class="myDivision">
            <div class="myTitle"> Availability: </div> 
              <div class="content" style="padding-right: 20px">
                  This property isn't available from {{ checkIn.getDate() }}-{{ checkIn.getMonth() }}-{{ checkIn.getFullYear() }} to {{ checkOut.getDate() }}-{{ checkOut.getMonth() }}-{{ checkOut.getFullYear() }}.
                  Choose different dates to book the accommodation.
                  <v-menu
                    ref="changeDateMenu"
                    v-model="changeDateModel"
                    :close-on-content-click="false"
                    :return-value.sync="selectedDates"
                    :nudge-top="20"
                    offset-y
                    max-width="50%"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field :value="selectedDates.join(' ')" label="Choose dates" readonly v-on="on" outlined></v-text-field>
                    </template>
                    <v-date-picker v-model="selectedDates" no-title scrollable range :allowed-dates="allowedDates" :min="today">
                      <v-spacer></v-spacer>
                      <v-btn text color="#F57C00" @click="changeDateModel = false">Cancel</v-btn>
                      <v-btn text color="#F57C00" @click="$refs.changeDateMenu.save(selectedDates)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
              </div>
            </div>
          </div>
          <v-card-actions>
            <v-btn width="100%" v-if="isOwner" dark color="amber darken-3" @click="editDetail()">Edit Detail</v-btn>
            <v-btn
              width="100%"
              v-if="!isOwner && isShowBook"
              dark
              large
              color="amber darken-3"
              @click="book()"
              :disabled="!availableToBook"
              >Book</v-btn
            >
          </v-card-actions>
 
      </v-col>
    </v-row>


    <!-- Review -->
    <h3 class="review-title">Reviews</h3>
    <v-row v-for="(r, index) in reviews" :key="index">
      <ReviewCard :title="r.reviewer" :text="r.review" :rating="r.rating" class="review-card"></ReviewCard>
    </v-row>
  </v-container>
</template>

<script>
import ReviewCard from '@/components/ReviewCard';
import { Auth } from 'aws-amplify';
import { Pano } from 'vuejs-vr';

export default {
  name: 'AdvertisementDetail',
  components: {
    ReviewCard,
    Pano
  },
  data() {
    return {
      tab: null,
      showPrice: false,
      checkIn: '',
      checkOut: '',
      changeDateModel: false,
      nights: '',
      total: 0,
      resData: [],
      title: '',
      rent: 0,
      description: '',
      city: '',
      aptNo: '',
      street: '',
      postcode: '',
      id: '',
      availableToBook: false,
      checkin: '',
      checkout: '',
      checkInDate: '',
      checkOutDate: '',
      availableDates: [],
      selectedDates: [],
      owner: '',
      userEmail: null,
      suburb: '',
      avgReview: -1,
      photos: [
        {
          src: 'http://via.placeholder.com/600x400.png',
          thumbnail: 'http://via.placeholder.com/64x64.png'
        }
      ],
      photos_360: [],
      address: '',
      imgsrc: '',
      keynum: 1,
      reviews: [],
      today: ''
    };
  },
  mounted() {
    this.today = this.$moment(Date.now()).format('YYYY-MM-DD')
  },
  computed: {
    showTotal() {
      console.log(this.availableToBook)
      return this.showPrice && this.availableToBook;
    },
    showDatePicker() {
      console.log(this.availableToBook)
      return this.showPrice && !this.availableToBook;
    },
    isOwner() {
      if (this.isSignedIn) {
        return this.userEmail === this.owner;
      }
      return false;
    },
    isShowBook() {
      return this.showPrice && this.isSignedIn;
    },
    isSignedIn() {
      return !!this.$store.state.user;
    },
    has360() {
      return this.photos_360.length > 0;
    },
    tabToShow() {
      if (this.has360) {
        return [
          {
            key: 1,
            name: 'Gallery'
          },
          {
            key: 2,
            name: '360'
          }
        ];
      }
      return [
        {
          key: 1,
          name: 'Gallery'
        }
      ];
    }
  },

  async beforeUpdate() {
    const usr = await Auth.currentAuthenticatedUser();
    this.userEmail = usr.attributes.email;
  },

  async created() {
    this.init(true);
    const usr = await Auth.currentAuthenticatedUser();
    this.userEmail = usr.attributes.email;
  },

  methods: {
    async init(firstTime) {
      this.id = this.$route.params.id;
      this.checkin = this.$route.query.checkin || '';
      this.checkout = this.$route.query.checkout || '';
      const params = {
        checkin: this.checkin,
        checkout: this.checkout
      };
      // compute number of nights
      if (this.checkin) {
        this.showPrice = true;
        const oneDay = 24 * 60 * 60 * 1000;
        this.checkIn = this.$route.query.checkin.split('-');
        this.checkOut = this.$route.query.checkout.split('-');
        const date1 = new Date(this.checkIn[2], this.checkIn[1], this.checkIn[0]);
        const date2 = new Date(this.checkOut[2], this.checkOut[1], this.checkOut[0]);
        this.nights = Math.round(Math.abs((date1 - date2) / oneDay));
        this.checkIn = date1;
        this.checkOut = date2;
      }

      const res = await this.$http.get(`${this.$api_hostname}/advertisement/${this.$route.params.id}`, { params });

      console.log(params);
      console.log(res.data);

      this.resData = res.data;
      this.owner = this.resData.owner;
      this.title = this.resData.title;
      this.rent = this.resData.rent;
      // this.description = this.resData.description.split('\n');
      this.description = this.resData.description;
      this.aptNo = this.resData.aptNo;
      this.street = this.resData.street;
      this.postcode = this.resData.postcode;
      this.city = this.resData.city;
      this.suburb = this.resData.suburb;
      this.avgReview = this.resData.averageReview;
      this.address =
        this.aptNo == null
          ? `${this.street} , ${this.suburb} , ${this.city}`
          : `${this.aptNo} ${this.street} ${this.city}`;
      this.availableToBook = (this.resData.availableToBook && (this.checkin != this.checkout)) || false;
      console.log(this.resData.availableToBook && (this.checkIn != this.checkOut))
      console.log(this.checkIn, this.checkOut)
      

      this.total = this.nights * this.rent;
      if (firstTime) {
        if (this.resData['360PhotoURLs'] != null) {
          for (let i = 0; i < this.resData['360PhotoURLs'].length; i += 1) {
            this.photos_360.push(this.$s3_hostname + this.resData['360PhotoURLs'][i]);
          }
        }
        if (this.resData.photoURLs.length > 0) {
          for (let i = 0; i < this.resData.photoURLs.length; i += 1) {
            const url = this.$s3_hostname + this.resData.photoURLs[i];
            this.photos.push({
              src: url,
              thumbnail: url
            });
          }
        }
        this.photos.shift();

        // get reviews
        const reviewRes = await this.$http.get(`${this.$api_hostname}/reviews/${this.$route.params.id}`);
        this.reviews = reviewRes.data;
        for (const date in this.resData.availability) {
          if (this.resData.availability[date]) {
            this.availableDates.push(this.formatDateForDatePicker(date));
          }
        }
      }
    },
    async book() {
      const body = {
        advertisementID: this.id,
        from: this.checkin,
        to: this.checkout,
        email: this.$store.state.user.signInUserSession.idToken.payload.email
      };
      const res = await this.$http.post(`${this.$api_hostname}/booking`, body);
      this.$router.push({
        name: 'MyBookings'
      });
      console.log(res.data);
    },
    editDetail() {
      this.$router.push(`/editDetail/${this.id}`);
    },
    formatDateForAPI(date) {
      return this.$moment(date, 'YYYY-MM-DD').format('DD-MM-YYYY');
    },
    formatDateForDatePicker(date) {
      return this.$moment(date, 'DD-MM-YYYY').format('YYYY-MM-DD');
    },
    allowedDates(val) {
      return this.availableDates.indexOf(val) >= 0;
    },
    sortSelectedDates() {
      if (this.selectedDates.length != 2) {
        return this.selectedDates;
      }
      let firstDate = new Date(this.selectedDates[0])
      let secondDate = new Date(this.selectedDates[1])
      if (secondDate < firstDate) {
        this.selectedDates.reverse()
      }
      return this.selectedDates;
    }
  },
  watch: {
    selectedDates() {
      if (this.selectedDates.length == 2) {
        this.sortSelectedDates();
        console.log('sorted', this.selectedDates)
        const url = `/detail/${this.id}`;
        this.$router.push({
          name: 'AdvertisementDetail',
          params: { id: this.id },
          query: {
            checkin: this.formatDateForAPI(this.selectedDates[0]),
            checkout: this.formatDateForAPI(this.selectedDates[1])
          }
        });
        this.init(false);
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Gotu&display=swap');


.card-desc {
  overflow: scroll;
}

.review-card {
  border: none !important;
  overflow: scroll;
  height: 10rem;
  width: 100%;
}

.content {
  padding: 0;
  margin: 0;
  font-size: 1em;
  display: inline-block;
}

.myTitle {
  padding: 0;
  margin: 0;
  font-size: 1.2em;
  display: inline-block;
  padding-right: 20px;
  font-style: italic;
}

.description {
  text-align: justify;
  margin-top: 0;
}

.v-card__text {
  margin-top: 0;
  padding-top: 0;
}

.v-card__title {
  margin-bottom: 0;
  padding-bottom: 0;
}

.rightCard {
  display: inline-block;
  width: 100%;
}

.myDivision {
  padding-bottom: 10px;
  padding-left: 15px;
}

.review-title {
  margin-top: 4em;
  font-size: 30px;
  font-family: 'Gotu', sans-serif;
}
</style>
