import dataProvider from "$lib/dataProvider";
import type { Post } from "$lib/type/resources/post";
import getUserLocation from "$lib/utils/getUserLocation";
import { latLng } from "leaflet";

import type { PageLoad } from "./$types";
import type { Plant } from "$lib/type/resources/plant";

interface conversationList {
  user_id: number;
  list: {
    udpated_at: string;
    contact: { name: string; role: string; profile_picture: string };
    content: string;
    expeditor: "me" | "contact";
  }[];
}

// Mock de données
const mockConversation: conversationList = {
  user_id: 1,
  list: [
    {
      udpated_at: "2025-06-24T10:00:00Z",
      contact: {
        name: "Alice Dupont",
        role: "Botaniste",
        profile_picture: "https://picsum.photos/200",
      },
      content: "Salut, comment va ta plante ?",
      expeditor: "contact",
    },
    {
      udpated_at: "2025-06-24T10:01:00Z",
      contact: {
        name: "Moi",
        role: "Utilisateur",
        profile_picture: "https://picsum.photos/200",
      },
      content: "Elle se porte super bien, merci !",
      expeditor: "me",
    },
    {
      udpated_at: "2025-06-24T10:03:00Z",
      contact: {
        name: "Alice Dupont",
        role: "Botaniste",
        profile_picture: "https://picsum.photos/200",
      },
      content: "Tu penses qu'elle a besoin d'eau ?",
      expeditor: "contact",
    },
    {
      udpated_at: "2025-06-24T10:04:00Z",
      contact: {
        name: "Moi",
        role: "Utilisateur",
        profile_picture: "https://picsum.photos/200",
      },
      content: "Oui, je vais l'arroser cet après-midi.",
      expeditor: "me",
    },
    {
      udpated_at: "2025-06-24T10:06:00Z",
      contact: {
        name: "Alice Dupont",
        role: "Botaniste",
        profile_picture: "https://picsum.photos/200",
      },
      content: "Parfait ! N'oublie pas de lui donner un peu d'engrais.",
      expeditor: "contact",
    },
    {
      udpated_at: "2025-06-24T10:07:00Z",
      contact: {
        name: "Moi",
        role: "Utilisateur",
        profile_picture: "https://picsum.photos/200",
      },
      content: "Bonne idée, je vais m'en occuper.",
      expeditor: "me",
    },
  ],
};

export const load = (async ({ params }) => {
  return {
    conversation: mockConversation,
  };
}) satisfies PageLoad;
