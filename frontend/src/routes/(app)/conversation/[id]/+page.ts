import dataProvider from "$lib/dataProvider";
import type { Post } from "$lib/type/resources/post";
import getUserLocation from "$lib/utils/getUserLocation";
import { latLng } from "leaflet";

import type { PageLoad } from "./$types";
import type { Plant } from "$lib/type/resources/plant";

interface conversation {
  contact: { name: string; role: string };

  messages: {
    date: string;
    content: string;
    expeditor: "me" | "contact";
  }[];
}

// Mock de données
const mockConversation: conversation = {
  contact: { name: "Alice Dupont", role: "Botaniste" },
  messages: [
    {
      date: "2025-06-24T10:00:00Z",
      content: "Salut, comment va ta plante ?",
      expeditor: "contact",
    },
    {
      date: "2025-06-24T10:01:00Z",
      content: "Elle se porte super bien, merci !",
      expeditor: "me",
    },
    {
      date: "2025-06-24T10:03:00Z",
      content: "Tu penses qu'elle a besoin d'eau ?",
      expeditor: "contact",
    },
    {
      date: "2025-06-24T10:04:00Z",
      content: "Oui, je vais l'arroser cet après-midi.",
      expeditor: "me",
    },
    {
      date: "2025-06-24T10:00:00Z",
      content: "Salut, comment va ta plante ?",
      expeditor: "contact",
    },
    {
      date: "2025-06-24T10:01:00Z",
      content: "Elle se porte super bien, merci !",
      expeditor: "me",
    },
    {
      date: "2025-06-24T10:03:00Z",
      content: "Tu penses qu'elle a besoin d'eau ?",
      expeditor: "contact",
    },
    {
      date: "2025-06-24T10:04:00Z",
      content: "Oui, je vais l'arroser cet après-midi.",
      expeditor: "me",
    },
  ],
};

export const load = (async ({ params }) => {
  return {
    conversation: mockConversation,
  };
}) satisfies PageLoad;

export const ssr = false;
