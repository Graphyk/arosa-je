<script>
  import { onMount } from 'svelte';

  // Props avec runes Svelte 5
  let {
    plantData = $bindable({
      id: 1,
      name: "Plante super cool",
      location: "Charleville-Mézières",
      address: "8 avenue du Roi, moche (0.5 KM)",
      owner: "Fabrice Plantenpot",
      dateRange: "17 Nov 2024 - 22 Nov 2024",
      image: "/api/placeholder/300/400",
      rating: 2, // sur 5
      wateringFrequency: 3, // jours
      lastWatered: "2 ans",
      isOwner: false // si c'est la plante de l'utilisateur actuel
    }),
    userPlants = $bindable([
      {
        id: 2,
        name: "Orchidée à frou-frou",
        image: "/api/placeholder/150/200",
        size: "0.5 KM",
        dateRange: "17 Nov 2024 22 Nov 2024"
      },
      {
        id: 3,
        name: "Orchidée à frou-frou",
        image: "/api/placeholder/150/200",
        size: "0.5 KM",
        dateRange: "17 Nov 2024 22 Nov 2024"
      }
    ]),
    currentUserId = $bindable(123)
  } = $props();

  // State reactif avec runes
  let currentSlideIndex = $state(0);
  let isLoading = $state(false);

  // Derived state pour les étoiles
  let stars = $derived(() => {
    return Array.from({ length: 5 }, (_, i) => i < plantData.rating ? '⭐' : '☆');
  });

  // Derived state pour les gouttes d'eau
  let waterDrops = $derived(() => {
    return Array.from({ length: 5 }, (_, i) => ({
      icon: '💧',
      isActive: i < plantData.wateringFrequency
    }));
  });

  // Derived state pour le texte du bouton
  let buttonText = $derived(() => {
    return plantData.isOwner ? 'Garder' : 'Faire garder';
  });

  // Derived state pour la plante actuelle du slider
  let currentPlant = $derived(() => {
    return userPlants[currentSlideIndex] || userPlants[0];
  });

  // Effect pour logger les changements
  $effect(() => {
    console.log('Plant data changed:', plantData.name);
  });

  // Fonction pour gérer le clic sur le bouton principal
  function handleMainAction() {
    isLoading = true;
    
    if (plantData.isOwner) {
      console.log('Garder la plante');
      // Logique pour garder sa propre plante
    } else {
      console.log('Faire garder la plante');
      // Logique pour faire garder la plante d'autrui
    }
    
    // Simulation d'une requête async
    setTimeout(() => {
      isLoading = false;
    }, 1000);
  }

  // Fonctions pour naviguer dans le slider
  function goToPreviousSlide() {
    if (currentSlideIndex > 0) {
      currentSlideIndex--;
    }
  }

  function goToNextSlide() {
    if (currentSlideIndex < userPlants.length - 1) {
      currentSlideIndex++;
    }
  }

  // Computed properties pour la navigation
  let canGoPrevious = $derived(currentSlideIndex > 0);
  let canGoNext = $derived(currentSlideIndex < userPlants.length - 1);
</script>

<div class="mx-auto w-full max-w-sm bg-white font-sans min-h-screen">
  <!-- Section principale avec une seule plante -->
  <div class="px-5 py-5">
    <div class="mb-5">
      <h1 class="text-center text-2xl font-bold text-gray-900">{plantData.name}</h1>
    </div>

    <div class="mb-5 flex items-start justify-between">
      <div class="flex-1">
        <h2 class="mb-1 text-base font-semibold text-gray-900">{plantData.location}</h2>
        <p class="text-xs text-gray-600">{plantData.address}</p>
      </div>
      
      <div class="text-right">
        <p class="mb-1 text-sm font-medium text-gray-900">{plantData.owner}</p>
        <p class="text-xs text-gray-600">{plantData.dateRange}</p>
      </div>
    </div>

    <div class="mb-5 flex justify-center">
      <img 
        src={plantData.image} 
        alt={plantData.name} 
        class="h-72 w-48 rounded-lg object-cover shadow-md transition-opacity duration-300"
        loading="lazy"
      />
    </div>

    <div class="mb-5 flex flex-col items-center gap-3">
      <!-- Rating stars avec derived state -->
      <div class="flex gap-1">
        {#each stars as star}
          <span class="text-xl transition-colors duration-200 {star === '⭐' ? 'text-yellow-400' : 'text-gray-300'}">
            {star}
          </span>
        {/each}
      </div>
      
      <!-- Water drops avec derived state -->
      <div class="flex gap-1">
        {#each waterDrops as drop}
          <span class="text-base transition-opacity duration-200 {drop.isActive ? 'opacity-100' : 'opacity-30'}">
            {drop.icon}
          </span>
        {/each}
      </div>
    </div>

    <div class="mb-5 text-center">
      <p class="mb-2 text-xs text-gray-600">
        Sous pesticide Truksmuchintruc vivante depuis {plantData.lastWatered}
      </p>
      <p class="text-sm text-gray-900">Garde de plante du même utilisateur</p>
    </div>

    <div class="mb-8 flex justify-center">
      <button 
        class="flex items-center gap-2 rounded-full bg-green-500 px-8 py-3 font-medium text-white transition-all duration-300 hover:bg-green-600 disabled:bg-green-300 disabled:cursor-not-allowed"
        onclick={handleMainAction}
        disabled={isLoading}
      >
        {#if isLoading}
          <div class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
        {/if}
        {buttonText}
      </button>
    </div>
  </div>

  <!-- Section slider avec les plantes du même utilisateur -->
  <div class="mt-5 bg-green-500 px-5 py-5">
    <h3 class="mb-4 text-center text-base font-medium text-white">
      Autres plantes du même utilisateur
    </h3>
    
    <!-- Card avec navigation -->
    {#if currentPlant}
      <div class="mx-2 rounded-lg bg-white p-4 transition-transform duration-300">
        <div class="flex items-center gap-4">
          <img 
            src={currentPlant.image} 
            alt={currentPlant.name} 
            class="h-24 w-20 flex-shrink-0 rounded-lg object-cover transition-opacity duration-300"
            loading="lazy"
          />
          <div class="min-w-0 flex-1">
            <h4 class="mb-1 text-sm font-semibold text-gray-900">{currentPlant.name}</h4>
            <p class="mb-1 text-xs text-gray-600">{currentPlant.size}</p>
            <p class="text-xs text-gray-600">{currentPlant.dateRange}</p>
          </div>
        </div>
      </div>
    {/if}
    
    <!-- Navigation arrows avec état réactif -->
    <div class="mt-4 flex items-center justify-between px-2">
      <button 
        class="flex h-10 w-10 items-center justify-center rounded-full bg-white/80 text-xl font-bold text-gray-700 transition-all duration-200 hover:bg-white disabled:cursor-not-allowed disabled:opacity-50"
        onclick={goToPreviousSlide}
        disabled={!canGoPrevious}
        aria-label="Plante précédente"
      >
        ‹
      </button>
      
      <!-- Indicateurs de slides -->
      <div class="flex gap-2">
        {#each userPlants as _, index}
          <button
            class="h-2 w-2 rounded-full transition-all duration-200 {index === currentSlideIndex ? 'bg-white' : 'bg-white/50'}"
            onclick={() => currentSlideIndex = index}
            aria-label="Aller à la plante {index + 1}"
          ></button>
        {/each}
      </div>
      
      <button 
        class="flex h-10 w-10 items-center justify-center rounded-full bg-white/80 text-xl font-bold text-gray-700 transition-all duration-200 hover:bg-white disabled:cursor-not-allowed disabled:opacity-50"
        onclick={goToNextSlide}
        disabled={!canGoNext}
        aria-label="Plante suivante"
      >
        ›
      </button>
    </div>
    
    <!-- Compteur de slides -->
    <div class="mt-2 text-center">
      <span class="text-xs text-white opacity-75">
        {currentSlideIndex + 1} / {userPlants.length}
      </span>
    </div>
  </div>
</div>