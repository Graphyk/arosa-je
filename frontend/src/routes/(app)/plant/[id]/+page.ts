import dataProvider from "$lib/dataProvider";
import type { Post } from "$lib/type/resources/post";
import getUserLocation from "$lib/utils/getUserLocation";
import { latLng } from "leaflet";

import type { PageLoad } from './$types';
import type { Plant } from "$lib/type/resources/plant";

export const load = (async ({params}) => {

    let plant = (await dataProvider.get<Plant>("api/plants/", {id: params.id})).data
    let post = (await dataProvider.getList<Post>("api/posts", {filter: {plant: plant.id}})).data[0]

    let userLocation = (await getUserLocation()) ?? latLng(40.731253, -73.996139);

    let distanceToPlant = (Math.round(userLocation.distanceTo(latLng(plant.lat,plant.lon))) / 1000).toFixed(2);

    return {
        post: post,
        distanceToPlant: distanceToPlant,
        plant: plant
    }
}) satisfies PageLoad;

export const ssr = false;