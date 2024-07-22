<template>
  <div class="q-mx-xl q-mt-md">
    <q-toolbar class="q-no-bg no-border">
      <router-link to="/" @click="$emit('changeHeaderLabel', 'License Checker')"
        v-if="header_label != 'License Checker'">
        <q-btn size="md" flat color="primary" icon="img:/home.svg"></q-btn>
      </router-link>
      <q-toolbar-title class="text-center text-primary text-h4">
        {{ header_label }}
      </q-toolbar-title>
      <!-- <q-btn size="md" flat color="primary" icon="menu"></q-btn> -->
    </q-toolbar>

    <hr style="margin: 0; color: #909cad" />
  </div>
</template>

<script>

export default {
  name: "Header-Nav",
  props: ["header_label"],

};
</script>
<style scoped>
h4 {
  color: #2f60ac;

}
</style>
