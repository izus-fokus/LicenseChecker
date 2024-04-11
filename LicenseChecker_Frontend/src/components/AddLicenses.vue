<template>
  <q-page>
    <div style="max-width: 600px; margin: 0 auto;">
      <q-tabs v-model="selectedOption" align="left" class="q-mx-xl q-mt-md" style="background-color: #feddd6;"
        indicator-class="custom-indicator">
        <q-tab v-for="option in options" :key="option.value" :name="option.value" :label="option.label"></q-tab>
      </q-tabs>
    </div>
    <div v-if="selectedOption === 'DependencyFileUpload'">
      <q-uploader :auto-upload="false" label="Upload Dependency File" @added="onFileAdded" />
      <q-table :rows="dependencyLicenses" row-key="package_name" wrap-cells no-data-label="No data available">
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th>
              Select
            </q-th>
            <q-th>
              Package Name
            </q-th>
            <q-th>
              License IDs
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td>
              <q-checkbox v-model="props.row.checked" />
            </q-td>
            <q-td>
              {{ props.row.package_name }}
            </q-td>
            <q-td>
              <q-select v-if="props.row.license_id.length > 1" v-model="props.row.dropdown"
                :options="props.row.license_id" label="Select License ID" :multiple="false" />
              <template v-else>
                {{ props.row.license_id[0] }}
              </template>
            </q-td>
          </q-tr>
        </template>
      </q-table>
      <q-btn label="Add to Compatibility List" color="primary" @click="addToCompatibilityList" />
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
      dependencyLicenses: [], //array to fetch licenses from dependency file (req.txt)
      selectedLicenseIds: [], //array to store selected license ids of dependenies (req.txt)  
      permissiveLicenses: [], // Array of permissive licenses
      copyleftLicenses: [], // Array of copyleft licenses
      selectedLicenses: {}, // Object to store selected licenses
      dropdown: "null",
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
          checked: false, // Added property to track checkbox state
          //selectedLicenseId: '', // Added property to track selected license ID
          dropdown: '',

        }));
        this.selectedLicenseIds = [];

        // this.selectedLicenseIds = Array(this.dependencyLicenses.length).fill([]);

      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
    addToCompatibilityList() {
      this.selectedLicenseIds = [];
      this.dependencyLicenses.forEach(row => {
        if (row.checked && (row.dropdown || row.license_id.length === 1)) {
          const selectedLicenseId = row.dropdown || row.license_id[0];
          this.selectedLicenseIds.push(selectedLicenseId);
        }
      });
      this.selectedLicenseIds = [...new Set(this.selectedLicenseIds)];
      console.log("Selected license id", this.selectedLicenseIds);
      // const plainArray = JSON.parse(JSON.stringify(this.selectedLicenseIds));
      // this.$emit('getselectedLicenseids', plainArray);
      // this.$router.push("/LicenseRecommedation");

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
          this.selectedLicenses[license] = false;
        });

        this.copyleftLicenses.forEach(license => {
          this.selectedLicenses[license] = false;
        });
      } catch (error) {
        console.error("Error fetching licenses:", error);
      }
    },

  },
  watch: {
    dependencyLicenses: {
      handler(newVal) {
        // Clear selectedLicenseIds array
        this.selectedLicenseIds = [];

        // Filter out selected license IDs from rows where checkbox is checked
        newVal.forEach(row => {
          if (row.checked) {
            this.selectedLicenseIds.push(...row.license_id);
          }
        });

        // Add selected license ID from the dropdown if it exists
        // newVal.forEach(row => {
        //   if (row.checked && row.selectedLicenseId && !this.selectedLicenseIds.includes(row.selectedLicenseId)) {
        //     this.selectedLicenseIds.push(row.selectedLicenseId);
        //   }
        // });
      },
      deep: true
    }
  }
};
</script>
