<script lang="ts">
  import type { PageProps } from '../$types';
  import type { Plant } from '$lib/type/resources/plant';
  import type { Post } from '$lib/type/resources/post';
  import { Water, Light } from '$lib/icon';
  import { user } from '$lib/store/user';

  import { Button, Datepicker, Label, Modal, Textarea } from 'flowbite-svelte';
  import { getContext } from 'svelte';
    import type { DataProvider } from '$lib/type/dataProvider';
  import { goto } from '$app/navigation';

  let { data }: PageProps = $props();

  let conversation: any = data.conversation;

  let isLoading = $state(false);
  let textValue = $state("");

  // Function to add something to a conversation

  // Je sais pas trop comment faire donc je me contente de récuperer la date du last message
  // const dataProvider = getContext<DataProvider>("dataProvider");

</script>

<div class="mx-auto w-full bg-white min-h-screen bg-[#F0F4FA]">
    <div class="min-h-screen bg-[#F0F4FA]">
        {#each conversation.list as conversationElement, i}
            <button onclick={() => goto(`/conversation/${'1'}`)} class={`flex  cursor-pointer p-2 py-4  h-24 w-full ${Number.isInteger(i / 2) ? "bg-[#F0F4FA]" : "bg-gray-50"}`}>
                <div>
                    <img class="h-16 w-16 ml-4 border-1 border-green-700 mr-4 bg-gray-300 rounded-full" alt={`Photo de profil de ${conversationElement.contact.name}`}/>
                </div>
                <div class="grid w-full items-start">
                    <div class="flex leading-none justify-between w-full">
                        <p class="text-xl capitalize">{conversationElement.contact.name}</p>
                        <!-- <p class="text-green-700 font-bold">{conversationElement.contact.role}</p> -->
                        <!-- C'est moche je sais  -->
                        <p class="text-sm text-green-700 my-auto">{new Date(conversationElement.udpated_at).toLocaleDateString('fr-FR')}</p>
                    </div>
                    <p class="bg-gray-50 text-gray-800 border-1 border-green-700 truncate rounded-lg p-1">{conversationElement.content}</p>
                    
                </div>
            </button>
        {/each}
    </div>

    <!-- Adapt the calc based on the top element and the nav element -->
   
</div>