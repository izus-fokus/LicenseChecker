<template>
  <q-page>
    <div style="max-width: 600px; margin: 0 auto;">
      <q-tabs v-model="selectedOption" align="left" class="q-mx-xl q-mt-md" style="background-color: #feddd6;"
        indicator-class="custom-indicator">
        <q-tab v-for="option in options" :key="option.value" :name="option.value" :label="option.label"></q-tab>
      </q-tabs>
    </div>
    <div v-if="selectedOption === 'DependencyFileUpload'">
      <q-uploader auto-upload label="Upload Dependency File" @added="onFileAdded" :url="null" />
      <q-expansion-item v-for="(license, index) in dependencyLicenses" :key="index" :label="getExpansionLabel(license)">
        <q-checkbox v-model="selectedLicenseIds[index]" label="Select All" @input="selectAll(index)" />
        <q-checkbox v-for="id in license.license_id" :key="id" v-model="selectedLicenseIds[index]" :label="id" />
      </q-expansion-item>
    </div>
    <div v-if="selectedOption === 'addLicensesManually'">


      <q-table :rows="permissiveLicenses" :columns="permissiveColumns" row-key="license" class="q-table-striped">
        <template v-slot:body-cell-name="props">
          <q-checkbox v-model="selectedLicenses[props.row]" />
        </template>
      </q-table>
      <q-table :rows="copyleftLicenses" :columns="copyleftColumns" row-key="license" class="q-table-striped">
        <template v-slot:body-cell-name="props">
          <q-checkbox v-model="selectedLicenses[props.row]" />
        </template>
      </q-table>



    </div>

  </q-page>
</template>

<script>
export default {

  data() {
    return {
      dependencyLicenses: [], //array to fetch licenses from dependency file 
      selectedLicenseIds: [],
      permissiveLicenses: [], // Array of permissive licenses
      copyleftLicenses: [], // Array of copyleft licenses
      selectedLicenses: {}, // Object to store selected licenses
      permissiveColumns: [
        {
          name: "name",
        }
      ],
      copyleftColumns: [
        {
          name: "name",
        }
      ],

      // licenseIds: [], // Array to store the list of license ID
      selectedOption: 'DependencyFileUpload', // Default to upload Dependency file upload (requirement.txt file)
      options: [
        { value: 'DependencyFileUpload', label: 'Dependency File Upload' },
        { value: 'addLicensesManually', label: 'Add Licenses' }
      ],

    };
  },
  mounted() {
    this.fetchLicenses();

  },
  methods: {
    async onFileAdded(files) {
      const file = files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://127.0.0.1:8000/uploaddependencyfile/', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        this.dependencyLicenses = Object.entries(data.Content).map(([key, value]) => ({
          package_name: key,
          license_name: value.license_name,
          license_id: value.license_id,
        }));
        this.selectedLicenseIds = Array(this.dependencyLicenses.length).fill([]);

      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
    getExpansionLabel(license) {
      if (license.license_id.length === 1) {
        return license.license_id[0];
      } else {
        return `Choose License for ${license.package_name}`;
      }
    },

    // function to fetch list of permissive and copyleft licenses
    async fetchLicenses() {
      try {
        const permissiveResponse = await fetch("http://127.0.0.1:8000/types/permissive");
        const copyleftResponse = await fetch("http://127.0.0.1:8000/types/copyleft");

        if (!permissiveResponse.ok || !copyleftResponse.ok) {
          throw new Error("Failed to fetch licenses");
        }

        // Parse the JSON data directly
        const permissiveData = await permissiveResponse.json();
        const copyleftData = await copyleftResponse.json();

        // Assign response data directly to permissiveLicenses and copyleftLicenses
        this.permissiveLicenses = permissiveData;
        this.copyleftLicenses = copyleftData;

        // Initialize selectedLicenses object with false for each license ID
        this.selectedLicenses = {};

        this.permissiveLicenses.forEach(license => {
          this.$set(this.selectedLicenses, license, false);
        });

        this.copyleftLicenses.forEach(license => {
          this.$set(this.selectedLicenses, license, false);
        });
      } catch (error) {
        console.error("Error fetching licenses:", error);
      }
    },

    //async fetchLicenseIds() {
    //try {
    // const response = await fetch("http://127.0.0.1:8000/licenseList/");
    //if (!response.ok) {
    // throw new Error("Failed to fetch license IDs");
    //}
    //this.licenseIds = await response.json();
    // Initialize selectedLicenses object with false for each license ID
    //this.selectedLicenses = {};
    //this.licenseIds.forEach(licenseId => {
    // this.selectedLicenses[licenseId] = false;
    // });
    // } catch (error) {
    // console.error("Error fetching license IDs:", error);
    // }
    //},
    // submitSelectedLicenses() {
    //   console.log("Selected licenses:", this.selectedLicenses);
    // },



  },
};
</script>
