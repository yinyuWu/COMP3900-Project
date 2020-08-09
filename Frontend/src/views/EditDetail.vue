<template>
  <div>
    <h2
      class="display-1"
      align="center"
      style="margin: 80px 50px; text-transform:capitalize;"
    >Details of your accommodation</h2>
    <v-container fluid :class="{ 'my-width': $vuetify.breakpoint.mdAndUp}">
      <v-row>
        <v-col cols="8">
          <h3 class="title">Title</h3>
        </v-col>
        <v-col cols="4">
          <h3 class="title">Rent</h3>
        </v-col>
        <v-col cols="8">
          <v-text-field outlined v-model="title" label="Accommodation Title" />
        </v-col>
        <v-col cols="4">
          <v-text-field outlined v-model="rent" label="$ per Night" />
        </v-col>
        <v-col cols="12">
          <h3 class="title">Description</h3>
        </v-col>
        <v-col cols="12">
          <v-textarea outlined v-model="description" label="Description" />
        </v-col>
        <v-col cols="12">
          <h3 class="title">Accommodation Availability</h3>
        </v-col>
        <v-col cols="12" sm="6">
          <v-row justify="center">
            <v-date-picker
              color="amber darken-3"
              v-model="dates"
              multiple
              :min="today"
              :allowed-dates="allowedDates"
            ></v-date-picker>
          </v-row>
        </v-col>
        <v-col cols="12" sm="6">
          <v-menu
            ref="menu"
            v-model="menu"
            :disabled="true"
            :close-on-content-click="false"
            :return-value.sync="dates"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-combobox
                v-model="dates"
                color="amber darken-3"
                multiple
                chips
                small-chips
                label="Selected dates"
                readonly
                v-on="on"
              ></v-combobox>
            </template>
            <v-date-picker v-model="dates" multiple no-title scrollable>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
              <v-btn text color="primary" @click="$refs.menu.save(dates)">OK</v-btn>
            </v-date-picker>
          </v-menu>
        </v-col>
      </v-row>
      <h3 class="title">Address of Your accommodation</h3>
      <v-text-field v-model="street" outlined label="Street Address" required />
      <v-text-field v-model="aptNo" outlined label="Apt, Suite. (optional)" />
      <v-text-field v-model="city" outlined label="City" required />
      <v-text-field v-model="suburb" outlined label="Suburb" required />
      <v-text-field v-model="postcode" outlined label="Postcode" required />
      <h3 class="title">Photos of your accommodation</h3>
      <p>
        Photos help guests know what your place is like. You can add multiple photos.
      </p>
      <file-pond
        name="pond"
        ref="pond"
        :allow-multiple="true"
        accepted-file-types="image/png,image/jpeg"
        :allowImageResize="true"
        maxFileSize="3MB"
        :imageResizeTargetHeight="300"
        :server="server"
      />
      <h3 class="title">360 image of your accommodation (optional)</h3>
      <p>
        Photos help guests know what your place is like. You can add one photo only. 
      </p>
      <file-pond
        name="pond360"
        ref="pond360"
        :allow-multiple="false"
        accepted-file-types="image/jpeg"
        :allowImageResize="true"
        maxFileSize="4MB"
        maxFiles="1"
        :imageResizeTargetHeight="300"
        :server="server360"
      />
      <v-row justify="end">
        <v-col sm="6" md="3">
          <v-btn @click="deleteAd()" dark block color="amber darken-3">Delete</v-btn>
        </v-col>
        <v-col sm="6" md="3">
          <v-btn @click="saveAd()" dark block color="amber darken-3">Save Change</v-btn>
        </v-col>
      </v-row>
      <v-row v-if="errors.length">
        <b>Please correct the following error(s):</b>
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </v-row>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable */
/* eslint-disable consistent-return */
// Import Vue FilePond
import vueFilePond from 'vue-filepond';

// Import FilePond styles
import 'filepond/dist/filepond.min.css';

// Import FilePond plugins
// Please note that you need to install these plugins separately

// Import image preview plugin styles
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css';

// Import image preview and file type validation plugins
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import FilePondPluginFileValidateSize from 'filepond-plugin-file-validate-size';
import FilePondPluginImageResize from 'filepond-plugin-image-resize';

// Create component
const FilePond = vueFilePond(
  FilePondPluginFileValidateType,
  FilePondPluginImagePreview,
  FilePondPluginFileValidateSize,
  FilePondPluginImageResize
);
export default {
  name: 'Create',
  components: {},
  data() {
    return {
      errors: [],
      myFiles: [],
      resData: [],
      title: '',
      rent: 0,
      description: '',
      city: '',
      aptNo: '',
      street: '',
      suburb: '',
      postcode: '',
      photoURLs: [],
      '360PhotoURLs': [],
      owner: '',
      id: '',
      menu: false,
      dates: [],
      availability: {},
      alreadyBookDates: [],
      today: this.$moment(Date.now()).format('YYYY-MM-DD'),
      server: {
        url: `${this.$api_hostname}/image`,
        process: (fieldName, file, metadata, load, error, progress, abort, transfer, options) => {
          if (this.photoURLs.indexOf(file.name) >= 0) {
            load(file.name);
            return;
          }
          const request = new XMLHttpRequest();
          const reader = new FileReader();

          reader.onload = (event) => {
            const image_encode64string = event.target.result;
            request.open('POST', `${this.$api_hostname}/image`);
            const json = JSON.stringify(image_encode64string);
            request.send(json);
          };
          reader.readAsDataURL(file);

          request.upload.onprogress = (e) => {
            progress(e.lengthComputable, e.loaded, e.total);
          };

          request.onload = function() {
            if (request.status >= 200 && request.status < 300) {
              load(request.responseText);
            } else {
              error('file upload error');
            }
          };

          return {
            abort: () => {
              request.abort();
              abort();
            }
          };
        }
      },
      server360: {
        url: `${this.$api_hostname}/image`,
        process: (fieldName, file, metadata, load, error, progress, abort, transfer, options) => {
          if (this['360PhotoURLs'].indexOf(file.name) >= 0) {
            load(file.name);
            return;
          }

          const request = new XMLHttpRequest();
          const reader = new FileReader();

          reader.onload = (event) => {
            const image_encode64string = event.target.result;
            request.open('POST', `${this.$api_hostname}/image`);
            const json = JSON.stringify(image_encode64string);
            console.log('seneindg request', json);
            request.send(json);
          };
          reader.readAsDataURL(file);

          request.upload.onprogress = (e) => {
            progress(e.lengthComputable, e.loaded, e.total);
          };

          request.onload = function() {
            if (request.status >= 200 && request.status < 300) {
              load(request.responseText);
            } else {
              error('file upload error');
            }
          };

          return {
            abort: () => {
              request.abort();
              abort();
            }
          };
        }
      }
    };
  },

  created() {
    this.init();
  },
  methods: {
    async init() {
      this.id = this.$route.params.id;
      this.owner = this.$store.state.user.signInUserSession.idToken.payload.email;

      const res = await this.$http.get(`${this.$api_hostname}/advertisement/${this.id}`);
      this.resData = res.data;
      console.log(res.data);
      this.title = this.resData.title;
      this.rent = this.resData.rent;
      this.description = this.resData.description;
      this.aptNo = this.resData.aptNo;
      this.street = this.resData.street;
      this.postcode = this.resData.postcode;
      this.city = this.resData.city;
      this.suburb = this.resData.suburb;
      this.photoURLs = this.resData.photoURLs;
      this['360PhotoURLs'] = this.resData['360PhotoURLs'];

      this.photoURLs.forEach((url) => {
        this.$http.get(this.$s3_hostname + url, { responseType: 'blob' }).then((res) => {
          const blob_image = res.data;
          blob_image.name = url;
          this.$refs.pond.addFile(blob_image);
        });
      });
      this['360PhotoURLs'].forEach((url) => {
        this.$http.get(this.$s3_hostname + url, { responseType: 'blob' }).then((res) => {
          const blob_image = res.data;
          blob_image.name = url;
          this.$refs.pond360.addFile(blob_image);
        });
      });

      for (const date in this.resData.availability) {
        if (this.resData.availability[date]) {
          this.dates.push(this.$moment(date, 'DD-MM-YYYY').format('YYYY-MM-DD'));
          this.availability[date] = false;
        } else {
          this.alreadyBookDates.push(this.$moment(date, 'DD-MM-YYYY').format('YYYY-MM-DD'));
        }
      }
    },

    async deleteAd() {
      if (confirm('Are you sure you want to delete this advertisement')) {
        const res = await this.$http.delete(`${this.$api_hostname}/advertisement/${this.id}`);
        this.$router.push('/advertisements');
        console.log(res);
      }
    },

    async saveAd() {
      if (this.validateData() === false) {
        alert('Error');
        return;
      }
      if (confirm('Are you sure you want to save the change')) {
        const change_date = this.dates.map((date) => this.$moment(date).format('DD-MM-YYYY'));
        change_date.forEach((date) => (this.availability[date] = true));
        // image handler

        const photoURLs = [];
        const _360PhotoURLs = [];
        this.$refs.pond.getFiles().forEach((file) => {
          if (file.serverId) photoURLs.push(file.serverId);
        });
        this.$refs.pond360.getFiles().forEach((file) => {
          if (file.serverId) _360PhotoURLs.push(file.serverId);
        });
        const params = {
          id: this.id,
          title: this.title,
          rent: parseInt(this.rent),
          description: this.description,
          city: this.city,
          aptNo: this.aptNo,
          street: this.street,
          suburb: this.suburb,
          postcode: this.postcode,
          owner: this.owner,
          availability: this.availability,
          photoURLs,
          '360PhotoURLs': _360PhotoURLs
        };

        const res = await this.$http.put(`${this.$api_hostname}/advertisement`, params);
        console.log(res.data);
        this.$router.push('/advertisements');
      }
    },
    validateData() {
      this.errors = [];

      if (!this.title) {
        this.errors.push('Accommodation title required.');
      }
      if (this.rent <= 0) {
        this.errors.push('Rent must be valid number');
      }
      if (!this.description) {
        this.errors.push('Description required');
      }
      if (!this.street || !this.postcode || !this.city || !this.suburb) {
        this.errors.push('Address required');
      }
      if (this.$refs.pond.getFiles().length + this.$refs.pond360.getFiles().length < 1) {
        this.errors.push('Upload a photo of your accommodation');
      }
      if (
        this.$refs.pond.getFiles().filter((x) => x.status !== 5).length !== 0 ||
        this.$refs.pond360.getFiles().filter((x) => x.status !== 5).length !== 0
      ) {
        console.log(this.$refs.pond.getFiles().map((x) => x.status));
        this.errors.push('Wait until files have finished uploading');
      }

      if (!this.errors.length) {
        return true;
      }
      return false;
    },
    allowedDates(val) {
      return this.alreadyBookDates.indexOf(val) < 0;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* @media (min-width: 30em) {
  .filepond--item {
    width: calc(50% - 0.5em);
  }
} */
</style>
<style scoped>
.my-width {
  width: 60% !important;
}
</style>
