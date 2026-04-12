import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

// Update `site` to your production URL once DNS is pointed.
// It's used by absolute URL helpers and canonical tags.
// (To enable a sitemap later: `npx astro add sitemap`.)
export default defineConfig({
  site: 'https://example.com',
  integrations: [mdx()],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
      wrap: true,
    },
  },
});
