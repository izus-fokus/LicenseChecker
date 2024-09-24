<template>
  <div>
    <div class="q-pa-md">
      <div v-if="this.detailedCompatibleLicensesId.length > 0">
        <h5 class="text-primary">
          Detailed List Of Compatible Licenses with
          <!-- change the line below for multiple items -->
          <span class="text-primary q-pr-md" v-for="(compId, k) in detailedCompatibleLicensesId" :key="k">{{ compId }}
          </span>
        </h5>
        <q-table ref="table" :rows="detailedCompatibleLicenses" flat bordered row-key="name"
          :visible-columns="visibleColumns" :filter="filter" v-if="this.detailedCompatibleLicenses.length > 0">
          <template v-slot:top-left>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Search" rounded outlined>
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>

          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td v-for="col in props.cols" :key="col.name" :props="props">
                <span v-if="col.name == 'conditions'"><span v-for="(cond, i) in col.value" :key="i">
                    <q-tooltip class="bg-primary">
                      {{ cond.description }}
                    </q-tooltip>
                    <q-icon :name="this.iconvar + cond.id + '.svg'" class="q-mr-sm" size="25px"></q-icon>
                  </span></span>
                <span v-else-if="col.name == 'name'">
                  <router-link to="LicenseDetails" @click="$parent.$emit('changeLicenseName', props.row.id)">
                    {{ col.value }}
                  </router-link>
                </span>

                <span v-else-if="col.name == 'permissions'"><span v-for="(per, i) in col.value" :key="i">
                    <q-tooltip class="bg-primary">
                      {{ per.description }}
                    </q-tooltip>
                    <q-icon :name="this.iconvar + per.id + '.svg'" class="q-mr-sm" size="25px"></q-icon></span></span>
                <span v-else-if="col.name == 'limitations'"><span v-for="(lim, i) in col.value" :key="i">
                    <q-icon :name="this.iconvar + lim.id + '.svg'" class="q-mr-sm" size="25px"></q-icon><q-tooltip
                      class="bg-primary">
                      {{ lim.description }}
                    </q-tooltip></span></span>
                <span v-else-if="col.name == 'compatibility'"><span v-for="(comp, i) in col.value" :key="i">{{ comp
                    }}<br /></span></span>
                <span v-else-if="col.name == 'type'"><q-tooltip class="bg-primary">{{
                  col.value.description
                }}</q-tooltip>
                  {{ col.value.id }}</span>

                <span v-else> {{ col.value }}</span>
              </q-td>
            </q-tr>
          </template>
        </q-table>
        <h5 v-else>No license was found that is compatible to all selected licenses</h5>
      </div>
      <h5 v-else>No Licenses Selected</h5>
      <q-btn color="primary" glossy label="Back" @click="$router.back()"></q-btn>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  name: "CompatibleLicenses",
  props: [
    "detailedCompatibleLicenses",
    "licenseid",
    "detailedCompatibleLicensesId",
  ],
  data() {
    return {
      iconvar: "img:/",
      visibleColumns: [
        "id",
        "name",
        "permissions",
        "limitations",

        "conditions",
        "type",
      ],
      filter: ref(""),
    };
  },
};
</script>
