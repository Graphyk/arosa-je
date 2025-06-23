<script lang="ts">
	import '../app.css';
	import dataProvider from '$lib/dataProvider';
	import { setContext } from 'svelte'
    import { NavigationBar, type NavItem } from '$lib/components/navigationBar';
    import { Home, Profile } from '$lib/icon';
    import authProvider from '$lib/authProvider';
	
	let { children } = $props();

	let navItems = $state<NavItem[]>([
		{
			path: '/home',
			icon: Home
		},
		{
			path: '/profile',
			icon: Profile
		},
	]);

	setContext("dataProvider", dataProvider)
</script>
<div class="font-base max-h-[100vh]">
	{#if authProvider.isAuthenticated()}
		<NavigationBar 
		bind:items={navItems}
		/>
	{/if}
	<div class={authProvider.isAuthenticated() ? "h-[calc(100vh-var(--spacing)*16)]" : ''}>
		{@render children()}
	</div>
</div>
