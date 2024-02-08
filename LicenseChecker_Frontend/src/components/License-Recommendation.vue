<template>
  <div>
    <div v-show="showDiv1">
      <!-- Step 1: User provides GitHub link and branch name -->
      <div class="row q-mt-md justify-center">
        <div class="col-3 text-center q-pt-sm" style="border: dotted 1px; padding-bottom: none">
          <p class="text">Retrieve code from a GitHub repository</p>
        </div>
      </div>
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
            <q-input outlined id="input-1" v-model="form.url" label="GitHub Link *"
              hint="Provide the GitHub repository link" required :rules="[
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
              <q-btn label=" Submit" type="submit" color="primary" />
              <q-btn label="Reset" type="reset" color="primary" class="q-ml-sm" />
            </div>
          </q-form>
        </div>
      </div>
    </div>
    <div v-show="!showDiv1">
      <div v-if="licenses && Object.keys(licenses).length > 0">
        <h6>Your code has following license</h6>

        <q-expansion-item v-for="(paths, license) in licenses" :key="license" header-class="bg-teal text-white">
          <!-- Use a slot for the expansion item header -->
          <template v-slot:header>
            <q-item>
              <q-item-section>
                <q-checkbox v-model="checkboxSelection[license]" :label="` ${license}`"></q-checkbox>
              </q-item-section>
            </q-item>
          </template>
          <q-card class="bg-teal-2">
            <q-card-section>
              <q-list v-for="path in paths" :key="path">{{ path }}</q-list>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </div>


      <!-- Step 3: Button to get compatible licenses -->
      <q-btn label="Compatible Licences" color="primary" @click="compatibleLicenses" />

      <!-- Step 3: Button to get compatible licenses -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Notify } from 'quasar';

export default {
  name: "License-Recommendation",
  props: ["errorMessage"],
  data() {
    return {
      form: {
        id: " ",
        url: "https://github.com/izus-fokus/metadata2dataverse",
        branch: "main",
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
    };

  },
  methods: {
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
          "http://253caac3-21ac-4f4b-be0a-076655c66384.ma.bw-cloud-instance.org:7000/api/v1/software/status/" +
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

                this.$q.notify({
                  message: "The software has been analyzed already.",
                  caption: "Do you want to utilize the current results or initiate a new analysis?",
                  position: "center",
                  icon: "info",
                  timeout: 0,
                  classes: "custom-notification",
                  actions: [
                    {
                      label: "Reanalyze",
                      color: "primary",
                      class: "retry-button",
                      handler: () => {
                        this.reanalyze();
                      },
                    },
                    {
                      label: "Show Licenses",
                      color: "white",
                      handler: () => {
                        this.foundLincences();
                      },
                    },
                  ],
                });
              } else {
                // Display a success notification
                this.$q.notify({
                  color: "positive",
                  message:
                    "Your code was successfully uploaded. You can get the list of found licenses.",
                  position: "center",
                  timeout: 0,
                  icon: "check",
                  actions: [
                    {
                      label: "Show Licenses",
                      color: "white",
                      handler: () => {
                        this.foundLincences();
                      },
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
          "http://253caac3-21ac-4f4b-be0a-076655c66384.ma.bw-cloud-instance.org:7000/api/v1/software/" +
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
      let result = await axios
        .post("http://127.0.0.1:8000/licenses/check/", licensesArray)
        .then((res) => {
          console.log("asyncawait");
          return res.data;
        })
        .catch((error) => {
          console.log(error);
        });
      //      this.compatibleLicenses = result;

      this.$emit("listCompatibleLicenses", result);
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
          "http://253caac3-21ac-4f4b-be0a-076655c66384.ma.bw-cloud-instance.org:7000/api/v1/software/" + this.generateSoftwareid()
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
  /* Optional: Include padding and border in the width */

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
  background-color: #feddd6;
  border-radius: 10px;
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
}

.blur-background {
  filter: blur(5px);
}
</style>
