<template>
  <div>
    <!-- QTabs for selecting options -->
    <h6 style="text-align: center;"> To identify compatible licenses provide your code or
      dependency file. </h6>
    <div style="max-width: 600px; margin: 0 auto;">
      <q-tabs v-model="selectedOption" align="left" class="q-mx-xl q-mt-md" style="background-color: #feddd6;"
        indicator-class="custom-indicator">
        <q-tab v-for="option in options" :key="option.value" :name="option.value" :label="option.label">
          <q-tooltip class="bg-indigo" :offset="[10, 10]">
            Github!
          </q-tooltip>
        </q-tab>
      </q-tabs>
    </div>

    <!-- Display license recommendation when selectedOption is 'github' -->
    <div v-if="selectedOption === 'github'">
      <div v-show="showDiv1">
        {{ licenses }}
        <!-- Step 1: User provides GitHub link and branch name -->
        <div class="row q-mx-xl q-mt-md center-container" :class="{
          'custom-background-color': !$q.screen.lt.md,
          'max-width-1000': !$q.screen.lt.md,
          'margin-20-auto-0': !$q.screen.lt.md,
        }">
          <div class="col" :class="{
            'max-width-700': !$q.screen.lt.md,
            'flex-center': !$q.screen.lt.md,
          }">
            <q-form @submit="submitForm()" @reset="onReset" class="q-gutter-md custom-q-form">
              <q-input class="custom-input" outlined id="input-1" v-model="form.url" label="Public Git Link *"
                hint="Provide the repository link (e.g https://gitlab.com/...) " required :rules="[
                  (val) => /^https?:\/\/.+$/.test(val) || 'Enter a valid URL',
                ]">
                <template v-slot:prepend>
                  <q-avatar>
                    <img src="/src/assets/github.svg" />
                  </q-avatar>
                </template>
              </q-input>
              <q-input outlined id="input-3" v-model="form.branch" label="Branch name *"
                hint="Specify the branch name (e.g., development, feature, etc.)" :rules="[
                  (val) => (val && val.length > 0) || 'Enter branch name ',
                ]">
                <template v-slot:prepend>
                  <q-avatar>
                    <img src="/src/assets/git-branch.svg" />
                  </q-avatar>
                </template>
              </q-input>
              <div>

                <q-btn label=" Analyze Code" type="submit" color="primary" />
                <q-btn label="Reset" type="reset" color="primary" class="q-ml-sm" />
              </div>
            </q-form>
          </div>
        </div>
      </div>
      <div v-show="!showDiv1">

        <div v-if="licenses && Object.keys(licenses).length > 0">
          <div class="row q-mt-md justify-center">
            <div class="col-3 text-center q-pt-sm" style="border:0.1px solid  #2F60AC ; background-color: #feddd6;">
              <p class="text">Your code includes the following licenses </p>
            </div>

          </div>
          <br>
          <p class="text" style="text-align: center;"> Please choose all licenses that should be included in the
            compatibility
            check. You can also add additional licenses manually or from a dependency file. </p>
          <div>
            <div class="q-mx-xl q-mt-md ">
              <q-expansion-item v-for="(paths, license) in licenses" :key="license" class="custom-headerclass">
                <!-- Use a slot for the expansion item header -->
                <template v-slot:header>
                  <q-item>
                    <q-item-section>
                      <q-checkbox v-model="checkboxSelection[license]" :label="` ${license}`"></q-checkbox>
                    </q-item-section>
                  </q-item>
                </template>
                <q-card class="custom-detailclass">
                  <q-card-section>
                    <p class="text-subtitle1">This license was found in the following file(s) </p>
                    <q-list v-for="path in paths" :key="path">{{ path }}</q-list>
                    <!-- <div v-if="this.selectedRows.length > 0">
                      <p class="text-subtitle1">Selected License Rows</p>
                      <q-list v-for="row in selectedRows" :key="row">{{ row }}</q-list>
                    </div> -->
                  </q-card-section>
                </q-card>
              </q-expansion-item>
              <q-expansion-item v-if="selectedRows.length > 0" :key="'selected-rows'" class="custom-headerclass">
                <template v-slot:header>
                  <q-item>
                    <q-item-section>
                      <q-checkbox v-model="checkboxSelection['selected-rows']"
                        label="Selected License Rows"></q-checkbox>
                    </q-item-section>
                  </q-item>
                </template>
                <q-card class="custom-detailclass">
                  <q-card-section>
                    <p class="text-subtitle1">Selected License Rows</p>
                    <q-list v-for="row in selectedRows" :key="row">{{ row }}</q-list>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <div class="q-pa-md q-gutter-sm">
                <q-btn style="text-transform: capitalize; " label=" Find Compatible Licences" color="primary"
                  @click="compatibleLicenses" />
                <q-btn style="text-transform: capitalize; " label=" Add more licenses" color="primary" @click=" goToAddLicenses()
                  " />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Display desktop upload when selectedOption is 'desktop' -->
    <div v-show="selectedOption === 'desktop'">
      <DesktopUpload />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import DesktopUpload from './Desktop-Upload.vue'
import { mapGetters, mapActions } from 'vuex';

export default {

  name: "License-Recommendation",
  props: {
    errorMessage: String,
    selectedRows: {
      type: Array,
      required: true
    }
  },

  components: {
    DesktopUpload
  },

  data() {
    return {


      selectedOption: 'github', // Default to license recommendation
      options: [
        { value: 'github', label: 'Retrieve Code from GitHub' },
        { value: 'desktop', label: 'Upload Code from Local Machine' }
      ],
      form: {
        id: " ",
        url: "",
        branch: "",
      },
      status: " ",
      name: " ",
      toggle: 0,
      checkTimer: null,
      repoName: " ",
      softwareid: null,
      uploadSuccess: false,
      licenses: null,
      checkboxSelection: {},
      responseArray: [],
      showDiv1: true,
      scrollPosition: 0,
      savedState: null,

    };


  },

  computed: { // accessing the state from store
    ...mapGetters(['getSelectedOption', 'getShowDiv1', 'getLicenses']),

  },
  mounted() {
    this.selectedOption = this.getSelectedOption;
    this.showDiv1 = this.getShowDiv1;
    this.licenses = this.getLicenses;
    this.logValues();
  },

  methods: {
    logValues() {
      console.log('selectedOption:afer ', this.selectedOption);
      console.log('showDiv1:', this.showDiv1);
      console.log('licenses:', this.licenses);
    },
    ...mapActions(['updateSelectedOption', 'updateShowDiv1', 'updateLicenses']),
    goToAddLicenses() {
      // Store the current state before navigating away
      this.updateSelectedOption(this.selectedOption);
      this.updateShowDiv1(this.showDiv1);
      this.updateLicenses(this.licenses);
      console.log("Selected Option", this.selectedOption);
      console.log("Showdiv1", this.showDiv1);
      console.log("Available licenses", this.licenses);

      // Navigate to AddLicenses.vue
      this.$router.push({ name: 'AddLicenses' });
    },

    generaterepoName: function () {
      this.name = this.form.url.split("/").pop();
      console.log("Repo Name", this.name);
      return this.name;
    },
    generateSoftwareid: function () {
      this.softwareid = this.generaterepoName() + this.form.branch;
      return this.softwareid;
    },
    getStatus: function () {

      axios
        .get(
          "http://localhost:7000/api/v1/software/status/" +
          this.generateSoftwareid()
        )

        .then((response) => {
          this.status = response.data;
          console.log("Status", response.data);
          if (response.data.status) {
            // checking if it already has a status, i.e "Finished"
            this.status = response.data.status;
            this.$q.loading.show({
              message: this.status,
              boxClass: "bg-grey-2 text-grey-9",
              spinnerColor: "primary",
            });
            if (this.checkTimer) {
              setTimeout(() => {
                this.$q.loading.hide();
              }, 3000);
              clearTimeout(this.checkTimer);
            }
          } else {
            this.status = response.data;
            this.$q.loading.show({
              message: this.status,
              boxClass: "bg-grey-2 text-grey-9",
              spinnerColor: "primary",
            });
          }
          if (this.status == "FINISHED") {
            setTimeout(() => {
              // Check if there is an error message
              if (this.errorMessage) {
                console.log("Error Message...")

                this.$q.notify({
                  message: "This software has been analyzed already.",
                  caption: "Do you want to use the existing results or start a new analysis?",
                  position: "center",
                  icon: "info",
                  timeout: 0,
                  classes: "custom-notification",
                  actions: [
                    {
                      label: "Show Licenses",
                      color: "primary",
                      class: "action-button",
                      title: "Show already analyzed licenses",
                      handler: () => {
                        this.foundLincences();

                      },

                    },

                    {
                      label: "Reanalyze",
                      color: "primary",
                      class: "action-button",
                      title: "Initiate a new analysis",

                      handler: () => {
                        this.reanalyze();
                      },
                    },

                    {
                      label: 'Dismiss',
                      color: 'primary',
                      class: "action-button",
                      title: "Close",
                      handler: () => { /* ... */ }
                    },

                  ],
                });
              } else {
                // Display a success notification
                this.$q.notify({
                  message: "Your code has been successfully uploaded.",
                  caption: "You may now access the list of found licenses.",
                  position: "center",
                  icon: "check",
                  timeout: 0,
                  classes: "pos-custom-notification",
                  actions: [
                    {
                      label: "Show Licenses",
                      class: "pos-action-button",
                      title: "Show found licenses",
                      handler: () => {
                        this.foundLincences();
                      },
                    },
                    {
                      label: 'Dismiss',
                      class: "pos-action-button",
                      title: "Close",
                      handler: () => { /* ... */ }
                    },
                  ],
                });
              }
            }, 2000);
          }
        });
    },
    submitForm: function () {
      this.repoName = this.generaterepoName();
      this.$parent.$emit(
        "githubpost",
        this.form,
        this.repoName,
        this.generateSoftwareid()
      );
      this.ready();
      this.$q.loading.show({
        message: "Searching for Licenses",
        boxClass: "bg-grey-2 text-grey-9",
        spinnerColor: "primary",
      });
      console.log("SENDING FORM");
      this.updateShowDiv1(false);
    },
    ready: function () {
      this.checkTimer = setInterval(() => {
        this.getStatus();
      }, 5000);
    },
    foundLincences() {


      this.showDiv1 = !this.showDiv1;


      axios
        .get(
          "http://localhost:7000/api/v1/software/" +
          this.generateSoftwareid() +
          "/licenses"
        )

        .then((response) => {

          this.licenses = response.data;
          console.log("Licenses from backend:", this.licenses);
          this.checkboxSelection = Object.fromEntries(
            Object.keys(this.licenses).map((license) => [license, true])
          );
        })
        .catch((error) => {
          console.error("Error fetching licenses:", error);
        });
    },
    getCompatibleLicenses() {
      axios
        .post("http://127.0.0.1:8000/licenses/check/", ["MIT"])
        .then((response) => {
          console.log("getClic");
          this.responseArray = response.data;
        })
        .catch((error) => {
          console.error("Error in getCompatibleLicenses:", error);
        });
    },

    async compatibleLicenses() {
      const selectedLicenses = Object.keys(this.checkboxSelection).filter(
        (license) => this.checkboxSelection[license]
      );
      // console.log("Selected Licenses:", selectedLicenses);
      this.$emit("changedetailedCompatibleLicensesId", selectedLicenses);
      //  Ensure selectedLicenses is an array
      const licensesArray = Array.isArray(selectedLicenses)
        ? selectedLicenses
        : [selectedLicenses];
      this.$emit("getCompatibleLicenses", licensesArray);
      this.$router.push("/compatibleLicenses");
    },

    onReset() {
      this.form.url = null;
      this.form.branch = null;
    },

    reanalyze() {
      // Delete the software with the specified software-id
      axios
        .delete(
          "http://localhost:7000/api/v1/software/" + this.generateSoftwareid()
        )
        .then(() => {
          console.log("the software is deleted", this.generateSoftwareid());
          this.submitForm();
        })
        .catch((error) => {
          console.error("Error deleting software:", error);
        });
    },

  },
};
</script>

<style scoped>
.custom-q-form {
  width: 60%;
  box-sizing: border-box;


  @media (max-width: 599px) {
    width: 100%;
  }
}

.max-width-1000 {
  max-width: 1000px;
}

.max-width-700 {
  max-width: 700px;
}

.margin-20-auto-0 {
  margin: 20px auto 0;
}

@media (max-width: 599px) {
  .custom-background-color {
    background-color: transparent;
  }
}

.flex-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.custom-background-color {
  border: 2px dotted #2F60AC;
  /* background-color: #feddd6;
  border-radius: 10px; */
}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  /* background-color: azure; */
  min-height: 60vh;
}

.text {
  font-size: 14px;
  color: #2f60ac;
  font-weight: bold;
  padding-top: 3px;
}

.custom-headerclass {
  background-color: #ffffff;
  border-radius: 10px;
  border: 2px solid #2f60ac;
  max-width: 800px;
  margin: 0 auto;
}

.custom-detailclass {
  border-top: 2px solid #2F60AC;
  border-bottom-left-radius: 10px !important;
  border-bottom-right-radius: 10px !important;
}

.blur-background {
  filter: blur(5px);
}

.custom-indicator {
  color: yellow;
  /* Example custom styling for the indicator */
  height: 3px;
  /* Example custom height for the indicator */
}
</style>
