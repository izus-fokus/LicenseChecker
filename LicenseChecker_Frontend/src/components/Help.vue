<template>
  <div class="help-content q-pa-md">
    <h5 class="text-center text-primary">FoKUS – Kompetenzzentrum für Forschungsdaten</h5>

    <div class="contact-info q-mt-lg q-pa-lg">
      <!-- Phone Information -->
      <div class="info-item row q-mb-md">
        <q-icon name="phone" class="icon" />
        <p class="info-text">+49 711 685 88028</p>
      </div>

      <!-- Email Information -->
      <div class="info-item row q-mb-md">
        <q-icon name="email" class="icon" />
        <p class="info-text">
          <a href="mailto:fokus@izus.uni-stuttgart.de" class="link">E-Mail schreiben</a>
        </p>
      </div>

      <!-- Further Information Link -->
      <div class="info-item row q-mb-md">
        <q-icon name="language" class="icon" />
        <p class="info-text">
          <a href="https://www.izus.uni-stuttgart.de/fokus/" target="_blank" class="link">
            Weitere Informationen
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelpPage",
};
</script>

<style scoped>
.help-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 600px;
  margin: auto;
}

.contact-info {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.info-item {
  display: flex;
  align-items: center;
}

.icon {
  font-size: 24px;
  color: #2f60ac;
  margin-right: 10px;
}

.info-text {
  font-size: 16px;
  color: #2f60ac;
}

.link {
  text-decoration: none;
  color: #2f60ac;
}

.link:hover {
  text-decoration: underline;
}
</style>
