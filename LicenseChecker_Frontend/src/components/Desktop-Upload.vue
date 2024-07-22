<!-- <template>

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
            <q-chip removable @remove="abort" class="bg-primary text-white">
              {{ file.name }}
            </q-chip>
          </template>
        </q-uploader>
        <q-card-section v-if="files.length > 0">
          <q-btn label="Upload" color="primary" @click="uploadFiles" />
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
      files: []
    }
  },

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
  border: 2px dotted #2F60AC;

}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
</style> -->

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
        <q-uploader class=".custom-q-form" :url="uploadUrl" label="Click or Drop files here to upload"
          accept=".zip,.rar" :auto-upload="false" v-model="files" @added="onFileAdded" @failed="onUploadFailed"
          @uploading="onUploading">
          <template v-slot:file="{ file, abort }">
            <q-chip removable @remove="abort" class="bg-primary text-white">
              {{ file.name }}
            </q-chip>
          </template>
        </q-uploader>
        <q-card-section v-if="files.length > 0">
          <q-btn label="Upload" color="primary" @click="uploadFiles" />
        </q-card-section>
      </div>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DesktopUpload',
  data() {
    return {
      files: [],
      folderId: 4,  // Replace with your actual folder ID
      uploadUrl: '/repo/api/v1/uploads',  // Replace with your actual FOSSology API URL
      authToken: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjEyNjA3OTksIm5iZiI6MTcyMDU2OTYwMCwianRpIjoiTWpFdU13PT0iLCJzY29wZSI6IndyaXRlIn0.peALzdBwhcFnt5YADoZO9-euF1oNinRmfT9Co_AB5xk'  // Replace with your actual authorization token
    }
  },
  methods: {
    onFileAdded(files) {
      this.file = files[0];
      // Handle file added
      console.log('Files added:', files);
    },
    onUploadFailed(error) {
      // Handle upload failed
      console.error('Upload failed:', error);
    },
    onUploading(progress) {
      // Handle uploading progress
      console.log('Uploading:', progress);
    },
    async uploadFiles() {
      const formData = new FormData();
      this.files.forEach(file => {
        formData.append('fileInput', file);
      });

      try {
        const response = await axios.post(this.uploadUrl, formData, {
          headers: {
            'folderId': this.folderId,
            'uploadDescription': 'created by REST',
            'public': 'public',
            'Content-Type': 'multipart/form-data',
            'Authorization': this.authToken
          }
        });
        console.log('Upload successful:', response.data);
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    }

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
  border: 2px dotted #2F60AC;
}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
</style>
