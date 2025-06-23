<script lang="ts">
    import { getContext, onMount } from 'svelte';
    import plantPin from '$lib/icon/pin/plantPin';

    import { map as createMap, latLng, tileLayer, type MapOptions, marker, type MarkerOptions, type LeafletMouseEvent, LatLng, circle, Circle} from 'leaflet';
    import type { DataProvider } from '$lib/type/dataProvider';
    import getUserLocation from '$lib/utils/getUserLocation';
    import type { Plant } from '$lib/type/resources/plant';
    import { goto } from '$app/navigation';

    interface Props {
        classes: string;
    }

    let {
        classes
    }: Props = $props(); 

    let mapDiv: HTMLElement;
    let radius = 500;

    let currentRange: Circle<any>

    const dataProvider = getContext<DataProvider>("dataProvider");

    async function onMapClick(e: LeafletMouseEvent) {
      if (currentRange) {
        currentRange.remove();
      }
      const plantsInRange = await dataProvider.getCount("api/plants", {
        filter: {
          center_lat: e.latlng.lat,
          center_lng: e.latlng.lng,
          radius: radius
        }
      });
      currentRange = circle(e.latlng, {
        color: '#4CAF50',
        fillColor: '#4CAF50',
        fillOpacity: 0.2,
        radius: radius
      }).addTo(e.target);


      currentRange.bindTooltip(plantsInRange.toString(), {
        permanent: true,
        direction: 'center',
        className: '!bg-primary-600'
      })

    }
    
    function onPinClick(e: LeafletMouseEvent) {
      goto(`/plant/${e.target.options.dataPlant.id}`);
    }

    interface plantMarkerOptions extends MarkerOptions {
      dataPlant?: Plant;
    }
    
    onMount(async () => {
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
</script>

<div bind:this={mapDiv} class={classes}></div>