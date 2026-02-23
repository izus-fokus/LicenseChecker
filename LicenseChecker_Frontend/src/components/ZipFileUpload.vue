<template>
  <q-page class="custom-content">

    <!-- Section for uploading zip files -->
    <div v-if="selectedOption === 'ZipFileUpload'">
      <div v-show="!showTable" class="center-container custom-background-color">
        <div class="form-container">
          <q-form @submit="uploadZipFile()">
            <q-uploader ref="uploader" hide-upload-btn label="Upload zip file" accept=".zip" @added="handleFileUpload"
              color="secondary">
            </q-uploader>

            <q-btn style=" margin-top: 15px; background-color:#1A8917; text-transform:capitalize; color: white;"
              :label="loading ? 'Uploading...' : 'Submit'" type="submit" :loading="loading" :disable="loading || !file" />
          </q-form>
          <q-banner v-if="fileError" dense inline-actions class="text-secondary bg-red q-mt-lg ">
            {{ fileError }}
            <template v-slot:action>
              <q-btn flat color="secondary" label="Dismiss" @click="dismissError" />
            </template>
          </q-banner>
        </div>

      </div>
      <!-- Expansion list showing found licenses from uploaded zip file -->
      <div class="q-pa-md" v-show="showTable">
        <div v-if="licenses && Object.keys(licenses).length > 0">
          <div class="row q-mt-md justify-center">
            <div class="col-3 text-center q-pt-sm">
              <p class="text">Your code includes the following licenses</p>
            </div>
          </div>
          <p class="text-secondary" style="text-align: center;">Please choose all licenses that should be included in the compatibility check.</p>
          <div class="q-mx-xl q-mt-md">
            <q-expansion-item v-for="(paths, license) in licenses" :key="license" class="custom-headerclass bg-primary">
              <template v-slot:header>
                <q-item>
                  <q-item-section>
                    <q-checkbox v-model="checkboxSelection[license]" :label="` ${license}`" color="green"></q-checkbox>
                  </q-item-section>
                </q-item>
              </template>
              <q-card class="custom-detailclass">
                <q-card-section>
                  <p class="text-subtitle1 text-secondary">This license was found in the following file(s)</p>
                  <q-list class="text-secondary" v-for="path in paths" :key="path">{{ path }}</q-list>
                </q-card-section>
              </q-card>
            </q-expansion-item>
            <div class="q-pa-md q-gutter-sm">
              <q-btn v-if="!fromLR"
                style="text-transform: capitalize; background-color: #1A8917; color: white;"
                label="Find Compatible Licences" @click="saveSelected" />
              <q-btn v-if="fromLR"
                style="text-transform: capitalize; background-color: #1A8917; color: white;"
                label="Add to Compatibility list" @click="updateSelected" />
              <q-btn style="text-transform: capitalize;" label="Add Licenses from Dependency File" color="secondary"
                @click="goToAddLicenses('fromDependencyFile')" />
              <q-btn style="text-transform: capitalize;" label="Add Licenses from License List" color="secondary"
                @click="goToAddLicenses('manually')" />
            </div>
          </div>
        </div>
      </div>

    </div>

  </q-page>
</template>

<script>

import axios from 'axios';
import { mapGetters, mapActions } from 'vuex'

export default {
  name: "ZipFileUpload",
  data() {
    return {
      showTable: false,
      loading: false,
      file: null,
      fileError: null,
      selectedOption: 'ZipFileUpload',
      options: [
        { value: 'ZipFileUpload', label: 'Zip File Upload' },
      ],
      fromLR: false,
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

  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.fromLR = from.name === 'LicenseRecommendation';
    });
  },
  methods: {
    handleFileUpload(files) {
      const limitMb = Number(import.meta.env.VITE_ZIP_UPLOAD_LIMIT_MB) || 50;
      const maxSize = limitMb * 1024 * 1024;
      if (files[0].size > maxSize) {
        this.$q.notify({
          message: 'File too large',
          caption: `The selected file exceeds the ${limitMb}MB limit. Please upload a smaller file.`,
          type: 'negative',
          position: 'center',
          timeout: 5000,
        });
        this.file = null;
        return;
      }
      this.file = files[0];
      this.getSoftwareId();
    },
    dismissError() {
      this.fileError = '';
    },
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
    async getSoftwareId() {
      const fullBuffer = await this.file.arrayBuffer();
      const hashBuffer = await crypto.subtle.digest('SHA-256', fullBuffer);
      const sha256 = Array.from(new Uint8Array(hashBuffer))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
      this.softwareid = sha256;
      console.log("File Software ID SHA256:", this.softwareid);
    },
    getStatus() {
      console.log("In status", this.softwareid)

      axios
        .get(
          this.engineURL + "/api/v1/software/status/" +
          this.softwareid
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
    async uploadZipFile() {
      const vtApiKey = import.meta.env.VITE_VIRUSTOTAL_API_KEY;
      if (vtApiKey && this.softwareid) {
        try {
          const vtResponse = await axios.get(
            `https://www.virustotal.com/api/v3/files/${this.softwareid}`,
            { headers: { 'x-apikey': vtApiKey } }
          );
          const stats = vtResponse.data?.data?.attributes?.last_analysis_stats;
          if (stats && stats.malicious > 0) {
            this.fileError = `VirusTotal flagged this file as malicious (${stats.malicious} detection(s)). Upload blocked.`;
            return;
          }
          console.log("VirusTotal: file is clean", stats);
        } catch (vtError) {
          if (vtError.response?.status === 404) {
            // File unknown to VirusTotal – proceed with upload
            console.log("VirusTotal: file not in database, proceeding");
          } else if (vtError.response?.status === 429) {
            // Rate limit reached – silently skip and proceed with upload
            console.warn("VirusTotal rate limit reached, skipping check");
          } else {
            // API unreachable or other error – warn but don't block upload
            console.warn("VirusTotal check failed, proceeding:", vtError.message);
          }
        }
      }
      this.$parent.$emit(
        "uploadZipFile",
        this.file.name,
        this.file,
        this.softwareid,
      );
      this.loading = true;
      this.ready();
      this.$q.loading.show({
        message: "Searching for Licenses",
        boxClass: "bg-grey-2 text-secondary",
        spinnerColor: "secondary",
      });
    },
    ready() {
      this.checkTimer = setInterval(() => {
        this.getStatus();
      }, 5000);
    },
    foundLincences() {
      this.showTable = true;
      this.loading = false;
      this.file = null;
      if (this.$refs.uploader) {
        this.$refs.uploader.reset();
      }
      axios
        .get(
          this.engineURL + "/api/v1/software/" +
          this.softwareid +
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

    goBack() {
      this.showTable = false;
    },
    saveSelected() {
      const selectedLicenses = Object.keys(this.checkboxSelection).filter(
        (license) => this.checkboxSelection[license]
      );
      this.$parent.$emit('changedetailedCompatibleLicensesId', selectedLicenses);
      this.$parent.$emit('getCompatibleLicenses', selectedLicenses);
      this.$router.push("/compatibleLicenses");
    },
    updateSelected() {
      const selectedLicenses = Object.keys(this.checkboxSelection).filter(
        (license) => this.checkboxSelection[license]
      );
      this.$parent.$emit('selected-rows', selectedLicenses);
      this.$router.push('/licenseRecommendation');
    },

    reanalyze() {
      // Delete the software with the specified software-id
      axios
        .delete(
          this.engineURL + "/api/v1/software/" + this.softwareid
        )
        .then(() => {
          console.log("the software is deleted", this.softwareid);
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

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  border: 2px dotted #004191;
  max-width: 1000px;
  margin: 20px auto 0;
}

.form-container {
  max-width: 700px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.btn {
  text-transform: capitalize;
  background-color: #1A8917;
  color: white;
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
</style>
