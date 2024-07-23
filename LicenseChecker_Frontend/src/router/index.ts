import { createRouter, createWebHistory } from "vue-router";
import Home from "../components/Home.vue";
import Signup from "../components/Signup.vue";
import LicenseRecommendation from "../components/License-Recommendation.vue";
import LicenseSearch from "../components/License-Search.vue";
import Imprint from "../components/Imprint.vue";
import Help from "../components/Help.vue";
import LicenseDetails from "../components/License-Details.vue";
import CompatibleLicenses from "../components/Compatible-Licenses.vue";
import AddLicenses from "../components/AddLicenses.vue";


const router = createRouter({
  history: createWebHistory(),
  routes: [

    {
      path: "/",

      name: "HomePage", //it has to be consistant
      component: Home,
    },
    {
      path: "/licenseRecommendation",
      name: "LicenseRecommendation",
      component: LicenseRecommendation,

    },
    {
      path: "/licenseSearch", // camel case
      name: "LicenseSearch",
      component: LicenseSearch,
    },
    {
      path: "/compatiblelicenses", // camel case
      name: "CompatibleLicenses",
      component: CompatibleLicenses,
    },
    {
      path: "/LicenseDetails",
      name: "LicenseDetails",
      component: LicenseDetails,
    },
    {
      path: "/help", // camel case
      name: "help",
      component: Help,
    },
    {
      path: "/Imprint",
      name: "Imprint",
      component: Imprint,
    },
    {
      path: '/add-license',
      name: 'AddLicenses',
      component: AddLicenses,
    },
  ],
});

export default router;
