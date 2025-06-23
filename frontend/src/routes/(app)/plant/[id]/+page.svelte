<script lang="ts">
  import type { PageProps } from './$types';
  import type { Plant } from '$lib/type/resources/plant';
  import type { Post } from '$lib/type/resources/post';
  import { Water, Light } from '$lib/icon';
  import { user } from '$lib/store/user';

  import { Button, Datepicker, Label, Modal, Textarea } from 'flowbite-svelte';
  import { getContext } from 'svelte';
    import type { DataProvider } from '$lib/type/dataProvider';

  let { data }: PageProps = $props();

  let post: Post = data.post;
  let plant: Plant = data.plant;
  let distanceToPlant = data.distanceToPlant;

  let isLoading = $state(false);
  let createPostFormOpened = $state(false);

  const dataProvider = getContext<DataProvider>("dataProvider");

  const createPostRequestData = $state({
    start_of_event: new Date(Date.now()),
    end_of_event: new Date(Date.now()),
    plant_id: plant.id,
    commentary: ""
  })

  const submitCreatePostForm = async (e: SubmitEvent) => {
    e.preventDefault();

    const startDate = createPostRequestData.start_of_event;
    const endDate = createPostRequestData.end_of_event;

    const formattedStartDate = `${startDate.getFullYear()}-${startDate.getMonth() + 1}-${startDate.getDate()}`
    const formattedEndDate = `${endDate.getFullYear()}-${endDate.getMonth() + 1}-${endDate.getDate()}`

    dataProvider.create<Post>("api/posts/", {data: {
        ...createPostRequestData,
        start_of_event: formattedStartDate,
        end_of_event: formattedEndDate
    }})

    createPostFormOpened = false;
  }

  // Derived state pour les étoiles
  let lightSuns = $derived.by(() => {
    return Array.from({ length: 5 }, (_, i) => ({
      icon: Light,
      isActive: i < plant.species.light_dependency
    }));
  });

  // Derived state pour les gouttes d'eau
  let waterDrops = $derived.by(() => {
    return Array.from({ length: 5 }, (_, i) => ({
      icon: Water,
      isActive: i < plant.species.water_dependency
    }));
  });

  // Derived state pour le texte du bouton
  let owned = $derived(plant.owner.id === $user?.id);

  // Fonction pour gérer le clic sur le bouton principal
  function handleMainAction() {
    isLoading = true;
    
    if (owned) {
      createPostFormOpened = true;
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
      
      <div class="text-right w-full">
        <p class="mb-1 text-sm font-medium">owner: {plant.owner.username}</p>
        {#if post}
          <p class="text-xs text-gray-600">Garde demandée: <span class="whitespace-nowrap">{post.start_of_event} - {post.end_of_event}</span></p>
        {/if}
      </div>
    </div>

    <img 
      src={plant.picture_url} 
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
                <Icon color={light.isActive ? 'orange' : 'grey'} size={25} />
              </span>
            {/each}
          </div>
          
          <!-- Water drops avec derived state -->
          <div class="flex justify-between">
            {#each waterDrops as water}
              {@const Icon = water.icon}
              <span class="text-xl transition-colors duration-200 ">
                <Icon color={water.isActive ? 'blue' : 'grey'} size={25} />
              </span>
            {/each}
          </div>

        </div>

        <button 
          class="flex items-center gap-2 rounded-lg bg-primary-500 px-6 py-2 font-medium text-white transition-all duration-300 
                hover:bg-green-600 disabled:bg-green-300 disabled:cursor-not-allowed"
          onclick={handleMainAction}
          disabled={isLoading}
        >
          {#if isLoading}
            <div class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
          {/if}
          {owned ? 'Faire garder' : 'Garder'}
        </button>

      </div>
      {#if post && post.commentary !== ""}
        <p class="mb-2 text-xs text-gray-600 bg-background-200 py-2 px-4 rounded-md">
          {post.commentary}
        </p>
      {/if}
    </div>

  </div>
  {#if owned}
    <Modal 
      title="Créez un post pour votre plant" 
      class="max-h-[90vh]" bodyClass="h-full" 
      bind:open={createPostFormOpened}
      onsubmit={submitCreatePostForm}
    >
      <form class="mt-6 flex flex-col items-center gap-2" method="dialog">
        <Label class="flex flex-col items-center w-full" for="datepicker">
          <span class="self-start">Date de garde</span>
          <Datepicker
            inline 
            range
            bind:rangeFrom={createPostRequestData.start_of_event}
            bind:rangeTo={createPostRequestData.end_of_event}
          />
        </Label>
        <Label class="w-full" for="commentary">
          Commentaire
          <Textarea 
            name="commentary" 
            bind:value={createPostRequestData.commentary} 
            class="w-full"
          />
        </Label>
        <Button type="submit">
          Envoyer
        </Button>
      </form>

    </Modal>
  {/if}
</div>