<script lang="ts">
    import type { DataProvider } from "$lib/type/dataProvider";
    import type { Species } from "$lib/type/resources/species";
    import getUserLocation from "$lib/utils/getUserLocation";
    import { Button, Label, Modal, Select, type SelectOptionType } from "flowbite-svelte";
    import { getContext, onMount } from "svelte";

    let videoSource: HTMLVideoElement | null = $state(null);
    let canvas: HTMLCanvasElement | null = $state(null);

    let loading = $state(false);

    let items = $state<SelectOptionType<Species>[]>([]);

    const plantData: {
        picture: string | null,
        species: Species | null
    } = $state({
        picture: null,
        species: null
    })

    const dataProvider = getContext<DataProvider>("dataProvider");

    const obtenerVideoCamara = async () => {
        if (videoSource) {
            try {
                plantData.picture = null
                loading = true;
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: true,
                });
                videoSource.srcObject = stream;
                videoSource.play();
                loading = false;
            } catch (error) {
                console.log(error);
            }
        }
    };

    let loadGoogleMapsScript: (() => Promise<void>) | null = $state(null);

    const takePhoto = () => {
        if (videoSource && canvas && !plantData.picture) {
            const width = videoSource.videoWidth;
            const height = videoSource.videoHeight;

            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext('2d');
            if (ctx) {
                ctx.drawImage(videoSource, 0, 0, width, height);
                plantData.picture = canvas.toDataURL('image/png');
            }
        }
    };

    let openCreatePlantModal = $state(false);

    function dataURLtoBlob(dataurl: string): Blob {
        const arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)![1],
            bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        for (let i = 0; i < n; i++) u8arr[i] = bstr.charCodeAt(i);
        return new Blob([u8arr], { type: mime });
    }

    onMount(async () => {
        items = (await dataProvider.getList<Species>("api/species")).data.map(
            (e) => {return {name: e.name, value: e}}
        )
        obtenerVideoCamara()
        loadGoogleMapsScript = () => {
            return new Promise<void>((resolve, reject) => {
                if (window.google && window.google.maps) {
                    resolve();
                    return;
                }

                const script = document.createElement('script');
                script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyB_u4F6HL4erkQbr0BIDfpa7qfZf9zBcec`;
                script.async = true;
                script.defer = true;
                script.onload = () => resolve();
                script.onerror = () => reject(new Error('Google Maps script failed'));
                document.head.appendChild(script);
            });
        };
    })

    const createPlant = async () => {
        if (loadGoogleMapsScript === null) return;
        if (!plantData.picture || !plantData.species) {
            return;
        }
        const payload = {
            picture: dataURLtoBlob(plantData.picture),
            species_id: plantData.species?.id,
            lat: 0,
            lon: 0,
            "address.raw": ""
        }

        await loadGoogleMapsScript()
        // Appel reverse geocoding ici
        const geocoder = new google.maps.Geocoder();
        const latlng = await getUserLocation(); // Paris
        if (latlng === null) return 

        payload.lat = latlng.lat;
        payload.lon = latlng.lng;

        geocoder.geocode({ location: latlng }, (results, status) => {
            if (status === 'OK' && results) {
                payload["address.raw"] = results[0].formatted_address;
                const formData = new FormData();
                
                formData.append("picture", payload.picture, "plant.png");
                formData.append("species_id", payload.species_id.toString());
                formData.append("lat", payload.lat.toString());
                formData.append("lon", payload.lon.toString());
                formData.append("address.raw", payload["address.raw"]);

                dataProvider.create("api/plants/", {data: formData})
                    .then((e) => alert("plante ajoutée avec succès !"))
                    .catch((e) => alert("Une erreur est survenue lors de l'ajout de la plante. Veuillez réessayer."));
            } else {
                console.error('Erreur de géocodage : ', status);
            }
            });
        };
</script>

<div class="h-full flex relative">
    {#if loading}
        <h1>LOADING</h1>
    {/if}
    
    <canvas bind:this={canvas} class="hidden"></canvas>
    <img class="object-cover" class:hidden={!plantData.picture} src={plantData.picture} alt="Photo prise" />
    <!-- svelte-ignore a11y_media_has_caption -->
    <video class="aspect-ratio-[3/4] object-cover" class:hidden={plantData.picture}  bind:this={videoSource}></video>
    <div class="absolute bottom-0 h-20 w-full bg-white/40 flex items-center justify-around">
        {#if !plantData.picture}
            <button onclick={takePhoto} aria-label="take a photo" class="bg-red-500 border-4 border-white p-6 rounded-full"></button> 
        {:else}
            <Button aria-label="accept the picture" onclick={() => openCreatePlantModal = true}>accept</Button>
            <Button color="red" aria-label="deny the picture" onclick={() => plantData.picture=""}>cancel</Button>
        {/if}
    </div>

    <Modal title="Add your plant" bind:open={openCreatePlantModal}>
        <div class="flex flex-col items-center gap-2">
            <Label>
                Quelle est l'espèce de cette plante ?
                <Select {items} bind:value={plantData.species}/>
            </Label>
            <Button onclick={createPlant}>Envoyer</Button>
        </div>
    </Modal>
</div>
