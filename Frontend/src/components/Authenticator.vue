<template>
  <div>
    <div v-if="!getUser">
      <v-card flat>
        <v-card-actions class="d-flex justify-center flex-wrap flex-shrink-1">
          <amplify-authenticator v-bind:authConfig="authConfig"></amplify-authenticator>
        </v-card-actions>
      </v-card>
    </div>
    <div v-if="getUser&&!this.$route.query.redirect">{{ this.$router.push({name:'Home'}) }}</div>
    <div
      v-if="getUser&&this.$route.query.redirect"
    >{{ this.$router.push({path:this.$route.query.redirect}) }}</div>
  </div>
</template>

<script>
import { Auth } from 'aws-amplify';
import { AmplifyEventBus } from 'aws-amplify-vue';

export default {
  name: 'AmplifyAuthen',
  components: {},
  props: {},
  data() {
    return {
      // isSignedIn: false,
      authConfig: {
        signUpConfig: {
          header: 'Sign Up',
          hideAllDefaults: true,
          defaultCountryCode: '1',
          signUpFields: [
            {
              label: 'Given Name',
              key: 'given_name',
              required: true,
              displayOrder: 3,
              type: 'string',
            },
            {
              label: 'Email',
              key: 'username',
              required: true,
              displayOrder: 1,
              type: 'string',
              signUpWith: true,
            },
            {
              label: 'Password',
              key: 'password',
              required: true,
              displayOrder: 2,
              type: 'password',
            },
            {
              label: 'Family Name',
              key: 'family_name',
              required: true,
              displayOrder: 4,
              type: 'string',
            },
          ],
        },
        signInConfig: {},
        usernameAttributes: 'Email',
      },
    };
  },
  created() {
    this.findUser();

    AmplifyEventBus.$on('authState', (info) => {
      if (info === 'signedIn') {
        this.findUser();
      } else {
        this.$store.commit('setUser', null);
      }
    });
  },
  computed: {
    getUser() {
      return this.$store.state.user;
    },
  },
  methods: {
    async findUser() {
      try {
        const user = await Auth.currentAuthenticatedUser();
        this.$store.commit('setUser', user);
      } catch (err) {
        this.$store.commit('setUser', null);
      }
    },
  },
};
</script>

<style>
div[class^="Form__"] {
  box-shadow: none;
  min-width: initial !important;
}

button[class^="Button__"] {
  background: linear-gradient(169deg, #FDBB2D 0%, #22C1C3 100%);
  color: white;
}
</style>
<style scoped></style>
