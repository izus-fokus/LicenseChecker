<template>
  <q-footer elevated class="my-custom-footer q-mx-xl q-mt-md">
    <q-toolbar>
      <q-toolbar-title class="text-primary my-toolbar">
        The content of this site is licensed under the Creative Commons
        Attribution 4.0 Unported License.
      </q-toolbar-title>
      <q-tabs class="my-toolbar text-primary">
        <q-tab name="About" label="About" />
        <q-tab name="Terms" label="Terms" />
        <q-tab name="Imprint" label="Imprint" />
      </q-tabs>
    </q-toolbar>
  </q-footer>
</template>

<script>
export default {
  name: "FooterNav",
};
</script>

<style scoped>
.my-custom-footer {
  font-size: 14px;
  background-color: transparent;
}

.my-toolbar {
  font-size: 14px;
}
</style>
