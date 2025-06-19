<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { type NavItem } from '.';

  // Props avec Svelte 5 runes
  interface Props {
    items: NavItem[];
    activeColor?: string;
    inactiveColor?: string;
    showLabels?: boolean;
  }

  let {
    items = $bindable(),
    activeColor = 'primary-500',
    inactiveColor = 'gray-500',
  }: Props = $props();

  // État réactif avec runes
  const currentPath = $derived(page.url.pathname);

  // Fonction pour naviguer
  const handleNavigation = (path: string) => {
    goto(path);
  };

  // Fonction pour vérifier si l'élément est actif
  const isActive = (path: string): boolean => {
    return currentPath === path;
  };

  const getCssVariable = (variableName: string) => 
    getComputedStyle(document.documentElement).getPropertyValue(`--color-${variableName}`);
  

  // Classes dynamiques avec Svelte 5
  const getNavItemClasses = (item: NavItem) => `relative flex flex-col items-center justify-center px-6
    transition-all duration-200 ease-in-out cursor-pointer min-w-12 gap-1
    hover:bg-${activeColor}/10 hover:-translate-y-0.5 hover:scale-105
    ${isActive(item.path) 
      ? `text-${activeColor} border-y-2 border-${activeColor}` 
      : `text-${inactiveColor} hover:text-${activeColor}`
    }
  `
</script>

<nav class="bg-gradient-to-r w-full from-slate-50 to-slate-100 border-b border-slate-200 shadow-sm fixed h-16 bottom-0 z-50">
  <div class="flex justify-around max-w-md mx-auto px-4 h-16">
    {#each items as item (item.path)}
      {@const Icon = item.icon}
      <button
        class={getNavItemClasses(item)}
        onclick={() => handleNavigation(item.path)}
        aria-label={`Naviguer vers ${item.path}`}
        type="button"
      >

        <!-- Icône SVG -->
         {console.log(getCssVariable(inactiveColor))}
        <Icon size={30} color={isActive(item.path) ? getCssVariable(activeColor) : getCssVariable(inactiveColor)}/>
      </button>
    {/each}
  </div>
</nav>

<style>
  /* Styles personnalisés pour les pseudo-éléments que Tailwind ne peut pas gérer */
  button.relative::before {
    content: '';
  }
</style>