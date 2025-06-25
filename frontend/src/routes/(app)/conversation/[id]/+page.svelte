<script lang="ts">
  import type { PageProps } from '../$types';
  import type { Plant } from '$lib/type/resources/plant';
  import type { Post } from '$lib/type/resources/post';
  import { Water, Light } from '$lib/icon';
  import { user } from '$lib/store/user';

  import { Button, Datepicker, Label, Modal, Textarea } from 'flowbite-svelte';
  import { getContext } from 'svelte';
    import type { DataProvider } from '$lib/type/dataProvider';

  let { data }: PageProps = $props();

  let conversation: any = data.conversation;

  let isLoading = $state(false);
  let textValue = $state("");

  // Function to add something to a conversation

  // Je sais pas trop comment faire donc je me contente de récuperer la date du last message
  const today = new Date(conversation.messages[conversation.messages.length - 1].date).toLocaleDateString('fr-FR')
  // const dataProvider = getContext<DataProvider>("dataProvider");

</script>

<div class="mx-auto w-full bg-white min-h-screen">
    <div class="flex p-2 py-4 bg-[#F0F4FA] h-24 w-full">
      <img class="h-16 w-16 ml-4 mr-8 bg-gray-300 rounded-full" alt="Photo de profil du contact"/>
      <div class="grid leading-none">
        <p class="text-xl capitalize">{conversation.contact.name}</p>
        <p class="text-green-700 font-bold">{conversation.contact.role}</p>
      </div>
    </div>
    <!-- Adapt the calc based on the top element and the nav element -->
    <div class="flex flex-col relative bg-gray-50 h-[calc(100vh-250px)] overflow-scroll">
      <div class="border-b-1 h-6 border-gray-800 w-[90%] mx-auto text-center mt-1 text-sm">
        <p class="text-green-700 font-bold">{today}</p>
      </div>
      <ul class="flex flex-col gap-4 mt-4 mx-2">
        {#each conversation.messages as message}
          {#if message.expeditor == "contact"}
            <li class="w-2/3 p-2 border-green-700 text-green-700 border-2 rounded-lg">{message.content}</li>
          {:else}
            <li class="w-2/3 ml-auto p-2 bg-green-700 text-white border-2 rounded-lg">{message.content}</li>
          {/if}
        {/each}
      </ul>
      <!-- Adapt the bottom to move the textarea -->
      <div class="flex fixed w-full bottom-[100px] gap-2">
        <textarea class="w-full border-green-700 rounded-md" bind:value={textValue}>
        </textarea>
        <!-- Maybe go with an icon here -->
        <Button aria-label="Send the message" onclick={() => openCreatePlantModal = true}>send</Button>
      </div>
    </div>
</div>