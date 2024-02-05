<!-- <template> -->
<!-- <div class="q-mx-xl q-mt-md" style="border-top: solid 0.5px  #2F60AC;"> -->
<!-- <q-footer elevated class="q-no-bg no-border text-primary q-mx-xl q-mt-md" style="border-top: solid 0.5px  #2F60AC;">
8.	    <q-toolbar class="q-no-bg no-border">
9.	      <q-toolbar-title class="text-accent my-toolbar">
10.	        The content of this site is licensed under the Creative Commons
11.	        Attribution 4.0 Unported License.
12.	      </q-toolbar-title>
13.	      <q-tabs class="my-toolbar text-primary">
14.	        <q-tab name="About" label="About" />
15.	        <q-tab name="Terms" label="Terms" />
16.	        <q-tab name="Imprint" label="Imprint" />
17.	      </q-tabs>
18.	    </q-toolbar>
19.	  </q-footer>
20.	</template>
21.	
22.	<script>
23.	export default {
24.	  name: "Footer-Nav",
25.	};
26.	</script>
27.	<style scoped>
28.	.my-toolbar {
29.	  font-size: 14px;
30.	}
31.	</style> -->

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

  /* border-top: solid 0.25px #2F60AC; */

  /* dd any other custom styles here */
}

.my-toolbar {
  font-size: 14px;
}
</style>
