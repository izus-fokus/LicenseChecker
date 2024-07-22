<template>
  <div>
    <div class="row q-mt-md justify-center">
      <div class="col-3 text-center q-pt-sm" style="border: dotted 1px; padding-bottom: none">
        <p class="text">Give your code a license to facilitate the reuse to your terms. </p>
      </div>
    </div>

    <div class="row" style="margin: 80px 0">
      <q-card-section class="hide" style="
          position: absolute;
          width: 75%;
          height: 35%;
          border-radius: 6px;
          transform: translate(160px, 100px);
          background-color: #2f61aca8;
        ">
      </q-card-section>
      <div class="col-12 col-md">
        <router-link to="/licenseRecommendation" style="text-decoration: none"
          @click="$parent.$emit('changeHeaderLabel', 'License Recommendation')">
          <q-card class="my-card small-screen rih">
            <img style="
                width: 90%;
                border-radius: 15px;
                margin: 0 auto;
                padding-top: 2px;
              " src="\src\assets\License-Recommendation.svg" />

            <q-card-section>
              <div class="text">Licence Recommendation</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              I have an existing code and need a recommendation for a compatible license
            </q-card-section>
          </q-card>
        </router-link>
      </div>
      <div class="col-12 col-md">
        <router-link to="/LicenseSearch" style="text-decoration: none"
          @click="$parent.$emit('changeHeaderLabel', 'License Search')">
          <q-card class="my-card small-screen" style="margin: 0 auto">
            <img style="
                width: 90%;
                border-radius: 15px;
                margin: 0 auto;
                padding-top: 2px;
              " src="\src\assets\License-Search.svg" />

            <q-card-section>
              <div class="text">License Search</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              I want to explore existing open source licenses and learn more about their properties and compatibility
            </q-card-section>
          </q-card>
        </router-link>
      </div>
      <div class="col-12 col-md">
        <router-link to="/help" style="text-decoration: none" @click="$parent.$emit('changeHeaderLabel', 'Help')">
          <q-card class="my-card small-screen">
            <img style="
                width: 90%;
                border-radius: 15px;
                margin: 0 auto;
                padding-top: 2px;
              " src="\src\assets\License-Help.svg" />

            <q-card-section>
              <div class="text">Help</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              I need help to find the right license for my software
            </q-card-section>
          </q-card>
        </router-link>
      </div>
    </div>
  </div>
  <h6 style="font-size: smaller;">The information provided via this service is of a general nature and is for
    information purposes only. It does not constitute legal advice. If you need legal advice for your individual
    situation, you should seek the advice of a
    qualified lawyer.</h6>
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
  padding-top: 3px;
}

.my-card {
  width: 50%;
  /* height: 17.5rem; */
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
