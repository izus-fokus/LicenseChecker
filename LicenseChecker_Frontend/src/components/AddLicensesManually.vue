<template>
    <div class="home-content q-pa-md">
        <!-- Table for Permissive Licenses -->

        <div class="license-table">
            <q-table bordered virtual-scroll :rows="permissiveLicenses" :columns="licenseColumns" row-key="license"
                title="Permissive Licenses" class="text-primary license-table-content sticky-header">
                <template v-slot:body="props">
                    <q-tr :props="props">
                        <q-td>
                            <q-checkbox v-model="selectedPermissiveLicenses[props.row]"
                                @update:model-value="updateSelected" />
                        </q-td>
                        <q-td>
                            {{ props.row }}
                        </q-td>
                    </q-tr>
                </template>
            </q-table>
        </div>
        <!-- Table for Copyleft Licenses -->
        <div class="license-table">
            <q-table flat bordered virtual-scroll :rows="copyleftLicenses" :columns="licenseColumns" row-key="license"
                title="Copyleft Licenses" class="sticky-header license-table-content text-primary">
                <template v-slot:body="props">
                    <q-tr :props="props">
                        <q-td>
                            <q-checkbox v-model="selectedCopyleftLicenses[props.row]"
                                @update:model-value="updateSelected" />
                        </q-td>
                        <q-td>
                            {{ props.row }}
                        </q-td>
                    </q-tr>
                </template>
            </q-table>
        </div>


    </div>
    <div class="q-pa-md custom-pos">
        <q-btn v-if="fromLR" style="text-transform: capitalize; " class="q-ml-sm" @click="() => {
            $parent.$emit('selected-rows', this.combinedSelectedLicenses);
            this.$router.push('/licenseRecommendation');
        }
            " label="Add to Compatiblity list" color="primary" />
        <q-btn v-if="!fromLR" @click="
            $parent.$emit(
                'changedetailedCompatibleLicensesId',
                this.combinedSelectedLicenses
            );
        $parent.$emit(
            'getCompatibleLicenses',
            this.combinedSelectedLicenses
        );
        " to="/compatibleLicenses" label="Find Compatible Licenses" class="btn" />


    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
    name: "AddLicensesManually",
    data() {
        return {
            permissiveLicenses: [],
            copyleftLicenses: [],
            selectedPermissiveLicenses: {},
            selectedCopyleftLicenses: {},
            combinedSelectedLicenses: [],
            licenseColumns: [
                { name: 'checkbox', label: 'Select', align: 'left', field: 'checkbox' },
                { name: 'license', label: 'License Name', align: 'left', field: 'license', sortable: true }
            ],
            fromLR: false,
        };
    },
    beforeRouteEnter(to, from, next) {
        next((vm) => { // 'vm' will be the instance of the component after it is created
            console.log("Navigating from:", from); // Debugging log
            vm.fromLR = from.name === 'LicenseRecommendation'; // Check if the previous route is 'licenseRecommendation'
            console.log("fromLR value:", vm.fromLR); // Log the value of fromLR
        });
    },
    methods: {
        // Function to fetch permissive and copyleft licenses for manual display
        async fetchLicenses() {
            try {
                const [permissiveResponse, copyleftResponse] = await Promise.all([
                    axios.get("http://backend:8000/types/permissive"),
                    axios.get("http://backend:8000/types/copyleft")
                ]);

                this.permissiveLicenses = permissiveResponse.data;
                this.copyleftLicenses = copyleftResponse.data;
                console.log("Permissive Licenses", this.permissiveLicenses);
                console.log("Copyleft Licenses", this.copyleftLicenses);

                // Initialize selectedLicenses to be unchecked by default (false)
                this.permissiveLicenses.forEach(license => {
                    this.selectedPermissiveLicenses[license] = false; // Set to false for unchecked state
                });

                this.copyleftLicenses.forEach(license => {
                    this.selectedCopyleftLicenses[license] = false; // Set to false for unchecked state
                });
            } catch (error) {
                console.error("Error fetching licenses:", error);
            }
        },
        // Responsive Function- on each checkbox/uncheck license upadtes/remove the license from the array  
        updateSelected() {
            // Combine selected values from both permissive and copyleft tables
            const permissiveSelected = Object.keys(this.selectedPermissiveLicenses)
                .filter(license => this.selectedPermissiveLicenses[license]);
            const copyleftSelected = Object.keys(this.selectedCopyleftLicenses)
                .filter(license => this.selectedCopyleftLicenses[license]);

            // Combine selected values from both permissive and copyleft tables into a single array
            this.combinedSelectedLicenses = [...permissiveSelected, ...copyleftSelected];

            console.log("User selected Manually", this.combinedSelectedLicenses);
        },

    },
    mounted() {
        this.fetchLicenses();
    },
    filter: ref(""),
};
</script>

<style scoped>
.home-content {
    display: flex;
    justify-content: space-between;
    padding-bottom: 6rem;
    padding-top: 3rem;
}

.license-table {
    flex: 1;
    width: 35%;
    max-height: 350px;
    overflow-y: auto;
}

.license-table-content {
    height: 100%;
}

.sticky-header thead th {
    position: sticky;
    top: 0;
    z-index: 1;
    background-color: white;
}

.btn {
    text-transform: capitalize;
    background-color: #1A8917;
    text-transform: capitalize;
    color: white;
}

.custom-pos {
    transform: translateY(-103px);
}
</style>