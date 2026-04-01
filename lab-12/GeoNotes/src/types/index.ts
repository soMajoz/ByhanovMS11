export interface GeoNote {
    id: string;
    title: string;
    content: string;
    latitude: number;
    longitude: number;
    address?: string;
    photoUri?: string;
    createdAt: number;
}
