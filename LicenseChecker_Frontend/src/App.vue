<template>
  <div>
    <q-layout view="hHh lpR fff">
      <q-page-container>
        <Header_nav @scroll-to-disclaimer="scrollToDisclaimer" :header_label="header_label" :header_icon="header_icon"
          @changeHeaderLabel="changeHeaderLabel" />

        <router-view @selected-rows="updateSelectedRows" :selected-rows="selectedRows" :licenseid="licenseid"
          @changeHeaderLabel="changeHeaderLabel" @githubpost="githubpost" @generateid="generateid"
          @changeLicenseName="changeLicenseName" @listCompatibleLicenses="listCompatibleLicenses"
          :errorMessage="errorMessage" :compatibleLicenses="compatibleLicenses" :allLicenses="allLicenses"
          :detailedCompatibleLicenses="detailedCompatibleLicenses"
          :detailedCompatibleLicensesId="detailedCompatibleLicensesId" @changedetailedCompatibleLicensesId="changedetailedCompatibleLicensesId
            " @getCompatibleLicenses="getCompatibleLicenses" />
      </q-page-container>

      <q-footer elevated>
        <Footer_nav ref="footerNav" />
      </q-footer>
    </q-layout>
  </div>
</template>

<script>
import Header_nav from "./components/Header.vue";
import Footer_nav from "./components/Footer.vue";
import recommendationIcon from '@/assets/License-Recommendation.svg';
import licensesearch from '@/assets/License-Search.svg';
import licensechecker from '@/assets/License-Checker.svg';
import help from '@/assets/License-Help.svg';
import detailinfo from '@/assets/detail-info.svg';



import axios from "axios";
import { mapGetters } from 'vuex';
export default {
  name: "App",
  components: {
    Header_nav,
    Footer_nav,

  },

  data: () => ({
    header_label: "License Checker",
    header_icon: "licensechecker",

    hello: null,
    id: null,
    postResponse: null,
    allLicenses: [],
    allLicensesFields: null,
    compatibleLicenses: [],
    licenseid: null,
    detailedCompatibleLicensesId: [],
    selectedRows: [],

    errorMessage: null,



  }),

  methods: {

    scrollToDisclaimer() {
      this.$nextTick(() => {
        // Ensure the footer component is rendered and available
        const footer = this.$refs.footerNav?.$el;
        console.log('Footer Element:', footer);  // Debugging

        const disclaimer = footer?.querySelector('.disclaimer-text');
        console.log('Disclaimer Element:', disclaimer);  // Debugging

        if (disclaimer) {
          // Scroll smoothly to the disclaimer section
          disclaimer.scrollIntoView({ behavior: 'smooth' });

          // Add a class to highlight the disclaimer
          disclaimer.classList.add('highlight');

          // Remove the highlight after 3 seconds
          setTimeout(() => {
            disclaimer.classList.remove('highlight');
          }, 3000);
        } else {
          console.error("Disclaimer section not found!");
        }
      });
    },
    updateSelectedRows(rows) {
      console.log("Selected rows from app.vue", rows);
      this.selectedRows = rows;
    },
    changeLicenseName(licenseid) {
      /*Stores the license id in session storage to make it persistent   */
      sessionStorage.setItem("licenseid", licenseid);
      this.licenseid = sessionStorage.getItem("licenseid");
    },

    changedetailedCompatibleLicensesId(changedId) {
      console.log("In app.vue: received licenses", changedId);
      this.detailedCompatibleLicensesId = changedId;
    },

    changeHeaderLabel(headerlabel) {
      /* Change header label */
      this.header_label = headerlabel;

    },

    generateid() {
      this.id =
        "id-" +
        Math.random().toString(36).substring(2, 9) +
        "-" +
        Date.now().toString(36);
      //console.log(this.id)
    },

    githubpost(bodyFormData, repoName, softwareid) {
      /* Posts data to github */
      axios({
        method: "post",
        url: "http://license-engine:7000/api/v1/software",
        data: {
          id: softwareid,
          name: repoName,
          url: bodyFormData.url,
          branch: bodyFormData.branch,
        },
        headers: {
          "Content-Type": "application/json",
        },

      })
        .then((response) => {
          this.postResponse = response;
          this.errorMessage = null;
          // this.uploadSuccess = true;
          console.log("Upload is Sucessful:", this.uploadSuccess)
        })
        .catch((error) => {
          // Handle error
          if (error.response) {
            this.errorMessage = error.response.data.message;
            console.error("Response Error Data:", error.response.data.message);
            console.error("Response Error Status:", error.response.status);
          }
        });
    },
    listCompatibleLicenses(cl) {
      this.compatibleLicenses = cl;
    },
    getCompatibleLicenses(list) {
      /* Gets Compatible Licenses from backend */
      axios
        .post("http://backend:8000/licenses/check/", list)
        .then((response) => {
          this.compatibleLicenses = response.data;
        })
        .catch((error) => {
          console.error("Error fetching results:", error);
        });
    },
  },
  mounted() {
    axios.get("http://backend:8000/licenses/").then(
      (response) => (this.allLicenses = response.data)
    );

  },
  watch: {
    /* Changes header label based on routes */
    $route() {
      if (this.$route.path == "/") {
        this.header_label = "License Checker";
        this.header_icon = licensechecker;
      } else if (this.$route.path == "/licenseRecommendation") {
        this.header_label = "License Recommendation";
        this.header_icon = recommendationIcon;
      } else if (this.$route.path == "/LicenseSearch") {
        this.header_label = "License Search";
        this.header_icon = licensesearch;
      } else if (this.$route.path == "/LicenseDetails") {
        this.header_label = "License Details";
        this.header_icon = detailinfo;
      } else if (this.$route.path == "/compatibleLicenses") {
        this.header_label = "Compatible Licenses";
      } else if (this.$route.path == "/help") {
        this.header_label = "Help";
        this.header_icon = help;
      } else {
        //do nothing
      }

    },
  },
  computed: {
    detailedCompatibleLicenses() {
      /* Filters the detail of compatible Licenses */
      return this.allLicenses.filter((item) =>
        this.compatibleLicenses.includes(item.id)
      );
    },
  },
};
</script>
