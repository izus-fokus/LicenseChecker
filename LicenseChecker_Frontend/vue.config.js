// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { quasar, transformAssetUrls } from '@quasar/vite-plugin';

// Use `defineConfig` to export the configuration as an ES module
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    quasar({
      sassVariables: 'src/quasar-variables.sass',
      importStrategy: 'kebab',
      rtlSupport: false,
    }),
  ],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  transpileDependencies: ['quasar'],
});
