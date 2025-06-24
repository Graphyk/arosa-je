import dataProvider from "$lib/dataProvider";
import type { Post } from "$lib/type/resources/post";
import getUserLocation from "$lib/utils/getUserLocation";
import { latLng } from "leaflet";

import type { PageLoad } from './$types';
import type { Plant } from "$lib/type/resources/plant";

export const load = (async ({params}) => {

    let plant = (await dataProvider.get<Plant>("api/plants/", {id: params.id})).data
    let post = (await dataProvider.getList<Post>("api/posts", {filter: {plant: plant.id}})).data[0]

    return {
        post: post,
        plant: plant
    }
}) satisfies PageLoad;

export const ssr = false;