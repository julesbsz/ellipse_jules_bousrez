"use client";

// React & Dependencies
import { useEffect, useRef, useState } from "react";
import { FeatureCollection, Point, featureCollection, point } from "@turf/helpers";

// Mapbox
import mapboxgl, { GeoJSONSource } from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

// Components
import PositionComponent from "@/components/Position";
import InformationsComponent from "@/components/Informations";

// API Call
import getStations from "@/api/data";

function MapboxMap({}) {
	const mapNode = useRef(null);

	const isMapInitialized = useRef<boolean>(false);

	const [lng, setLng] = useState(2.213749);
	const [lat, setLat] = useState(46.227638);
	const [zoom, setZoom] = useState(5);

	const [stationData, setStationData] = useState<any>(null);

	// Création du GeoJSON à partir des données de l'API -> il sera utilisé pour afficher les stations sur la map
	const createGeoJSONData = (stations: any[]): FeatureCollection<Point> => {
		const features = stations.map((station: { [x: string]: { [x: string]: any } }) => {
			const coordinates = [station["position"]["lng"], station["position"]["lat"]];
			const geometry = point(coordinates);
			const properties = { ...station };
			return { ...geometry, properties };
		});

		return featureCollection(features);
	};

	// Récupération des stations et mise à jour de la map -> fonction appelée toutes les 60 secondes
	const fetchAndUpdateStations = async (mapboxMap: mapboxgl.Map) => {
		// Récupération des stations avec une requête API
		const stations = await getStations();

		if (isMapInitialized.current) {
			// La map a déjà été initialisée -> on met à jour les données
			const source = (await mapboxMap.getSource("stations")) as GeoJSONSource;
			source.setData(createGeoJSONData(stations));
		} else {
			// La map n'a pas encore été initialisée -> on l'initialise avec les données
			mapboxMap.addSource("stations", {
				type: "geojson",
				data: createGeoJSONData(stations),
				cluster: true,
				clusterMaxZoom: 13,
				clusterRadius: 50,
			});

			// Ajout des clusters (regroupement des stations)
			mapboxMap.addLayer({
				id: "clusters",
				type: "circle",
				source: "stations",
				filter: ["has", "point_count"],
				paint: {
					"circle-color": ["step", ["get", "point_count"], "#50C878", 100, "#f1f075", 750, "#f28cb1"],
					"circle-radius": ["step", ["get", "point_count"], 20, 100, 30, 750, 40],
				},
			});

			// Ajout du nombre de stations dans les clusters
			mapboxMap.addLayer({
				id: "cluster-count",
				type: "symbol",
				source: "stations",
				filter: ["has", "point_count"],
				layout: {
					"text-field": "{point_count_abbreviated}",
					"text-font": ["DIN Offc Pro Medium", "Arial Unicode MS Bold"],
					"text-size": 12,
				},
			});

			// Ajout des stations non regroupées
			mapboxMap.addLayer({
				id: "unclustered-point",
				type: "circle",
				source: "stations",
				filter: ["!", ["has", "point_count"]],
				paint: {
					"circle-color": "#51bbd6",
					"circle-radius": 10,
					"circle-stroke-width": 1,
					"circle-stroke-color": "#fff",
				},
			});

			// Mise à jour des informations de la station sélectionnée -> elles seront affichées dans le composant Informations
			mapboxMap.on("click", "unclustered-point", (e) => {
				if (e.features && e.features.length > 0) {
					setStationData(e.features[0].properties);
				}
			});

			// Lorqu'on clique sur un cluster, on zoome dessus
			mapboxMap.on("click", "clusters", (e) => {
				mapboxMap.flyTo({
					center: [e.lngLat.lng, e.lngLat.lat],
					zoom: mapboxMap.getZoom() + 2.5,
					essential: true,
					speed: 5,
					curve: 0.5,
					easing(t) {
						return t;
					},
				});
			});

			// Lorsqu'on passe la souris sur une station, on change le curseur (pour indiquer qu'on peut cliquer dessus)
			mapboxMap.on("mouseenter", "unclustered-point", () => {
				mapboxMap.getCanvas().style.cursor = "pointer";
			});

			mapboxMap.on("mouseleave", "unclustered-point", () => {
				mapboxMap.getCanvas().style.cursor = "";
			});
		}

		isMapInitialized.current = true;
	};

	useEffect(() => {
		// Initialisation de Mapbox
		const node = mapNode.current;

		if (typeof window === "undefined" || node === null) return;

		const mapboxMap = new mapboxgl.Map({
			container: node,
			accessToken: process.env.NEXT_PUBLIC_MAPBOX_GL_ACCESS_TOKEN,
			style: "mapbox://styles/mapbox/streets-v12",
			zoom,
			center: [lng, lat],
		});

		// Lorsqu'on se déplace, on met à jour les coordonnées -> elles seront affichées dans le composant Position
		mapboxMap.on("move", () => {
			setLng(parseFloat(mapboxMap.getCenter().lng.toFixed(4)));
			setLat(parseFloat(mapboxMap.getCenter().lat.toFixed(4)));
			setZoom(parseFloat(mapboxMap.getZoom().toFixed(2)));
		});

		// Lorsque la map est chargée, on récupère les stations et on les affiche
		mapboxMap.on("load", () => {
			fetchAndUpdateStations(mapboxMap);
		});

		// Mise à jour des stations toutes les 60 secondes
		const intervalId = setInterval(() => {
			fetchAndUpdateStations(mapboxMap);
		}, 60000);

		return () => {
			mapboxMap.remove();
			clearInterval(intervalId);
		};
	}, []);

	return (
		<div ref={mapNode} style={{ width: "100%", height: "100%" }}>
			<PositionComponent lng={lng} lat={lat} zoom={zoom} />
			<InformationsComponent data={stationData} />
		</div>
	);
}
export default MapboxMap;
