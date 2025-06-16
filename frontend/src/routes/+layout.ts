import authProvider from "$lib/authProvider";
import dataProvider from "$lib/dataProvider";
import type { LayoutLoad } from "./$types";

export const load = (({fetch}) => {
    authProvider.login({username: "admin", password: "admin"})

    dataProvider.getList("api/plants/")
}) satisfies LayoutLoad;

export const ssr = false;