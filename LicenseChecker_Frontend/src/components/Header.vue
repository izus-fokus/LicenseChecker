<template>
  <q-header reveal elevated class="my-custom-header ">
    <q-toolbar class="q-no-bg no-border">
      <router-link to="/" @click="$emit('changeHeaderLabel', 'License Checker')"
        v-if="header_label != 'License Checker'">
        <q-btn size="md" flat color="primary" icon="img:/home.svg"></q-btn>
      </router-link>

      <q-toolbar-title class=" custom_title text-primary">
        <q-avatar style="border-radius: 7px; margin-right: 7px;">
          <img :src="header_icon" alt="icon" />
        </q-avatar>

        {{ header_label }}
        <q-btn class="exclaim-btn" flat color="primary" icon="img:/exclaimation.svg" @click="scrollToDisclaimer"
          aria-label="Scroll to Disclaimer" />
      </q-toolbar-title>

      <!-- <q-btn flat color="primary" icon="img:/unistuttgart_logo_de.svg" /> -->
      <img class="header-logo1" src="\NFDI4ING_logo.svg"
        @click="navigateTo('https://nfdi4ing.de/')" />

      <!-- <q-btn flat color="primary" icon="img:/NFDI4ING_logo.svg" /> -->
      <img class="header-logo2" src="\unistuttgart_logo_de.svg"
        @click="navigateTo('https://izus.uni-stuttgart.de/fokus')" />

    </q-toolbar>
  </q-header>
</template>

<script>

export default {
  name: "Header-Nav",
  props: ["header_label", "header_icon"],
  methods: {
    scrollToDisclaimer() {
      // Emit an event to scroll to the disclaimer in the footer
      this.$emit('scroll-to-disclaimer');
      console.log("In header method");
    },
    navigateTo(url) {
      window.open(url, '_blank'); // Open the URL in a new tab
    }
  }
};
</script>
<style scoped>
.custom_title {
  font-size: 30px;
  display: flex;
  align-items: center;
  /* Vertically center title content */
  justify-content: center;
  /* Center title content horizontally */
  flex-grow: 1;
  /* Take up remaining space in the toolbar */
  position: relative;
}



.custom_title {
  display: flex;
  align-items: center;
  /* Vertically center the avatar, title, and button */
  justify-content: center;
  /* Ensure title is centered */
  position: absolute;
  /* Center absolutely to the page */
  left: 50%;
  transform: translateX(-50%);
  /* Offset by 50% to center it exactly */
}

.my-custom-header {
  background-color: rgb(0, 81, 158);
}

.custom_title {
  padding-top: 8px;
  padding-bottom: 10px;
}

.header-logo1 {
  margin-right: auto;
  /* Push the logo to the right side */
  width: 11%;
  /* Set a more reasonable width for the logo */
  height: auto;
  cursor: pointer;
}

.header-logo2 {
  margin-left: auto;
  /* Push the logo to the right side */
  width: 11%;
  /* Set a more reasonable width for the logo */
  height: auto;
  cursor: pointer;
}

.exclaim-btn {
  margin-left: 8px;
  /* Adjust spacing from the label */
  margin-bottom: 14px;
  font-size: 10px;

  height: 20px;
  /* Control the height of the button */
  width: 20px;
  /* Control the width of the button */
  padding: 0;
  /* Remove any extra padding */
  display: inline-block;
}
</style>
