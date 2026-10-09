import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import regions from './src/data/regions.json';

// Страницы услуг регионов с одним городом неканонические (дублируют городские) — в sitemap не нужны
const singleCityRegions = Object.values(regions).filter(r => r.cities.length === 1).map(r => r.slug);

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
      filter: (page) => !singleCityRegions.some(slug => new RegExp(`^https://nmaus\\.ru/${slug}/[^/]+/$`).test(page)),
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
