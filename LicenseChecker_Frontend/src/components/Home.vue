<template>
  <div class="home-content">
    <div class="row q-mt-md justify-center">
      <div class="col-3 text-center" style="border: dotted 1px; height:43px;; width:inherit;">
        <q-item>
          <q-item-section>
            <p class="text">Give your code a license to facilitate the reuse to
              your terms</p>
          </q-item-section>

          <q-avatar size="21px" style="padding:3px 5px 0 0">
            <img src="/questionMark.svg" />
            <q-tooltip max-width="500px" class="bg-primary text-secondary shadow-4" :offset="[12, 22]">
              If your code reuses libraries or other third-party code that is already licensed, you are not free in your
              choice of a software license for your own code.
            </q-tooltip>
          </q-avatar>

        </q-item>
      </div>
    </div>

    <div class="row" style="margin: 80px 0">
      <q-card-section class="hide reponsive-card large-screen" style="
       
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

            <q-card-section class="q-pt-none text-justify text-secondary">
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

            <q-card-section class="q-pt-none text-justify text-secondary">
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

            <q-card-section class="q-pt-none text-justify text-secondary">
              I need help to find the right license for my software
            </q-card-section>
          </q-card>
        </router-link>
      </div>
    </div>
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
  color: #323232;
  font-weight: bold;
  padding-top: 3px;
  margin: 0 4px 9px 4px;
}

.my-card {
  width: 50%;
  height: 19rem;
  border: none;
  border-width: 0;
  box-shadow: none;
  border-radius: 15px;
}

.reponsive-card {
  position: absolute;
  width: 75%;
  height: 15rem;
  border-radius: 6px;
  transform: translate(160px, 100px);
  background-color: #2f61aca8;
}

.rih {
  float: right;
}

.home-content {
  padding-bottom: 6rem;
  padding-top: 1rem;
  /* Add bottom padding for space between content and footer */
}

@media (min-width: 1333px) {

  .small-screen {
    float: none;
    margin: 10px auto;
  }

  .hide {
    visibility: hidden;
  }
}
</style>
