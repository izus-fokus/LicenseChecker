<template>
  <div class="q-pa-md">
    <q-table
      ref="table"
      :rows="allLicenses"
      flat
      bordered
      row-key="name"
      :visible-columns="visibleColumns"
      :filter="filter"
      column-sort-order="ad"
    >
      <template v-slot:top-left>
        <q-input
          borderless
          dense
          debounce="300"
          v-model="filter"
          placeholder="Search"
          rounded
          outlined
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <span v-if="col.name == 'id'"
              ><q-checkbox
                v-model="selectedLicensesCompatibilityCheck"
                :val="col.value"
                color="teal"
              ></q-checkbox
            ></span>
            <span v-if="col.name == 'conditions'"
              ><span v-for="(cond, i) in col.value" :key="i">
                <q-tooltip class="bg-primary">
                  {{ cond.description }}
                </q-tooltip>
                <q-icon
                  :name="this.iconvar + cond.id + '.svg'"
                  class="q-mr-sm"
                  size="25px"
                ></q-icon>

                <!-- {{ cond.name }} -->
              </span></span
            >
            <span v-else-if="col.name == 'name'">
              <router-link
                to="LicenseDetails"
                @click="
                  $parent.$emit('changeLicenseName', props.row.id);
                  $parent.$emit('changedetailedCompatibleLicensesId', [
                    props.row.id,
                  ]);
                "
              >
                {{ col.value }}
              </router-link>
            </span>

            <span v-else-if="col.name == 'permissions'"
              ><span v-for="(per, i) in col.value" :key="i">
                <q-tooltip class="bg-primary">
                  {{ per.description }}
                </q-tooltip>
                <q-icon
                  :name="this.iconvar + per.id + '.svg'"
                  class="q-mr-sm"
                  size="25px"
                ></q-icon></span
            ></span>
            <span v-else-if="col.name == 'limitations'"
              ><span v-for="(lim, i) in col.value" :key="i">
                <q-icon
                  :name="this.iconvar + lim.id + '.svg'"
                  class="q-mr-sm"
                  size="25px"
                ></q-icon
                ><q-tooltip class="bg-primary">
                  {{ lim.description }}
                </q-tooltip></span
              ></span
            >
            <span v-else-if="col.name == 'compatibility'"
              ><span v-for="(comp, i) in col.value" :key="i"
                >{{ comp }}<br /></span
            ></span>
            <span v-else-if="col.name == 'type'"
              ><q-tooltip class="bg-primary">{{
                col.value.description
              }}</q-tooltip>
              {{ col.value.id }}</span
            >

            <span v-else> {{ col.value }}</span>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <!-- $parent.$emit('listCompatibleLicenses', this.compatibleLicenses) -->
    <q-btn
      @click="
        $parent.$emit(
          'changedetailedCompatibleLicensesId',
          this.selectedLicensesCompatibilityCheck
        )
      "
      to="/compatibleLicenses"
      label="Detailed View"
      color="primary"
    />
  </div>
</template>

<script>
import { ref } from "vue";
//import axios from "axios";

export default {
  name: "License-Search",
  props: ["allLicenses"],
  data() {
    return {
      licenses: [],
      iconvar: "img:/",
      selectedLicensesCompatibilityCheck: [],
      filteredLicenses: this.licenses,
      compatibleLicenses: [],
      visibleColumns: [
        "id",
        "name",
        "permissions",
        "limitations",

        "conditions",
        "type",
      ],

      methods: {
        compatibleLicensesCheck: function () {
          console.log("this is called");
          axios
            .post(
              "http://127.0.0.1:8000/licenses/check/",
              this.selectedLicensesCompatibilityCheck
            )
            .then((response) => {
              this.compatibleLicenses = response.data;
            })
            .catch((error) => {
              console.error("Error fetching results:", error);
            });
        },
      },
      filter: ref(""),

      // url:this.allLicenses.url
      // columnName:this.allLicenses.flatMap(x => Object.keys(x)),
    };
  },

  // beforeCreate: function () {
  //   axios.get("http://127.0.0.1:8000/licenses/").then(
  //     (response) => (this.licenses = response.data)
  //     //this.allLicensesFields=Object.values(Object.values(this.allLicenses)
  //   );

  // },
};
</script>
