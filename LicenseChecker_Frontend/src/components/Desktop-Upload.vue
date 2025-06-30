<template>

  <q-page>

    <div class="row q-mx-xl q-mt-md center-container" :class="{
      'custom-background-color': !$q.screen.lt.md,
      'max-width-1000': !$q.screen.lt.md,
      'margin-20-auto-0': !$q.screen.lt.md,
    }">
      <div class="col" :class="{
        'max-width-700': !$q.screen.lt.md,
        'flex-center': !$q.screen.lt.md,
      }">
        <q-uploader class=".custom-q-form" url="/api/upload" label="Click or Drop files here to upload"
          accept=".zip,.rar" :auto-upload="false" v-model="files" @added="onFileAdded" @failed="onUploadFailed"
          @uploading="onUploading">
          <template v-slot:file="{ file, abort }">
            <q-chip removable @remove="abort" class="bg-primary text-secondary">
              {{ file.name }}
            </q-chip>
          </template>
        </q-uploader>
        <q-card-section v-if="files.length > 0">
          <q-btn label="Upload" color="secondary" @click="uploadFiles" />
        </q-card-section>
      </div>
    </div>
  </q-page>

</template>

<script>
export default {
  name: 'DesktopUpload',
  data() {
    return {
      files: [],
      onUploading: false,
      onFileAdded: false,
      onUploadFailed: false,
    }
  },
  methods:{
    
  }

}
</script>
<style scoped>
.max-width-1000 {
  max-width: 1000px;
}

.max-width-700 {
  max-width: 700px;
}

.margin-20-auto-0 {
  margin: 20px auto 0;
}

.flex-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.custom-background-color {
  border: 2px dotted #004191;

}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
</style>
