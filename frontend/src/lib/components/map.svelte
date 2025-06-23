<script lang="ts">
    import { getContext, onMount } from 'svelte';
    import { List } from '$lib/icon';

    import { map as createMap, latLng, tileLayer, type MapOptions, marker, type MarkerOptions, type LeafletMouseEvent, LatLng, circle, Circle} from 'leaflet';
    import type { DataProvider } from '$lib/type/dataProvider';
    import getUserLocation from '$lib/utils/getUserLocation';
    import type { Plant } from '$lib/type/resources/plant';
    import { Button, Modal } from 'flowbite-svelte';
    import { goto } from '$app/navigation';

    let mapDiv: HTMLElement;
    let radius = 500;
    let listModalOpen = $state(false);

    let currentRange: Circle<any>
    let plants = $state<Plant[]>([]);

    const dataProvider = getContext<DataProvider>("dataProvider");

    async function onMapClick(e: LeafletMouseEvent) {
      if (currentRange) {
        currentRange.remove();
      }

      const countPlantsInRange = await dataProvider.getCount("api/plants", {
        filter: {
          center_lat: e.latlng.lat,
          center_lng: e.latlng.lng,
          radius: radius
        }
      });

      const plantsInRange = await dataProvider.getList<Plant>('api/plants', {
        filter: {
          center_lat: e.latlng.lat,
          center_lng: e.latlng.lng,
          radius: radius
        }
      });
      plants = plantsInRange.data;

      currentRange = circle(e.latlng, {
        color: '#4CAF50',
        fillColor: '#4CAF50',
        fillOpacity: 0.2,
        radius: radius
      }).addTo(e.target);

      currentRange.bindTooltip(countPlantsInRange.toString(), {
        permanent: true,
        direction: 'center',
        className: '!bg-primary-600'
      })
    }
    
    onMount(async () => {
      dataProvider.getList<Plant>('api/plants').then(({ data }) => {
        plants = data;
      });

      const baseLocation = await getUserLocation() ?? latLng(40.731253, -73.996139);

      let options: MapOptions = {
        center: baseLocation,
        zoom: 16,
      };

      const map = createMap(mapDiv, options);
      map.on('click', onMapClick);

      const newMarker = marker(baseLocation, options)
      newMarker.addTo(map);

      tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);

  });

  const openList = () => {
    listModalOpen = true;
  }
</script>
<div class="relative h-full w-full">
  <div bind:this={mapDiv} class='h-full w-full'></div>

  <Button 
    class="absolute top-2 right-2 p-3 rounded-lg bg-white z-[1000]"
    onclick={openList}
  >
    <List color="black" size={40} />
  </Button>

  <Modal
    bind:open={listModalOpen}
    class="rounded-t-none max-h-[80vh]"
    bodyClass="px-0"
    aria-label="Plant List"
    placement="top-center"
    title="Plants in range"
  >
    <div class="grid grid-cols-1 pb-5">
      {#each plants as plant, index (plant.id)}
        <a 
          class="flex justify-between" 
          class:bg-gray-300={index % 2 === 0} 
          class:bg-white={index % 2 !== 0}
          onclick={() => goto(`/plant/${plant.id}`)}
          href={`/plant/${plant.id}`}
        >
          <div class="flex">
            <img 
              class="w-16 h-16 object-cover mr-2"
              src={plant.picture_url} 
              alt={`photo de ${plant.species.name}`} 
              />
            <div class="text-black font-title font-bold">
                {plant.species.name}
            </div>
          </div>

          <div class="italic">
            {plant.owner.username}
          </div>
        </a>
      {/each}
    </div>
  </Modal>
</div>