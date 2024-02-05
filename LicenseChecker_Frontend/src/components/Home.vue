<template>
  <div>
    <div class="row q-mt-md justify-center">
      <div
        class="col-3 text-center q-pt-sm"
        style="border: dotted 1px; padding-bottom: none"
      >
        <p class="text">Choose an Open Source Licence</p>
      </div>
    </div>

    <div class="row" style="margin: 80px 0">
      <q-card-section
        class="hide"
        style="
          position: absolute;
          width: 75%;
          height: 35%;
          border-radius: 6px;
          transform: translate(160px, 100px);
          background-color: #2f61aca8;
        "
      >
      </q-card-section>
      <div class="col-12 col-md">
        <router-link
          to="/licenseRecommendation"
          style="text-decoration: none"
          @click="$parent.$emit('changeHeaderLabel', 'License Recommendation')"
        >
          <q-card class="my-card small-screen rih">
            <img
              style="
                width: 90%;
                border-radius: 15px;
                margin: 0 auto;
                padding-top: 2px;
              "
              src="\src\assets\License-Recommendation.svg"
            />

            <q-card-section>
              <div class="text">Licence Recommendation</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              I need Licence recommendation for existing code
            </q-card-section>
          </q-card>
        </router-link>
      </div>
      <div class="col-12 col-md">
        <router-link
          to="/LicenseSearch"
          style="text-decoration: none"
          @click="$parent.$emit('changeHeaderLabel', 'License Search')"
        >
          <q-card class="my-card small-screen" style="margin: 0 auto">
            <img
              style="
                width: 90%;
                border-radius: 15px;
                margin: 0 auto;
                padding-top: 2px;
              "
              src="\src\assets\License-Search.svg"
            />

            <q-card-section>
              <div class="text">License Search</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              I need help to get the right license
            </q-card-section>
          </q-card>
        </router-link>
      </div>
      <div class="col-12 col-md">
        <router-link
          to="/help"
          style="text-decoration: none"
          @click="$parent.$emit('changeHeaderLabel', 'Help')"
        >
          <q-card class="my-card small-screen">
            <img
              style="
                width: 90%;
                border-radius: 15px;
                margin: 0 auto;
                padding-top: 2px;
              "
              src="\src\assets\License-Help.svg"
            />

            <q-card-section>
              <div class="text">Help</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              I want to search for the Licence
            </q-card-section>
          </q-card>
        </router-link>
      </div>
    </div>

    <!-- <b-container>
    <b-row align-h="center" class="pb-5">
      <b-col class="text-center" cols="3">
        <h6>Choose an Open Source License</h6>
      </b-col>
    </b-row>
    <div>
      <b-card-group deck style="padding-left: 200px">
        <router-link
          to="/licenseRecommendation"
          class="text-decoration-none text-black"
          @click="$parent.$emit('changeHeaderLabel','License Recommendation')"
        >
          <b-card
            title="License Recommendation"
            title-tag="h5"
            img-src="/src/assets/License-Recommendation.svg"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 15rem; font-size: medium; min-height: 20.3rem"
            class="mb-2"
          >
            <b-card-text>
              I need licence recommendation for my existing code.
            </b-card-text>
          </b-card>
        </router-link>
        <router-link
          to="/LicenseSearch"
          class="text-decoration-none text-black"
          @click="$parent.$emit('changeHeaderLabel','License Search')"
        >
          <b-card
            title="License Search"
            title-tag="h5"
            img-src="/src/assets/License-Search.svg"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 15rem; font-size: medium; min-height: 20.3rem"
            class="mb-2"
          >
            <b-card-text> I want to search for the Licence/es. </b-card-text>
          </b-card>
        </router-link>

        <b-card
          title="Help"
          title-tag="h5"
          img-src="/src/assets/License-Help.svg"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 15rem; font-size: medium; min-height: 20rem"
          class="mb-2"
        >
          <b-card-text> I need help to get the right license/es. </b-card-text>
        </b-card>
      </b-card-group>
    </div>
  </b-container> -->
  </div>
</template>

<script>
export default {
  name: "Home-Page",
};
</script>

<style scoped>
.text {
  font-size: 14px;
  color: #2f60ac;
  font-weight: bold;
}
.my-card {
  width: 50%;
  height: 17.5rem;
  border: none;
  border-width: 0;
  box-shadow: none;
  border-radius: 15px;
}

.rih {
  float: right;
}
@media (max-width: 992px) {
  .small-screen {
    float: none;
    margin: 10px auto;
  }
  .hide {
    visibility: hidden;
  }
}
</style>
