import { latLng, type LatLng } from "leaflet";

const getUserLocation: () => Promise<LatLng | null>  = () => {
    return new Promise((resolve, reject) => {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
        (position) => {
            resolve(latLng(position.coords.latitude, position.coords.longitude));
        },
        (err) => reject(err)
        );
    } else {
        resolve(null);
    }
    });
};

export default getUserLocation