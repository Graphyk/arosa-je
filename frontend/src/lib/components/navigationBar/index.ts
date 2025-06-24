import type { Component } from 'svelte';
import NavigationBar from './navigationBar.svelte'
import type { iconProps } from '$lib/icon';

interface NavItem {
    path: string;
    icon: Component<iconProps>;
}

export { NavigationBar, type NavItem}