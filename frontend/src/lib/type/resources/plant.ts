import type { user } from "./user";
import type { species } from "./species";
import type { address } from './address';

export type plant = {
    address: address;
    lat: number;
    lon: number;
    owner: user;
    species: species;
    url: string;
    creation_time: Date; 
}