<template>
  <q-page>
    <div style="max-width: 600px; margin: 0 auto;">
      <q-tabs v-model="selectedOption" no-caps align="left" class="q-mx-xl q-mt-md" style="background-color: #feddd6;"
        indicator-class="custom-indicator">
        <q-tab v-for="option in options" :key="option.value" :name="option.value" :label="option.label"></q-tab>
      </q-tabs>
    </div>
    <!-- Section for uploading dependency files -->
    <div v-if="selectedOption === 'DependencyFileUpload'">
      <div v-show="!showTable" class="center-container custom-background-color">
        <div class="form-container">
          <q-form @submit="uploadFile">
            <q-select outlined hint="Python (requirements.txt, Pipfile, pyproject.toml)"
              :rules="[val => !!val || 'This field is required']" v-model="selectedChoice" :options="choices"
              label="Select Dependency File Type">
            </q-select>
            <q-uploader hide-upload-btn label="Upload your files" @added="handleFileUpload">
            </q-uploader>
            <q-btn :label="loading ? 'Uploading...' : 'Submit'" type="submit" :loading="loading" :disable="loading" />
          </q-form>
        </div>
      </div>
      <!-- Table showing dependency licenses -->
      <div v-show="showTable">
        <q-btn label="Back" @click="goBack" />
        <q-btn label="Add to Compatibility List" @click="saveSelected" />
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
      </div>
    </div>
    <!-- Section for manually adding licenses -->
    <div v-if="selectedOption === 'addLicensesManually'">
      <!-- Table for Permissive Licenses -->
      <q-table :rows="permissiveLicenses" :columns="licenseColumns" row-key="license" title="Permissive Licenses"
        class="q-table-striped">
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td>
              <q-checkbox v-model="selectedPermissiveLicenses[props.row]" />
            </q-td>
            <q-td>
              {{ props.row }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
      <!-- Table for Copyleft Licenses -->
      <q-table :rows="copyleftLicenses" :columns="licenseColumns" row-key="license" title="Copyleft Licenses"
        class="q-table-striped">
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td>
              <q-checkbox v-model="selectedCopyleftLicenses[props.row]" />
            </q-td>
            <q-td>
              {{ props.row }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
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
      selectedOption: 'DependencyFileUpload',
      options: [
        { value: 'DependencyFileUpload', label: 'Dependency File Upload' },
        { value: 'addLicensesManually', label: 'Add Licenses' }
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
      ]
    };
  },
  methods: {
    // Function to handle file upload
    handleFileUpload(files) {
      this.file = files[0];
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

        const response = await axios.post(`http://127.0.0.1:8000/uploaddependencyfile/?choice=${this.selectedChoice}`, formData, {
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
      return name.replace(/^\(|\)$/g, '');
    },
    // Function to go back from table view
    goBack() {
      this.showTable = false;
    },
    // Function to save selected licenses and move to License-Recommendation.vue 
    saveSelected() {
      // Filter selected licenses and extract IDs
      const selectedRows = this.dependencyLicenses
        .filter(row => row.selected)
        .map(row => row.dropdown);

      console.log('Selected Rows:', selectedRows);
      this.$emit('selected-rows', selectedRows);
      this.$router.push({ name: 'LicenseRecommendation' });
    },
    // Function to fetch permissive and copyleft licenses for manual display
    async fetchLicenses() {
      try {
        const [permissiveResponse, copyleftResponse] = await Promise.all([
          axios.get("http://127.0.0.1:8000/types/permissive"),
          axios.get("http://127.0.0.1:8000/types/copyleft")
        ]);
        this.permissiveLicenses = permissiveResponse.data;
        this.copyleftLicenses = copyleftResponse.data;
        console.log("Permissive Liceses", this.permissiveLicenses);
        console.log("Copyleft Liceses", this.copyleftLicenses);

        [...this.permissiveLicenses, ...this.copyleftLicenses].forEach(license => {
          this.selectedLicenses[license] = false;
        });
      }
      catch (error) {
        console.error("Error fetching licenses:", error);
      }
    }
  },

  mounted() {
    this.fetchLicenses();
  },
  // Watcher for dependencyLicenses to update selectedLicenseIds
  watch: {
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
</style>
