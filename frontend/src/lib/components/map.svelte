<script lang="ts">
    import { getContext, onMount } from 'svelte';
    import plantPin from '$lib/icon/pin/plantPin';

    import { map as createMap, latLng, tileLayer, type MapOptions, marker, type MarkerOptions, type LeafletMouseEvent, LatLng} from 'leaflet';
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

    const dataProvider = getContext<DataProvider>("dataProvider");

    function onMapClick(e: LeafletMouseEvent) {
      console.log(e);
    }
    
    function onPinClick(e: LeafletMouseEvent) {
      goto(`/plant/${e.target.options.dataPlant.id}`);
    }

    interface plantMarkerOptions extends MarkerOptions {
      dataPlant?: Plant;
    }
    
    onMount(async () => {
      let options: MapOptions = {
        center: await getUserLocation() ?? latLng(40.731253, -73.996139),
        zoom: 16,
      };

      const map = createMap(mapDiv, options);
      map.on('click', onMapClick);

      tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);

      dataProvider.getList("api/plants").then(res => {
        res.data.forEach(element => {
          const options: plantMarkerOptions = {
            icon: plantPin, 
            dataPlant: element
          }
  
          const newMarker = marker(latLng(element.lat, element.lon), options)

          newMarker.on("click", onPinClick);
          
          newMarker.addTo(map);
        })
      })
  });
</script>

<div bind:this={mapDiv} class={classes}></div>