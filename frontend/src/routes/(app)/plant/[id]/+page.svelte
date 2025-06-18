<script lang="ts">
  import type { PageProps } from './$types';
  import type { Plant } from '$lib/type/resources/plant';
  import type { Post } from '$lib/type/resources/post';
  import { water, light } from '$lib/icon';
    import { user } from '$lib/store/user';

  let { data }: PageProps = $props();

  let post: Post = data.post;
  let plant: Plant = data.plant;
  let distanceToPlant = data.distanceToPlant;

  // State reactif avec runes
  let currentSlideIndex = $state(0);
  let isLoading = $state(false);

  // Derived state pour les étoiles
  let lightSuns = $derived.by(() => {
    return Array.from({ length: 5 }, (_, i) => ({
      icon: light,
      isActive: i < plant.species.light_dependency
    }));
  });

  // Derived state pour les gouttes d'eau
  let waterDrops = $derived.by(() => {
    return Array.from({ length: 5 }, (_, i) => ({
      icon: water,
      isActive: i < plant.species.water_dependency
    }));
  });

  // Derived state pour le texte du bouton
  let owned = $derived(plant.owner.id !== $user?.id);

  // Fonction pour gérer le clic sur le bouton principal
  function handleMainAction() {
    isLoading = true;
    
    if (owned) {
      console.log('Faire garder la plante');
      // Logique pour faire garder la plante d'autrui
    } else {
      console.log('Garder la plante');
      // Logique pour garder sa propre plante
    }

    isLoading = false;

  }

  
</script>

<div class="mx-auto w-full bg-white min-h-screen">

  <div class="px-5 py-5">
    <div class="mb-5">
      <h1 class="text-center text-3xl font-extrabold  font-title">{plant.species.name}</h1>
    </div>

    <div class="mb-5 flex items-start gap-10 justify-between">
      <div class="flex-1">
        <h2 class="mb-1 text-sm">{plant.address.raw} <span class="text-gray-600">(<span class="italic">{distanceToPlant}KM</span>)</span></h2>
      </div>
      
      <div class="text-right">
        <p class="mb-1 text-sm font-medium">{plant.owner.username}</p>
        <p class="text-xs text-gray-600">Garde demandée: <span class="whitespace-nowrap">{post.start_of_event} - {post.end_of_event}</span></p>
      </div>
    </div>

    <img 
      src={plant.picture} 
      alt={`picture of a ${plant.species.name}`} 
      class="w-[calc(100%+var(--spacing)*10)] max-w-none -mx-5"
      loading="lazy"
    />

    <div class="mb-5 flex flex-col gap-3 mt-2">
      <!-- Rating stars avec derived state -->
       <div class="flex justify-between items-center">

        <div>
          <div class="flex justify-between">
            {#each lightSuns as light}
              {@const Icon = light.icon}
              <span class="text-xl transition-colors duration-200">
                <Icon color={light.isActive ? 'orange' : 'grey'}/>
              </span>
            {/each}
          </div>
          
          <!-- Water drops avec derived state -->
          <div class="flex justify-between">
            {#each waterDrops as water}
              {@const Icon = water.icon}
              <span class="text-xl transition-colors duration-200 ">
                <Icon color={water.isActive ? 'blue' : 'grey'} />
              </span>
            {/each}
          </div>

        </div>

        <button 
          class="flex items-center gap-2 rounded-lg bg-primary-400 px-6 py-2 font-medium text-white transition-all duration-300 
                hover:bg-green-600 disabled:bg-green-300 disabled:cursor-not-allowed"
          onclick={handleMainAction}
          disabled={isLoading}
        >
          {#if isLoading}
            <div class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
          {/if}
          {owned ? 'Garder' : 'Faire garder'}
        </button>

      </div>
          
      <p class="mb-2 text-xs text-gray-600 bg-background-200 py-2 px-4 rounded-md">
        Sous pesticide Truksmachintruc vivante depuis 2023
      </p>
    </div>

  </div>
</div>