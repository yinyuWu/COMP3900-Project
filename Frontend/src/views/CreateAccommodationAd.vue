<template>
  <div>
    <h2 class="display-1" align="center" style="margin: 80px 50px; text-transform:capitalize;">Let's get started listing your accommodation</h2>
    <v-form v-model="valid" ref="form" :lazy-validation="false">
      <v-container fluid :class="{'my-width': $vuetify.breakpoint.mdAndUp}">
        <!-- Step 1 -->
        <v-row>
          <v-col cols="12">
            <h3 class="title">STEP 1: Tell us about your accommodation</h3>
          </v-col>
          <v-col cols="8">
            <v-text-field outlined v-model="title" :rules="string" label="Accommodation Title" />
          </v-col>
          <v-col cols="4">
            <v-text-field outlined v-model="rent" :rules="number" label="$ per Night" />
          </v-col>
          <v-col cols="12">
            <v-textarea outlined v-model="description" :rules="string" label="Description" />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <h3 class="title">STEP 2: Tell us what dates the accommodation will be available</h3>
          </v-col>
          <v-col cols="12" sm="6">
            <v-row justify="center">
              <v-date-picker color="amber darken-3" v-model="dates" multiple :min="today"></v-date-picker>
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
        <!-- <v-row>
          {{ today }}
          {{ dates }}
        </v-row> -->
        <h3 class="title">STEP 3: Where is your NSW accommodation located?</h3>
        <v-text-field outlined label="Street Address" :rules="string" v-model="address.street" />
        <v-text-field outlined label="Apt, Suite. (optional)" v-model="address.aptNo" />
        <v-text-field outlined label="Suburb" :rules="string" v-model="address.suburb" />
        <v-text-field outlined label="City" :rules="string" v-model="address.city" />
        <v-text-field outlined label="Postcode" :rules="string" v-model="address.postcode" />
        <h3 class="title">STEP 4: Add photos of your accommodation</h3>
        <p>
          Photos help guests know what your place is like. You can start with one and add more after you publish your
          advertisement.
        </p>
        <!-- <input
            multiple="multiple"
            label="Upload image"
            type="file"
            ref="file"
            accept="image/*"
            @change="handleFileUpload()"
          />-->
        <file-pond
          name="pond"
          ref="pond"
          :allow-multiple="true"
          accepted-file-types="image/jpeg"
          :allowImageResize="true"
          maxFileSize="3MB"
          :imageResizeTargetHeight="300"
          :server="server"
        />

        <h3 class="title">STEP 5: Add a 360 panoramic image of your accommodation (optional)</h3>
        <p>
          Photos help guests know what your place is like. You can add one after you publish your
          advertisement.
        </p>
        <!-- <input
            label="Upload 360 image"
            type="file"
            ref="file360"
            accept="image/*"
            @change="handleFileUpload()"
          />-->
        <file-pond
          name="pond360"
          ref="pond360"
          :allow-multiple="false"
          accepted-file-types="image/png,image/jpeg"
          :allowImageResize="true"
          maxFileSize="3MB"
          maxFiles="1"
          :imageResizeTargetHeight="300"
          :server="server360"
        />

        <v-row v-if="errors.length">
          <b>Please correct the following error(s):</b>
          <ul>
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
          </ul>
        </v-row>
        <v-row justify="end">
          <v-col sm="12" md="3">
            <v-btn block dark color="amber darken-3" v-on:click="submit">Submit</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script>
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

import { Auth } from 'aws-amplify';
// Create component
const FilePond = vueFilePond(
  FilePondPluginFileValidateType,
  FilePondPluginImagePreview,
  FilePondPluginFileValidateSize,
  FilePondPluginImageResize
);

const { uuid } = require('uuidv4');
const aws = require('aws-sdk');
const axios = require('axios');

export default {
  name: 'CreateAccommodationAd',
  created() {
    this.uuid = uuid();
  },
  data() {
    return {
      valid: true,
      title: '',
      rent: 0,
      description: '',
      address: {
        street: '',
        aptNo: '',
        suburb: '',
        city: '',
        postcode: ''
      },
      photoURLs: [],
      '360PhotoURLs': [],
      errors: [],
      string: [(v) => !!v || 'Required'],
      number: [(v) => v > 0 || 'Invalid number'],
      dates: [],
      menu: false,
      today: this.$moment(Date.now()).format('YYYY-MM-DD'),
      uuid: '',
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
            const imageEncode64String = event.target.result;
            request.open('POST', `${this.$api_hostname}/image`);
            const json = JSON.stringify(imageEncode64String);
            request.send(json);
          };
          reader.readAsDataURL(file);

          request.upload.onprogress = (e) => {
            progress(e.lengthComputable, e.loaded, e.total);
          };

          // eslint-disable-next-line func-names
          request.onload = function () {
            if (request.status >= 200 && request.status < 300) {
              load(request.responseText);
            } else {
              error('file upload error');
            }
          };

          // eslint-disable-next-line consistent-return
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
            const imageEncode64String = event.target.result;
            request.open('POST', `${this.$api_hostname}/image`);
            const json = JSON.stringify(imageEncode64String);
            request.send(json);
          };
          reader.readAsDataURL(file);

          request.upload.onprogress = (e) => {
            progress(e.lengthComputable, e.loaded, e.total);
          };

          // eslint-disable-next-line func-names
          request.onload = function () {
            console.log(request);
            if (request.status >= 200 && request.status < 300) {
              load(request.responseText);
            } else {
              error('file upload error');
            }
          };

          // eslint-disable-next-line consistent-return
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
  methods: {
    async submit(event) {
      if (this.validateData() === false) {
        return;
      }
      const advertisementAPI = `${this.$api_hostname}/advertisement`;
      const key = uuid();
      const user = await Auth.currentAuthenticatedUser();
      this.dates.sort();
      this.dates = this.dates.map((date) => this.$moment(date).format('DD-MM-YYYY'));
      const photos = [];
      const photoURLs = [];
      this.$refs.pond.getFiles().forEach((file) => {
        if (file.serverId) photos.push(file.serverId);
      });
      this.$refs.pond360.getFiles().forEach((file) => {
        if (file.serverId) photoURLs.push(file.serverId);
      });
      console.log(photos, photoURLs);
      const advertisementParams = {
        owner: user.attributes.email,
        title: this.title,
        rent: parseInt(this.rent),
        description: this.description,
        photoURLs: photos,
        '360PhotoURLs': photoURLs,
        street: this.address.street,
        aptNo: this.address.aptNo,
        suburb: this.address.suburb,
        city: this.address.city,
        postcode: this.address.postcode,
        availability: this.dates
      };
      const vm = this;
      await axios.post(advertisementAPI, advertisementParams).then(
        (resp) => {
          console.log('response', resp);
          if (resp.status !== 200) {
            vm.errors.push('The request returned an error.');
          } else {
            vm.$router.push({ path: `/detail/${resp.data.ID}` });
          }
        },
        (err) => {
          vm.errors.push('There was an error sending the request.');
          console.log('failed request', err);
        }
      );
    },
    setToday() {
      let today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const yyyy = today.getFullYear();

      today = `${yyyy}-${mm}-${dd}`;
      this.today = today;
      return today;
    },
    async handleFileUpload() {
      if (this.$refs.file.files.length > 0) {
        for (let i = 0; i < this.$refs.file.files.length; i += 1) {
          this.createImage(this.$refs.file.files[i], true);
        }
      }
      if (this.$refs.file360.files.length > 0) {
        for (let i = 0; i < this.$refs.file.files.length; i += 1) {
          this.createImage(this.$refs.file360.files[i], false);
        }
      }
    },
    createImage(file, normalImage = true) {
      const reader = new FileReader();
      const vm = this;
      reader.onload = () => {
        if (normalImage === true) {
          vm.file.push([reader.result][0]);
        } else {
          vm.file360.push([reader.result][0]);
        }
      };
      // eslint-disable-next-line func-names
      reader.onerror = function (error) {
        console.log('Error: ', error);
      };
      reader.readAsDataURL(file);
    },
    removeImage(e) {
      this.image = '';
    },
    validateData() {
      this.errors = [];
      this.$refs.form.validate();

      if (!this.title) {
        this.errors.push('Accommodation title required.');
      }
      if (this.rent <= 0) {
        this.errors.push('Rent must be valid number');
      }
      if (!this.description) {
        this.errors.push('Description required');
      }
      if (!this.address.street || !this.address.postcode || !this.address.city) {
        this.errors.push('Address required');
      }
      if (this.$refs.pond.getFiles().length + this.$refs.pond360.getFiles().length < 1) {
        this.errors.push('Upload a photo of your accommodation');
      }
      if (this.$refs.pond.getFiles().filter((x) => x.status !== 5).length !== 0 || this.$refs.pond360.getFiles().filter((x) => x.status !== 5).length !== 0) {
        console.log(this.$refs.pond.getFiles().map((x) => x.status));
        this.errors.push('Wait until files have finished uploading');
      }

      if (!this.errors.length) {
        return true;
      }
      return false;
    }
  }
};
</script>

<style scoped>
.my-width {
  width: 60% !important;
}
</style>
