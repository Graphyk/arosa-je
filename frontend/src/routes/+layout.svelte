<script lang="ts">
	import '../app.css';
	import dataProvider from '$lib/dataProvider';
	import { setContext } from 'svelte'
    import { NavigationBar, type NavItem } from '$lib/components/navigationBar';
    import { home, profile } from '$lib/icon';
	
	let { children } = $props();

	let navItems = $state<NavItem[]>([
		{
			path: '/home',
			icon: home
		},
		{
			path: '/profile',
			icon: profile
		},
	]);

	setContext("dataProvider", dataProvider)
</script>
<div class="font-base max-h-[100vh]">
	<NavigationBar 
		bind:items={navItems}
	/>
	<div class="h-[calc(100vh-var(--spacing)*16)]">
		{@render children()}
	</div>
</div>
