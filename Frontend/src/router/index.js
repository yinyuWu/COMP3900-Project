import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';
import Authenticator from '@/components/Authenticator.vue'; // TODO
import ViewAds from '@/views/ViewAds';
import CreateAccommodationAd from '@/views/CreateAccommodationAd';
import EditDetail from '@/views/EditDetail';
import AdvertisementDetail from '@/views/AdvertisementDetail';
import MyBookings from '@/views/MyBookings';
import Reservations from '@/views/Reservations';
import DisplaySearch from '@/views/DisplaySearch.vue';
import Review from '@/views/Review';
import About from '@/views/About';

Vue.use(VueRouter);

function getUser() {
  return Vue.prototype.$Amplify.Auth.currentAuthenticatedUser()
    .then((data) => {
      if (data && data.signInUserSession) {
        return data;
      }
      return null;
    })
    .catch((e) => null);
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/create',
    name: 'Create Advertisement',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    meta: { requiresAuth: true },
    component: CreateAccommodationAd
  },
  {
    path: '/auth',
    name: 'Authenticator',
    component: Authenticator
  },
  {
    path: '/advertisements',
    name: 'Advertisements',
    component: ViewAds,
    meta: { requiresAuth: true }
  },
  {
    path: '/editDetail/:id',
    name: 'EditDetail',
    component: EditDetail
  },
  {
    path: '/detail/:id',
    name: 'AdvertisementDetail',
    component: AdvertisementDetail
  },
  {
    path: '/myBookings',
    name: 'MyBookings',
    component: MyBookings
  },
  {
    path: '/reservations',
    name: 'Reservations',
    component: Reservations
  },
  {
    path: '/search',
    name: 'search',
    component: DisplaySearch
  },
  {
    path: '/review/:id',
    name: 'Review',
    component: Review
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
];

const router = new VueRouter({
  mode: 'history',
  routes
});

router.beforeResolve(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const user = await getUser();
    if (!user) {
      return next({
        path: '/auth',
        query: {
          redirect: to.fullPath
        }
      });
    }
    return next();
  }
  return next();
});

export default router;
