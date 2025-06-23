import lightSvg from "./light.svelte";
import waterSvg from "./water.svelte";
import listSvg from "./list.svelte";
import profileSvg from "./profile.svelte";
import homeSvg from "./home.svelte";

interface Props {
    "color": string;
    "size": number;
}

export { lightSvg as Light, waterSvg as Water, listSvg as List, profileSvg as Profile, homeSvg as Home, type Props as iconProps}