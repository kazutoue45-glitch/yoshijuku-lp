// @ts-check
import { defineConfig } from 'astro/config';

// 義塾LP（寝屋川市成田町）
// 並行運用：
//  - GitHub Pages : https://kazutoue45-glitch.github.io/claude-code-keiei/yoshijuku/
//  - Vercel       : https://<project>.vercel.app/  （ルート公開、base なし）
// Vercel ビルド時は VERCEL=1 が自動セットされるので、それで分岐する
const isVercel = process.env.VERCEL === '1';

export default defineConfig({
  site: isVercel ? undefined : 'https://kazutoue45-glitch.github.io',
  base: isVercel ? '/' : '/claude-code-keiei/yoshijuku/',
  outDir: isVercel ? './dist' : '../../../../docs/yoshijuku',
  trailingSlash: 'ignore',
  server: {
    host: true,
  },
});
