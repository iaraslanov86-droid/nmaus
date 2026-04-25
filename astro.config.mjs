import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://nmaus.ru',
  trailingSlash: 'always',
  build: {
    format: 'directory',
    inlineStylesheets: 'auto'
  },
  compressHTML: true,
  integrations: [
    sitemap({
      changefreq: 'weekly',
      lastmod: new Date(),
      serialize(item) {
        const u = item.url;
        const depth = (u.replace('https://nmaus.ru/', '').match(/\//g) || []).length;
        if (u === 'https://nmaus.ru/') return { ...item, priority: 1.0, changefreq: 'daily' };
        if (u.includes('/about/')) return { ...item, priority: 0.9 };
        if (depth === 1) return { ...item, priority: 0.8 };
        if (depth === 2) return { ...item, priority: 0.7 };
        return { ...item, priority: 0.6 };
      }
    })
  ]
});
