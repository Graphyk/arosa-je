import type { Plant } from "./plant"

export type Post = {
    plant: Plant;
    end_of_event: Date;
    start_of_event: Date;
    url: Base64URLString;
    commentary: string;
}