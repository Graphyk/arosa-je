<script lang="ts">
    import type { DataProvider } from '$lib/type/dataProvider';
    import { Button, Modal, Spinner } from 'flowbite-svelte';
    import { getContext, onMount } from 'svelte';
    import { type Consentment } from '$lib/type/resources/consentment';

    let { children } = $props();

    const dataProvider = getContext<DataProvider>('dataProvider');
    
    let open = $state(false);

    onMount(async() => {
        const notSignedCount: number = (await dataProvider.getCount('api/consentments', defaultFilters))
        if (notSignedCount > 0) {
            open = true;
        }
    })

    const defaultFilters = {
        filter: {
            "not_signed": true,
            "required": true
        }
    }

    const acceptConsentments = (consentments: Consentment[]) => {
        for (const consentment of consentments) {
            dataProvider.create('/api/consentments/accept/', {
                data : {
                    consentment_id: consentment.id,
                }
            });
        }
    };
</script>
{@render children()}

<Modal bind:open title="We need your attention" dismissable={false}>
    <div class="text-sm flex flex-col align-center w-full">
        
        {#await dataProvider.getList<Consentment>("/api/consentments", defaultFilters)}
            <Spinner />
        {:then res} 
        <div class="overflow-y-scroll"> 
            <span class="font-bold">
                Our application needs you to know and accept these treatments we will make on your data
            </span>
            <br>
            <span>
                Your consent is required for these treatments, you can't access the application without accepting them:
            </span>

            <br>
            <br>

            <ul class="text-xs ml-5">
                {#each res.data as consentment}
                    <li class="list-disc">{consentment.text}</li>
                {/each}
            </ul>
        </div>

        <Button class="self-center mx-auto mt-5" onclick={() => acceptConsentments(res.data)}>
            Accept
        </Button>
        {/await}
    </div>
</Modal>