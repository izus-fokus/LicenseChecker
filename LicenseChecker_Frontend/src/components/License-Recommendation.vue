<template>
  <div class="custom-content">
    <div v-show="showDiv1" class="row q-mt-md justify-center">
      <div class="col-3 text-center" style="border: dotted 1px; height:41px; width:inherit;">
        <q-item>
          <q-item-section>
            <p class="text-secondary">To identify compatible licenses provide your code or
              dependency file.</p>
          </q-item-section>

          <q-avatar size="21px" style="padding:3px 5px 0 0">
            <img src="/questionMark.svg" />
            <q-tooltip max-width="500px" class="bg-primary text-secondary shadow-4" :offset="[12, 22]">
              Identify existing
              licenses in your code or in the dependencies of your code.
              List these licenses and allow you to remove or add licenses.
              Suggest open-source licenses that are compatible to this list of licenses
            </q-tooltip>
          </q-avatar>

        </q-item>
      </div>
    </div>



    <!-- QTabs for selecting options -->

    <div style="max-width: 752px; margin: 0 auto;">
      <q-tabs v-model="selectedOption" align="left" class="q-mx-xl q-mt-md text-secondary" style="background-color: #00beff;"
        indicator-class="custom-indicator">
        <q-tab v-for="option in options" :key="option.value" :name="option.value" :label="option.label">
          <q-tooltip class="bg-primary text-secondary shadow-4" :offset="[10, 10]">
            {{ getTooltipContent(option.value) }}
          </q-tooltip>

        </q-tab>
      </q-tabs>
    </div>

    <!-- Display license recommendation when selectedOption is 'github' -->
    <div v-if="selectedOption === 'github'">
      <div v-show="showDiv1">
        <!-- Step 1: User provides GitHub link and branch name -->
        <div class="row q-mx-xl q-mt-md center-container text-secondary" :class="{
          'custom-background-color': !$q.screen.lt.md,
          'max-width-1000': !$q.screen.lt.md,
          'margin-20-auto-0': !$q.screen.lt.md,
        }">
          <div class="col" :class="{
            'max-width-700': !$q.screen.lt.md,
            'flex-center': !$q.screen.lt.md,
          }">
            <q-form @submit="submitForm()" @reset="onReset" class="q-gutter-md custom-q-form">
              <q-input class="custom-input" outlined id="input-1" v-model="form.url" label="Public Git Link *" color="grey-6"
                hint="Provide the repository link (e.g https://gitlab.com/...) " required :rules="[
                  (val) => /^https?:\/\/.+$/.test(val) || 'Enter a valid URL',
                ]">
                <template v-slot:prepend>
                  <q-avatar>
                    <img src="/src/assets/github.svg" />
                  </q-avatar>
                </template>
              </q-input>
              <q-input outlined id="input-3" v-model="form.branch" label="Branch name *" color="grey-6"
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

                <q-btn label=" Analyze Code" type="submit"
                  style=" background-color:#1A8917; text-transform:capitalize; color: white;" />
                <q-btn label="Reset" type="reset" color="grey" class="q-ml-sm" style=" text-transform:capitalize;" />
              </div>
            </q-form>
          </div>
        </div>
      </div>
      <!-- Show licenses extracted from github code -->

      <div v-show="!showDiv1">

        <div v-if="licenses && Object.keys(licenses).length > 0">
          <div class="row q-mt-md justify-center">
            <div class="col-3 text-center q-pt-sm">
              <p class="text">Your code includes the following licenses </p>
            </div>

          </div>

          <p class="text-secondary" style="text-align: center;">Please choose all
            licenses that
            should be included in the
            compatibility
            check. You can also add additional licenses manually or from a dependency file. </p>
          <div>
            <div class="q-mx-xl q-mt-md">
              <q-expansion-item v-for="(paths, license) in licenses" :key="license" class="custom-headerclass bg-primary" >
                <!-- Use a slot for the expansion item header -->
                <template v-slot:header>
                  <q-item>
                    <q-item-section>
                      <q-checkbox v-model="checkboxSelection[license]" :label="` ${license}`" color="green"></q-checkbox>
                    </q-item-section>
                  </q-item>
                </template>
                <q-card class="custom-detailclass">
                  <q-card-section>
                    <p class="text-subtitle1 text-secondary">This license was found in the following file(s) </p>
                    <q-list class="text-secondary" v-for="path in paths" :key="path">{{ path }}</q-list>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <!-- Shows additional licenses selected from DependencyFileUpload and AddLicensesManually -->

              <q-expansion-item v-if="selectedRows.length > 0" :key="'selected-rows'"
                class="custom-headerclass expansion-background bg-primary">
                <template v-slot:header>
                  <q-item>
                    <q-item-section>
                      <span class="text-secondary bg-primary">Added Licenses</span>
                    </q-item-section>
                  </q-item>
                </template>
                <q-card class="custom-detailclass">
                  <q-card-section>
                    <q-list>
                      <q-item v-for="row in selectedRows" :key="row">
                        <q-item-section>
                          <!-- Checkbox for each row item -->
                          <q-checkbox v-model="checkboxSelection[row]" :label="row" color="green" ></q-checkbox> 
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-card-section>
                </q-card>
              </q-expansion-item>
              <div class="q-pa-md q-gutter-sm">
                <q-btn
                  style="text-transform: capitalize; background-color: #1A8917;; text-transform:capitalize; color: white;"
                  label=" Find Compatible Licences" @click="compatibleLicenses" />
                <q-btn style="text-transform: capitalize; " label=" Add Licenses from Dependency File" color="secondary"
                  @click=" goToAddLicenses('fromDependencyFile')
                    " />
                <q-btn style="text-transform: capitalize; " label=" Add Licenses from License List" color="secondary"
                  @click=" goToAddLicenses('manually')
                    " />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Display desktop upload when selectedOption is 'desktop' -->
    <!-- <div v-show="selectedOption === 'desktop'">
      <DesktopUpload />
    </div> -->
    <!-- Display Addlicense when selectedOption is 'addlicense' -->
    <div v-show="selectedOption === 'AddLicensesManually'">
      <AddLicensesManually />
    </div>
    <div v-show="selectedOption === 'DependencyFileUpload'">
      <DependencyFileUpload />
    </div>
    <div v-show="selectedOption === 'ZipFileUpload'">
      <ZipFileUpload />
    </div>

  </div>


</template>

<script>
import axios from "axios";
// import DesktopUpload from './Desktop-Upload.vue'
import AddLicensesManually from './AddLicensesManually.vue'
import DependencyFileUpload from './DependencyFileUpload.vue'
import ZipFileUpload from './ZipFileUpload.vue'

import { mapGetters, mapActions } from 'vuex';

export default {

  name: "License-Recommendation",
  props: {
    errorMessage: String,
    selectedRows: {
      type: Array,
      required: true
    },
  },

  components: {
    // DesktopUpload,
    AddLicensesManually,
    DependencyFileUpload,
    ZipFileUpload,
  },

  data() {
    return {

      selectedOption: 'github', // Default to license recommendation
      options: [
        { value: 'github', label: 'Retrieve Code from GitHub' },
        // { value: 'desktop', label: 'Upload Code from Local Machine' },
        { value: 'DependencyFileUpload', label: 'Dependency File Upload' },
        { value: 'ZipFileUpload', label: 'Zip File Upload' },
        { value: 'AddLicensesManually', label: 'Add Licenses Manually' },

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
    // Function to show tooltips to each option available
    getTooltipContent(value) {
      switch (value) {
        case 'github':
          return 'Retrieve code from github';
        case 'DependencyFileUpload':
          return 'Upload dependencies (upload a dependency file like a requirements.txt or a project.toml)';
        case 'ZipFileUpload':
          return 'Upload a zip file containing your project to analyze its licenses';
        case 'AddLicensesManually':
          return 'Select licenses from the list of Premissive and Copyleft licenses';
        default:
          return '';
      }
    },
    logValues() {
      console.log('selectedOption:afer ', this.selectedOption);
      console.log('showDiv1:', this.showDiv1);
      console.log('licenses:', this.licenses);
    },
    ...mapActions(['updateSelectedOption', 'updateShowDiv1', 'updateLicenses']),
    goToAddLicenses(actionType) {
      // Store the current state before navigating away
      this.updateSelectedOption(this.selectedOption);
      this.updateShowDiv1(this.showDiv1);
      this.updateLicenses(this.licenses);

      console.log("Selected Option", this.selectedOption);
      console.log("Showdiv1", this.showDiv1);
      console.log("Available licenses", this.licenses);



      // Navigate to DependencyFileUpload.vue
      if (actionType === 'fromDependencyFile') {
        this.$router.push('/DependencyFileUpload');
      } else if (actionType === 'manually') {
        this.$router.push('/AddLicensesManually');
      }

    },

    generaterepoName() {
      this.name = this.form.url.split("/").pop();
      console.log("Repo Name", this.name);
      return this.name;
    },
    generateSoftwareid() {
      this.softwareid = this.generaterepoName() + this.form.branch;
      console.log("Software ID", this.softwareid);
      return this.softwareid;
    },
    getStatus() {
      console.log("In status", this.generateSoftwareid())

      axios
        .get(
          this.engineURL + "/api/v1/software/status/" +
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
              boxClass: "bg-grey-2 text-secondary",
              spinnerColor: "secondary",
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
              boxClass: "bg-grey-2 text-secondary",
              spinnerColor: "secondary",
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
                  color: "secondary",
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
                  color: '#1A8917',
                  timeout: 0,
                  classes: "pos-custom-notification",
                  actions: [
                    {
                      label: "Show Licenses",
                      class: "pos-action-button",
                      color: "accent",
                      title: "Show found licenses",
                      handler: () => {
                        this.foundLincences();
                      },
                    },
                    {
                      label: 'Dismiss',
                      class: "pos-action-button",
                      color: "accent",
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
    submitForm() {
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
        boxClass: "bg-grey-2 text-secondary",
        spinnerColor: "secondary",
      });
      console.log("SENDING FORM");
      this.updateShowDiv1(false);
    },
    ready() {
      this.checkTimer = setInterval(() => {
        this.getStatus();
      }, 5000);
    },
    foundLincences() {
      this.showDiv1 = !this.showDiv1;
      axios
        .get(
          this.engineURL + "/api/v1/software/" +
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

    async compatibleLicenses() {
      const selectedLicenses = Object.keys(this.checkboxSelection).filter(
        (license) => this.checkboxSelection[license]
      );
      console.log("changedetailedCompatibleLicensesId fromLR", selectedLicenses);
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
          this.engineURL + "/api/v1/software/" + this.generateSoftwareid()
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
.custom-content {
  padding-bottom: 6rem;
  padding-top: 1rem;
}

.custom-q-form {
  width: 60%;
  box-sizing: border-box;
  color: #004191;


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
    background-color: "secondary";
  }
}

.flex-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.custom-background-color {
  border: 2px dotted #004191;
  /* background-color: #feddd6;
  border-radius: 10px; */
}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  min-height: 60vh;
}

.text {
  font-size: 14px;
  color: #323232;
  font-weight: bold;
  padding-top: 3px;
}

.custom-headerclass {
  background-color: #323232;
  border-radius: 10px;
  border: 2px solid #004191;
  max-width: 800px;
  margin: 0 auto;
}

.custom-detailclass {
  border-top: 2px solid #ffffff;
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
