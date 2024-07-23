<template>
  <div class="row">
    <div class="col-6 q-pa-xl">
      <h6>{{ license.name }}</h6>

      <h6><span v-html="license.description"></span></h6>

      <div class="q-pa-md border-primary pillshapedborder">

        <q-expansion-item v-model="expanded" icon="img:/Compatible.svg" label="Compatible Licenses"
          class="text-primary text-h6 text-center" @click="
            $parent.$emit('listCompatibleLicenses', this.compatibleLicenses)
            ">
          <q-card>
            <q-card-section>
              <q-list dense padding class="rounded-borders">
                <q-table color="primary" :visible-columns="visibleColumns" table-class="text-grey-8"
                  table-header-class="text-brown" flat :rows="detailedCompatibleLicenses" row-key="name"></q-table>
              </q-list>
            </q-card-section>
            <q-btn to="/compatibleLicenses" label="Detailed View" color="primary" @click="
              $parent.$emit('changedetailedCompatibleLicensesId', [
                license.id,
              ])
              " />
          </q-card>
        </q-expansion-item>
      </div>

      <div class="q-pa-md q-mt-lg border-primary pillshapedborder">
        <q-expansion-item icon="img:/permission.svg" label="Permissions" class="text-primary text-h6 text-center">
          <q-card>
            <q-card-section>
              <span v-for="(per, i) in license.permissions" :key="i">
                <q-list>
                  <q-item>
                    <q-item-section>
                      <q-item-label>{{ per.name }}</q-item-label>
                      <q-item-label caption lines="2">{{
                        per.description
                      }}</q-item-label>
                    </q-item-section>

                    <q-item-section side top>
                      <q-icon :name="this.iconvar + per.id + '.svg'" class="q-mr-sm"></q-icon>
                    </q-item-section>
                  </q-item>

                  <q-separator spaced inset></q-separator> </q-list></span>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </div>
      <div class="q-pa-md q-mt-lg border-primary pillshapedborder">
        <q-expansion-item icon="img:/condition.svg" label="Conditions" class="text-primary text-h6 text-center">
          <q-card>
            <q-card-section>
              <span v-for="(cond, i) in license.conditions" :key="i">
                <q-list>
                  <q-item>
                    <q-item-section>
                      <q-item-label>{{ cond.name }}</q-item-label>
                      <q-item-label caption lines="2">{{
                        cond.description
                      }}</q-item-label>
                    </q-item-section>

                    <q-item-section side top>
                      <q-icon :name="this.iconvar + cond.id + '.svg'" class="q-mr-sm"></q-icon>
                    </q-item-section>
                  </q-item>

                  <q-separator spaced inset></q-separator> </q-list></span>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </div>
      <div class="q-pa-md q-mt-lg border-primary pillshapedborder">
        <q-expansion-item icon="img:/limitation.svg" label="Limitations" class="text-primary text-h6 text-center">
          <q-card>
            <q-card-section>
              <span v-for="(lim, i) in license.limitations" :key="i">
                <q-list>
                  <q-item>
                    <q-item-section>
                      <q-item-label>{{ lim.name }}</q-item-label>
                      <q-item-label caption lines="2">{{
                        lim.description
                      }}</q-item-label>
                    </q-item-section>

                    <q-item-section side top>
                      <q-icon :name="this.iconvar + lim.id + '.svg'" class="q-mr-sm"></q-icon>
                    </q-item-section>
                  </q-item>

                  <q-separator spaced inset></q-separator> </q-list></span>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </div>
      <br />
    </div>
    <div class="col-6 q-pa-xl border-primary">
      <q-scroll-area style="
          height: 100%;
          max-width: 100%;
          border: 1px solid black;
          border-radius: 4px;
          padding: 10px;
        ">
        <span v-html="licenseText"></span></q-scroll-area>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LicenseDetails",
  props: ["licenseid", "detailedCompatibleLicenses"],
  data() {
    return {
      license: {},
      licenseText: null,
      iconvar: "img:/",
      compatibleLicenses: [],
      expanded: false,
      visibleColumns: ["id", "name"],
    };
  },
  beforeMount: function () {
    /* get the license id from session storage to make it persisten */
    axios
      .get(
        "http://127.0.0.1:8000/licenses/" + sessionStorage.getItem("licenseid")
      )
      .then(
        (response) => (this.license = response.data)

      );
    axios
      .get(
        "http://127.0.0.1:7000/api/v1/licenses/" +
        sessionStorage.getItem("licenseid") +
        "/text",
        {
          headers: {
            Accept: "text/html",
          },
        }
      )
      .then((response) => (this.licenseText = response.data));

    axios
      .post("http://127.0.0.1:8000/licenses/check/", [
        sessionStorage.getItem("licenseid"),
      ])
      .then((response) => {
        this.compatibleLicenses = response.data;
      })
      .catch((error) => {
        console.error("Error fetching results:", error);
      });
  },
};
</script>
<style>
.pillshapedborder {
  border: 2px solid #2f61aca8;
  border-radius: 20px;
}
</style>
