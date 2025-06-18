import lightSvg from "./light.svelte";
import waterSvg from "./water.svelte";
import listSvg from "./list.svelte";
import profileSvg from "./profile.svelte";
import homeSvg from "./home.svelte";

interface Props {
    "color": string;
    "size": number;
}

export { lightSvg as light, waterSvg as water, listSvg as list, profileSvg as profile, homeSvg as home, type Props as iconProps}