<script lang="ts">
    import { getContext, onMount } from 'svelte';
    import plantPin from '$lib/icon/plantPin';

    import { map as createMap, latLng, tileLayer, type MapOptions, marker, LatLng, type MarkerOptions, type LeafletMouseEvent} from 'leaflet';
    import type { DataProvider } from '$lib/type/dataProvider';

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
      console.log(e);
    }

    interface plantMarkerOptions extends MarkerOptions {
      dataPlant?: {
        id: number;
        name: string;
        type: string;
      };
    }

    const getUserLocation: () => Promise<LatLng | null>  = () => {
      return new Promise((resolve, reject) => {
        if ("geolocation" in navigator) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              resolve(latLng(position.coords.latitude, position.coords.longitude));
            },
            (err) => reject(err)
          );
        } else {
          resolve(null);
        }
      });
    };
    
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