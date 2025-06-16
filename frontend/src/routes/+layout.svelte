<script lang="ts">
	import '../app.css';
	import dataProvider from '$lib/dataProvider';
	import { setContext } from 'svelte'
	
	let { children } = $props();

	setContext("dataProvider", dataProvider)
</script>

{@render children()}
