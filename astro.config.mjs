// @ts-check
import { defineConfig } from 'astro/config';

// 義塾LP - 公開URL: https://kazutoue45-glitch.github.io/yoshijuku-lp/
export default defineConfig({
  site: 'https://kazutoue45-glitch.github.io',
  base: '/yoshijuku-lp/',
  outDir: './docs',
  trailingSlash: 'ignore',
  server: {
    host: true,
  },
});
