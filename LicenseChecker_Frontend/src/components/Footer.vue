<template>
  <q-footer elevated class="custom-footer">
    <q-toolbar class="footer-top">
      <q-toolbar-title class="text-primary q-mx-xl q-mt-md footer-title">
        <q-avatar class="custom-img">
          <img src="/public/CC.svg" />
        </q-avatar>
        The content of this site is licensed under the Creative Commons
        Attribution 4.0 Unported License.
      </q-toolbar-title>

      <q-tabs class="text-primary q-mx-xl q-mt-md" style="font-size: 12px;">
        <q-tab name="About" label="About"
          @click="navigateTo('https://www.izus.uni-stuttgart.de/fokus/services/licensechecker/')" />
        <q-tab name="Terms" label="Terms"
          @click="navigateTo(' https://www.izus.uni-stuttgart.de/fokus/services/licensechecker/nutzungsbedingungenhttps://www.izus.uni-stuttgart.de/en/fokus/services/licensechecker/termsofuse/')" />
        <q-tab name="Privacy" label="Privacy Policy"
          @click="navigateTo('https://www.izus.uni-stuttgart.de/en/fokus/services/licensechecker/privacy/')" />
        <q-tab name="Imprint" label="Imprint" @click="navigateTo('https://www.uni-stuttgart.de/en/legal-notice')" />
      </q-tabs>
    </q-toolbar>

    <hr class="q-mx-xl" style="border: 1px solid #E0E7F2; " />

    <q-toolbar class="footer-bottom">
      <q-toolbar-title style="  overflow: visible; /* Ensure that overflow is visible */
  white-space: normal; " class="disclaimer-text text-primary q-mx-xl q-mt-md">
        <q-avatar>
          <img style="width: 24px; height: 24px;" src="/public/disclaimer.svg" />
        </q-avatar>

        <span style="display: block;">
          The information provided via this service is of a general nature and is
          for information purposes only. It does not constitute legal advice. If you need legal advice for your
          individual
          situation, you should seek the advice of a qualified lawyer.
        </span>

      </q-toolbar-title>
    </q-toolbar>
  </q-footer>
</template>
<script>
export default {
  name: "FooterNav",
  methods: {
    navigateTo(url) {
      window.open(url, '_blank'); // Open the URL in a new tab
    }
  }
}
</script>
<style scoped>
.custom-footer {
  background-color: #323232;
}

.footer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;

}

.footer-title {
  display: flex;
  align-items: center;
  flex: 1;
  font-size: 12px;

}

.disclaimer-text.highlight {
  border: 2px solid red;
  background-color: #323232;
  transition: border 0.5s ease-in-out;
  padding-bottom: 10px;

}

.custom-img {
  width: 22px;
  height: 22px;
  margin-right: 8px;
}

.footer-bottom {
  display: flex;
  align-items: center;
  padding-bottom: 0.2rem;


}

.disclaimer-text {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 350;
  line-height: 1.5;
  padding-bottom: 1rem;
}

/* Avatar inside disclaimer */
.disclaimer-avatar img {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  /* Space between image and text */
}

/* Responsive Styles */
@media (max-width: 600px) {
  .footer-title {
    font-size: 12px;
    /* Smaller font size for mobile */
    text-align: center;
    /* Center-align text on small screens */
  }

  .disclaimer-text {
    font-size: 10px;

    /* Smaller font size for mobile */
    text-align: center;
    /* Center-align text on small screens */
  }

  .custom-img {
    width: 20px;
    height: 20px;
  }
}
</style>

<!-- <template>
  <q-footer elevated class="custom-footer">
    <q-toolbar>

      <q-toolbar-title class="text-primary text q-mx-xl q-mt-md">
        <q-avatar class="custom-img">
          <img src="/public/CC.svg" />
        </q-avatar>
        The content of this site is licensed under the Creative Commons
        Attribution 4.0 Unported License.
      </q-toolbar-title>

      <q-tabs class=" text-primary text q-mx-xl q-mt-md">
        <q-tab name="About" label="About" />
        <q-tab name="Terms" label="Terms" />
        <q-tab name="Imprint" label="Imprint" />
      </q-tabs>
    </q-toolbar>
    <hr class="q-mx-xl q-mt-md" style="border: 1px solid #E0E7F2; " />

    <q-toolbar>
      <q-toolbar-title class="disclaimer-text text-primary q-mx-xl q-mt-md">
        <q-avatar>
          <img style="width: 24px; height: 24px;" src="/public/disclaimer.svg" />
        </q-avatar>
        <span>
          The information provided via this service is of a general nature and is
          for
          information purposes only. It does not constitute legal advice. If you need legal advice for your individual
          situation, you should seek the advice of a qualified lawyer. </span>
      </q-toolbar-title>
    </q-toolbar>
  </q-footer>
</template>

<script>
export default {
  name: "FooterNav",
};
</script>

<style scoped>
.disclaimer-text {
  display: inline-block;
  font-size: 12px;
  font-weight: 300;
  /* Light weight font */
  display: flex;
  align-items: center;

  /* Align the avatar and text vertically */
  line-height: 1.5;

}



@media (max-width: 600px) {
  .disclaimer-text {
    font-size: 12px;
    /* Smaller font for mobile devices */
  }

  .disclaimer-text img {
    width: 20px;
    /* Smaller avatar size on mobile */
    height: 20px;
  }
}

.custom-footer {
  background-color: transparent;
}

.custom-img {
  width: 30px;
  height: 28px;
}


.text {
  font-size: 12px;
  color: #2f60ac;
  font-weight: 500;
}
</style> -->
