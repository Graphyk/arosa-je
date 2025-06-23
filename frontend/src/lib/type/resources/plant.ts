import type { User } from "./user";
import type { Species } from "./species";
import type { Address } from './address';

export type Plant = {
    id: string;
    address: Address;
    lat: number;
    lon: number;
    owner: User;
    species: Species;
    url: string;
    creation_time: Date;
    picture: Base64URLString;
    picture_url: string;
}