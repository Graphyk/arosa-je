import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
	preprocess: vitePreprocess(),
	kit: { adapter: adapter({ fallback: 'index.html', pages: 'dist', assets: 'dist' }) },
	server: {
		proxy: { '/api': 'http://back:8000' },
		host: 'localhost',
	},
};

export default config;
