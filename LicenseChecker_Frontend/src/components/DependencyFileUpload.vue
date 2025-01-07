<template>
  <q-page class="custom-content">

    <!-- Section for uploading dependency files -->
    <div v-if="selectedOption === 'DependencyFileUpload'">
      <div v-show="!showTable" class="center-container custom-background-color">
        <div class="form-container">
          <q-form @submit="uploadFile">
            <q-select outlined hint="Python (requirements.txt, Pipfile, pyproject.toml)"
              :rules="[val => !!val || 'This field is required']" v-model="selectedChoice" :options="choices"
              label="Select Dependency File Type" style="margin-bottom: 15px;">
            </q-select>
            <q-uploader hide-upload-btn label="Upload dependency file" @added="handleFileUpload">
            </q-uploader>



            <q-btn style=" margin-top: 15px; background-color:#1A8917; text-transform:capitalize; color: white;"
              :label="loading ? 'Uploading...' : 'Submit'" type="submit" :loading="loading" :disable="loading" />
          </q-form>
          <q-banner v-if="fileError" dense inline-actions class="text-white bg-red q-mt-lg ">
            {{ fileError }}
            <template v-slot:action>
              <q-btn flat color="white" label="Dismiss" @click="dismissError" />
            </template>
          </q-banner>
        </div>

      </div>
      <!-- Table showing  found licenses from uploaded dependecy file  -->
      <div class="q-pa-md" v-show="showTable">
        <q-table :rows="dependencyLicenses" :columns="columns" row-key="package_name">
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td v-for="col in props.cols" :key="col.name" :props="props">
                <span v-if="col.name === 'selected'">
                  <q-checkbox v-model="props.row.selected" />
                </span>
                <span v-else-if="col.name === 'package_name'">
                  {{ props.row.package_name }}
                </span>
                <span v-else-if="col.name === 'license_name'">
                  {{ props.row.license_name }}
                </span>
                <span v-else-if="col.name === 'dropdown'">
                  <template v-if="Array.isArray(props.row.license_id) && props.row.license_id.length > 1">
                    <q-select v-model="props.row.dropdown" :options="props.row.license_id" outlined dense
                      style="width: 145px;" />
                  </template>
                  <template v-else>
                    {{ props.row.license_id[0] }} <!-- Ensure this shows the correct license ID -->
                  </template>
                </span>
                <span v-else>
                  {{ col.value }}
                </span>
              </q-td>
            </q-tr>
          </template>
        </q-table>
        <div class="q-mt-md">
          <q-btn v-if="!fromLR" label="Find Compatible Licenses" @click="saveSelected" class="btn q-mr-xs" />
          <q-btn v-if="fromLR" @click="updateSelected" label="Add to Compatiblity list" class="btn q-mr-xs" />
          <q-btn label="Back" @click="goBack" color="primary" />
        </div>
      </div>

    </div>

  </q-page>
</template>

<script>
import axios from 'axios';


export default {
  name: "DependencyFileUpload",
  data() {
    return {
      showTable: false,
      loading: false,
      selectedChoice: 'Python',
      file: null,
      dependencyLicenses: [],
      selectedLicenseIds: [],
      selectedPermissiveLicenses: {},
      selectedCopyleftLicenses: {},
      selectedLicenses: {},
      fileError: null,
      selectedOption: 'DependencyFileUpload',
      options: [
        { value: 'DependencyFileUpload', label: 'Dependency File Upload' },

      ],
      choices: ['Python', 'JS'],
      columns: [
        { name: 'selected', label: 'Select', align: 'left' },
        { name: 'package_name', label: 'Package Name', align: 'left' },
        { name: 'license_name', label: 'License Name', align: 'left' },
        { name: 'dropdown', label: 'License ID', align: 'left' },
      ],
      licenseColumns: [
        { name: 'checkbox', label: 'Select', align: 'left' },
        { name: 'license', label: 'License Name', align: 'left' }
      ],
      fromLR: false,
    };
  },
  beforeRouteEnter(to, from, next) {
    // Check if the user came from LR.vue by its route name or path
    next((vm) => {
      vm.fromLR = from.name === 'LicenseRecommendation'; // Or use `from.path === '/path-to-LR'` if route name is not set
    });
  },
  methods: {
    // Function to handle file upload
    handleFileUpload(files) {
      this.file = files[0];
      this.validateFileType();
    },
    dismissError() {
      this.fileError = ''; // Clear the error message
    },
    // Function to upload file and fetch dependency licenses
    async uploadFile() {
      this.loading = true;
      this.$q.loading.show({
        message: 'Searching for licenses',
        boxClass: 'bg-grey-2 text-grey-9',
        spinnerColor: 'primary'
      });
      try {
        if (!this.file) {
          console.error("No file selected.");
          this.loading = false;
          this.$q.loading.hide();
          return;
        }

        const formData = new FormData();
        formData.append('file', this.file);
        formData.append('choice', this.selectedChoice);

        const response = await axios.post(`http://backend:8000/uploaddependencyfile/?choice=${this.selectedChoice}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        // Process response data to format and display in table
        const data = response.data;
        this.dependencyLicenses = Object.entries(data.Content).map(([key, value]) => ({
          package_name: this.sanitizePackageName(key),
          license_name: this.sanitizeLicenseName(value.license_name),
          license_id: value.license_id.includes('AND')
            ? value.license_id.split(' AND ').map(this.sanitizeLicenseName)
            : [this.sanitizeLicenseName(value.license_id)],
          dropdown: value.license_id.includes('AND')
            ? this.sanitizeLicenseName(value.license_id.split(' AND ')[0])
            : this.sanitizeLicenseName(value.license_id),
          selected: false

        }));
        this.showTable = true;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
        this.$q.loading.hide();
      }
    },
    // Function to sanitize package name
    sanitizePackageName(name) {
      return name.startsWith('@') ? name.substring(1) : name;
    },
    // Function to sanitize license name
    sanitizeLicenseName(name) {
      // Check if name is a string, otherwise return it as is
      if (typeof name === 'string') {
        return name.replace(/^\(|\)$/g, '');
      }
      // If name is not a string, return an empty string or the original value
      return name || '';
    },

    // Function to go back from table view
    goBack() {
      this.showTable = false;
    },
    updateSelected() {
      const addtocompatiblelist = this.dependencyLicenses.filter(row => row.selected).map(row => row.dropdown);
      this.$parent.$emit('selected-rows', addtocompatiblelist);
      this.$router.push('/licenseRecommendation'); // Navigate programmatically

    },
    // Function to save selected licenses and move to License-Recommendation.vue 
    saveSelected() {
      // Filter selected licenses and extract IDs
      const selectedRows = this.dependencyLicenses.filter(row => row.selected).map(row => row.dropdown);

      console.log('Selected Rows:', selectedRows);
      this.$parent.$emit('changedetailedCompatibleLicensesId',
        selectedRows
      );
      this.$parent.$emit(
        'getCompatibleLicenses',
        selectedRows
      );
      this.$router.push("/compatibleLicenses");
    },
    validateFileType() {
      if (!this.file || !this.selectedChoice) {
        this.fileError = null;
        return;
      }

      const fileName = this.file.name.toLowerCase();
      if (
        (this.selectedChoice === 'Python' && !fileName.endsWith('.txt') && !fileName.endsWith('.toml') && !fileName.includes('Pipfile')) ||
        (this.selectedChoice === 'JSON' && !fileName.endsWith('.json'))
      ) {
        this.fileError = `The uploaded file does not match the selected file type (${this.selectedChoice}).`;
      } else {
        this.fileError = null;
      }
    },
  },

  // Watcher for dependencyLicenses to update selectedLicenseIds
  watch: {
    selectedChoice() {
      this.validateFileType();
    },
    dependencyLicenses: {
      handler(newVal) {
        this.selectedLicenseIds = [];
        newVal.forEach(row => {
          if (row.selected) {
            this.selectedLicenseIds.push(...row.license_id);
          }
        });
      },
      deep: true
    }
  }
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
  border: 2px dotted #2F60AC;
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
  text-transform: capitalize;
  color: white;
}
</style>
