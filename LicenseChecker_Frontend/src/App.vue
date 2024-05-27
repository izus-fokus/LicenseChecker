<template>
  <div>
    <q-layout view="hHh lpR fff">
      <q-page-container>
        <Header_nav :header_label="header_label" @changeHeaderLabel="changeHeaderLabel" />

        <router-view :licenseid="licenseid" @changeHeaderLabel="changeHeaderLabel" @githubpost="githubpost"
          @generateid="generateid" @changeLicenseName="changeLicenseName"
          @listCompatibleLicenses="listCompatibleLicenses" :errorMessage="errorMessage"
          :compatibleLicenses="compatibleLicenses" :allLicenses="allLicenses"
          :detailedCompatibleLicenses="detailedCompatibleLicenses"
          :detailedCompatibleLicensesId="detailedCompatibleLicensesId" @changedetailedCompatibleLicensesId="changedetailedCompatibleLicensesId
            " @getCompatibleLicenses="getCompatibleLicenses" />
      </q-page-container>

      <Footer_nav />
    </q-layout>
  </div>
</template>

<script>
import Header_nav from "./components/Header.vue";
import Footer_nav from "./components/Footer.vue";
import axios from "axios";

export default {
  name: "App",
  components: {
    Header_nav,
    Footer_nav,
  },

  data: () => ({
    header_label: "License Checker",
    hello: null,
    id: null,
    postResponse: null,
    allLicenses: [],
    allLicensesFields: null,
    compatibleLicenses: [],
    licenseid: null,
    detailedCompatibleLicensesId: [],
    // getselectedLicenseids: null,
    // selectedLicenseIds: [],
    // plainArray: [],

    errorMessage: null,
    // uploadSucess: false,
  }),
  methods: {
    changeLicenseName: function (licenseid) {
      console.log("Running");
      sessionStorage.setItem("licenseid", licenseid);
      this.licenseid = sessionStorage.getItem("licenseid");
    },
    changedetailedCompatibleLicensesId: function (changedId) {
      this.detailedCompatibleLicensesId = changedId;
    },
    // getselectedLicenseids: function (plainArray) {
    //   console.log("Running");
    //   this.plainArray = plainArray;
    //   console.log('Selected License IDs', plainArray);
    // },

    changeHeaderLabel: function (headerlabel) {
      this.header_label = headerlabel;
    },
    generateid: function generateId() {
      this.id =
        "id-" +
        Math.random().toString(36).substring(2, 9) +
        "-" +
        Date.now().toString(36);
      //console.log(this.id)
    },
    githubpost: function (bodyFormData, repoName, softwareid) {
      axios({
        method: "post",
        url: "http://localhost:7000/api/v1/software",
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
          // console.log("Upload is Sucessful:", this.uploadSuccess)
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
    listCompatibleLicenses: function (cl) {
      this.compatibleLicenses = cl;
    },
    getCompatibleLicenses: function (list) {
      axios
        .post("http://127.0.0.1:8000/licenses/check/", list)
        .then((response) => {
          this.compatibleLicenses = response.data;
        })
        .catch((error) => {
          console.error("Error fetching results:", error);
        });
    }
  },
  mounted() {
    axios.get("http://127.0.0.1:8000/licenses/").then(
      (response) => (this.allLicenses = response.data)

      //this.allLicensesFields=Object.values(Object.values(this.allLicenses)
    );
  },
  watch: {
    $route() {
      if (this.$route.path == "/") {
        this.header_label = "License Checker";
      } else if (this.$route.path == "/licenseRecommendation") {
        this.header_label = "License Recommendation";
      } else if (this.$route.path == "/LicenseSearch") {
        this.header_label = "License Search";
      } else if (this.$route.path == "/LicenseDetails") {
        this.header_label = "License Details";
      } else if (this.$route.path == "/compatibleLicenses") {
        this.header_label = "Compatible Licenses";
      } else {
        //do nothing
      }
    },
  },
  computed: {
    detailedCompatibleLicenses: function () {
      return this.allLicenses.filter((item) =>
        this.compatibleLicenses.includes(item.id)
      );
    },
  },
};
</script>
